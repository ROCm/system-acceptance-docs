# OS Tuning

This section describes the operating system tuning parameters including C-states, NUMA configuration, and environment variables common to all AMD Instinct GPU models.

## Overview

Operating system tuning is essential for achieving optimal performance with AMD Instinct accelerators. This section covers C-states configuration, NUMA optimization, kernel parameters, and environment variables that should be applied to all AMD Instinct GPU systems.

For all BIOS-level optimizations that complement these OS settings, refer to the [BIOS Settings](bios-settings.md) guide.

## C-states Configuration

### C-state Definitions

- **C0**: Active state while running an application
- **C1**: Idle state with minimal latency to return to active
- **C2**: Deeper sleep state with greater latency when returning to active

### Linux Configuration

If C-states must be enabled in BIOS, it's recommended to disable the C2 state to reduce latency, which is particularly important for high-performance networking.

```bash
# Install cpupower tool
sudo apt install linux-tools-common

# Disable power-gating on all cores (disable C2 state)
cpupower idle-set -d 2
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

For systems with 256 logical CPU cores or more, configure the kernel for IOMMU passthrough mode:

1. **Kernel Parameters**: Add `iommu=pt` to GRUB arguments
2. **Apply Changes**: Update GRUB and reboot
3. **Verification**: Check with `dmesg | grep iommu`

> **Note**: This kernel setting requires IOMMU to be enabled in the system BIOS. Refer to the [BIOS Settings](bios-settings.md) guide for details.

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
