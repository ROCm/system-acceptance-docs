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

For more information on AMD Instinct products, applications, configuration, and related software, see the [AMD Instinct Documentation](https://instinct.docs.amd.com/latest/).

## Testing Overview

Testing is generally divided into two categories: single-node tests, which verify the functionality of individual nodes, and multi-node tests, which validate the overall operation of the cluster. An exception to this division is the use of Open Fabrics Enterprise Distribution (OFED) Performance Tests, which are particularly useful for diagnosing network-related issues for a single node such as faulty cables.

The following tables provide estimated test durations; however, these estimates do not include the time required for test configuration or workload file transfers, which can be significant. Actual test durations may vary depending on the number of nodes and the level of thoroughness desired.

### Single Node Tests

| Test | Estimated Duration |
| --- | --- |
| CVS Configuration Checker | 12 Minutes |
| AGFHC all_lvl5 | 2 Hours |
| AGFHC hbm_lvl5 | 4 Iterations, 8 Hours |
| AGFHC minihpl | 4 Hours |
| AGFHC xgmi_lvl1 | 5 Minutes |
| AGFHC pcie_lvl2 | 10 Minutes |
| Single Node RCCL | 2 to 11 Minutes |
| Optional TransferBench | 2 Hours |
| Optional Llama 3.1 70B | 1 to 24 Hours |

### Multi-Node Tests

| Test | Estimated Duration |
| --- | --- |
| OFED Performance Tests | 2 Hours |
| Multi-node RCCL | 10 Minutes |
| Llama 3.1 405B with JAX | 1 Hour |

### Cluster Validation Suite

Many of the tasks described in this guide, from checking system configuration to executing single-node and multi-node tests, can be automated using the Cluster Validation Suite (CVS). This toolset verifies the health and performance of AMD AI clusters at scale, extending validation across multiple nodes without requiring extensive manual intervention.

- [Cluster Validation Suite Documentation](https://rocm.docs.amd.com/projects/cvs/en/latest/)
- [CVS GitHub Repository](https://github.com/ROCm/cvs)

Individual test examples utilizing the CVS for single and multi-node tests are called out in the following sections. Ensure that the configuration files for your specific platform and the nodes under test are correctly defined in the `cvs/input/config_file/` subdirectories before running CVS. Misconfigured files can lead to delays in testing and inaccurate results.

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
3. **[Topology Mapping](network/topology-mapping.md)** – Discover and map network topology relationships
4. **[RDMA Benchmarking](network/rdma-benchmarking.md)** – Measure RDMA bandwidth and latency performance
5. **[Cluster Validation](network/validation.md)** – Execute multi-node validation tests and verify readiness gates

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
