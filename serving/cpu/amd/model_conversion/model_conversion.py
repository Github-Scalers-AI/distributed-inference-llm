import argparse
import glob
import os

from transformers import AutoConfig, AutoTokenizer


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Convert transformer model to ONNX format"
    )
    parser.add_argument(
        "--model_name", type=str, required=True, help="Transformer model name"
    )
    parser.add_argument(
        "--data_type",
        type=str,
        default="int8",
        help="Data type for model precision",
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    save_directory = ""

    if "/" in args.model_name:
        filename = args.model_name.split("/")
        save_directory = f"onnx_{filename[1]}-{args.data_type}"
    else:
        save_directory = f"onnx_{args.model_name}-{args.data_type}"

    command = (
        f"python3 -m onnxruntime.transformers.models.llama.convert_to_onnx"
        f" -m {args.model_name}"
        f" --output {save_directory} --precision {args.data_type}"
        " --quantization_method quantize_dynamic --execution_provider cpu"
    )
    os.system(command)

    files_to_delete = glob.glob(os.path.join(f"{save_directory}", "*fp32*"))
    for file in files_to_delete:
        os.remove(file)

    onnx_files = glob.glob(os.path.join(f"{save_directory}", "*.onnx"))
    for old_filename in onnx_files:
        new_name = os.path.join(save_directory, "model.onnx")
        os.rename(old_filename, new_name)

    # Save config file in ONNX model directory
    config = AutoConfig.from_pretrained(args.model_name)
    config.save_pretrained(save_directory)
    tokenizer = AutoTokenizer.from_pretrained(args.model_name)
    tokenizer.save_pretrained(save_directory)


if __name__ == "__main__":
    main()
