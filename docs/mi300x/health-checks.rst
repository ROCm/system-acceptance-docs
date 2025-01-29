.. meta::
   :description lang=en: AMD Instinct MI300X system health checks for acceptance testing.
   :keywords: prereq, prerequisite, memory, smi, log

**************************
Basic system health checks
**************************

Before proceeding with more extensive system validation, it's important to
ensure all components in the system are operating at peak performance and
bandwidth.

A typical MI300X-based GPU server architecture consists of the following
components.

- Host CPUs: Usually dual socket, handling general processing and orchestrating
  tasks.

- Memory: DRAM attached to each CPU socket for fast data access.

- GPUs: Multiple GPUs connected over AMD Infinity Fabric Link for parallel
  processing and acceleration.

- HBM3 Memory: attached to GPUs through I/O Die (IOD).

- Storage: High-speed NVMe SSDs or traditional HDDs for data storage.

- Networking: High-bandwidth network interfaces like 100-400 GbE or InfiniBand
  for fast data transfer between systems.

The CPUs, memory, GPUs, storage, and networking components are interconnected
via high-speed communication paths, with PCIe lanes facilitating data flow
between CPUs and GPUs. This architecture allows for efficient parallel
processing and accelerated computation for AI, HPC, and other demanding
workloads.

This section covers the basic system checks for the Instinct MI300X accelerators
connected in the system using:

- Basic Linux system commands: ``cat``, ``dmesg``, ``lsmem``, and ``lspci``

- ROCm monitoring tool: ``amd-smi``

.. note::

   Checking the health of other system components in the system is outside the
   scope of this document.

After the system boots, run the commands listed in the following sections. For
each command, an example output is provided. Expect to see similar output when
these commands are executed on the System Under Test (SUT). For illustration
purposes, commands and the output shown below were obtained from a system
running Ubuntu 22.04, which is one of the supported distributions for ROCm 6.2.
Running other supported distributions on the SUT may result in slightly
different output.

OS and host system checks
=========================

The following sections list the operating system and host CPU and memory
checks. A sample command and corresponding log output are shown for each item.
The sample outputs provide typical results and serve as a guideline.

.. note::

   If results vary from the sample expected output, contact your system
   manufacturer support representative for further assistance.

.. _mi300x-health-checks-os-release:

Check OS distribution
---------------------

Check the OS distribution installed on the SUT using the following command.

.. code-block:: shell

   cat /etc/os-release

Example output (varies depending on the running Linux distribution):

.. code-block:: shell-session

   VERSION="22.04.4 LTS (Jammy Jellyfish)"

Ensure that the OS distribution used is listed in the :doc:`ROCm compatibility
matrix <rocm:compatibility/compatibility-matrix>` or in :ref:`Past versions of
ROCm compatibility matrix <rocm:past-rocm-compatibility-matrix>`.

Result:

- PASSED: VERSION is listed in the compatibility matrix page.

- FAILED: Not listed in the compatibility matrix page.

  - Action: If the operating system distribution is not listed in the
    compatibility matrix pages, do not continue with the following steps.
    Instead, install a supported distribution and then proceed with the
    installation of ROCm 6.2 or a newer version.

.. _mi300x-health-checks-cmdline:

Check kernel boot arguments
---------------------------

The Linux kernel must utilize correct boot arguments during the startup of the
System Under Test (SUT). Once the system has booted, run the following command
in the terminal to display the boot arguments:

Command:

.. code-block:: shell

   cat /proc/cmdline

An example of the output from an AMD CPU-based system is given below, with the
required boot parameters highlighted in yellow. Output might vary based on OS
distribution and GRUB settings. When using Intel host processors, replace
``amd_iommu`` with ``intel_iommu``.

.. code-block:: shell-session

   BOOT_IMAGE=/boot/vmlinuz-6.8.0-40-generic root=UUID=372435f6-bb80-4d82-83ed-c4d077dc5e23 ro pci=realloc=off amd_iommu=on iommu=pt

Result:

- PASSED: If output displays the following settings:

  - ``pci=realloc=off``

  - ``amd_iommu=on`` or ``intel_iommu=on``

    - Be sure to use the parameter appropriate for the host CPU used

  - ``iommu=pt``

- FAILED:

  - Action: Don’t proceed. Update the GRUB settings of the SUT
    and reboot, and then start the acceptance testing from this section.
    Note that if ``pci=realloc=off`` is not in GRUB configuration in Ubuntu
    distribution, not all GPUs may be recognized.

.. _mi300x-health-checks-driver-errors:

Check for driver errors
-----------------------

Use the following command to check for driver errors in the Linux OS
diagnostic messages (``dmesg``).

.. code-block:: shell

   sudo dmesg -T | grep amdgpu | grep -i error

The expected output should return no results (null).

Result:

- PASSED: Null

- FAILED: Errors reported

  - Action: Don’t proceed. Reinstall amdgpu driver and then
    start the acceptance testing from this section.

.. _mi300x-health-checks-lsmem:

Check for available memory
--------------------------

Confirm there is at least 1.5T of memory in the system.

Command:

.. code-block:: shell

   lsmem | grep "Total online memory"

Expected output:

.. code-block:: shell-session

   Total online memory: 1.5T

.. warning::

   If the available memory is less than 1.5T, the system may not function
   properly when a large workload is run. But you can continue to next check.

.. _mi300x-health-checks-lspci:

Check GPU presence
==================

Confirm all GPU accelerators are present and available on the PCIe bus by
running the following command.

.. code-block:: shell

   lspci | grep MI300X

Example output:

.. code-block:: shell-session

   05:00.0 Processing accelerators: Advanced Micro Devices, Inc. [AMD/ATI] Aqua Vanjaram [Instinct MI300X]
   26:00.0 Processing accelerators: Advanced Micro Devices, Inc. [AMD/ATI] Aqua Vanjaram [Instinct MI300X]
   46:00.0 Processing accelerators: Advanced Micro Devices, Inc. [AMD/ATI] Aqua Vanjaram [Instinct MI300X]
   65:00.0 Processing accelerators: Advanced Micro Devices, Inc. [AMD/ATI] Aqua Vanjaram [Instinct MI300X]
   85:00.0 Processing accelerators: Advanced Micro Devices, Inc. [AMD/ATI] Aqua Vanjaram [Instinct MI300X]
   a6:00.0 Processing accelerators: Advanced Micro Devices, Inc. [AMD/ATI] Aqua Vanjaram [Instinct MI300X]
   c6:00.0 Processing accelerators: Advanced Micro Devices, Inc. [AMD/ATI] Aqua Vanjaram [Instinct MI300X]
   e5:00.0 Processing accelerators: Advanced Micro Devices, Inc. [AMD/ATI] Aqua Vanjaram [Instinct MI300X]

Result:

- PASSED: If all eight GPUs are found shown above

- FAILED:

  - Action:

    - Don’t proceed further. Adjust GRUB configuration to ensure
      ``pci=realloc=off`` is present.

    - Reboot and rerun the above command to confirm all eight GPUs are shown.

    - If the issue persists despite previous attempts, verify that the torque
      applied to OAMs meets required specification.

    - If adjusting the torque does not resolve the problem, contact your system
      manufacturer for further assistance.

.. _mi300x-health-checks-gpu-link-speed:

Check GPU link speed and width on PCIe bus
==========================================

Confirm PCIe links to each of the GPUs are running at full speed and width. Use
the following ``lspci`` command with the highest verbosity mode (``-vvv``)
available and designating the vendor ``ID=1002`` with device ``ID=0x74a1`` and
``grep`` for device status (``DevSta``) and link status (``LnkSta``).

Command:

.. code-block:: shell

   sudo lspci -d 1002:74a1 -vvv | grep -e DevSta -e LnkSta

Expected output:

.. code-block:: shell-session

   DevSta: CorrErr- NonFatalErr- FatalErr- UnsupReq- AuxPwr- TransPend-
   LnkSta: Speed 32GT/s, Width x16
   DevSta: CorrErr- NonFatalErr- FatalErr- UnsupReq- AuxPwr- TransPend-
   LnkSta: Speed 32GT/s, Width x16
   DevSta: CorrErr- NonFatalErr- FatalErr- UnsupReq- AuxPwr- TransPend-
   LnkSta: Speed 32GT/s, Width x16
   DevSta: CorrErr- NonFatalErr- FatalErr- UnsupReq- AuxPwr- TransPend-
   LnkSta: Speed 32GT/s, Width x16
   DevSta: CorrErr- NonFatalErr- FatalErr- UnsupReq- AuxPwr- TransPend-
   LnkSta: Speed 32GT/s, Width x16
   DevSta: CorrErr- NonFatalErr- FatalErr- UnsupReq- AuxPwr- TransPend-
   LnkSta: Speed 32GT/s, Width x16
   DevSta: CorrErr- NonFatalErr- FatalErr- UnsupReq- AuxPwr- TransPend-
   LnkSta: Speed 32GT/s, Width x16
   DevSta: CorrErr- NonFatalErr- FatalErr- UnsupReq- AuxPwr- TransPend-
   LnkSta: Speed 32GT/s, Width x16

Result:

- PASSED: Each output line must have:

  - ``LinkSta`` displays link speed is 32GT/s and width is ``x16``, and

  - ``FatalErr+`` is not displayed

- FAILED: If ``FatalErr+`` is present

  - Action: Do not proceed further. Report this issue to your system
    manufacturer immediately.

.. _mi300x-health-checks-monitor-utilization:

Monitor utilization metrics
===========================

The ``amd-smi`` monitor command-line tool, typically installed with ROCm, can be
used to monitor AMD GPU hardware, including thermal, power, hardware performance
along with error reporting. The ``amd-smi`` can be run in parallel with the
validation tests outlined in this guide to provide additional information on the
operation of the system. See `Getting to Know Your GPU: A Deep Dive into AMD SMI
<https://rocm.blogs.amd.com/software-tools-optimization/amd-smi-overview/README.html>`_
for details on this tool.

.. note::

   This check requires that ROCm be installed on the SUT. The monitoring tool
   ``rocm-smi`` may alternatively be used.

Run the following command to display GPU metrics when the system is idle, that
is, not running any workload.

.. code-block:: shell

   amd-smi monitor -putm

Example output (results will vary when the system is running a workload):

.. code-block:: shell-session

   GPU POWER GPU_TEMP MEM_TEMP **GFX_UTIL** **GFX_CLOCK** **MEM_UTIL** **MEM_CLOCK**
   0 125 W 37 °C 32 °C 0 % 158 MHz 0 % 900 MHz
   1 121 W 36 °C 28 °C 0 % 139 MHz 0 % 900 MHz
   2 124 W 39 °C 29 °C 0 % 141 MHz 0 % 900 MHz
   3 122 W 36 °C 28 °C 0 % 158 MHz 0 % 900 MHz
   4 125 W 40 °C 32 °C 0 % 140 MHz 0 % 900 MHz
   5 124 W 36 °C 29 °C 0 % 139 MHz 0 % 900 MHz
   6 124 W 38 °C 31 °C 0 % 139 MHz 0 % 900 MHz
   7 122 W 37 °C 29 °C 0 % 142 MHz 0 % 900 MHz

When the system is idle, the GPU’s utilization (``GFX_UTIL``) and memory
utilization (``MEM_UTIL``) will be 0%. The frequency of the GPU clock
(``GFX_CLOCK``) will be throttled back to under 200MHz and memory
(``MEM_CLOCK``) throttled down to 900 MHz. The GPU temperature (``GPU_TEMP``)
should also be well under 85°C when idle.

Result for an idle system:

- PASSED: When the system is idle, the GPU’s utilization (``GFX_UTIL``) and
  memory utilization (``MEM_UTIL``) should be 0%, the frequency of the GPU
  clock (``GFX_CLOCK``) throttled back to under 200 MHz, memory (``MEM_CLOCK``)
  throttled down to 900 MHz, and GPU temperature (``GPU_TEMP``) should also
  be well under 85°C.

- FAILED: Otherwise

  - Action: Check the data center ambient temperature and system fan speed.
    Power cycle the system. If the issue persists, report this issue to your
    system manufacturer.

.. _mi300x-health-checks-system-kernel-logs:

Check the system kernel logs for other errors
=============================================

The command line utility ``dmesg`` prints boot-time message and on-going kernel
event messages about the state of the system hardware and drivers. The utility
is useful for capturing diagnostic information for troubleshooting hardware and
driver issues.

To check for errors in the kernel messages, use the following command:

.. code-block:: shell

   sudo dmesg -T | grep -i 'error\|warn\|fail\|exception'

Expected output:

When system is operating without errors, warnings, or failures, the output of
the command will be null.

Result:

- PASSED: The output will be null when the system is running properly.

- FAILED: Otherwise

  - Action: Don’t proceed further. Analyze each ``dmesg`` error, fail, and
    exception.

See :doc:`/reference/rocm-techsupport` for information on the
``rocm_techsupport.sh`` script utility, which collects system logs for support
and troubleshooting.
