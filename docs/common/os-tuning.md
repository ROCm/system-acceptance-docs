# OS Tuning

This section describes the operating system tuning parameters including C-states, NUMA configuration, and environment variables common to all AMD Instinct GPU models.

## Overview

Operating system tuning is essential for achieving optimal performance with AMD Instinct accelerators. This section covers C-states configuration, NUMA optimization, kernel parameters, and environment variables that should be applied to all AMD Instinct GPU systems.

For all BIOS-level optimizations that complement these OS settings, refer to the [BIOS Settings](bios-settings.md) guide.

```{note}
The AMD Instinct MI300A APU uses a unified CPU+GPU shared-memory architecture that requires additional OS-level configuration not covered in this page. If you are working with MI300A systems, see the [APU-specific OS tuning](../gpus/mi300a.md#apu-specific-os-tuning) section in the MI300A page before proceeding.
```

## C-states Configuration

### C-state Definitions

- **C0**: Active state while running an application
- **C1**: Idle state with minimal latency to return to active
- **C2**: Deeper sleep state with greater latency when returning to active

### Linux Configuration

If C-states must be enabled in BIOS, it's recommended to disable the C2 state to reduce latency, which is particularly important for high-performance networking.

First, install the `cpupower` tool. The package name varies by distribution:

````{tab-set}
```{tab-item} Ubuntu
sudo apt install linux-tools-common
```

```{tab-item} RHEL
sudo yum install cpupowerutils
```

```{tab-item} SLES
sudo zypper install cpupower
```
````

Then disable power-gating on all cores:

```bash
cpupower idle-set -d 2
```

```{note}
If the CPU core states (C-states) has not been restricted in kernel command-line with the parameter processor.max_cstate=0, then the C-state should be set after every reboot. The kernel command-line method is preferred.
```

## NUMA Configuration

### Kernel Parameters

Add the following to your GRUB configuration:

```bash
numa_balancing=disable
```

This parameter disables NUMA page migration which can cause overhead during GPU operations.

### Verification

```bash
# Check NUMA balancing status
cat /proc/sys/kernel/numa_balancing
```

- **0**: Disabled (recommended)
- **1**: Enabled

> **Note**: Disabling NUMA balancing should be done cautiously and tested in controlled environments first.

### Persist NUMA balancing setting across kernel updates

Kernel updates can re-enable NUMA balancing. To ensure the setting is always applied at boot, add a cron job for the root user:

```bash
sudo crontab -e
```

Add the following line:

```bash
@reboot sh -c 'echo 0 > /proc/sys/kernel/numa_balancing'
```

Verify the setting after the next reboot:

```bash
cat /proc/sys/kernel/numa_balancing
```

A value of `0` confirms NUMA balancing is disabled.

## Kernel Parameters for Performance

For recommended kernel parameters, refer to the [Kernel Parameters](kernel-parameters.md) document.

## Environment Variables

### Critical ROCm/HIP Environment Variables

These environment variables are essential for optimal ROCm performance:

```bash
export HIP_FORCE_DEV_KERNARG=1
export HSA_OVERRIDE_CPU_AFFINITY_DEBUG=0
```

- `HIP_FORCE_DEV_KERNARG=1`: Places HIP kernel arguments directly into device memory to reduce latency (default as of ROCm 6.2)
- `HSA_OVERRIDE_CPU_AFFINITY_DEBUG=0`: Prevents internal ROCm threads from having CPU core affinity to all available cores

### Making Variables Permanent

To make these environment variables permanent, add them to `/etc/environment`:

```bash
echo "export HIP_FORCE_DEV_KERNARG=1" | sudo tee -a /etc/environment
echo "export HSA_OVERRIDE_CPU_AFFINITY_DEBUG=0" | sudo tee -a /etc/environment
```

## IOMMU Configuration for Large Systems

For systems with 256 logical CPU cores or more, setting IOMMU to `disabled` in the BIOS can limit the available logical cores to 255. The reason is that the Linux kernel disables X2APIC in this case and falls back to the Advanced Programmable Interrupt Controller (APIC), which can only enumerate a maximum of 255 logical cores.

If SMT is enabled (`CCD/Core/Thread Enablement > SMT Control` set to `enable`), apply the following steps to expose all logical cores:

1. In the server BIOS, set IOMMU to **Enabled**.
2. Add `iommu=pt` to `GRUB_CMDLINE_LINUX` in `/etc/default/grub`.
3. Update GRUB and reboot.
4. Verify IOMMU passthrough mode:

   ```bash
   dmesg | grep iommu
   ```

   Expected output includes:

   ```text
   [    0.000000] Kernel command line: [...] iommu=pt
   ```

```{note}
This kernel setting requires IOMMU to be enabled in the system BIOS. Refer to the [BIOS Settings](bios-settings.md) guide for details.
```

## CPU Power Management

### Kernel Settings

- `processor.max_cstate=0` can be used to limit the CPU to its active state for better responsiveness.

## File System Tuning

### /proc and /sys File System Settings

- NUMA auto-balancing can be controlled via `/proc/sys/kernel/numa_balancing`
- Various kernel parameters can be tuned through `/proc` and `/sys` interfaces

## Common Commands for Verification

```bash
# Verify kernel parameters
cat /proc/cmdline

# Check NUMA status
cat /proc/sys/kernel/numa_balancing

# Verify IOMMU configuration
dmesg | grep iommu

# Disable C2 state if needed
cpupower idle-set -d 2

# Check current C-state settings
cpupower idle-info
```

```{warning}
Always test OS tuning changes in controlled environments before applying to production systems
```
