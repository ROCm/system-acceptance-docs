.. meta::
   :description lang=en: AMD Instinct MI300X acceptance criteria for system administrators.
   :keywords: tests, checklist, list, summary, overview, qualification

*******************
Acceptance criteria
*******************

Provided the system under test passes the following criteria, the SUT is ready
and should be accepted.

.. _mi300x-acceptance-health-checks:

.. list-table:: Summary of basic system health checks
   :header-rows: 1

   * - Test
     - Command
     - Pass/Fail criteria

   * - :ref:`Check OS distribution <mi300x-health-checks-os-release>`
     - .. code-block:: shell

          cat/etc/os-release

     - 
       * **Pass**: OS version listed in compatibility matrix
       * **Fail**: Otherwise

   * - :ref:`Check kernel boot arguments <mi300x-health-checks-cmdline>`
     - .. code-block:: shell

          cat/proc/cmdline

     - 
       * **Pass**: Contains ``pci-realloc=off``, ``amd_iommu=on`` or
         ``intel_iommu=on``, and ``iommu=pt``
       * **Fail**: Otherwise

   * - :ref:`Check for driver errors <mi300x-health-checks-driver-errors>`
     - .. code-block:: shell

          sudo dmesg -T | grep amdgpu | grep -i error

     - 
       * **Pass**: Null
       * **Fail**: Errors reported

   * - :ref:`Check available memory <mi300x-health-checks-lsmem>`
     - .. code-block:: shell

          lsmem | grep "Total online memory"

     - 
       * **Pass**: 1.5T or more
       * **Fail**: Less than 1.5T

   * - :ref:`Check GPU presence <mi300x-health-checks-lspci>`
     - .. code-block:: shell

          lspci | grep MI300X

     - 
       * **Pass**: All 8 GPUs found
       * **Fail**: Otherwise

   * - :ref:`Check GPU link speed and width <mi300x-health-checks-gpu-link-speed>`
     - .. code-block:: shell

          sudo lspci -d 1002:74a1 -vvv | grep -e DevSta -e LnkSta

     - 
       * **Pass**: Speed 32GT/s, width ``x16``, no ``FatalErr+``
       * **Fail**: Otherwise

   * - :ref:`Monitor utilization metrics <mi300x-health-checks-monitor-utilization>`
     - .. code-block:: shell

          amd-smi monitor -putm

     - 
       * **Pass**: Idle metrics as specified
       * **Fail**: Otherwise

   * - :ref:`Check system kernel logs for errors <mi300x-health-checks-system-kernel-logs>`
     - .. code-block:: shell

          sudo dmesg -T | grep -i 'error|warn|fail|exception'

     - 
       * **Pass**: Null
       * **Fail**: Otherwise

.. _mi300x-acceptance-system-validation:

.. list-table:: Summary of system validation tests
   :header-rows: 1

   * - Test
     - Command
     - Pass/Fail criteria

   * - :ref:`Compute/GPU properties <mi300x-rvs-compute-gpu>`
     - .. code-block:: shell

          rvs -c ${RVS_CONF}/gpup_single.conf

     - 
       * **Pass**: All GPUs listed with no errors
       * **Fail**: Missing GPUs or errors

   * - :ref:`GPU stress test (GST) <mi300x-rvs-gst>`
     - .. code-block:: shell

          rvs -c ${RVS_CONF}/MI300X/gst_single.conf

     - 
       * **Pass**: ``met: TRUE`` in logs
       * **Fail**: Target GFLOP/s not met

   * - :ref:`Input energy delay product (IET) <mi300x-rvs-iet>`
     - .. code-block:: shell

          rvs -c ${RVS_CONF}/MI300X/iet_single.conf

     - 
       * **Pass**: ``met: TRUE`` for all actions
       * **Fail**: Otherwise

   * - :ref:`Memory test (MEM) <mi300x-rvs-mem>`
     - .. code-block:: shell

          rvs -c ${RVS_CONF}/mem.conf -l mem.txt

     - 
       * **Pass**: All tests passed; bandwidth ~2TB/s
       * **Fail**: Any test failed or low bandwidth

   * - :ref:`PCIe bandwidth benchmark (PEBB) <mi300x-rvs-pebb>`
     - .. code-block:: shell

          rvs -c ${RVS_CONF}/MI300X/pebb_single.conf

     - 
       * **Pass**: All distances and bandwidths displayed
       * **Fail**: Missing data

   * - :ref:`PCIe qualification tool (PEQT) <mi300x-rvs-peqt>`
     - .. code-block:: shell

          rvs -c ${RVS_CONF}/peqt_single.conf

     - 
       * **Pass**: All actions true
       * **Fail**: Otherwise

   * - :ref:`P2P benchmark and qualification tool (PBQT) <mi300x-rvs-pbqt>`
     - .. code-block:: shell

          rvs -c ${RVS_CONF}/pbqt_single.conf

     - 
       * **Pass**: ``peers:true`` lines and non-zero throughput
       * **Fail**: Otherwise

.. _mi300x-acceptance-performance-bench:

.. list-table:: Summary of performance benchmarking tests
   :header-rows: 1

   * - Test
     - Command
     - Pass/Fail criteria

   * - :ref:`TransferBench all-to-all <mi300x-bench-transferbench-a2a>`
     - .. code-block:: shell

          TransferBench a2a

     - 
       * **Pass**: Greater than or equal to 32.9
       * **Fail**: Otherwise

   * - :ref:`TransferBench peer-to-peer <mi300x-bench-transferbench-p2p>`
     - .. code-block:: shell

          TransferBench p2p

     - 
       * **UniDir pass**: Greater than or equal to 33.9
       * **BiDir pass**: Greater than or equal to 43.9
       * **Fail**: Otherwise

   * - :ref:`TransferBench tests 1 to 6 <mi300x-bench-transferbench-configfile>`
     - .. code-block:: shell

          TransferBench example.cfg

     - 
       * **Test 1 pass**: Greater than or equal to 47.1 GB/s
       * **Test 2 pass**: Greater than or equal to 48.4 GB/s
       * **Test 3 pass**: Greater than or equal to 31.9 GB/s (0 to 1) and 38.9
         GB/s (1 to 0)
       * **Test 4 pass**: Greater than or equal to 1264 GB/s
       * **Test 5 pass**: N/A for GPU validation
       * **Test 6 pass**: Greater than or equal to 48.6 GB/s
       * **Fail**: Otherwise

   * - :ref:`RCCL Allreduce <mi300x-bench-rccl-allreduce>`
     - .. code-block:: shell

          build/all_reduce_perf -b 8 -e 8G -f 2 -g 8

     - 
       * **Pass**: Greater than or equal to 304 GB/s
       * **Fail**: Otherwise

   * - :ref:`rocBLAS FP32 benchmark <mi300x-bench-rocblas-fp32>`
     - .. code-block:: shell

          rocblas-bench -f gemm \
            -r s -m 4000 \
            --lda 4000 --ldb 4000 --ldc 4000 \
            --transposeA N --transposeB T

     - 
       * **Pass**: Greater than or equal to 94100 TFLOPS
       * **Fail**: Otherwise

   * - :ref:`rocBLAS BF16 benchmark <mi300x-bench-rocblas-bf16>`
     - .. code-block:: shell

          rocblas-bench -f gemm_strided_batched_ex \
            --transposeA N --transposeB T \
            -m 1024 -n 2048 -k 512 \
            --a_type h --lda 1024 --stride_a 4096 \
            --b_type h --ldb 2048 --stride_b 4096 \
            --c_type s --ldc 1024 --stride_c 2097152 \
            --d_type s --ldd 1024 --stride_d 2097152 \
            --compute_type s \
            --alpha 1.1 --beta 1 \
            --batch_count 5

     - 
       * **Pass**: Greater than or equal to 130600 TFLOPS
       * **Fail**: Otherwise

   * - :ref:`rocBLAS INT8 benchmark <mi300x-bench-rocblas-int8>`
     - .. code-block:: shell

          rocblas-bench -f gemm_strided_batched_ex \
            --transposeA N --transposeB T \
            -m 1024 -n 2048 -k 512 \
            --a_type i8_r --lda 1024 --stride_a 4096 \
            --b_type i8_r --ldb 2048 --stride_b 4096 \
            --c_type i32_r --ldc 1024 --stride_c 2097152 \
            --d_type i32_r --ldd 1024 --stride_d 2097152 \
            --compute_type i32_r \
            --alpha 1.1 --beta 1 \
            --batch_count 5

     - 
       * **Pass**: Greater than or equal to 162700 TFLOPS
       * **Fail**: Otherwise

   * - :ref:`BabelStream <mi300x-bench-babelstream>`
     - .. code-block:: shell

          mpiexec -n 8 wrapper.sh

     - 
       * **Copy pass**: Greater than or equal to 4,177,285 MB/s
       * **Copy pass**: Greater than or equal to 4,067,069 MB/s
       * **Copy pass**: Greater than or equal to 3,920,853 MB/s
       * **Copy pass**: Greater than or equal to 3,885,301 MB/s
       * **Copy pass**: Greater than or equal to 3,660,781 MB/s
       * **Fail**: Otherwise
