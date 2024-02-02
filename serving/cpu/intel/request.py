import ray
import requests

ray.init()  # Initialize Ray.


@ray.remote
class RequestActor:
    def send_request(self):
        prompt = "How to draw a triangle?"
        response = requests.post(
            f"http://localhost:8000/?prompt={prompt}", stream=True
        )
        response.raise_for_status()
        for chunk in response.iter_content(
            chunk_size=None, decode_unicode=True
        ):
            print(chunk)


actor = RequestActor.remote()  # Create an instance of the actor.
ray.get(
    actor.send_request.remote()
)  # Call the actor method and wait for it to complete.
