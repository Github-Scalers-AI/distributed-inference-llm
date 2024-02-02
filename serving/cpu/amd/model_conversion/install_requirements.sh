#!/bin/bash

# Install base requirements
pip3 install --no-cache-dir -r custom_requirements.txt

# Install PyTorch nightly build for CPU
pip3 install --no-cache-dir torch --index-url https://download.pytorch.org/whl/nightly/cpu

# Download requirements files
wget https://raw.githubusercontent.com/microsoft/onnxruntime/main/onnxruntime/python/tools/transformers/models/llama/requirements-cpu.txt
wget https://github.com/microsoft/onnxruntime/blob/main/onnxruntime/python/tools/transformers/models/llama/requirements-70b-model.txt
wget https://raw.githubusercontent.com/microsoft/onnxruntime/main/onnxruntime/python/tools/transformers/models/llama/requirements.txt

# Install requirements for CPU
pip3 install --no-cache-dir -r requirements-cpu.txt

# Install requirements for CPU
pip3 install --no-cache-dir -r requirements-70b-model.txt
