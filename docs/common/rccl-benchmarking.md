# RCCL Benchmarking

The ROCm Collective Communications Library ([ROCm/rccl](https://github.com/ROCm/rccl)) is available as open-source software. Though RCCL is designed to be used as a performant backend for downstream applications, particularly AI training and inference workloads, it also has a test suite to benchmark and validate performance.

GPU collectives can measure performance in several ways, and RCCL benchmarks include both "algorithm" bandwidth and "bus" bandwidth metrics. For point-to-point operations, algorithm bandwidth is a reliable indication of hardware utilization, while for large collective operations bus bandwidth is a better measurement of hardware utilization. For more on the bus band metrics, please refer to the [performance documentation](https://github.com/ROCm/rccl-tests/blob/develop/doc/PERFORMANCE.md) in the RCCL tests repository.

RCCL implements operations such as all-reduce, all-gather, reduce, broadcast, reduce-scatter, gather, scatter, all-to-all, and direct GPU-to-GPU send/receive on the current node or another node.

## RCCL Test Details

### Broadcast

Copies data from one "root" GPU to all others, so every GPU ends up with an identical set of information.

**Performance Metric:** Measures how fast the root GPU can distribute its data to all others, with the focus on the effective bandwidth of this one-to-many transfer.

**Bus Bandwidth (busbw):** Calculated as the total data sent divided by the time taken. Since only the root sends data, busbw reflects the root's ability to saturate the network and is a direct measure of the broadcast efficiency.

### AllGather

Takes a unique chunk of data from each GPU and shares the full collection with every GPU, so everyone has the complete dataset.

**Performance Metric:** Assesses the total bandwidth and efficiency of exchanging and assembling all pieces among GPUs, highlighting how well the network handles simultaneous data sharing.

**Bus Bandwidth (busbw):** Adjusted for the number of GPUs, since each GPU both sends and receives data. This metric shows how efficiently the hardware can handle the collective data transfer required for all_gather.

### AllReduce

Combines data from all GPUs using an operation like sum or max, and then gives the final, combined result back to every GPU.

**Performance Metric:** Measures both the speed of combining data and distributing the result, focusing on throughput and latency-crucial for keeping distributed computations coordinated.

**Bus Bandwidth (busbw):** Considers that each GPU's data must be shared and the result returned, effectively doubling the data movement compared to all_gather. This metric reflects the maximum achievable bandwidth for this two-way communication pattern.

In this document, we report the expected bus bandwidth of the all_reduce operators. Additional tests are available in the [RCCL tests directory](https://github.com/ROCm/rccl-tests/tree/develop/test).

Measurements are reported for bus bandwidth and in-place operations, for message sizes of 8 GB. Higher scores are better.

## RCCL Installation

For running multi-node testing, rccl-tests need to be compiled with MPI support. The [GPU-enabled Message Passing Interface Guide](https://rocm.docs.amd.com/en/docs-6.1.2/how-to/gpu-enabled-mpi.html) contains specific instructions for how to install a ROCm-aware MPI installation for RoCE and InfiniBand-based networks.

### UCX and OpenMPI Installation

Follow the instructions in the [GPU-enabled MPI Guide](https://rocm.docs.amd.com/en/docs-6.1.2/how-to/gpu-enabled-mpi.html) to install UCX and OpenMPI with ROCm support.

### RCCL Installation from Source

RCCL can be installed from source using the following commands. Use the appropriate version tag for your ROCm version:

| ROCm Version | RCCL Tag |
|--------------|----------|
| ROCm 7.0.2 | `tags/rocm-7.0.2` |
| ROCm 7.0.1 | `tags/rocm-7.0.1` |
| ROCm 6.3.x/6.4.x | `drop/2025-06-J13A-1` |

```bash
git clone https://github.com/ROCm/rccl.git
cd rccl
git checkout <appropriate_tag>
./install.sh -i
```

### RCCL-Tests Installation

Once OpenMPI is installed, install RCCL-tests with the following script:

```bash
# Define preferred paths for MPI and RCCL installations
# (ensure /lib/libmpi.so and /lib/librccl.so exist in both install paths)
MPI_INSTALL_DIR=/path/to/mpi
RCCL_INSTALL_DIR=/path/to/rccl

# If HIP is not installed in /opt/rocm, add `HIP_HOME=/path/to/hip` to the cmake parameters.

build_rccl_tests() {
  if [ ! -d rccl-tests ]; then
    git clone https://github.com/ROCm/rccl-tests
    cd rccl-tests
    make MPI=1 MPI_HOME=${MPI_INSTALL_DIR} NCCL_HOME=${RCCL_INSTALL_DIR} -j
  fi
}

# Build RCCL tests
build_rccl_tests
```

This script differs from the previous commands by specifying flags and locations for the MPI install in the cmake parameters. RCCL-tests should now have MPI support.

## Single-Node RCCL Testing

### Allreduce Test

To evaluate the Allreduce operator using the RCCL tests benchmark, run the following command:

```bash
./all_reduce_perf -b 8 -e 8G -f 2 -g 8
```

The RCCL all-reduce test criteria is to exceed an in-place busbw metric of **304 GB/s** for MI300X or **350 GB/s** for MI350X/MI355X at a message size of 8 GB.

**Example output:**

```
# nThread 1 nGpus 8 minBytes 8 maxBytes 8589934592 step: 2(factor) warmup iters: 5 iters: 20 agg iters: 1 validation: 1 graph: 0
#
rccl-tests: Version Unknown
# Using devices
#  Rank  0 Group  0 Pid 657053 on smci350-zts-gtu-e14-05 device  0 [0000:75:00] AMD Instinct MI350X
#  Rank  1 Group  0 Pid 657053 on smci350-zts-gtu-e14-05 device  1 [0000:05:00] AMD Instinct MI350X
...
#                                                              out-of-place                       in-place
#       size         count      type   redop    root     time   algbw   busbw  #wrong     time   algbw   busbw  #wrong
#        (B)    (elements)                               (us)  (GB/s)  (GB/s)           (us)  (GB/s)  (GB/s)
           8             2     float     sum      -1    58.63    0.00    0.00       0    49.68    0.00    0.00       0
...
  8589934592    2147483648     float     sum      -1   41644  206.27  360.97       0   40903  210.01  367.51       0
# Errors with asterisks indicate errors that have exceeded the maximum threshold.
# Out of bounds values : 0 OK
# Avg bus bandwidth    : 111.827
```

The MPI enabled version then runs with one GPU per MPI rank and is launched by mpirun:

```bash
mpirun -np 8 ./all_reduce_perf -b 8 -e 8G -f 2 -g 1
```

**Result:**

* **PASSED:** In-place busbw at 8 GB message size is 304 GB/s or greater for MI300X, or 350 GB/s or greater for MI350X/MI355X.
* **FAILED:** busbw less than expected values.

### Single-Node RCCL Test Script

The following is an example single-node test script that runs all RCCL collectives:

```bash
#!/usr/bin/bash

# Updated Date: 6/2/2025
# Notes: Single-node RCCL test script

RCCL_TESTS_DIR=<path_to_rccl_tests>
TIMESTAMP=$(date +"%Y%m%d%H%M%S")

# Ensure IOMMU is disabled or in passthrough mode
# Ensure ACS is disabled for consistent results

for bench in all_gather_perf all_reduce_perf alltoall_perf broadcast_perf \
             gather_perf reduce_perf reduce_scatter_perf scatter_perf sendrecv_perf; do
  echo "Running ${bench}..."
  ${RCCL_TESTS_DIR}/build/${bench} -b 8 -e 8G -f 2 -g 8 2>&1 | tee ${TIMESTAMP}_${bench}.txt
  sleep 5
done
```

## Single-Node RCCL with the Cluster Validation Suite

The single-node RCCL tests recommended for deployment can be automated using the [Cluster Validation Suite](https://rocm.docs.amd.com/projects/cvs/en/latest/).

Before running CVS, ensure that the configuration files for your specific platform and the nodes under test are correctly defined in the `cvs/input/config_file/` subdirectories.

After [installing the test suite](https://rocm.docs.amd.com/projects/cvs/en/latest/install/cvs-install.html), run the single-node RCCL test using:

```bash
pytest -vvv --log-file=/tmp/test.log -s ./tests/rccl/rccl_singlenode_cvs.py \
  --cluster_file input/cluster_file/cluster.json \
  --config_file input/config_file/rccl/single_node_mi355_rccl.json \
  --html=/var/www/html/cvs/rccl.html --capture=tee-sys --self-contained-html
```

## Multi-Node RCCL Testing

For multi-node RCCL testing instructions, see the [Network and Cluster Validation](../network/validation.md#rccl-multi-node-fabric-test) section.
