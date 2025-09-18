# RDMA and RCCL Benchmarking

This section covers essential steps for validating network performance and reliability on AMD Instinct™ platforms. The process includes both software and hardware checks—from enabling RDMA (Remote Direct Memory Access) and verifying link speed to running targeted performance benchmarks and evaluating collective GPU operations. By following the outlined procedures, you can quickly identify and resolve network bottlenecks, ensuring your system delivers optimal performance for high-demand workloads.

## OFED RDMA Perftest

Install and run the [OFED performance tests](https://github.com/linux-rdma/perftest) for GPU to NIC, NIC to switch, and host to host (H2H) testing. Loopback is implemented in the tests to remove the switch from benchmark results.

### Perftest installation

Remember to install OFED perftests on both nodes you plan to use in this section. Commands may require `sudo` depending on user privileges.

Install the prerequisites:

```bash
sudo apt install libibumad-dev pciutils libpci* automake autoconf libtool libibverbs-dev ibverbs-utils infiniband-diags perftest ethtool librdmacm-dev
```

From the CLI of your host, clone the perftest repository.

```bash
git clone https://github.com/linux-rdma/perftest.git
```

Navigate to the installation directory and build the tests.

```bash
cd perftest
./autogen.sh
./configure --prefix=$PWD/install --enable-rocm --with-rocm=/opt/rocm
```

Locate and open `makefile` in your editor of choice, then append `-D__HIP_PLATFORM_AMD__` to `CFLAGS` and `CXXFLAGS`. This is required to compile the code correctly for this guide.

Run `make -j && make install`.

Repeat these steps on a second node for when starting multi-node testing.

### Perftest Sanity Test

Utilizing commands supported by the perftest suite, various system components can be unit tested. This allows for fast and accurate debugging by isolating the components. Common issues include peer-to-peer enablement, network configuration, transceivers, and cables. A methodical approach checking each component will save time overall.

### Disabling ACS

For performance testing with perftest and RCCL, ACS should be disabled for optimal and consistent performance. If virtualization is not needed for this implementation, ACS can be permanently disabled in the BIOS for improved performance. In addition to disabling ACS in BIOS, it can temporarily be disabled in the system via software.

To temporarily disable ACS, use the script linked at: [dis_acs.sh](https://github.com/ROCm/cluster-networking/blob/main/general_scripts/dis_acs.sh) This change will only take effect on the system until it is rebooted.

#### Perftest GPU to NIC

Testing the path from the GPU to the NIC to check that there is an optimized peer-to-peer path. This ensures that peer-to-peer RDMA support has been enabled. For accurate testing it is important to use the GPU adjacent to the backend network interface card. All 8 GPUs should be tested to their adjacent NIC.

Run the following command pairs for each of the 8 GPUs and the adjacent NICs:

```bash
# Host/Listener
sudo ./ib_write_bw -x 3 -a -b -F -d <NIC 0> --report_gbits

# Client in a separate window
sudo ./ib_write_bw -x 3 -a -b -F --use_rocm=<GPU Adjacent to NIC 0> -d <NIC 0> --report_gbits 127.0.0.1
```

##### Result

* PASSED: All 8 paths report average throughput of 700 Gbps or greater at some point during the test.
* FAILED: Unable to reach an average speed equal to or greater than 700 Gbps.

#### Perftest NIC to Switch to NIC

Testing the path from one NIC to another through the network switch is to ensure that each NIC sends and receives data at the expected speed to validate the NIC, all transceivers, the cable, and the backend switch ports.

Run the following set of commands 16 times, once to check the send path and once to check the receive path for each of the 8 network interfaces. A second node is needed for this test since data will be routed locally over the PCIe bus if a single node is used. This will ensure that all NICs are functioning properly and that the connection to the supporting network switch is valid.

```bash
# NIC to NIC for a single node
# Node 0 Host/Listener
sudo ./ib_write_bw -x 3 -a -b -F -d <NIC 0> --report_gbits

# Node 1 Client in a separate window
sudo ./ib_write_bw -x 3 -a -b -F -d <NIC 1> --report_gbits <host_ip for NIC 0 on node 0>
```

##### Result

* PASSED: All paths report average throughput of a 400G NIC as 380 Gbps or greater at some point during the test.
* FAILED: Unable to reach an average speed equal to or greater than 380 Gbps for a 400G NIC.

#### Perftest GPU to GPU through the Switch

Run the following set of commands 16 times, once to check the send path and once to check the receive path GPU though the NIC out to the switch is valid. A second node is needed for this test since data will be routed locally over the PCIe bus if a single node is used. This will ensure that all NICs are functioning properly and that the connection to the supporting network switch is valid.

```bash
# GPU to GPU for a single node. Should use GPU and NIC that are adjacent to one another.
# Node 0 Host/Listener
sudo ./ib_write_bw -x 3 -a -b -F --use_rocm=<GPU Adjacent to NIC 0> -d <NIC 0> --report_gbits

# Node 1 Client in a separate window
sudo ./ib_write_bw -x 3 -a -b -F --use_rocm=<GPU Adjacent to NIC 1> -d <NIC 1> --report_gbits <host_ip for NIC 0 on node 0>
```

Result:

* PASSED: All paths report average throughput of a 400G NIC as 370 Gbps or greater at some point during the test.
* FAILED: Unable to reach an average speed equal to or greater than 370 Gbps for a 400G NIC.

## RCCL Benchmarking Results

The ROCm Collective Communications Library ([ROCm/rccl](https://github.com/ROCm/rccl)) is available as open-source software. Though RCCL is designed to be used as a performant backend for downstream applications, particularly AI training and inference workloads, it also has a test suite to benchmark and validate performance.

GPU collectives can measure performance in several ways, and RCCL benchmarks include both “algorithm” bandwidth and “bus” bandwidth metrics. For point-to-point operations, algorithm bandwidth is a reliable indication of hardware utilization, while for large collective operations bus bandwidth is a better measurement of hardware utilization. For more on the bus band metrics, please refer to the [performance documentation](https://github.com/ROCm/rccl-tests/blob/develop/doc/PERFORMANCE.md) in the RCCL tests repository.

RCCL implements operations such as all-reduce, all-gather, reduce, broadcast, reduce-scatter, gather, scatter, all-to-all, and direct GPU-to-GPU send/receive on the current node or another node.

### Test Details

[Broadcast](https://github.com/ROCm/rccl-tests/blob/develop/test/test_Broadcast.py)

Copies data from one “root” GPU to all others, so every GPU ends up with an identical set of information-like giving everyone in a group the same set of starting instructions.

* **Performance Metric**: Measures how fast the root GPU can distribute its data to all others, with the focus on the effective bandwidth of this one-to-many transfer.
* **Bus Bandwidth (busbw)**: Calculated as the total data sent divided by the time taken. Since only the root sends data, busbw reflects the root’s ability to saturate the network and is a direct measure of the broadcast efficiency.

[AllGather](https://github.com/ROCm/rccl-tests/blob/develop/test/test_AllGather.py)

Takes a unique chunk of data from each GPU and shares the full collection with every GPU, so everyone has the complete dataset. As an analogy, imagine that each GPU brings a different piece to a group project, and by the end, everyone has the entire project.

* **Performance Metric**: Assesses the total bandwidth and efficiency of exchanging and assembling all pieces among GPUs, highlighting how well the network handles simultaneous data sharing.
* **Bus Bandwidth (busbw)**: Adjusted for the number of GPUs, since each GPU both sends and receives data. This metric shows how efficiently the hardware can handle the collective data transfer required for all_gather.

[AllReduce](https://github.com/ROCm/rccl-tests/blob/develop/test/test_AllReduce.py)

Combines data from all GPUs using an operation like sum or max, and then gives the final, combined result back to every GPU-think of pooling everyone’s results together to get a group consensus, then making sure every participant knows the outcome.

* **Performance Metric**: Measures both the speed of combining data and distributing the result, focusing on throughput and latency-crucial for keeping distributed computations coordinated.
* **Bus Bandwidth (busbw)**: Takes into account that each GPUs data must be shared and the result returned, effectively doubling the data movement compared to all_gather. This metric reflects the maximum achievable bandwidth for this two-way communication pattern.

In this document, we report the expected bus bandwidth of the all_reduce operators. Additional tests are available in the [RCCL tests directory](https://github.com/ROCm/rccl-tests/tree/develop/test).

Measurements are reported for bus bandwidth and in-place operations, for message sizes of 8 GB. Higher scores are better.

### RCCL Installation

For running multi-node testing, rccl-tests need to be compiled with MPI support. The [GPU-enabled Message Passing Interface Guide](https://amdcloud.sharepoint.com/sites/DCGPUTME/Shared%20Documents/Documentation/Cluster%20Acceptance%20Test%20Guides/MI3xx%20Cluster%20Acceptance%20Test%20Guide/GPU-enabled%20Message%20Passing%20Interface) contains specific instructions for how to install a ROCm-aware MPI installation for RoCE and InfiniBand-based networks. Once OpenMPI is installed, install RCCL-tests with the following script:

```bash
# Define preferred paths for MPI and RCCL installations (ensure /lib/libmpi.so and /lib/librccl.so exist in both install paths)
MPI_INSTALL_DIR=/path/to/mpi
RCCL_INSTALL_DIR=/path/to/rccl

# If HIP is not installed in /opt/rocm, add `HIP_HOME=/path/to/hip` to the cmake parameters.
build_rccl_tests() {
if [ ! -d rccl-tests ]; then
git clone https://github.com/ROCm/rccl-tests
fi
cd rccl-tests
make MPI=1 MPI_HOME="${MPI_INSTALL_DIR}" NCCL_HOME="${RCCL_INSTALL_DIR}" -j

# Build RCCL tests
build_rccl_tests
```

This script differs from the previous commands by specifying flags and locations for the MPI install in the cmake parameters. RCCL-tests should now have MPI support.

#### Allreduce

To evaluate the Allreduce operator using the RCCL tests benchmark, run the following command in your terminal:

```bash
all_reduce_perf -b 8 -e 8G -f 2 -g 8
```

The RCCL all-reduce test criteria is to exceed an in-place busbw metric of 304 GB/s at a message size of 8 GB.

Example output

```bash
# nThread 1 nGpus 8 minBytes 8 maxBytes 8589934592 step: 2(factor) warmup iters: 5 iters: 20 agg iters: 1 validation: 1 graph: 0
#
rcccl-tests: Version Unknown
# Using devices
# Rank 0 Group 0 Pid 657053 on smci350-zts-gtu-e14-05 device 0 [0000:75:00] AMD Instinct MI350X
# Rank 1 Group 0 Pid 657053 on smci350-zts-gtu-e14-05 device 1 [0000:05:00] AMD Instinct MI350X
# Rank 2 Group 0 Pid 657053 on smci350-zts-gtu-e14-05 device 2 [0000:65:00] AMD Instinct MI350X
# Rank 3 Group 0 Pid 657053 on smci350-zts-gtu-e14-05 device 3 [0000:15:00] AMD Instinct MI350X
# Rank 4 Group 0 Pid 657053 on smci350-zts-gtu-e14-05 device 4 [0000:f5:00] AMD Instinct MI350X
# Rank 5 Group 0 Pid 657053 on smci350-zts-gtu-e14-05 device 5 [0000:85:00] AMD Instinct MI350X
# Rank 6 Group 0 Pid 657053 on smci350-zts-gtu-e14-05 device 6 [0000:e5:00] AMD Instinct MI350X
# Rank 7 Group 0 Pid 657053 on smci350-zts-gtu-e14-05 device 7 [0000:95:00] AMD Instinct MI350X
#
# out-of-place in-place
# size count type redop root time algbw busbw #wrong time algbw busbw #wrong
# (B) (elements) (us) (GB/s) (GB/s) (us) (GB/s) (GB/s) 
8 2 float sum -1 58.63 0.00 0.00 0 49.68 0.00 0.00 0
16 4 float sum -1 51.42 0.00 0.00 0 51.15 0.00 0.00 0
32 8 float sum -1 50.95 0.00 0.00 0 50.26 0.00 0.00 0
64 16 float sum -1 50.20 0.00 0.00 0 56.04 0.00 0.00 0
128 32 float sum -1 51.04 0.00 0.00 0 57.36 0.00 0.00 0
256 64 float sum -1 43.78 0.01 0.01 0 43.42 0.01 0.01 0
512 128 float sum -1 43.37 0.01 0.02 0 43.77 0.01 0.02 0
1024 256 float sum -1 42.68 0.02 0.04 0 49.59 0.02 0.04 0
2048 512 float sum -1 49.20 0.04 0.07 0 49.92 0.04 0.07 0
4096 1024 float sum -1 50.88 0.08 0.14 0 49.81 0.08 0.14 0
8192 2048 float sum -1 42.11 0.19 0.34 0 43.78 0.19 0.33 0
16384 4096 float sum -1 49.84 0.33 0.58 0 50.24 0.33 0.57 0
32768 8192 float sum -1 50.08 0.65 1.14 0 51.27 0.64 1.12 0
65536 16384 float sum -1 50.03 1.31 2.29 0 43.56 1.50 2.63 0
131072 32768 float sum -1 53.33 2.46 4.30 0 59.59 2.20 3.85 0
262144 65536 float sum -1 59.53 4.40 7.71 0 53.49 4.90 8.58 0
524288 131072 float sum -1 61.08 8.58 15.02 0 59.47 8.82 15.43 0
1048576 262144 float sum -1 53.29 19.68 34.43 0 52.83 19.85 34.73 0
2097152 524288 float sum -1 60.75 34.52 60.41 0 61.07 34.34 60.10 0
4194304 1048576 float sum -1 57.41 73.06 127.85 0 56.88 73.75 129.05 0
8388608 2097152 float sum -1 83.38 100.60 176.05 0 81.35 103.12 180.45 0
16777216 4194304 float sum -1 140.4 119.50 209.13 0 141.8 118.32 207.06 0
33554432 8388608 float sum -1 255.1 131.54 230.19 0 254.0 132.13 231.22 0
67108864 16777216 float sum -1 1049.3 63.95 111.92 0 405.1 165.67 289.92 0
134217728 33554432 float sum -1 694.2 193.34 338.35 0 695.7 192.94 337.64 0
268435456 67108864 float sum -1 1947.9 137.81 241.16 0 1318.3 203.62 356.33 0
536870912 134217728 float sum -1 2591.9 207.14 362.49 0 2589.3 207.34 362.84 0
1073741824 268435456 float sum -1 5185.9 207.05 362.34 0 5184.9 207.09 362.41 0
2147483648 536870912 float sum -1 15948 134.66 235.65 0 10279 208.92 365.60 0
4294967296 1073741824 float sum -1 20503 209.48 366.58 0 20515 209.35 366.37 0
8589934592 2147483648 float sum -1 41644 206.27 360.97 0 40903 210.01 367.51 0
# Errors with asterisks indicate errors that have exceeded the maximum threshold.
# Out of bounds values : 0 OK
# Avg bus bandwidth : 111.827
```
