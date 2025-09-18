<!--
description: AMD Instinct GPU and system/cluster acceptance, validation, and optimization guide covering node (GPU) and multi-node (network / fabric) workflows for CDNA3+ full validation and earlier-generation performance tuning.
keywords: AMD Instinct, system validation, cluster validation, acceptance testing, performance tuning, ROCm, CDNA3, RDMA, networking
-->

# AMD Instinct™ Customer Acceptance Guide

This comprehensive guide provides a structured, repeatable methodology for configuring, validating, benchmarking, and baselining AMD Instinct™ GPU platforms at both single-node and multi-node (cluster) levels.

**Target Audience:** Data center operators, solution engineers, performance engineers, and validation teams preparing AMD Instinct systems and clusters for customer acceptance and production deployment.

**Purpose:** Build confidence that your system under test (SUT) and the broader cluster are functionally correct, performance-aligned with expectations, and ready for production workloads including HPC, AI/LLM, and analytics applications.

## Validation Approach

This guide follows a two-phase validation approach:

**Node (GPU/Server) Validation**  
Establish a known-good baseline for each individual server, including prerequisites verification, firmware and BIOS alignment, kernel parameter configuration, ROCm installation, health checks, GPU validation, microbenchmark performance testing, and acceptance threshold validation per GPU.

**Cluster & Fabric Validation**  
Extend validation across multiple nodes, covering NIC driver installation, network routing and configuration, performance optimization, topology mapping, RDMA benchmarking, and comprehensive cluster-level validation.

## Getting Started

1. Complete all node-level steps on one representative system
2. Replicate the validated configuration across all remaining nodes  
3. Proceed to cluster-level networking and multi-node validation

### Node (Single-System) Validation

Start by selecting the page for the specific GPU accelerator you are validating. Each GPU-specific page provides a guided flow and links back to the prerequisite, health check, and validation/benchmark steps you must complete for that platform:

- **[AMD Instinct MI355X](gpus/mi355x.md)**
- **[AMD Instinct MI350X](gpus/mi350x.md)**
- **[AMD Instinct MI325X](gpus/mi325x.md)**
- **[AMD Instinct MI300X](gpus/mi300x.md)**

Follow the GPU page end‑to‑end; it will walk you through verifying system prerequisites, running health checks, executing validation suites and microbenchmarks, and applying acceptance criteria thresholds.

For reference, these are the core supporting steps the GPU pages will direct you through:

1. **[System Prerequisites](common/prerequisites.md)** – Supported OS, firmware/BIOS alignment, GRUB configuration, and foundational OS tuning
2. **[Health Checks](common/health-checks.md)** – Rapid validation of OS state, boot configuration, host memory, PCIe/GPU visibility, and interconnect health
3. **[System Validation & Benchmarks](common/system-validation.md)** – Comprehensive compute, memory, I/O, and power validation using ROCm Validation Suite (RVS)/AMD GPU Field Health Check (AGFHC) and microbenchmarks (TransferBench, RCCL, rocBLAS, BabelStream)

After completing the GPU-specific acceptance sequence on one node, replicate the validated configuration across remaining nodes before moving to multi-node (cluster) validation.

### Cluster & Network Validation

After completing node validation, proceed with network and multi-node testing:

1. **[NIC Driver Installation](network/nic-installation.md)** – Install and validate network interface card drivers
2. **[Network Configuration](network/configuration.md)** – Configure network routing and establish baseline settings
3. **[Performance Optimization](network/optimization.md)** – Apply network performance tuning for optimal throughput
4. **[Topology Mapping](network/topology-mapping.md)** – Discover and map network topology relationships
5. **[RDMA Benchmarking](network/rdma-benchmarking.md)** – Measure RDMA bandwidth and latency performance
6. **[Cluster Validation](network/validation.md)** – Execute multi-node validation tests and verify readiness gates

Additional networking and cluster performance guidance is available in the AMD [GPU cluster networking documentation](https://instinct.docs.amd.com/projects/gpu-cluster-networking/en/latest/)

### GPU Support Coverage

- **CDNA3+ (MI300 series and later):** Complete validation workflows including detailed health checks, ROCm Validation Suite (RVS) procedures, microbenchmark baselines, and explicit pass/fail acceptance criteria.
- **Earlier-generation GPUs (pre-CDNA3):** Focused guidance through concise overview pages covering essential configuration steps and recommended performance tuning procedures.

## Reference Resources

Additional supporting materials and documentation:

- **[Related Documentation](reference/related-documentation.md)** – Links to AMD official documentation, ROCm guides, and third-party resources
- **[Glossary](reference/glossary.md)** – Definitions of technical terms and acronyms used throughout this guide  
- **[ROCm Technical Support](reference/rocm-techsupport.md)** – Troubleshooting procedures and technical support contact information

```{note}
This guide is a work in progress and its content is subject to updates and improvements in future revisions.
```
