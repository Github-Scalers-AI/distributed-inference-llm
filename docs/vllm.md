# vLLM Documentation


## Table of Contents

* [Introduction](#introduction)
* [PagedAttention: The Magic Behind vLLM](#pagedattention-the-magic-behind-vllm)
* [Features of vLLM](#features-of-vllm)

## Introduction

Using LLMs today is computationally expensive and is slow even on expensive hardware.vLLMs are an open source library aiming to change that by making inference and serving faster.vLLMs achieve up to 24x higher throughput compared to HuggingFace Transformers(HF). The algorithm behind this performance is called PagedAttention.

## PagedAttention: The Magic Behind vLLM

LLM performance takes a hit because of memory. In the decoding process, all input tokens create their attention keys and values, hogging GPU memory to generate the next tokens. This cache, known as KV cache. This cache, which is in charge of holding the data required to produce subsequent tokens, is difficult to manage well since it is both big (up to 1.7GB for a single sequence) and dynamic in size.

PagedAttention makes it possible to store keys and values in non-contiguous memory space.This method is similar to how operating systems' virtual memory systems optimise resource allocation and storage. In this case, tokens are like bytes, blocks are like pages, and sequences are like processes. Even though a sequence's logical blocks are continuous, a block table maps them to physically non-contiguous blocks. Physical blocks are allocated on demand as new tokens are created, allowing for a more dynamic and effective usage of memory.

As a result, memory efficiency is improved by reducing fragmentation and enabling sharing.

## Features of vLLM

* Seamless integration with popular Hugging Face models
* High-throughput serving with various decoding algorithms, including _parallel sampling_, _beam search_, and more
* Tensor parallelism support for distributed inference
* Streaming outputs
* OpenAI-compatible API server

For more information refer [vLLM Documentation](https://vllm.readthedocs.io/).
