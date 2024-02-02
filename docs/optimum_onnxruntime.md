# HuggingFace Optimum Onnx Runtime Documentation

## Table of Contents

- [Introduction](#introduction)
- [Model Optimizations](#model-optimizations)
   * [Quantize ONNX Models](#quantize-onnx-models)

# Introduction

Optimum is a utility package for building and running inference with accelerated runtime like ONNX Runtime. Optimum can be used to load optimized models from the Hugging Face Hub and create pipelines to run accelerated inference without rewriting your APIs.

ONNX (Open Neural Network Exchange) is an open standard for representing machine learning models, created by Microsoft and partners. It allows users to convert models trained in one framework into a format that can be used with other frameworks, making it easier to switch between different deep learning libraries and tools.

ONNX Runtime is the runtime component of the ONNX ecosystem, designed to execute ONNX models efficiently across a wide range of platforms(Linux, Windows, Mac) and integrates with accelerators like TensorRT, OpenVINO, and DirectML. With APIs in C, Python, C#, Java, and JavaScript, it streamlines model deployment and optimization, making it a versatile solution for varied hardware configurations.This possibility can be done through the APIs provided by ONNX Runtime itself (under the title of Execution Providers or EP). In other words, Execution Providers are hardware acceleration interfaces for querying the capabilities of that hardware.

## Model Optimizations

### Quantize ONNX Models

1. Quantization in ONNX Runtime refers to 8 bit linear quantization of an ONNX model.
2. Pre-processing is to transform a float32 model to prepare it for quantization. It consists of the following three optional steps:
   * Symbolic shape inference. This is best suited for transformer models.
   * Model optimization: This step uses ONNX Runtime native library to rewrite the computation graph, including merging computation nodes, eliminating redundancies to improve runtime efficiency.
   * ONNX shape inference.
3. There are two ways of quantizing a model: dynamic and static.
    1. Dynamic quantization calculates the quantization parameters (scale and zero point) for activations dynamically. These calculations increase the cost of inference, while usually achieve higher accuracy comparing to static ones.Python API for dynamic quantization is in module `onnxruntime.quantization.quantize`, function `quantize_dynamic()`
    2. Static quantization method first runs the model using a set of inputs called calibration data. During these runs, we compute the quantization parameters for each activations. These quantization parameters are written as constants to the quantized model and used for all inputs. Our quantization tool supports three calibration methods: MinMax, Entropy Python API for static quantization is in module `onnxruntime.quantization.quantize`, function `quantize_static()`.


For more information refer [HuggingFace Optimum ONNX Runtime](https://huggingface.co/docs/optimum/v1.2.1/en/onnxruntime/modeling_ort) and [ONNX Runtime](https://github.com/microsoft/onnxruntime).
