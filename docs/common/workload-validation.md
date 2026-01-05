# Workload Validation

Systems under test should be capable of running large AI models, including Large Language Models (LLMs). This section provides guidance on validating AI model performance on AMD Instinct systems.

## AI Model Performance Check

For LLM Inference and Training performance results for validation, refer to the latest [Performance Results with AMD ROCm Software](https://www.amd.com/en/developer/resources/rocm-hub/dev-ai/performance-results.html) on the [AMD ROCm AI Developer Hub](https://www.amd.com/en/developer/resources/rocm-hub/dev-ai.htm) or the [AMD Infinity Hub](https://www.amd.com/en/developer/resources/infinity-hub.html).

Detailed instructions on how to reproduce these results can be found at the following links:

* [Measuring inference performance with vLLM](https://rocm.docs.amd.com/en/latest/how-to/rocm-for-ai/inference/vllm-benchmark.html)
* [Measuring training performance with ROCm PyTorch Docker](https://rocm.docs.amd.com/en/latest/how-to/rocm-for-ai/training/benchmark-docker/pytorch-training.html)
* [Measuring training performance with ROCm Megatron-LM Docker](https://rocm.docs.amd.com/en/latest/how-to/rocm-for-ai/training/benchmark-docker/megatron-lm.html)

## Single-Node Workload Validation

For single-node deployment validation, AMD recommends running Llama 3.1 70B with JAX using the Cluster Validation Suite.

### AI Model Performance Validation with the Cluster Validation Suite

For system validation during deployment, AMD recommends using Llama 3.1 70B with JAX for single-node testing.

The [Cluster Validation Suite](https://rocm.docs.amd.com/projects/cvs/en/latest/) includes scripts for automatically installing and running these workloads. See the [Jax training test scripts](https://rocm.docs.amd.com/projects/cvs/en/latest/how-to/run-cvs-tests.html#jax-training-test-scripts) section.

The [Megatron](https://rocm.docs.amd.com/projects/cvs/en/latest/how-to/run-cvs-tests.html#megatron-training-test-scripts) workload is also supported as an optional deployment workload.

## Multi-Node Workload Validation

For multi-node workload validation, see the [Network and Cluster Validation](../network/validation.md#ai-workload-validation-with-the-cluster-validation-suite) section.

AMD recommends using the workload of Llama 3.1 405B with JAX for multi-node testing. The runtime will vary depending on the number of nodes, NICs per node, and overall cluster configuration.

There is no multi-node inference benchmark suggested to evaluate clusters at this time, but use of vLLM and SGLang should be considered.
