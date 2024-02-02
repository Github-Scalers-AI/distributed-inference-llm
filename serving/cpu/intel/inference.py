import asyncio
import logging
import os
import time
from enum import Enum
from queue import Empty, Queue
from typing import List, Optional

import torch
from bigdl.llm.transformers import AutoModelForCausalLM
from fastapi import FastAPI, Request
from huggingface_hub import HfFolder
from pydantic import BaseModel
from ray import serve
from ray.serve import Application
from starlette.responses import StreamingResponse
from transformers import AutoTokenizer

logger = logging.getLogger("ray.serve")


class RawStreamer:
    """A simple streaming class for handling raw data asynchronously.

    This class is designed for streaming raw data asynchronously using a queue.
    It allows putting data into the queue, ending the stream, and iterating
    over the stream to retrieve the data.

    :param timeout: Timeout for getting values from the queue.
    :type timeout: float, optional
    """

    def __init__(self, timeout: float = None):
        self.q = Queue()
        self.stop_signal = None
        self.timeout = timeout

    def put(self, values):
        """Put values into the stream.

        :param values: Values to put into the stream.
        """
        self.q.put(values)

    def end(self):
        """Signal the end of the stream."""
        self.q.put(self.stop_signal)

    def __iter__(self):
        return self

    def __next__(self):
        """Get the next value from the stream.

        :raises StopIteration: When the stop signal is received.
        """
        result = self.q.get(timeout=self.timeout)
        if result == self.stop_signal:
            raise StopIteration()
        else:
            return result


class DataTypes(str, Enum):
    """Supported datatypes by BigDL."""

    int8 = "int8"


class DeployArgs(BaseModel):
    """DeployArgs pydantic model."""

    model_name: Optional[str] = "meta-llama/Llama-2-7b-chat-hf"
    data_type: Optional[DataTypes] = DataTypes.int8
    max_new_tokens: Optional[int] = 128
    temperature: Optional[float] = 1.0
    batch_size: Optional[int] = 10
    batch_timeout: Optional[float] = 1.0
    hf_token: str


fastapi_app = FastAPI()


@serve.deployment(ray_actor_options={"num_cpus": 50})
@serve.ingress(fastapi_app)
class BigDLDeployment:
    def __init__(self, deploy_args: DeployArgs):
        """Initialize the BigDLDeployment class.

        :param deploy_args: Deployment arguments.
        :type deploy_args: DeployArgs
        """
        self.loop = asyncio.get_running_loop()
        self.tokens = 0
        self.time = 0
        self.num_requests = 0
        HfFolder.save_token(os.environ.get("HF_TOKEN", deploy_args.hf_token))
        self.model_name = deploy_args.model_name
        self.data_type = deploy_args.data_type
        self.max_new_tokens = deploy_args.max_new_tokens
        self.temperature = deploy_args.temperature
        self.batch_size = deploy_args.batch_size
        self.batch_timeout = deploy_args.batch_timeout
        # Construct save directory based on model name and data type
        if "/" in self.model_name:
            filename = self.model_name.split("/")
            self.save_directory = f"bigdl_{filename[1]}-{self.data_type}"
        else:
            self.save_directory = f"bigdl_{self.model_name}-{self.data_type}"

        # Load model and tokenizer if the directory exists, otherwise export and save them
        if os.path.exists(f"./{self.save_directory}"):
            self.model = AutoModelForCausalLM.load_low_bit(self.save_directory)
            self.tokenizer = AutoTokenizer.from_pretrained(self.save_directory)
            self.tokenizer.pad_token = self.tokenizer.eos_token
        else:
            model = AutoModelForCausalLM.from_pretrained(
                self.model_name, load_in_low_bit="sym_int8"
            )
            tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            model.save_low_bit(self.save_directory)
            tokenizer.save_pretrained(self.save_directory)
            self.model = AutoModelForCausalLM.load_low_bit(self.save_directory)
            self.tokenizer = AutoTokenizer.from_pretrained(self.save_directory)
            self.tokenizer.pad_token = self.tokenizer.eos_token

    @fastapi_app.post("/")
    async def handle_request(self, request: Request) -> StreamingResponse:
        """Handle incoming requests.

        :param request: HTTP request.
        :type request: Request
        :returns: StreamingResponse containing the generated text.
        :rtype: StreamingResponse
        """
        self.num_requests += 1
        request_dict = await request.json()
        prompt = request_dict.pop("prompt")
        logger.info(f'Got prompt: "{prompt}"')
        return StreamingResponse(
            self.run_model(prompt), media_type="text/plain"
        )

    @serve.batch(max_batch_size=10, batch_wait_timeout_s=1)
    async def run_model(self, prompts: List[str]):
        """Run the BigDL model to generate text.

        :param prompts: List of input prompts.
        :type prompts: List[str]
        :returns: Generator of decoded token batches.
        :rtype: Generator
        """
        streamer = RawStreamer()
        self.loop.run_in_executor(None, self.generate_text, prompts, streamer)
        on_prompt_tokens = True
        async for decoded_token_batch in self.consume_streamer(streamer):
            # The first batch of tokens contains the prompts, so we skip it.
            if not on_prompt_tokens:
                logger.info(
                    f"Yielding decoded_token_batch: {decoded_token_batch}"
                )
                yield decoded_token_batch
            else:
                logger.info(f"Skipped prompts: {decoded_token_batch}")
                on_prompt_tokens = False

    def generate_text(
        self,
        prompts: str,
        streamer: RawStreamer,
    ):
        """Generate text based on the given prompts.

        :param prompts: List of input prompts.
        :type prompts: List[str]
        :param streamer: RawStreamer object.
        :type streamer: RawStreamer
        """
        input_ids = self.tokenizer(prompts, return_tensors="pt", padding=True)
        start = time.perf_counter()
        generate_ids = self.model.generate(
            **input_ids,
            streamer=streamer,
            max_new_tokens=self.max_new_tokens,
            temperature=self.temperature,
        )
        end = time.perf_counter()
        num_tokens = sum([len(seq) for seq in generate_ids])
        self.tokens += num_tokens
        self.time += end - start
        throughput = float(num_tokens) / (end - start)
        logger.info(
            f"Throughput of the token generation is : {throughput:.3f} tokens/sec"
        )
        logger.info(
            f"avg_tokens_per_second: {self.tokens / self.time}\n"
            f"avg_inference_time:{self.time / self.num_requests} seconds"
        )

    async def consume_streamer(self, streamer: RawStreamer):
        """Consume the streamer and yield decoded token batches.

        :param streamer: RawStreamer object.
        :type streamer: RawStreamer
        :yields: Decoded token batches.
        :rtype: Generator
        """
        while True:
            try:
                for token_batch in streamer:
                    decoded_tokens = []
                    for token in token_batch:
                        decoded_tokens.append(
                            self.tokenizer.decode(
                                token, skip_special_tokens=True
                            )
                        )
                    logger.info(f"Yielding decoded tokens: {decoded_tokens}")
                    yield decoded_tokens
                break
            except Empty:
                await asyncio.sleep(0.001)

    def update_batch_params(self):
        """Update the server parameters through handler."""
        self.run_model.set_max_batch_size(self.batch_size)
        self.run_model.set_batch_wait_timeout_s(self.batch_timeout)


def typed_app_builder(deploy_args: DeployArgs) -> Application:
    """Application builder to handle typed deployment arguments.

    :param deploy_args: Deployment arguments.
    :type deploy_args: DeployArgs
    :returns: Ray Serve Application.
    :rtype: Application
    """
    return BigDLDeployment.bind(deploy_args)