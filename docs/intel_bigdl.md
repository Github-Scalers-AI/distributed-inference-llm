# Intel BigDL-LLM Documentation


## Table of Contents


* [Features of BigDL Project](#features-of-bigdl-project)
* [What is BigDL-LLM?](#what-is-bigdl-llm)
* [Why BigDL- LLM?](#why-bigdl--llm)

## Features of BigDL Project

BigDL scales Machine Learning and AI applications from laptop to cloud by offering the following libraries.

1. **LLM** - Low-bit (INT3/INT4/INT5/INT8) large language model library for Intel CPU/GPU
2. **Orca** - Distributed Big Data and AI(TF and Pytorch) Pipeline on Spark and Ray
3. **Nano** - Transparent Acceleration of Tensorflow and Pytorch programs on Intel CPU/GPU
4. **DLlib** - Equivalent of Spark MLlib for Deep Learning
5. **Chronos** - Scalable Time Series Analysis using AutoML
6. **Friesian** - End-to-End Recommendation System
7. **PPML** - Secure Big Data and AI(with SGX Hardware Security)

## What is BigDL-LLM?

BigDL-LLM, recently open sourced by Intel, is a software development kit (SDK) created with a specific focus on large language models (LLMs) on Intel XPUs. Developers can enhance their LLM models for edge devices by utilizing BigDL-LLM and [INT4](https://arxiv.org/abs/2301.12017) support on compatible Intel XPUs. This optimization enables efficient execution, improved memory utilization, and enhanced computational performance.


## Why BigDL- LLM?

Human-language applications have undergone a revolutionary shift as a result of large language models' (LLMs) astounding scale—more than 100 billion parameters. However, due to these models' enormous size and latency, AI researchers and developers frequently run into problems. These difficulties may impede cooperation and the development of reliable applications.

Intel has unveiled BigDL-LLM, a method to address this problem. It includes several optimisations that make it possible for huge language models to run on laptops, increasing its usability for developers.

With BigDL-LLM,it is possible to:



* Convert models to lower precision (INT4).
* Use transformers like APIs to run the model inference.
* Integrate the model with a LangChain pipeline.

For more information on BigDL refer [BigDL Research paper](https://arxiv.org/abs/1804.05839) or [BigDL GitHub repo](https://github.com/intel-analytics/BigDL).
