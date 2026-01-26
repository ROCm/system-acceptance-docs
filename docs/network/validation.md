# Network and Cluster Validation

This chapter details validation of the network and the cluster. Validating network performance and reliability for AMD Instinct™ platforms is essential to ensure optimal data throughput and cluster efficiency.

This section outlines pre-validation checks, such as enabling RDMA on backend NICs and verifying link speeds, with 400G NICs recommended for avoiding bottlenecks. The chapter also details the installation and execution of Open Fabrics Enterprise Distribution (OFED) performance tests to validate GPU-to-NIC, NIC-to-switch, and host-to-host communication, including specific tests for GPU-to-GPU and NIC-to-switch paths. Disabling ACS is advised for consistent performance during testing.

Multi-node RCCL tests are introduced to verify inter-node GPU communication, with automation options available via the Cluster Validation Suite. The chapter then transitions to cluster validation, establishing performance baselines and guiding further optimization. It recommends AI model validation using benchmarks like Llama 3.1 and provides resources for multi-node network performance validation, emphasizing workload tuning for enhanced efficiency on AMD Instinct™ systems.

## Network Validation

This section covers essential steps for validating network performance and reliability on AMD Instinct™ platforms. Proper network validation is critical, as misconfigured settings or faulty hardware can significantly impact data throughput and cluster efficiency. The process includes both software and hardware checks—from enabling RDMA (Remote Direct Memory Access) and verifying link speed to running targeted performance benchmarks and evaluating collective GPU operations. By following the outlined procedures, you can quickly identify and resolve network bottlenecks, ensuring your system delivers optimal performance for high-demand workloads.

## Pre-Validation Network Checks

Before initiating network tests, follow the below steps to ensure all backend interfaces are RDMA-enabled and running at the specified speed. These checks confirm that your AMD Instinct™ cluster is prepared for consistent, high-performance networking.

### Enable RDMA on All Backend NICs

All the backend network interfaces should support RDMA. To ensure it is enabled use the command:

```bash
rdma link
```

Result:

* PASSED: All 8 backend NICs should be listed and report status as ENABLED.
* FAILED: One or more of the backend network interfaces is not listed or is DISABLED.

### Check NIC Link Speed

Verify the NICs in your servers are reporting the correct speeds. Several commands and utilities are available to measure speed based on your network type. For the AMD Instinct™ product line 400G network cards are generally advised. 200G cards are not sufficient to avoid bottlenecks and 800G cards and not needed.

#### RoCE / Ethernet

1. Set backend NIC speed

   ```bash
   ethtool -s "<interface>" autoneg off speed 400000 duplex full
   ```

2. Check backend NIC speed

```bash
sudo ethtool <interface> | grep -i speed
cat /sys/class/net/<interface>/speed
```

#### InfiniBand

`ibdiagnet` provides an output of the entire fabric in the default log files. You can verify link speeds here.
`ibstat` or `ibstatus` tells you if the link is up and reports the speed at which it is running for all HCAs in the server.

#### Result

* PASSED: All backend NICs report a speed of 400000
* FAILED: Any result less than 400000

## RCCL Multi-Node Fabric Test

Multi-node RCCL testing verifies that GPUs in one node can communicate correctly and efficiently with GPUs in other nodes in the cluster, ensuring that the communication fabric is functioning properly. An overview of RCCL, along with configuration instructions, is provided in the [RCCL Benchmarking](../common/rccl-benchmarking.md) section. It is generally recommended to run this test on a subset of the deployment, either the full cluster or up to sixteen nodes, whichever is smaller.

### RCCL Pre-Checks

To ensure that RCCL runs properly, please ensure that the following criteria are met:

1. Ensure that UCX, OpenMPI, RCCL-Tests and AMD ANP are built using the options given in this document.
2. Run a fabric ping test and ensure reachability.
3. Configure PFC and DCQCN with recommended parameters.
4. Ensure QoS (PFC + DCQCN) is configured across the network and DSCP marking at NICs and Switches are in sync.
5. Set ulimit value to infinite.
6. Run OFED Performance Tests, CPU-to-CPU and GPU-to-GPU, across the cluster.
7. Disable ACS. Performance will vary dramatically if ACS is enabled.

### RCCL Multi-Node Test

Refer to the [RCCL Benchmarking](../common/rccl-benchmarking.md) page for detailed instructions on building and running multi-node RCCL tests.

**Result:**

* PASSED: For a two node cluster, Allreduce performance of 304 GB/s or greater for MI300X. For a two node cluster, Allreduce performance of 350 GB/s or greater for MI350X or MI355X.
* FAILED: Allreduce performance less than expected values.

### RCCL Multi-Node Tests with the Cluster Validation Suite

The multi-node RCCL test recommended for deployment can be automated using the [Cluster Validation Suite](https://rocm.docs.amd.com/projects/cvs/en/latest/).

Before running CVS, ensure that the configuration files for your specific platform and the nodes under test are correctly defined in the `cvs/input/config_file/` subdirectories.

After [installing the test suite](https://rocm.docs.amd.com/projects/cvs/en/latest/install/cvs-install.html), deploy RCCL to the cluster using:

```bash
pytest -vvv --log-file=/tmp/test.log -s ./tests/rccl/rccl_multinode_cvs.py \
  --cluster_file input/cluster_file/cluster.json \
  --config_file input/config_file/rccl/rccl_config.json \
  --html=/var/www/html/cvs/rccl.html --capture=tee-sys --self-contained-html
```

## Cluster Validation

After successfully completing the tests mentioned in this guide, the System Under Test (SUT) meets the single-node customer acceptance criteria. The test results related to performance serve as a baseline for further enhancements. To further optimize the system, make incremental changes to individual parameters noted in the prerequisites and repeat the tests. Once complete, proceed with AI model validation and cluster network validation using the guides mentioned below.

### Cluster Network Performance Validation

After validating single-node performance, configure each server for maximum data transfer and bandwidth. It is essential to test both host and device performance in single-node and multi-node setups using targeted benchmarks.

The [Cluster Network Performance Validation Guide](https://rocm.docs.amd.com/projects/gpu-cluster-networking/en/latest/) for single-node and multi-node networking provides step-by-step instructions on configuring network settings, devices, and running performance tests to ensure AMD Instinct™-based GPU clusters operate at peak speed and bandwidth.

Use the guides as follows:

1. Validate and optimize a single server using the [Single Node Configuration](https://instinct.docs.amd.com/projects/gpu-cluster-networking/en/latest/how-to/single-node-config.html) section of the GPU Cluster Networking guide.
2. If you are using a RoCE network, consult the [RoCE Network Configuration Guide](https://instinct.docs.amd.com/projects/gpu-cluster-networking/en/latest/how-to/roce-network-config.html) for additional steps pertaining to your hardware. Otherwise, proceed to step 3.
3. Once all individual nodes are validated, proceed through the [Multi-node Networking Guide](https://instinct.docs.amd.com/projects/gpu-cluster-networking/en/latest/how-to/multi-node-config.html). If you did not install MPI-supported rccl-tests in the [RCCL Benchmarking](../common/rccl-benchmarking.md) section, ensure you do so when following the multi-node guide.

To thoroughly evaluate your cluster's performance, we recommend using the Llama 3.1 405B training benchmark with the JAX library. Please note that the runtime will vary depending on the number of nodes, NICs per node, and overall cluster configuration.

There is no multi-node inference benchmark suggested to evaluate clusters at this time, but use of vLLM and SGLang should be considered.

### AI Workload Validation with the Cluster Validation Suite

AMD recommends using the workload of Llama 3.1 405B with JAX for multi-node testing.

The [Cluster Validation Suite](https://rocm.docs.amd.com/projects/cvs/en/latest/) includes scripts for automatically installing and running this workload as part of deployment testing. Additional documentation is available on the ROCm website under *Run Cluster Validation Suite Tests* page, within the [Jax training test scripts](https://rocm.docs.amd.com/projects/cvs/en/latest/how-to/run-cvs-tests.html#jax-training-test-scripts) section.

### Workload Optimization

Once the system and networking have been fully validated, review the [Workload Optimization Guide](https://rocm.docs.amd.com/projects/gpu-cluster-networking/en/latest/how-to/workload-optimization.html) to learn more about how to tune workloads for maximum performance on AMD Instinct™ systems.
