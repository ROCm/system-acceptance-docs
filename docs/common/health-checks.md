# Basic system health checks

Before proceeding with more extensive system validation, it's important to ensure all components in the system are operating at peak performance and bandwidth.

A typical Instinct GPU server architecture consists of the following components:

- Host CPUs: Usually dual socket, handling general processing and orchestrating tasks.
- Memory: DRAM attached to each CPU socket for fast data access.
- GPUs: Multiple GPUs connected over AMD Infinity Fabric Link for parallel processing and acceleration.
- HBM Memory: attached to GPUs through I/O Die (IOD).
- Storage: High-speed NVMe SSDs or traditional HDDs for data storage.
- Networking: High-bandwidth network interfaces like 100-400 GbE or InfiniBand for fast data transfer between systems.

This section covers the basic system checks for Instinct accelerators connected in the system using:

- Basic Linux system commands: `cat`, `dmesg`, `lsmem`, and `lspci`
- ROCm monitoring tool: `amd-smi`

```{note}
Checking the health of other system components in the system is outside the scope of this document.
```

After the system boots, run the commands listed in the following sections. For each command, an example output is provided. For illustration
purposes, commands and the output shown below were obtained from a system running Ubuntu 22.04. Running other supported distributions on the SUT may result in slightly different output.

## OS and Host System Checks

This section outlines checks to verify your system’s operating environment, including OS distribution, kernel boot parameters, GPU driver status, and available memory. Each step includes example commands and expected outputs to help you confirm your system is properly configured for AMD Instinct™-based GPUs.

```{note}
If results vary from the sample expected output, contact your system manufacturer support representative for further assistance.
```

### Check OS Distribution

Verify the operating system distribution:

```bash
lsb_release -a
```

Or check the release file:

```bash
cat /etc/os-release
# Example output (varies depending on the running Linux distribution):
VERSION="22.04.5 LTS (Jammy Jellyfish)"
```

Ensure that the OS distribution used is listed in the [ROCm compatibility matrix](https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html).

**Result:**

- **PASSED:** The OS version is listed in the compatibility matrix.
- **FAILED:** The OS version is not listed in the compatibility matrix.
  - **Action:** Do not continue. Install a supported distribution before proceeding.

### Check Kernel Boot Arguments

The Linux kernel must utilize correct boot arguments. Once the system has booted, run the following command to display the boot arguments:

```shell
cat /proc/cmdline
```

An example of the output from an AMD CPU-based system is given below, with the required boot parameters highlighted. Output might vary based on OS distribution and GRUB settings. When using Intel host processors add `intel_iommu=on`.

```bash
BOOT_IMAGE=/boot/vmlinuz-6.8.0-40-generic ... ro pci=realloc=off pci=bfsort iommu=pt numa_balancing=disable modprobe.blacklist=amdgpu
```

**Result:**

- **PASSED:** If output displays the required settings.
- **FAILED:**
  - **Action:** Do not proceed. Update the GRUB settings as described in the [Kernel Parameters](kernel-parameters.md) guide, reboot, and restart the health checks.

### Check for Driver Errors

Check for any driver-related errors in the system logs:

```bash
dmesg | grep -i error
journalctl -p err
```

The expected output should be null or show no critical errors related to `amdgpu`.

**Result:**

- **PASSED:** No critical driver errors are reported.
- **FAILED:** Driver errors are present.
  - **Action:** Reinstall the `amdgpu` driver and restart the health checks.

### Check for Available System Memory

Verify sufficient system memory is available using `free -h` or `cat /proc/meminfo`. The recommended minimum system memory for AMD Instinct products is as follows:

| Product | Minimum System Memory (TB) |
|---|---|
| MI300X | 2.0 |
| MI308X | 2.0 |
| MI325X | 2.5 |
| MI350X | 3.0 |
| MI355X | 3.0 |

> **Warning:** If the available memory is less than the recommended amount, the system may not function properly under heavy workloads.

## Check GPU Presence

Confirm all GPU accelerators are present and available on the PCIe bus by running the command corresponding to your product.

| Product | Command |
| --- | --- |
| MI300X | `sudo lspci -d 1002:74a1` |
| MI308X | `sudo lspci -d 1002:74a2` |
| MI325X | `sudo lspci -d 1002:74a5` |
| MI350X | `sudo lspci -d 1002:75a0` |
| MI355X | `sudo lspci -d 1002:75a3` |

**Example output:**

```bash
05:00.0 Processing accelerators: Advanced Micro Devices, Inc. [AMD/ATI] Device 75a0
... (8 entries expected)
```

**Result:**

- **PASSED:** All eight GPUs are found.
- **FAILED:** Fewer than eight GPUs are found.
  - **Action:**
    - Ensure `pci=realloc=off` is present in the kernel boot arguments.
    - Reboot and rerun the command.
    - If the issue persists, verify the torque applied to OAMs meets the required specification.
    - If the problem is not resolved, contact your system manufacturer.

## Check GPU PCIe Bus Link Speed and Width

Confirm the PCIe links to each GPU are running at full speed and width. Use the `lspci` command associated with your product to check for device status (`DevSta`) and link status (`LnkSta`).

| Product | Command |
| --- | --- |
| MI300X | `sudo lspci -d 1002:74a1 -vvv \| grep -e DevSta -e LnkSta` |
| MI308X | `sudo lspci -d 1002:74a2 -vvv \| grep -e DevSta -e LnkSta` |
| MI325X | `sudo lspci -d 1002:74a5 -vvv \| grep -e DevSta -e LnkSta` |
| MI350X | `sudo lspci -d 1002:75a0 -vvv \| grep -e DevSta -e LnkSta` |
| MI355X | `sudo lspci -d 1002:75a3 -vvv \| grep -e DevSta -e LnkSta` |

**Expected output:**

```bash
DevSta: CorrErr- NonFatalErr- FatalErr- UnsupReq- AuxPwr- TransPend-
LnkSta: Speed 32GT/s (ok), Width x16 (ok)
... (8 pairs of entries expected)
```

**Result:**

- **PASSED:** Each GPU shows a link speed of 32GT/s, a width of x16, and no `FatalErr+`.
- **FAILED:** If `FatalErr+` is present or the link speed/width is suboptimal.
  - **Action:** Do not proceed. Report this issue to your system manufacturer immediately.

## Monitor Utilization Metrics

Verify all GPUs are operating within the expected range when the system is idle using `amd-smi`.

```shell
amd-smi monitor -putm
```

**Example idle output:**

```bash
GPU POWER PWR_CAP GPU_T MEM_T GFX_CLK GFX% MEM% MEM_CLOCK
0 251 W 1000 W 55 °C 43 °C 144 MHz 0 % 0 % 1900 MHz
... (8 entries expected)
```

When the system is idle, GPU and memory utilization should be 0%, clocks should be low, and temperature should be well under 85°C.

**Result for an idle system:**

- **PASSED:** All metrics are within the expected idle range.
- **FAILED:** Metrics are outside the expected idle range.
  - **Action:** Check data center ambient temperature and system fan speed. Power cycle the system. If the issue persists, contact your system manufacturer.

## Check System Kernel Logs

Use `dmesg` to check for other hardware or driver errors, warnings, or failures.

```shell
sudo dmesg -T | grep -i 'error\|warn\|fail\|exception'
```

**Result:**

- **PASSED:** The output is null or contains no relevant issues.
- **FAILED:** The output shows errors, warnings, or exceptions.
  - **Action:** Do not proceed. Analyze each message and troubleshoot accordingly.

See the [technical support reference](../reference/rocm-techsupport.md) for information on the `rocm_techsupport.sh` script utility, which collects system logs for support and troubleshooting.
