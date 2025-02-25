.. meta::
   :description lang=en: AMD Instinct MI300X performance benchmarking guide for acceptance testing.
   :keywords: perf, bench, accelerator, node, multi, type, precision

************************
Performance benchmarking
************************

The benchmarking tests outlined in this chapter validate compute, IO, and memory
performance for all eight GPUs in a server system. The benchmarking tests
require ROCm installation - see section 2.6 ROCm Installation for details.
During the test, it is recommended to monitor system utilization, power, and
temperature using AMD SMI (``amd-smi``), and check for errors using ``lspci`` and ``dmesg`` as
detailed in Chapter 2.

Benchmark tests in this section leverage and include instructions for
the following

- TransferBench

- ROCm Collective Communications Library (`<https://github.com/ROCm/rccl>`__)

- rocBLAS

- BabelStream

.. _mi300x-bench-transferbench:

TransferBench benchmarking results
==================================

TransferBench is a tool and utility for benchmarking copies between
user-specified CPU and GPU devices. For more information, see the
:doc:`TransferBench documentation <transferbench:index>` and `GitHub repository
<https://github.com/ROCm/TransferBench>`_.

The system health benchmarks run 6 TransferBench tests from the
`example.cfg file <https://github.com/ROCm/TransferBench/blob/develop/examples/example.cfg>`_.
For reference, the six transfers are:

1. Single GPU-executed Transfer between GPUs 0 and 1 using 4 Compute
   Units (CUs)

2. Single DMA executed Transfer between GPUs 0 and 1

3. Copy 1 MB from GPU 0 to GPU 1 with 4 CUs, and 2 MB from GPU 1 to GPU
   0 with 8 CUs – This test reports results for both Transfers

4. ``Memset`` by GPU 0 to GPU 0 memory

5. ``Read-only`` by CPU 0

6. Broadcast from GPU 0 to GPU 0 and GPU 1

TransferBench qualification
---------------------------

Ensure that ROCm and ``libnuma`` are first installed on the SUT. To download
and install TransferBench, run the following commands:

.. code-block:: shell

   git clone https://github.com/ROCm/TransferBench.git

   cd TransferBench

   CC=hipcc make

TransferBench can be run in a variety of configurations, however for SUT
validation use the built-in tests below. Once TransferBench is installed on your
SUT, follow the instructions below to run the All-to-All and Peer-to-Peer
benchmarks. We also include a section on the TransferBench ``ConfigFile`` format,
which allows for a set of Transfers (a Test) to run in parallel.

.. _mi300x-bench-transferbench-a2a:

All-to-all
~~~~~~~~~~

In GPU all-to-all benchmark, each GPU sends data to every other GPU and
receives data from every other GPU. TransferBench a2a test, measures and
reports all those data transfer rates. Run the following command:

.. code-block:: shell

   TransferBench a2a

Expected output (truncated) - Note that these values do not map to the run that
produced the results on :ref:`mi300x-bench-transferbench-a2a-table` but are
within our reproducibility acceptance criteria:

.. code-block:: shell-session

   Summary:
   ==========================================================
   SRC\\DST GPU 00 GPU 01 GPU 02 GPU 03 GPU 04 GPU 05 GPU 06 GPU 07 STotal Actual
   GPU 00 N/A 43.666 36.624 43.480 36.677 43.729 36.871 43.607 284.653 255.598
   GPU 01 37.858 N/A 39.964 37.983 40.440 38.410 40.209 38.156 273.019 264.392
   GPU 02 31.420 34.604 N/A 31.624 34.795 31.512 34.678 31.556 230.188 219.577
   GPU 03 30.883 28.583 30.972 N/A 28.649 30.883 28.658 30.918 209.546 199.797
   GPU 04 34.388 35.432 34.283 35.309 N/A 34.198 35.236 34.260 243.106 238.708
   GPU 05 29.553 30.244 29.432 30.169 29.448 N/A 30.152 29.392 208.391 204.972
   GPU 06 38.320 40.466 38.538 40.823 38.526 40.436 N/A 38.188 275.297 266.935
   GPU 07 42.405 36.295 42.521 36.361 42.635 36.472 42.553 N/A 279.240 253.728
   RTotal 244.827 249.288 252.334 255.749 251.169 255.639 248.357 246.077 2003.440 199.797 266.935
   Average bandwidth (GPU Timed): 35.776 GB/s
   Aggregate bandwidth (GPU Timed): 2003.440 GB/s
   Aggregate bandwidth (CPU Timed): 1411.163 GB/s

.. _mi300x-bench-transferbench-a2a-table:

.. list-table:: Average, Pass/Fail bandwidth for TransferBench all-to-all benchmarking
   :header-rows: 1

   * - TransferBench test
     - Minimum passing score (GB/s)

   * - ``a2a`` average bandwidth
     - 32.9

.. _mi300x-bench-transferbench-p2p:

Peer-to-peer
~~~~~~~~~~~~

Shows peak bandwidth of unidirectional and bidirectional copy between
CPU and GPUs. Run the following command:

.. code-block:: shell

   TransferBench p2p

Expected output (truncated) - Note that these values do not map to the run that
produced the results in :ref:`mi300x-bench-transferbench-p2p-table` but are
within our reproducibility acceptance criteria:

.. code-block:: shell-session

   Bytes Per Direction 67108864
   Unidirectional copy peak bandwidth GB/s [Local read / Remote write] (GPU-Executor: GFX)
   SRC+EXE\\DST CPU 00 CPU 01 GPU 00 GPU 01 GPU 02 GPU 03 GPU 04 GPU 05 GPU 06 GPU 07
   CPU 00 -> 42.75 38.85 41.97 42.33 42.50 42.19 41.56 41.45 41.31 41.05
   CPU 01 -> 32.85 43.39 41.53 41.65 41.76 42.38 42.67 42.36 42.31 42.60
   GPU 00 -> 55.23 55.26 1689.85 48.46 48.73 48.96 48.29 47.89 47.47 47.80
   GPU 01 -> 55.23 55.24 48.51 1672.91 48.40 48.72 48.47 48.12 47.79 47.73
   GPU 02 -> 55.25 55.24 48.83 48.53 1690.87 48.80 48.59 48.87 48.08 48.07
   GPU 03 -> 55.22 55.25 48.81 48.79 48.78 1675.13 48.72 48.66 48.32 47.93
   GPU 04 -> 55.23 55.26 48.39 48.46 48.76 48.72 1703.05 48.83 48.85 48.95
   GPU 05 -> 55.26 55.26 47.92 48.48 48.59 48.83 48.95 1650.41 48.63 48.88
   GPU 06 -> 55.22 55.24 47.71 47.74 48.12 48.35 48.78 48.87 1717.22 48.64
   GPU 07 -> 55.26 55.25 47.71 47.69 47.54 48.38 48.78 48.97 48.74 1699.95
   CPU->CPU CPU->GPU GPU->CPU GPU->GPU
   Averages (During UniDir): 35.85 41.98 55.24 48.44
   Bidirectional copy peak bandwidth GB/s [Local read / Remote write] (GPU-Executor: GFX)
   SRC\\DST CPU 00 CPU 01 GPU 00 GPU 01 GPU 02 GPU 03 GPU 04 GPU 05 GPU 06 GPU 07
   CPU 00 -> N/A 31.06 41.37 42.07 41.56 41.42 39.96 40.94 40.51 39.60
   CPU 00 <- N/A 37.56 54.66 54.63 54.49 54.64 39.40 37.32 37.70 39.52
   CPU 00 <-> N/A 68.62 96.03 96.70 96.05 96.06 79.35 78.26 78.20 79.12
   CPU 01 -> 32.89 N/A 40.64 41.25 41.25 40.14 41.99 42.04 42.23 42.03
   CPU 01 <- 21.38 N/A 39.22 37.17 37.57 39.67 54.51 54.50 54.49 54.49
   CPU 01 <-> 54.27 N/A 79.86 78.41 78.82 79.82 96.50 96.54 96.72 96.52
   GPU 00 -> 54.51 39.20 N/A 46.11 46.21 46.18 46.23 46.19 46.22 46.00
   GPU 00 <- 41.46 40.33 N/A 46.09 46.45 46.22 46.17 46.09 46.25 46.09
   GPU 00 <-> 95.97 79.53 N/A 92.20 92.65 92.40 92.40 92.28 92.48 92.09
   GPU 01 -> 54.53 37.43 46.22 N/A 46.37 46.44 46.25 46.09 46.03 46.25
   GPU 01 <- 41.00 41.07 46.16 N/A 46.20 46.44 46.27 46.22 46.05 46.09
   GPU 01 <-> 95.53 78.50 92.37 N/A 92.57 92.88 92.51 92.31 92.07 92.34
   GPU 02 -> 54.52 37.48 46.19 46.18 N/A 46.29 46.54 46.26 46.04 46.08
   GPU 02 <- 41.49 41.39 46.19 46.40 N/A 46.29 46.46 46.07 46.20 46.09
   GPU 02 <-> 96.00 78.87 92.38 92.58 N/A 92.58 93.00 92.33 92.24 92.17
   GPU 03 -> 54.63 39.36 46.28 46.50 46.32 N/A 46.41 46.23 46.23 46.13
   GPU 03 <- 41.79 40.15 46.27 46.15 46.27 N/A 46.37 46.62 46.24 46.29
   GPU 03 <-> 96.42 79.50 92.55 92.64 92.60 N/A 92.79 92.85 92.47 92.42
   GPU 04 -> 39.65 54.62 46.25 46.32 46.51 46.31 N/A 46.23 46.48 46.24
   GPU 04 <- 39.40 41.96 46.22 46.19 46.47 46.38 N/A 46.28 46.45 46.31
   GPU 04 <-> 79.05 96.58 92.47 92.52 92.98 92.69 N/A 92.51 92.94 92.56
   GPU 05 -> 37.54 54.65 46.01 46.23 46.21 46.33 46.31 N/A 46.10 46.51
   GPU 05 <- 39.82 42.12 46.00 46.24 46.23 46.28 46.08 N/A 46.18 46.26
   GPU 05 <-> 77.35 96.77 92.01 92.47 92.44 92.61 92.39 N/A 92.29 92.77
   GPU 06 -> 37.23 54.48 45.94 46.07 46.10 46.27 46.37 46.20 N/A 46.06
   GPU 06 <- 40.62 41.99 45.99 46.19 46.00 46.28 46.11 46.17 N/A 46.41
   GPU 06 <-> 77.85 96.47 91.93 92.26 92.10 92.55 92.48 92.37 N/A 92.47
   GPU 07 -> 39.38 54.61 46.20 46.26 46.13 46.27 46.25 46.25 46.30 N/A
   GPU 07 <- 39.37 42.31 46.21 46.21 46.08 46.20 46.50 46.45 46.21 N/A
   GPU 07 <-> 78.76 96.91 92.41 92.47 92.20 92.47 92.74 92.70 92.50 N/A
   CPU->CPU CPU->GPU GPU->CPU GPU->GPU
   Averages (During BiDir): 30.72 43.84 43.75 46.24

.. _mi300x-bench-transferbench-p2p-table:

.. list-table:: Average, Pass/Fail bandwidth for TransferBench peer-to-peer benchmarking
   :header-rows: 1

   * - TransferBench test
     - Minimum passing score (GB/s)

   * - ``p2p`` average unidirectional copy
     - 33.9

   * - ``p2p`` average bidirectional copy
     - 43.9

.. _mi300x-bench-transferbench-configfile:

TransferBench default ConfigFile test
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The TransferBench default ``ConfigFile`` test allows a set of transfers (or,
tests) to run in parallel. To learn more about the ``ConfigFile`` format,
please review the
`official documentation <https://rocm.docs.amd.com/projects/TransferBench/en/latest/how%20to/use-transferbench.html>`__.

Run the following command:

.. code-block:: shell

   TransferBench examples/example.cfg

Expected output (truncated) - Note that these values do not map to the run that
produced the results on :ref:`mi300x-bench-transferbench-tests-table` but are
within our reproducibility acceptance criteria:

.. code-block:: shell-session

   ## Single GPU-executed Transfer between GPUs 0 and 1 using 4 CUs
   Test 1:
   Executor: GPU 00 \| 47.772 GB/s \| 1.405 ms \| 67108864 bytes \| 47.774 GB/s (sum)
   Transfer 00 \| 47.774 GB/s \| 1.405 ms \| 67108864 bytes \| G0 -> GPU00:004 -> G1
   Aggregate (CPU) \| 42.490 GB/s \| 1.579 ms \| 67108864 bytes \| Overhead: 0.175 ms
   ## Single DMA executed Transfer between GPUs 0 and 1
   Test 2:
   Executor: DMA 00 \| 48.349 GB/s \| 1.388 ms \| 67108864 bytes \| 48.349 GB/s (sum)
   Transfer 00 \| 48.349 GB/s \| 1.388 ms \| 67108864 bytes \| G0 -> DMA00.\*:001 -> G1
   Aggregate (CPU) \| 44.653 GB/s \| 1.503 ms \| 67108864 bytes \| Overhead: 0.115 ms
   ## Copy 1Mb from GPU0 to GPU1 with 4 CUs, and 2Mb from GPU1 to GPU0 with 8 CUs
   Test 3:
   Executor: GPU 00 \| 35.921 GB/s \| 0.029 ms \| 1048576 bytes \| 32.809 GB/s (sum)
   Transfer 00 \| 32.809 GB/s \| 0.032 ms \| 1048576 bytes \| G0 -> GPU00:004 -> G1
   Executor: GPU 01 \| 41.228 GB/s \| 0.051 ms \| 2097152 bytes \| 39.603 GB/s (sum)
   Transfer 01 \| 39.603 GB/s \| 0.053 ms \| 2097152 bytes \| G1 -> GPU01:008 -> G0
   Aggregate (CPU) \| 16.036 GB/s \| 0.196 ms \| 3145728 bytes \| Overhead: 0.145 ms
   ## "Memset" by GPU 0 to GPU 0 memory
   Test 4:
   Executor: GPU 00 \| 1351.543 GB/s \| 0.050 ms \| 67108864 bytes \| 1274.598 GB/s (sum)
   Transfer 00 \| 1274.598 GB/s \| 0.053 ms \| 67108864 bytes \| N -> GPU00:032 -> G0
   Aggregate (CPU) \| 305.581 GB/s \| 0.220 ms \| 67108864 bytes \| Overhead: 0.170 ms
   ## "Read-only" by CPU 0
   Test 5:
   Executor: CPU 00 \| 20.344 GB/s \| 3.299 ms \| 67108864 bytes \| 20.344 GB/s (sum)
   Transfer 00 \| 20.344 GB/s \| 3.299 ms \| 67108864 bytes \| C0 -> CPU00:004 -> N
   Aggregate (CPU) \| 19.338 GB/s \| 3.470 ms \| 67108864 bytes \| Overhead: 0.171 ms
   ## Broadcast from GPU 0 to GPU 0 and GPU 1
   Test 6:
   Executor: GPU 00 \| 48.964 GB/s \| 1.371 ms \| 67108864 bytes \| 48.933 GB/s (sum)
   Transfer 00 \| 48.933 GB/s \| 1.371 ms \| 67108864 bytes \| G0 -> GPU00:016 -> G0G1
   Aggregate (CPU) \| 44.433 GB/s \| 1.510 ms \| 67108864 bytes \| Overhead: 0.140 ms

The table below shows the reference performance results for
TransferBench on an MI300X system. For TransferBench, higher scores are
better.

.. _mi300x-bench-transferbench-tests-table:

.. list-table:: Average, Pass/Fail bandwidth for TransferBench benchmarking
   :header-rows: 1

   * - TransferBench test
     - Minimum passing score (GB/s)

   * - Test 1
     - 47.1

   * - Test 2
     - 48.4

   * - Test 3 (0 to 1)
     - 31.9

   * - Test 3 (1 to 0)
     - 38.9

   * - Test 4
     - 1264

   * - Test 5 [#TransferBench-Test-5]_
     - N/A

   * - Test 6
     - 48.6

.. [#TransferBench-Test-5] TransferBench Test 5 is a CPU-only benchmark. Results
   are highly platform dependent and should not be used to validate GPU
   performance.

.. _mi300x-bench-rccl:

RCCL benchmarking results
=========================

The ROCm Collective Communications Library (`<https://github.com/ROCm/rccl>`__)
is available as open-source software. Though RCCL is designed to be used as a
performant backend for downstream applications, particularly AI training and
inference workloads, it also has a test suite to benchmark and validate
performance.

GPU collectives can measure performance in several ways, and RCCL benchmarks
include both “algorithm” bandwidth and “bus” bandwidth metrics. For
point-to-point operations, algorithm bandwidth is a reliable indication of
hardware utilization, while for large collective operations bus bandwidth is a
better measurement of hardware utilization. For more on the bus band metrics,
please refer to the `performance documentation
<https://github.com/ROCm/rccl-tests/blob/develop/doc/PERFORMANCE.md>`__
in the RCCL tests repository.

In this document, we report the expected bus bandwidth of the ``all_reduce``
operators. Additional tests are available in the `RCCL tests directory
<https://github.com/ROCm/rccl-tests/tree/develop/test>`__.

The **Table 4** contains RCCL benchmark pass/fail criteria. Measurements
are reported for bus bandwidth and in-place operations, for message
sizes of 8 GB. Higher scores are better.

RCCL qualification
------------------

Build RCCL tests from source using the official documentation or by
running the commands below in your terminal:

.. code-block:: shell

   git clone https://github.com/ROCm/rccl-tests.git

   cd rccl_tests/

   make NCCL_HOME=/opt/rocm/

Once RCCL tests is installed on your SUT, follow these instructions to run the
Allreduce benchmark.

.. _mi300x-bench-rccl-allreduce:

Allreduce
~~~~~~~~~

To evaluate the Allreduce operator using the RCCL tests benchmark, run the
following command in your terminal:

.. code-block:: shell

   build/all_reduce_perf -b 8 -e 8G -f 2 -g 8

The RCCL all-reduce test criteria is to exceed an in-place ``busbw`` metric of 304
GB/s at a message size of 8589934592B, approximately 8GB.

Example output:

.. code-block:: shell-session

   # nThread 1 nGpus 8 minBytes 8 maxBytes 8589934592 step: 2(factor) warmup iters: 5 iters: 20 agg iters: 1 validation: 1 graph: 0
   #
   rccl-tests: Version develop:ae3e635
   # Using devices
   # Rank 0 Pid 806883 on SMC-SC-DC19-06 device 0 [0000:05:00.0] AMD Instinct MI300X
   # Rank 1 Pid 806883 on SMC-SC-DC19-06 device 1 [0000:26:00.0] AMD Instinct MI300X
   # Rank 2 Pid 806883 on SMC-SC-DC19-06 device 2 [0000:46:00.0] AMD Instinct MI300X
   # Rank 3 Pid 806883 on SMC-SC-DC19-06 device 3 [0000:65:00.0] AMD Instinct MI300X
   # Rank 4 Pid 806883 on SMC-SC-DC19-06 device 4 [0000:85:00.0] AMD Instinct MI300X
   # Rank 5 Pid 806883 on SMC-SC-DC19-06 device 5 [0000:a6:00.0] AMD Instinct MI300X
   # Rank 6 Pid 806883 on SMC-SC-DC19-06 device 6 [0000:c6:00.0] AMD Instinct MI300X
   # Rank 7 Pid 806883 on SMC-SC-DC19-06 device 7 [0000:e5:00.0] AMD Instinct MI300X
   #
   # size count type redop root time algbw busbw #wrong time algbw busbw #wrong
   # (B) (elements) (us) (GB/s) (GB/s) (us) (GB/s) (GB/s)
   8 2 float sum -1 34.13 0.00 0.00 0 39.55 0.00 0.00 0
   16 4 float sum -1 38.73 0.00 0.00 0 38.92 0.00 0.00 0
   32 8 float sum -1 39.48 0.00 0.00 0 39.23 0.00 0.00 0
   64 16 float sum -1 39.18 0.00 0.00 0 54.09 0.00 0.00 0
   128 32 float sum -1 39.36 0.00 0.01 0 182.4 0.00 0.00 0
   256 64 float sum -1 41.24 0.01 0.01 0 44.39 0.01 0.01 0
   512 128 float sum -1 44.23 0.01 0.02 0 44.43 0.01 0.02 0
   1024 256 float sum -1 45.84 0.02 0.04 0 58.30 0.02 0.03 0
   2048 512 float sum -1 44.60 0.05 0.08 0 44.59 0.05 0.08 0
   4096 1024 float sum -1 45.01 0.09 0.16 0 45.16 0.09 0.16 0
   8192 2048 float sum -1 43.72 0.19 0.33 0 43.06 0.19 0.33 0
   16384 4096 float sum -1 55.70 0.29 0.51 0 43.96 0.37 0.65 0
   32768 8192 float sum -1 44.39 0.74 1.29 0 43.22 0.76 1.33 0
   65536 16384 float sum -1 44.35 1.48 2.59 0 57.02 1.15 2.01 0
   131072 32768 float sum -1 47.47 2.76 4.83 0 41.03 3.19 5.59 0
   262144 65536 float sum -1 59.18 4.43 7.75 0 41.75 6.28 10.99 0
   524288 131072 float sum -1 57.96 9.05 15.83 0 51.85 10.11 17.70 0
   1048576 262144 float sum -1 58.47 17.93 31.38 0 58.94 17.79 31.13 0
   2097152 524288 float sum -1 59.86 35.03 61.31 0 61.09 34.33 60.08 0
   4194304 1048576 float sum -1 90.74 46.22 80.89 0 90.50 46.34 81.10 0
   8388608 2097152 float sum -1 110.8 75.71 132.49 0 116.3 72.13 126.23 0
   16777216 4194304 float sum -1 169.7 98.87 173.02 0 171.7 97.71 170.99 0
   33554432 8388608 float sum -1 257.6 130.28 227.99 0 271.7 123.51 216.14 0
   67108864 16777216 float sum -1 428.1 156.76 274.33 0 437.3 153.44 268.53 0
   134217728 33554432 float sum -1 801.8 167.41 292.96 0 807.4 166.23 290.90 0
   268435456 67108864 float sum -1 1546.5 173.58 303.76 0 1554.9 172.64 302.12 0
   536870912 134217728 float sum -1 3038.1 176.71 309.25 0 3046.8 176.21 308.36 0
   1073741824 268435456 float sum -1 6003.9 178.84 312.97 0 6003.6 178.85 312.99 0
   2147483648 536870912 float sum -1 11938 179.88 314.80 0 11960 179.55 314.22 0
   4294967296 1073741824 float sum -1 23849 180.09 315.15 0 23881 179.85 314.74 0
   8589934592 2147483648 float sum -1 47488 180.88 316.55 0 47594 180.48 315.84 0
   # Errors with asterisks indicate errors that have exceeded the maximum threshold.
   # Out of bounds values : 0 OK
   # Avg bus bandwidth : 102.138

.. _mi300x-bench-rccl-table:

.. list-table:: Average, Pass/Fail bandwidth for RCCL benchmarking
   :header-rows: 1

   * - Operation
     - Minimum passing score (GB/s)

   * - ``all_reduce``
     - 304

.. _mi300x-bench-rocblas:

rocBLAS benchmarking results
============================

AI models rely on highly optimized GEMM kernels (General Matrix Multiply) for
optimal performance in both training and inference. AMD provides the rocBLAS and
other libraries to enable applications and libraries to leverage AMD-optimized
GEMM kernels.

The rocBLAS test application allows users to benchmark the GEMM performance of
rocBLAS in a standalone application. The numbers below indicate for the included
benchmark (``fp32``) and two half precision GEMMs the expected performance of
rocBLAS on a validated system.

.. note::

   rocBLAS provides generic, performant BLAS and GEMM operations, but for some
   situations and kernels, other AMD ROCm supported tools, such as hipBLASLt,
   Triton and Composable Kernel, can provide superior performance.

For more information, see
`rocblas-bench <https://rocm.docs.amd.com/projects/rocBLAS/en/develop/how-to/Programmers_Guide.html#rocblas-bench>`_.
Future updates of ROCm in particular can boost performance of GEMM benchmarks,
so these numbers are expected to vary in the future.

rocBLAS qualification
---------------------

rocBLAS can be built from source to target tests and benchmarks only,
which have a dependency on ``gtest``. On Ubuntu, install ``gtest`` by running
the following command:

.. code-block:: shell

   sudo apt install libgtest-dev

Build rocBLAS from source by running the following commands in your terminal:

.. code-block:: shell

   git clone https://github.com/ROCm/rocBLAS.git

   cd rocBLAS

   git checkout rocm-6.2.0

   ./install.sh --clients-only --library-path /opt/rocm

.. note::

   The instructions above target a release of rocBLAS at 6.2.0 –
   it is not recommended to use the latest development branchs of rocBLAS
   for system hardware validation. This build can take several minutes to
   complete.

We include 3 rocBLAS benchmarks here targeting single, bf16, and int8
precisions. Half precision and ``fp8`` precision are not in the scope of
rocBLAS, and are not included in system validation. Compare test results
to :ref:`mi300x-bench-gemm-table`, below.

.. _mi300x-bench-rocblas-fp32:

FP32 full precision benchmark
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To run the FP32 full precision benchmark, run the following command in
your terminal:

.. code-block:: shell

   rocblas-bench -f gemm -r s -m 4000 -n 4000 -k 4000 --lda 4000 --ldb 4000 --ldc 4000 --transposeA N --transposeB T

In the output, expect to find a performance benchmark line near the end of the
output. Truncated example output is shown here:

.. code-block:: shell-session

   rocBLAS info: maximum library size per device is 0.61866 GB.

   transA,transB,M,N,K,alpha,lda,beta,ldb,ldc,rocblas-Gflops,us

   N,T,4000,4000,4000,1,4000,0,4000,4000, 97190.6, 1317

.. _mi300x-bench-rocblas-bf16:

BF16 half precision benchmark
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To run the BF16 half-precision benchmark, run the following command in
your terminal:

.. code-block:: shell

   rocblas-bench -f gemm_strided_batched_ex --transposeA N --transposeB T -m 1024 -n 2048 -k 512 --a_type h --lda 1024 --stride_a 4096 --b_type h --ldb 2048 --stride_b 4096 --c_type s --ldc 1024 --stride_c 2097152 --d_type s --ldd 1024 --stride_d 2097152 --compute_type s --alpha 1.1 --beta 1 --batch_count 5

In the output, expect to find a performance benchmark line near the end of the
output. Truncated example output is shown here:

.. code-block:: shell-session

   rocBLAS info: maximum library size per device is 0.61866 GB.

   transA,transB,M,N,K,alpha,lda,stride_a,beta,ldb,stride_b,ldc,stride_c,ldd,stride_d,batch_count,rocblas-Gflops,us

   N,T,1024,2048,512,1.1,1024,4096,1,2048,4096,1024,2097152,1024,2097152,5, 159783, 67.2

.. _mi300x-bench-rocblas-int8:

INT8 integer precision benchmark
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To run the int8 integer-precision benchmark, run the following command in your
terminal:

.. code-block:: shell

   rocblas-bench -f gemm_strided_batched_ex --transposeA N --transposeB T -m 1024 -n 2048 -k 512 --a_type i8_r --lda 1024 --stride_a 4096 --b_type i8_r --ldb 2048 --stride_b 4096 --c_type i32_r --ldc 1024 --stride_c 2097152 --d_type i32_r --ldd 1024 --stride_d 2097152 --compute_type i32_r --alpha 1.1 --beta 1 --batch_count 5

In the output, expect to find a performance benchmark line near the end of the
output. Truncated example output is shown here:

.. code-block:: shell-session

   rocBLAS info: maximum library size per device is 0.61866 GB.

   transA,transB,M,N,K,alpha,lda,stride_a,beta,ldb,stride_b,ldc,stride_c,ldd,stride_d,batch_count,rocblas-Gflops,us

   N,T,1024,2048,512,1,1024,4096,1,2048,4096,1024,2097152,1024,2097152,5, 177478, 60.5

The following table contains GEMM benchmark pass/fail criteria. For GEMM
benchmarks, larger scores are better.

.. _mi300x-bench-gemm-table:

.. list-table:: Average, Pass/Fail bandwidth for GEMM benchmarking
   :header-rows: 1

   * - GEMM
     - Minimum passing score (TFLOPS)

   * - FP32 ``4kx4kx4k``
     - 94100

   * - Strided BF16, BS 5, ``1kx2kx512``
     - 130600

   * - Strided Int8, BS5, ``1kx2kx512``
     - 162700

.. note::

   Typically, rocBLAS benchmarking requires multiple test runs to obtain peak
   performance. It is recommended to use the highest TFLOPS score obtained for
   each GEMM test to validate the compute performance.

.. _mi300x-bench-babelstream:

BabelStream benchmarking results
================================

BabelStream is an open-source benchmark to measure transfer rates
to/from global device memory on GPUs. For more information, see
`BabelStream <https://github.com/UoB-HPC/BabelStream>`_.

The qualification section will explain how to configure BabelStream. Running the
test will perform the benchmark on each GPU concurrently.
:ref:`mi300x-bench-babelstream-table` contains BabelStream v5.0 benchmark
pass/fail criteria. For BabelStream, higher scores are better.

BabelStream qualification
-------------------------

Build BabelStream tests from source using the official documentation or
by running the commands below in your terminal:

.. code-block:: shell

   git clone https://github.com/UoB-HPC/BabelStream.git

   cd BabelStream

   cmake -Bbuild -H. -DMODEL=hip -DCMAKE_CXX_COMPILER=hipcc

   cmake --build build

   export PATH=$PWD/build:$PATH

Running BabelStream on all eight 300X GPUs concurrently requires coordinated
job launching and device identification as an argument to the ``hip-stream``
executable. AMD recommends MPI to orchestrate this, and the easiest way to
run on the SUT is to create a script called ``wrapper.sh`` and populate it with
the following lines:

.. code-block:: bash

   #!/bin/bash

   # Use the mpirank to manage the device:

   hip-stream --device $OMPI_COMM_WORLD_RANK -n 50 -s 268435456

.. note::

   The MPI rank needs to be specified properly based on the MPI
   implementation. We assume Open MPI.

Open MPI can be installed on Ubuntu platforms with the following syntax:

.. code-block:: shell

   sudo apt-get install openmpi-bin openmpi-common libopenmpi-dev

After completing the BabelStream tests, ``openmpi`` can be uninstalled.

For your first benchmark run, execute the following command to assign
proper permissions to the wrapper script:

.. code-block:: shell

   chmod u+x wrapper.sh`

To run the benchmark, execute the following command in the terminal:

.. code-block:: shell

   mpiexec -n 8 wrapper.sh

Expected output (truncated):

.. code-block:: shell-session

   BabelStream
   Version: 5.0
   Implementation: HIP
   Running kernels 50 times
   Precision: **double**
   Array size: 2147.5 MB (=2.1 GB)
   Total size: 6442.5 MB (=6.4 GB)
   BabelStream
   Version: 5.0
   Implementation: HIP
   Running kernels 50 times
   . . .
   Using HIP device AMD Instinct MI300X
   Driver: 60241133
   Memory: DEFAULT
   Using HIP device AMD Instinct MI300X
   Driver: 60241133
   Memory: DEFAULT
   Using HIP device AMD Instinct MI300X
   Driver: 60241133
   . . .
   Init: 0.400851 s (=16071.943100 MBytes/sec)
   Read: 0.189949 s (=33916.687305 MBytes/sec)
   Init: 0.401357 s (=16051.675182 MBytes/sec)
   . . .
   Function MBytes/sec Min (sec) Max Average
   Copy 4255995.148 0.00101 0.00117 0.00106
   Mul 4115971.910 0.00104 0.00111 0.00106
   Add 3956389.991 0.00163 0.00170 0.00165
   Triad 3948061.647 0.00163 0.00180 0.00166
   Dot 3878410.495 0.00111 0.00120 0.00116
   Function MBytes/sec Min (sec) Max Average
   Copy 4269126.275 0.00101 0.00109 0.00105
   Mul 4113642.067 0.00104 0.00111 0.00107
   Add 3948620.619 0.00163 0.00177 0.00166
   Triad 3947212.603 0.00163 0.00167 0.00165
   Dot 3927179.117 0.00109 0.00117 0.00113
   . . .

.. _mi300x-bench-babelstream-table:

.. list-table:: Average, Pass/Fail memory bandwidth for BabelStream benchmarking

   * - Function
     - Minimum passing score (MB/s)

   * - ``Copy``
     - 4,177,285

   * - ``Mul``
     - 4,067,069

   * - ``Add``
     - 3,920,853

   * - ``Triad``
     - 3,885,301

   * - ``Dot``
     - 3,660,781
