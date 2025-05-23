.. meta::
   :description lang=en: AMD Instinct MI300X system validation guide for acceptance testing.
   :keywords: validate, rvs, performance, benchmarking

***********************
System validation tests
***********************

The validation tests in this section are intended to ensure that a system is
operating correctly. In this section, ROCm Validation Suite (``rvs``) is used,
which is a collection of tests, benchmarks, and qualification tools, each
targeting a specific subsystem of the system under test (SUT).

If not already installed on the SUT, run the following install command
(Ubuntu):

.. code-block:: shell

   sudo apt install rocm-validation-suite

Then ensure that the path to the ``rvs`` executable, located at
``/opt/rocm/bin``, is added to the path. Use the following command:

.. code-block:: shell

   export PATH=$PATH:/opt/rocm/bin

The ``rvs`` tool consists of modules that implement a particular test
functionality. The collection of the modules can be broadly categorized as
targeting the following aspects of the hardware platform:

- Compute / GPU

- Memory

- IO / PCIe

Each of these categories runs a subset of ``rvs`` modules to validate that the
category is working as expected.

The standard way to run an ``rvs`` module is by providing a configuration file
prefixed with the ``-c`` option. When ``rvs`` is installed properly on the SUT,
the ``conf`` files are found in the
``/opt/rocm/share/rocm-validation-suite/conf/`` folder. Since this path is a
part of every ``rvs`` command in this document, an environment variable is
defined which will be used in place of the long path for commands and their
output. To set this variable in the environment, run the following command:

.. code-block:: shell

   export RVS_CONF=/opt/rocm/share/rocm-validation-suite/conf

The configuration files section of the `ROCm Validation Suite User Guide
<https://github.com/ROCm/ROCmValidationSuite/blob/master/docs/ug1main.md#configuration-files>`__
provides detailed description about the ``conf`` file, its formation, and keys.
It's recommended to become familiar with the ``conf`` file before running the
``rvs`` tests described in the following sections. Be aware that some ``conf``
files are included in product-specific subfolders (for instance,
``=/opt/rocm/share/rocm-validation-suite/conf/MI300X``). If present, always use
GPU-specific configurations instead of the default test configurations.

In the following subsections, under each of the categories, the relevant
``rvs`` test modules are listed along with descriptions how the category is
validated. Example ``rvs`` commands with the expected output are also provided.
Most of the ``rvs`` tests do not have strict PASS / FAIL conditions reported,
rather it is expected that when they are run on the SUT, the output observed
are within a reasonable range provided.

.. _mi300x-rvs-compute-gpu:

Compute / GPU
=============

The ``rvs`` has three different types of modules to validate the Compute
subsystem. These are:

- Properties

- Benchmark / Stress / Qualification

- Monitor

MI300X GPU accelerators have many architectural features. Similar to 
:ref:`Check GPU presence (lspci) <mi300x-health-checks-lspci>` section, ``rvs`` has an
option to display all MI300X GPU accelerators present in the SUT. Before
proceeding with the modules below, run the following command to make sure all
the GPUs are seen with their correct PCIe properties.

Command:

.. code-block:: shell

   rvs -g

Expected output:

.. code-block:: shell-session

   ROCm Validation Suite (version 0.0.60202)

   Supported GPUs available:

   0000:05:00.0 - GPU[ 2 - 28851] AMD Instinct MI300X (Device 29857)
   0000:26:00.0 - GPU[ 3 - 23018] AMD Instinct MI300X (Device 29857)
   0000:46:00.0 - GPU[ 4 - 29122] AMD Instinct MI300X (Device 29857)
   0000:65:00.0 - GPU[ 5 - 22683] AMD Instinct MI300X (Device 29857)
   0000:85:00.0 - GPU[ 6 - 53458] AMD Instinct MI300X (Device 29857)
   0000:a6:00.0 - GPU[ 7 - 63883] AMD Instinct MI300X (Device 29857)
   0000:c6:00.0 - GPU[ 8 - 53667] AMD Instinct MI300X (Device 29857)
   0000:e5:00.0 - GPU[ 9 - 63738] AMD Instinct MI300X (Device 29857)

Result:

- PASSED: All 8 GPUs are seen in the output

- FAILED: Otherwise

  - Action: Don’t proceed further. Debug the issue of not being able to
    see all GPUs.

Properties
----------

The GPU Properties module queries the configuration of a targeted GPU
and returns the device’s static characteristics. These static values can
be used to debug issues such as device support, performance and firmware
problems.

To confirm the architectural properties of the GPU, use the GPUP module, which
uses of the GPUP configuration file.

The configuration file for GPUP module is located at ``{RVS_CONF}/gpup_single.conf``.

The GPUP module section of the `ROCm Validation Suite User
Guide <https://github.com/ROCm/ROCmValidationSuite/blob/master/docs/ug1main.md#gpup-module>`__
provides detailed description about the GPUP ``conf`` file, its formation,
and keys.

Command:

.. code-block:: shell

   rvs -c ${RVS_CONF}/gpup_single.conf

Expected output (truncated):

The ``conf`` file has six test cases ``RVS-GPUP-TC1``, ``RVS-GPUP-TC2``, and so
on up to ``RV-GPUP-TC6``. Only a truncated version of the output of ``RVS-GPUP-TC1`` is
shown here. The other tests are modified versions of ``RVS-GPUP-TC1``, which display
a subset of properties and/or a subset of ``io_links-properties``.

The first block of output displays the properties (all):

.. code-block:: shell-session

   [RESULT] [ 54433.732433] Action name :RVS-GPUP-TC1
   [RESULT] [ 54433.733858] Module name :gpup
   [RESULT] [ 54433.733992] [RVS-GPUP-TC1] gpup 28851 cpu_cores_count 0
   [RESULT] [ 54433.733994] [RVS-GPUP-TC1] gpup 28851 simd_count 1216
   ...
   [RESULT] [ 54433.734018] [RVS-GPUP-TC1] gpup 28851 num_xcc 8
   [RESULT] [ 54433.734018] [RVS-GPUP-TC1] gpup 28851 max_engine_clk_ccompute 3250

The block below shows only one of the ``io_link-properties`` of the eight GPUs
(``0`` to ``7``):

.. code-block:: shell-session

   [RESULT] [ 96878.647964] [RVS-GPUP-TC1] gpup 28851 0 type 2
   [RESULT] [ 96878.647973] [RVS-GPUP-TC1] gpup 28851 0 version_major 0
   [RESULT] [ 96878.647982] [RVS-GPUP-TC1] gpup 28851 0 version_minor 0
   [RESULT] [ 96878.647990] [RVS-GPUP-TC1] gpup 28851 0 node_from 2
   [RESULT] [ 96878.647997] [RVS-GPUP-TC1] gpup 28851 0 node_to 0
   [RESULT] [ 96878.648013] [RVS-GPUP-TC1] gpup 28851 0 weight 20
   [RESULT] [ 96878.648020] [RVS-GPUP-TC1] gpup 28851 0 min_latency 0
   [RESULT] [ 96878.648029] [RVS-GPUP-TC1] gpup 28851 0 max_latency 0
   [RESULT] [ 96878.648037] [RVS-GPUP-TC1] gpup 28851 0 min_bandwidth 312
   [RESULT] [ 96878.648045] [RVS-GPUP-TC1] gpup 28851 0 max_bandwidth 64000
   [RESULT] [ 96878.648053] [RVS-GPUP-TC1] gpup 28851 0 recommended_transfer_size 0
   [RESULT] [ 96878.648060] [RVS-GPUP-TC1] gpup 28851 0 flags 1

Result:

- PASSED: If generated output looks similar

- FAILED: If any GPU is not listed in output or ERROR tagged logs are seen

  - Typically, it is not expected that this module will fail

Benchmark, stress, qualification
--------------------------------

These categories of modules perform qualification of the GPU subsystem, execute
stress test, and compute and display bandwidth. The modules do not produce a
PASS / FAIL result. When bandwidth is measured, it only reports the bandwidth
and doesn’t make any comparisons with the existing set of numbers. The only
exceptions are GST and IET modules.

.. _mi300x-rvs-gst:

Benchmark
~~~~~~~~~

The GPU Stress Test (GST) module stresses the GPU FLOPS performance for
SGEMM, DGEMM and HGEMM operations and computes and displays peak
GFLOPs/s. Two configuration files are used by the GST module – one is
general purpose (``gst_single.conf``), and the other is MI300X specific
(``gst_ext.conf``). Each is detailed below.

The MI300X specific ``gst_single.conf`` configuration file for the GST module
is located at:

.. code-block:: shell

   ${RVS_CONF}/MI300X/gst_single.conf

Run the following command to perform the general GPU stress test using the
``gst_single.conf`` config file.

Command:

.. code-block:: shell

   rvs -c ${RVS_CONF}/MI300X/gst_single.conf

Expected output (truncated):

.. code-block:: shell-session

   [RESULT] [1101980.682169] Action name :gst-1215Tflops-4K4K8K-rand-fp8
   [RESULT] [1101980.683973] Module name :gst
   [RESULT] [1101980.836841] [gst-1215Tflops-4K4K8K-rand-fp8] [GPU:: 28851] Start of GPU ramp up
   [RESULT] [1101987.830800] [gst-1215Tflops-4K4K8K-rand-fp8] [GPU:: 28851] GFLOPS 1539705
   [RESULT] [1101988.831928] [gst-1215Tflops-4K4K8K-rand-fp8] [GPU:: 28851] End of GPU ramp up
   [RESULT] [1101992.16545 ] [gst-1215Tflops-4K4K8K-rand-fp8] [GPU:: 28851] GFLOPS 1640057
   [RESULT] [1101995.85574 ] [gst-1215Tflops-4K4K8K-rand-fp8] [GPU:: 28851] GFLOPS 1595462
   [RESULT] [1101998.181333] [gst-1215Tflops-4K4K8K-rand-fp8] [GPU:: 28851] GFLOPS 1687129
   [RESULT] [1102001.278962] [gst-1215Tflops-4K4K8K-rand-fp8] [GPU:: 28851] GFLOPS 1686102
   [RESULT] [1102003.864611] [gst-1215Tflops-4K4K8K-rand-fp8] [GPU:: 28851] GFLOPS 1687129
   [RESULT] [1102003.864648] [gst-1215Tflops-4K4K8K-rand-fp8] [GPU:: 28851] GFLOPS 1687129 Target GFLOPS: 1215000 met: TRUE
   ...

Result:

- PASSED: If ``met: TRUE`` is displayed in test log for all eight GPUs and
  actions, it indicates the test was able to hit peak GFLOP/s which matches or
  exceeds the target values listed in the config file.

- FAILED: Test results fail to meet the target GFLOP/s

  - Action: Do not proceed further. Report this issue to your system
    manufacturer immediately.

The MI300X specific ``gst_ext.conf`` configuration file for the GST module is
located at:

.. code-block:: shell

   ${RVS_CONF}/MI300X/gst_ext.conf

Run the following command to perform the MI300X GPU specific stress test
using the ``gst_ext.conf`` config file.

Command:

.. code-block:: shell

   ROCBLAS_TENSILE_LIBPATH=/opt/rocm/lib/rocblas/library/ rvs -c ${RVS_CONF}/MI300X/gst_ext.conf

Expected output (truncated):

.. code-block:: shell-session

   [RESULT] [603545.521766] Action name :gst-1000Tflops-8KB-fp8_r-false
   [RESULT] [603545.523245] Module name :gst
   [RESULT] [603545.685745] [gst-1000Tflops-8KB-fp8_r-false] [GPU:: 28851] Start of GPU ramp up
   [RESULT] [603552.11787 ] [gst-1000Tflops-8KB-fp8_r-false] [GPU:: 28851] GFLOPS 1235406
   [RESULT] [603553.12495 ] [gst-1000Tflops-8KB-fp8_r-false] [GPU:: 28851] GFLOPS 1250866
   [RESULT] [603554.12557 ] [gst-1000Tflops-8KB-fp8_r-false] [GPU:: 28851] GFLOPS 1235406
   [RESULT] [603555.12386 ] [gst-1000Tflops-8KB-fp8_r-false] [GPU:: 28851] End of GPU ramp up
   [RESULT] [603556.12907 ] [gst-1000Tflops-8KB-fp8_r-false] [GPU:: 28851] GFLOPS 1220772
   [RESULT] [603557.13180 ] [gst-1000Tflops-8KB-fp8_r-false] [GPU:: 28851] GFLOPS 1221056
   [RESULT] [603558.13786 ] [gst-1000Tflops-8KB-fp8_r-false] [GPU:: 28851] GFLOPS 1238206
   [RESULT] [603559.13885 ] [gst-1000Tflops-8KB-fp8_r-false] [GPU:: 28851] GFLOPS 1231140
   [RESULT] [603560.14584 ] [gst-1000Tflops-8KB-fp8_r-false] [GPU:: 28851] GFLOPS 1232638
   [RESULT] [603561.14988 ] [gst-1000Tflops-8KB-fp8_r-false] [GPU:: 28851] GFLOPS 1237375
   [RESULT] [603562.15658 ] [gst-1000Tflops-8KB-fp8_r-false] [GPU:: 28851] GFLOPS 1237069
   [RESULT] [603563.16277 ] [gst-1000Tflops-8KB-fp8_r-false] [GPU:: 28851] GFLOPS 1237102
   [RESULT] [603564.16494 ] [gst-1000Tflops-8KB-fp8_r-false] [GPU:: 28851] GFLOPS 1236422
   [RESULT] [603565.17256 ] [gst-1000Tflops-8KB-fp8_r-false] [GPU:: 28851] GFLOPS 1236946
   [RESULT] [603566.17565 ] [gst-1000Tflops-8KB-fp8_r-false] [GPU:: 28851] GFLOPS 1236323
   [RESULT] [603567.17654 ] [gst-1000Tflops-8KB-fp8_r-false] [GPU:: 28851] GFLOPS 1235515
   [RESULT] [603568.17924 ] [gst-1000Tflops-8KB-fp8_r-false] [GPU:: 28851] GFLOPS 1235281
   [RESULT] [603569.18070 ] [gst-1000Tflops-8KB-fp8_r-false] [GPU:: 28851] GFLOPS 1235452
   [RESULT] [603570.18519 ] [gst-1000Tflops-8KB-fp8_r-false] [GPU:: 28851] GFLOPS 1235085
   [RESULT] [603571.18960 ] [gst-1000Tflops-8KB-fp8_r-false] [GPU:: 28851] GFLOPS 1234038
   [RESULT] [603572.19046 ] [gst-1000Tflops-8KB-fp8_r-false] [GPU:: 28851] GFLOPS 1234418
   [RESULT] [603573.19153 ] [gst-1000Tflops-8KB-fp8_r-false] [GPU:: 28851] GFLOPS 1234417
   [RESULT] [603574.19692 ] [gst-1000Tflops-8KB-fp8_r-false] [GPU:: 28851] GFLOPS 1233895
   [RESULT] [603575.20205 ] [gst-1000Tflops-8KB-fp8_r-false] [GPU:: 28851] GFLOPS 1233942
   [RESULT] [603576.20336 ] [gst-1000Tflops-8KB-fp8_r-false] [GPU:: 28851] GFLOPS 1233328
   [RESULT] [603577.20441 ] [gst-1000Tflops-8KB-fp8_r-false] [GPU:: 28851] GFLOPS 1233327
   [RESULT] [603578.21167 ] [gst-1000Tflops-8KB-fp8_r-false] [GPU:: 28851] GFLOPS 1233693
   [RESULT] [603579.21800 ] [gst-1000Tflops-8KB-fp8_r-false] [GPU:: 28851] GFLOPS 1231561
   [RESULT] [603580.22072 ] [gst-1000Tflops-8KB-fp8_r-false] [GPU:: 28851] GFLOPS 1232009
   [RESULT] [603581.22249 ] [gst-1000Tflops-8KB-fp8_r-false] [GPU:: 28851] GFLOPS 1232113
   [RESULT] [603582.22852 ] [gst-1000Tflops-8KB-fp8_r-false] [GPU:: 28851] GFLOPS 1232700
   [RESULT] [603583.23573 ] [gst-1000Tflops-8KB-fp8_r-false] [GPU:: 28851] GFLOPS 1232620
   [RESULT] [603584.23655 ] [gst-1000Tflops-8KB-fp8_r-false] [GPU:: 28851] GFLOPS 1231152
   [RESULT] [603585.12439 ] [gst-1000Tflops-8KB-fp8_r-false] [GPU:: 28851] GFLOPS 1238206
   [RESULT] [603585.12457 ] [gst-1000Tflops-8KB-fp8_r-false] [GPU:: 28851] GFLOPS 1238206 Target GFLOPS: 1000000 met: TRUE
   ...

Result:

- PASSED: If “met: TRUE” is displayed in the test log for all eight
  GPUs, it indicates the test was able to hit peak GFLOP/s which matches
  or exceeds the target values listed in the config file.

- FAILED: Test results fail to meet the target GFLOP/s

  - Action: Do not proceed further. Report this issue to your system
    manufacturer immediately.

.. _mi300x-rvs-iet:

Stress
~~~~~~

The Input Energy Delay Product (EDP) test (IET) module runs GEMM workloads to
stress the GPU power, that is, Total Graphics Power (TGP).

This test is used to:

- Verify the GPU can handle maximum power stress for a sustained period.

- Check that the GPU power reaches a set target power.

The configuration file for IET module is located at
``{RVS_CONF}/MI300X/iet_single.conf``.

Command:

.. code-block:: shell

   rvs -c ${RVS_CONF}/MI300X/iet_single.conf

IET module run six different actions. Each action will be performed on all
eight GPUs. Each GPU power test will display a ``TRUE`` or ``FALSE`` status as
shown in the following output example.

Expected output (truncated):

.. code-block:: shell-session

   [RESULT] [1102597.157090] Action name :iet-620W-1K-rand-dgemm
   [RESULT] [1102597.159274] Module name :iet
   [RESULT] [1102597.333747] [iet-620W-1K-rand-dgemm] [GPU:: 28851] Power(W) 127.000000
   [RESULT] [1102597.334457] [iet-620W-1K-rand-dgemm] [GPU:: 23018] Power(W) 123.000000
   [RESULT] [1102597.334500] [iet-620W-1K-rand-dgemm] [GPU:: 22683] Power(W) 123.000000
   ...
   [RESULT] [1102657.372824] [iet-620W-1K-rand-dgemm] [GPU:: 29122] pass: TRUE
   [RESULT] [1102657.372859] [iet-620W-1K-rand-dgemm] [GPU:: 23018] pass: TRUE
   [RESULT] [1102657.372936] [iet-620W-1K-rand-dgemm] [GPU:: 28851] pass: TRUE
   [RESULT] [1102657.373301] [iet-620W-1K-rand-dgemm] [GPU:: 53458] pass: TRUE
   [RESULT] [1102657.373508] [iet-620W-1K-rand-dgemm] [GPU:: 63738] pass: TRUE
   [RESULT] [1102657.373620] [iet-620W-1K-rand-dgemm] [GPU:: 63883] pass: TRUE
   [RESULT] [1102657.374090] [iet-620W-1K-rand-dgemm] [GPU:: 22683] pass: TRUE
   [RESULT] [1102657.374158] [iet-620W-1K-rand-dgemm] [GPU:: 53667] pass: TRUE
   [RESULT] [1102658.379728] Action name :iet-wait-750W-28K-rand-dgemm
   [RESULT] [1102658.379781] Module name :iet

Result:

- PASSED: ``pass: TRUE`` must be displayed for each GPU.

- FAILED: Test results FAIL

  - Action: Do not proceed further. Report this issue to your system
    manufacturer immediately.

Qualification
~~~~~~~~~~~~~

The GPU monitor (GM) module is used to report and validate the following
system attributes.

- Temperature

- Fan speed

- Memory clock

- System clock

- Power

The configuration file for GST module is located at
``{RVS_CONF}/gm_single.conf``.

Command:

.. code-block:: shell

   rvs -c ${RVS_CONF}/gm_single.conf

Expected output (truncated):

.. code-block:: shell-session

   [RESULT] [209228.305186] [metrics_monitor] gm 28851 temp violations 0
   [RESULT] [209228.305186] [metrics_monitor] gm 28851 clock violations 0
   [RESULT] [209228.305186] [metrics_monitor] gm 28851 mem_clock violations 0
   [RESULT] [209228.305186] [metrics_monitor] gm 28851 fan violations 0
   [RESULT] [209228.305186] [metrics_monitor] gm 28851 power violations 0
   ...

Result:

- PASSED: If the output displays ``violations 0`` for all give attributes for
  each GPU. Pipe output to grep to create a quick summary of violations.

- FAILED: If any violations have a non-zero value

  - Action: Continue with the next step but periodically monitor by running
    this module.

Memory
======

To validate the GPU memory subsystem, ``rvs`` has the following two *types* of
modules:

- MEM

- BABEL

.. _mi300x-rvs-mem:

MEM
---

The Memory module, MEM, tests the GPU memory for hardware errors and soft
errors using HIP. It consists of various tests that use algorithms like Walking
1 bit, Moving inversion and Modulo 20. The module executes the following memory
tests [Algorithm, data pattern]:

- Walking 1 bit

- Own address test

- Moving inversions, ones & zeros

- Moving inversions, 8-bit pattern

- Moving inversions, random pattern

- Block move, 64 moves

- Moving inversions, 32-bit pattern

- Random number sequence

- Modulo 20, random pattern

- Memory stress test

The configuration file for GST module is located at ``{RVS_CONF}/mem.conf``.

Command:

.. code-block:: shell

   rvs -c ${RVS_CONF}/mem.conf -l mem.txt

The entire output file is not shown here for brevity. Grepping for certain
strings in the file where the log is saved makes it easier to understand the
log. The ``-l mem.txt`` option in the command dumps the entire output into
the file.

Grepping for the string ``mem Test 1:`` shows, Test 1 (Change one
bit memory address) is launched for each GPU.

.. code-block:: shell-session

   grep "mem Test 1:" mem.txt
   [RESULT] [214775.925788] [action_1] mem Test 1: Change one bit memory addresss
   [RESULT] [214776.112738] [action_1] mem Test 1: Change one bit memory addresss
   [RESULT] [214776.299030] [action_1] mem Test 1: Change one bit memory addresss
   [RESULT] [214776.486354] [action_1] mem Test 1: Change one bit memory addresss
   [RESULT] [214776.674529] [action_1] mem Test 1: Change one bit memory addresss
   [RESULT] [214776.865057] [action_1] mem Test 1: Change one bit memory addresss
   [RESULT] [214777.52685 ] [action_1] mem Test 1: Change one bit memory addresss
   [RESULT] [214777.155703] [action_1] mem Test 1: Change one bit memory addresss

Grepping for the string ``mem Test 1 :`` shows, Test 1 passed for all GPUs.

.. code-block:: shell-session

   [RESULT] [214775.947349] [action_1] mem Test 1 : PASS
   [RESULT] [214776.134798] [action_1] mem Test 1 : PASS
   [RESULT] [214776.320838] [action_1] mem Test 1 : PASS
   [RESULT] [214776.509205] [action_1] mem Test 1 : PASS
   [RESULT] [214776.697979] [action_1] mem Test 1 : PASS
   [RESULT] [214776.888054] [action_1] mem Test 1 : PASS
   [RESULT] [214777.75572 ] [action_1] mem Test 1 : PASS
   [RESULT] [214777.178653] [action_1] mem Test 1 : PASS

Similarly, you can grep other strings to parse the log file easily.

Grepping for the string “bandwidth” shows the memory bandwidth perceived by
each of the eight GPUs.

.. code-block:: shell-session

   grep "bandwidth" mem.txt
   [RESULT] [214808.291036] [action_1] mem Test 11: elapsedtime = 6390.423828 bandwidth = 2003.017090GB/s
   [RESULT] [214812.175895] [action_1] mem Test 11: elapsedtime = 6387.198242 bandwidth = 2004.028564GB/s
   [RESULT] [214813.999085] [action_1] mem Test 11: elapsedtime = 6400.554199 bandwidth = 1999.846802GB/s
   [RESULT] [214814.406234] [action_1] mem Test 11: elapsedtime = 6397.101074 bandwidth = 2000.926392GB/s
   [RESULT] [214814.583630] [action_1] mem Test 11: elapsedtime = 6388.572266 bandwidth = 2003.597534GB/s
   [RESULT] [214815.176800] [action_1] mem Test 11: elapsedtime = 6378.345703 bandwidth = 2006.810059GB/s
   [RESULT] [214815.384878] [action_1] mem Test 11: elapsedtime = 6404.943848 bandwidth = 1998.476196GB/s
   [RESULT] [214815.419048] [action_1] mem Test 11: elapsedtime = 6416.849121 bandwidth = 1994.768433GB/s

Result:

- PASSED: If all memory tests passed without memory errors and the
  bandwidth obtained in Test 11 is about ~2TB/s

- FAILED: If any memory errors report and/or the obtained bandwidth is
  not even close to 2TB/s

  - Action: Do not proceed further. Report this issue to your system
    manufacturer immediately.

BABEL
-----

Refer to the :ref:`BabelStream section <mi300x-bench-babelstream>` for
instructions on how to run this module to test memory.

IO
==

To validate the GPU interfaces, ``rvs`` has the following three *types* of
modules:

- PEBB – PCIe Bandwidth Benchmark

- PEQT – PCIe Qualification Tool

- PBQT – P2P Benchmark and Qualification Tool

.. _mi300x-rvs-pebb:

PEBB (PCIe Bandwidth Benchmark)
-------------------------------

The PCIe Bandwidth Benchmark attempts to saturate the PCIe bus with DMA
transfers between system memory and a target GPU card’s memory. The maximum
bandwidth obtained is reported.

The configuration file for GST module is located at:

.. code-block:: shell

   {RVS_CONF}/MI300X/pebb_single.conf

Command:

.. code-block:: shell

   rvs -c ${RVS_CONF}/MI300X/pebb_single.conf -l pebb.txt

The PEBB modules has the following tests defined in the ``conf`` file (where
``h2d`` means host to device, ``d2h`` means device to host, ``xMB`` means
random block size, and ``b2b`` means back to back):

- ``h2d-sequential-51MB``

- ``d2h-sequential-51MB``

- ``h2d-d2h-sequential-51MB``

- ``h2d-parallel-xMB``

- ``d2h-parallel-xMB``

- ``h2d-d2h-xMB``

- ``h2d-b2b-51MB``

- ``d2h-b2b-51MB``

- ``h2d-d2h-b2b-51MB``

Each of these tests will produce the following header as part of the
output log. It shows the distances between CPUs and GPUs.

Expected output (truncated):

.. code-block:: shell-session

   [RESULT] [1103843.610745] [d2h-sequential-64MB] pcie-bandwidth [CPU:: 0] [GPU:: 2 - 28851 - 0000:05:00.0] distance:20 PCIe:20
   [RESULT] [1103843.610763] [d2h-sequential-64MB] pcie-bandwidth [CPU:: 1] [GPU:: 2 - 28851 - 0000:05:00.0] distance:52 PCIe:52
   [RESULT] [1103843.610771] [d2h-sequential-64MB] pcie-bandwidth [CPU:: 0] [GPU:: 3 - 23018 - 0000:26:00.0] distance:20 PCIe:20
   [RESULT] [1103843.610778] [d2h-sequential-64MB] pcie-bandwidth [CPU:: 1] [GPU:: 3 - 23018 - 0000:26:00.0] distance:52 PCIe:52
   [RESULT] [1103843.610787] [d2h-sequential-64MB] pcie-bandwidth [CPU:: 0] [GPU:: 4 - 29122 - 0000:46:00.0] distance:20 PCIe:20
   [RESULT] [1103843.610795] [d2h-sequential-64MB] pcie-bandwidth [CPU:: 1] [GPU:: 4 - 29122 - 0000:46:00.0] distance:52 PCIe:52
   [RESULT] [1103843.610802] [d2h-sequential-64MB] pcie-bandwidth [CPU:: 0] [GPU:: 5 - 22683 - 0000:65:00.0] distance:20 PCIe:20
   [RESULT] [1103843.610810] [d2h-sequential-64MB] pcie-bandwidth [CPU:: 1] [GPU:: 5 - 22683 - 0000:65:00.0] distance:52 PCIe:52
   [RESULT] [1103843.610817] [d2h-sequential-64MB] pcie-bandwidth [CPU:: 0] [GPU:: 6 - 53458 - 0000:85:00.0] distance:52 PCIe:52
   [RESULT] [1103843.610825] [d2h-sequential-64MB] pcie-bandwidth [CPU:: 1] [GPU:: 6 - 53458 - 0000:85:00.0] distance:20 PCIe:20
   [RESULT] [1103843.610833] [d2h-sequential-64MB] pcie-bandwidth [CPU:: 0] [GPU:: 7 - 63883 - 0000:a6:00.0] distance:52 PCIe:52
   [RESULT] [1103843.610841] [d2h-sequential-64MB] pcie-bandwidth [CPU:: 1] [GPU:: 7 - 63883 - 0000:a6:00.0] distance:20 PCIe:20
   [RESULT] [1103843.610848] [d2h-sequential-64MB] pcie-bandwidth [CPU:: 0] [GPU:: 8 - 53667 - 0000:c6:00.0] distance:52 PCIe:52
   [RESULT] [1103843.610856] [d2h-sequential-64MB] pcie-bandwidth [CPU:: 1] [GPU:: 8 - 53667 - 0000:c6:00.0] distance:20 PCIe:20
   [RESULT] [1103843.610863] [d2h-sequential-64MB] pcie-bandwidth [CPU:: 0] [GPU:: 9 - 63738 - 0000:e5:00.0] distance:52 PCIe:52
   [RESULT] [1103843.610871] [d2h-sequential-64MB] pcie-bandwidth [CPU:: 1] [GPU:: 9 - 63738 - 0000:e5:00.0] distance:20 PCIe:20

The other half of the output for each of the tests, shows the transfer
bandwidth and indicates whether its bidirectional or unidirectional transfer.

.. code-block:: shell-session

   [RESULT] [1103903.617888] [d2h-sequential-64MB] pcie-bandwidth [ 1/16] [CPU:: 0] [GPU:: 2 - 28851 - 0000:05:00.0] h2d::false d2h::true 56.298 GBps ...
   [RESULT] [1103903.617971] [d2h-sequential-64MB] pcie-bandwidth [ 2/16] [CPU:: 1] [GPU:: 2 - 28851 - 0000:05:00.0] h2d::false d2h::true 55.664 GBps ...
   [RESULT] [1103903.617982] [d2h-sequential-64MB] pcie-bandwidth [ 3/16] [CPU:: 0] [GPU:: 3 - 23018 - 0000:26:00.0] h2d::false d2h::true 56.304 GBps ...
   [RESULT] [1103903.617993] [d2h-sequential-64MB] pcie-bandwidth [ 4/16] [CPU:: 1] [GPU:: 3 - 23018 - 0000:26:00.0] h2d::false d2h::true 56.318 GBps ...
   [RESULT] [1103903.618009] [d2h-sequential-64MB] pcie-bandwidth [ 5/16] [CPU:: 0] [GPU:: 4 - 29122 - 0000:46:00.0] h2d::false d2h::true 56.318 GBps ...
   [RESULT] [1103903.618019] [d2h-sequential-64MB] pcie-bandwidth [ 6/16] [CPU:: 1] [GPU:: 4 - 29122 - 0000:46:00.0] h2d::false d2h::true 56.273 GBps ...
   [RESULT] [1103903.618029] [d2h-sequential-64MB] pcie-bandwidth [ 7/16] [CPU:: 0] [GPU:: 5 - 22683 - 0000:65:00.0] h2d::false d2h::true 56.297 GBps ...
   [RESULT] [1103903.618039] [d2h-sequential-64MB] pcie-bandwidth [ 8/16] [CPU:: 1] [GPU:: 5 - 22683 - 0000:65:00.0] h2d::false d2h::true 55.592 GBps ...
   [RESULT] [1103903.618052] [d2h-sequential-64MB] pcie-bandwidth [ 9/16] [CPU:: 0] [GPU:: 6 - 53458 - 0000:85:00.0] h2d::false d2h::true 56.293 GBps ...
   [RESULT] [1103903.618063] [d2h-sequential-64MB] pcie-bandwidth [10/16] [CPU:: 1] [GPU:: 6 - 53458 - 0000:85:00.0] h2d::false d2h::true 56.337 GBps ...
   [RESULT] [1103903.618072] [d2h-sequential-64MB] pcie-bandwidth [11/16] [CPU:: 0] [GPU:: 7 - 63883 - 0000:a6:00.0] h2d::false d2h::true 56.298 GBps ...
   [RESULT] [1103903.618083] [d2h-sequential-64MB] pcie-bandwidth [12/16] [CPU:: 1] [GPU:: 7 - 63883 - 0000:a6:00.0] h2d::false d2h::true 56.325 GBps ...
   [RESULT] [1103903.618116] [d2h-sequential-64MB] pcie-bandwidth [13/16] [CPU:: 0] [GPU:: 8 - 53667 - 0000:c6:00.0] h2d::false d2h::true 56.311 GBps ...
   [RESULT] [1103903.618124] [d2h-sequential-64MB] pcie-bandwidth [14/16] [CPU:: 1] [GPU:: 8 - 53667 - 0000:c6:00.0] h2d::false d2h::true 56.340 GBps ...
   [RESULT] [1103903.618134] [d2h-sequential-64MB] pcie-bandwidth [15/16] [CPU:: 0] [GPU:: 9 - 63738 - 0000:e5:00.0] h2d::false d2h::true 56.287 GBps ...
   [RESULT] [1103903.618142] [d2h-sequential-64MB] pcie-bandwidth [16/16] [CPU:: 1] [GPU:: 9 - 63738 - 0000:e5:00.0] h2d::false d2h::true 56.334 GBps ...

Result:

- PASSED: If all CPUs-GPUs distances are displayed and CPU x (x=0/1) to GPU y
  (y=2/3/4/5/6/7/8/9) PCIe transfer bandwidths are displayed.

- FAILED: Otherwise

  - Action: Proceed to next step. Run this same test later again.

.. _mi300x-rvs-peqt:

PEQT (PCIe Qualification Tool)
------------------------------

The PCIe Qualification Tool is used to qualify the PCIe bus the GPU is
connected to. The qualification tool can determine the following
characteristics of the PCIe bus interconnect to a GPU:

- Support for Gen 3 atomic completers

- DMA transfer statistics

- PCIe link speed

- PCIe link width

The configuration file for the PEQT module is located at ``{RVS_CONF}/peqt_single.conf``.

Command:

.. code-block:: shell

   sudo rvs -c ${RVS_CONF}/peqt_single.conf

This module has total 17 tests (``pcie_act_1`` to ``pcie_act_17``). Each test
checks for a subset of PCIe capabilities and shows the true or false status.

.. note::

   The tests needs ``sudo`` permission to run properly.

Expected output:

.. code-block:: shell-session

   [RESULT] [1105558.986882] Action name :pcie_act_1
   [RESULT] [1105558.988288] Module name :peqt
   [RESULT] [1105559.33461 ] [pcie_act_1] peqt true
   [RESULT] [1105559.33492 ] Action name :pcie_act_2
   [RESULT] [1105559.33497 ] Module name :peqt
   [RESULT] [1105559.72308 ] [pcie_act_2] peqt true
   [RESULT] [1105559.72325 ] Action name :pcie_act_3
   [RESULT] [1105559.72330 ] Module name :peqt
   [RESULT] [1105559.114937] [pcie_act_3] peqt true
   [RESULT] [1105559.114957] Action name :pcie_act_4
   [RESULT] [1105559.114962] Module name :peqt
   [RESULT] [1105559.155511] [pcie_act_4] peqt true
   [RESULT] [1105559.155526] Action name :pcie_act_5
   [RESULT] [1105559.155531] Module name :peqt
   [RESULT] [1105559.190472] [pcie_act_5] peqt true
   [RESULT] [1105559.190491] Action name :pcie_act_6
   [RESULT] [1105559.190495] Module name :peqt
   [RESULT] [1105559.230632] [pcie_act_6] peqt true
   [RESULT] [1105559.230646] Action name :pcie_act_7
   [RESULT] [1105559.230651] Module name :peqt
   [RESULT] [1105559.273512] [pcie_act_7] peqt true
   [RESULT] [1105559.273534] Action name :pcie_act_8
   [RESULT] [1105559.273538] Module name :peqt
   [RESULT] [1105559.316290] [pcie_act_8] peqt true
   [RESULT] [1105559.316305] Action name :pcie_act_9
   [RESULT] [1105559.316310] Module name :peqt
   [RESULT] [1105559.357042] [pcie_act_9] peqt true
   [RESULT] [1105559.357064] Action name :pcie_act_10
   [RESULT] [1105559.357069] Module name :peqt
   [RESULT] [1105559.391754] [pcie_act_10] peqt true
   [RESULT] [1105559.391767] Action name :pcie_act_11
   [RESULT] [1105559.391771] Module name :peqt
   [RESULT] [1105559.434373] [pcie_act_11] peqt true
   [RESULT] [1105559.434391] Action name :pcie_act_12
   [RESULT] [1105559.434395] Module name :peqt
   [RESULT] [1105559.470072] [pcie_act_12] peqt true
   [RESULT] [1105559.470087] Action name :pcie_act_13
   [RESULT] [1105559.470091] Module name :peqt
   [RESULT] [1105559.512754] [pcie_act_13] peqt true
   [RESULT] [1105559.512774] Action name :pcie_act_14
   [RESULT] [1105559.512778] Module name :peqt
   [RESULT] [1105559.552761] [pcie_act_14] peqt true
   [RESULT] [1105559.552779] Action name :pcie_act_15
   [RESULT] [1105559.552783] Module name :peqt
   [RESULT] [1105559.586778] [pcie_act_15] peqt true
   [RESULT] [1105559.586794] Action name :pcie_act_16
   [RESULT] [1105559.586798] Module name :peqt
   [RESULT] [1105559.620305] [pcie_act_16] peqt true
   [RESULT] [1105559.620322] Action name :pcie_act_17
   [RESULT] [1105559.620326] Module name :peqt
   [RESULT] [1105559.651564] [pcie_act_17] peqt true

Result:

- PASSED: ``[pcie_act_x] peqt true`` can be seen for all 17 actions.

- FAILED: If any tests show true.

  - Action: Check that you are running this test as root or with ``sudo``
    privileges. If not, actions 6 through 16 will fail. Run this same test
    later again.

.. _mi300x-rvs-pbqt:

PBQT (P2P Benchmark and Qualification Tool)
-------------------------------------------

The PBQT module executes the following tests:

- List all GPUs that support P2P

- Characterizes the P2P links between peers

- Performs a peer-to-peer throughput test between all P2P pairs

The configuration file for the ``pbqt`` module for MI300X is located here:
``{RVS_CONF}/MI300X/pbqt_single.conf``.

The ``conf`` file has 12 ``actions_xy`` test segments. Each of these checks for
peer-to-peer connectivity among GPUs and provides a true/false status. In
addition, it also performs bidirectional throughput test and reports the
throughput obtained based on config parameters. Since comparison is not
performed for some target throughput numbers, there is no PASS/FAIL condition
for the overall test.

It's recommended that you carefully review the ``pbqt_single.conf`` file before
running the following command.

Command:

.. code-block:: shell

   rvs -c ${RVS_CONF}/MI300X/pbqt_single.conf

Only two example lines from the very long log file is shown because other lines
look similar as all combinations of GPU pairs are considered and numbers for
those pairs are reported.

Expected output below (truncated) shows uni-directional connectivity is true
for the GPU and its connection to the other seven GPU peers:

.. code-block:: shell-session

   [RESULT] [1104553.34268 ] [p2p-unidir-sequential-64MB] p2p [GPU:: 2 - 28851 - 0000:05:00.0] [GPU:: 3 - 23018 - 0000:26:00.0] peers:true distance:15 xGMI:15
   [RESULT] [1104553.34276 ] [p2p-unidir-sequential-64MB] p2p [GPU:: 2 - 28851 - 0000:05:00.0] [GPU:: 4 - 29122 - 0000:46:00.0] peers:true distance:15 xGMI:15
   [RESULT] [1104553.34280 ] [p2p-unidir-sequential-64MB] p2p [GPU:: 2 - 28851 - 0000:05:00.0] [GPU:: 5 - 22683 - 0000:65:00.0] peers:true distance:15 xGMI:15
   [RESULT] [1104553.34283 ] [p2p-unidir-sequential-64MB] p2p [GPU:: 2 - 28851 - 0000:05:00.0] [GPU:: 6 - 53458 - 0000:85:00.0] peers:true distance:15 xGMI:15
   [RESULT] [1104553.34289 ] [p2p-unidir-sequential-64MB] p2p [GPU:: 2 - 28851 - 0000:05:00.0] [GPU:: 7 - 63883 - 0000:a6:00.0] peers:true distance:15 xGMI:15
   [RESULT] [1104553.34294 ] [p2p-unidir-sequential-64MB] p2p [GPU:: 2 - 28851 - 0000:05:00.0] [GPU:: 8 - 53667 - 0000:c6:00.0] peers:true distance:15 xGMI:15
   [RESULT] [1104553.34298 ] [p2p-unidir-sequential-64MB] p2p [GPU:: 2 - 28851 - 0000:05:00.0] [GPU:: 9 - 63738 - 0000:e5:00.0] peers:true distance:15 xGMI:15

The following lines show unidirectional throughput between the 56 GPU pairs
(not all are shown):

.. code-block:: shell-session

   [RESULT] [1104673.143726] [p2p-unidir-parallel-64MB] p2p-bandwidth[ 1/56] [GPU:: 2 - 28851 - 0000:05:00.0] [GPU:: 3 - 23018 - 0000:26:00.0] bidirectional: false 48.962 GBps duration: 1.462462 secs
   [RESULT] [1104673.144823] [p2p-unidir-parallel-64MB] p2p-bandwidth[ 2/56] [GPU:: 2 - 28851 - 0000:05:00.0] [GPU:: 4 - 29122 - 0000:46:00.0] bidirectional: false 48.914 GBps duration: 1.470746 secs
   [RESULT] [1104673.145898] [p2p-unidir-parallel-64MB] p2p-bandwidth[ 3/56] [GPU:: 2 - 28851 - 0000:05:00.0] [GPU:: 5 - 22683 - 0000:65:00.0] bidirectional: false 48.577 GBps duration: 1.480956 secs

Result:

- PASSED: If ``peers:true`` lines are observed for GPUs peer-to-peer
  connectivity and if throughput values are non-zeros.

- FAILED: Otherwise

  - Action: Do not proceed further. Report this issue to your system
    manufacturer immediately.
