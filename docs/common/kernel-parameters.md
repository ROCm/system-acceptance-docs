# Kernel Parameters

This section describes the GRUB and kernel parameter settings common to all AMD Instinct GPU models.

## Overview

Configuring the correct kernel command-line parameters is essential for stable operation and optimal performance of AMD Instinct™-based systems. These parameters are set using GRUB (GNU Grand Unified Bootloader), which controls how the Linux kernel initializes hardware during system startup. This section outlines the required and recommended kernel boot parameters to be appended in the GRUB configuration file (typically `/etc/default/grub`) required by AMD Instinct-based servers.

## GRUB Configuration Steps

1. Open `/etc/default/grub` with root privileges.
2. Locate the line starting with `GRUB_CMDLINE_LINUX`.
3. Append all required and recommended parameters to this line.
4. Save the file and apply changes:

   ```bash
   sudo update-grub
   ```

5. For RHEL-based systems, use the grubby tool:

   ```bash
   sudo grubby --update-kernel=ALL --args="pci=realloc=off"
   ```

6. Reboot the system for changes to take effect.
7. Verify the active kernel parameters:

   ```bash
   cat /proc/cmdline
   ```

## Kernel Parameters

### Required Kernel Parameters

| Parameter | Comments |
|---|---|
| `pci=realloc=off` | With this setting Linux can unambiguously detect all GPUs of the Instinct™-based system because this setting disables the automatic reallocation of PCI resources. It is used when Single Root I/O Virtualization (SR-IOV) Base Address Registers (BARs) have not been allocated by the BIOS. This can help avoid potential issues with certain hardware configurations. |
| `pci=bfsort` | The `pci=bfsort` parameter forces the kernel to use a breadth-first approach, meaning it will enumerate all devices on a bus before moving to the next bus. This ensures predictable device ordering which is significant for devices with persistent naming schemes like network interfaces. This results in performance improvement. |
| `iommu=pt` | The `iommu=pt` setting enables IOMMU pass-through mode. When in pass-through mode, the adapter does not need to use DMA translation to the memory, which can improve performance.  IOMMU is a system specific IO mapping mechanism and can be used for DMA mapping and isolation. This can be beneficial for virtualization and device assignment to virtual machines. It is recommended to enable IOMMU support. |
| `intel_iommu=on` | For systems with Intel host CPUs, not needed for systems with AMD CPUs. |
| `numa_balancing=disable` | The NUMA balancing feature allows the OS to scan memory and attempt to migrate to a DIMM that is logically closer to the cores accessing it. This causes an overhead because the OS is only estimating NUMA allocations, which may be useful if the NUMA locality access is not ideal. |
| `modprobe.blacklist=amdgpu` | For some system configurations, the amdgpu driver needs to be blacklisted to avoid instances where the DCGPU may not be ready when the driver loads or if system BIOS settings have not been set optimally. For the system to be functional if this parameter is used, the amdgpu driver must be loaded after booting.  Alternatively, configuring the AMD DCGPU with recommended system optimized BIOS settings, it might be possible to remove blacklisting the driver. However, blacklisting the driver is considered the safest option since the AMD DCGPU may not be ready during system boot if a firmware update is in progress. |

``````{note}
If `modprobe.blacklist=amdgpu` is used, the amdgpu module must be loaded after booting:

```bash
sudo modprobe amdgpu
```

For deployment, adding a sysctl task to load the amdgpu driver immediately after boot is recommended.
``````

### Optional Kernel Parameters

| Parameter | Comments |
|---|---|
| `nokaslr` | Disables KASLR (Kernel Address Space Layout Randomization) which reduces boot time and increases cache locality. |
| `norandmaps` | Disable random memory allocation, which increases performance, but can reduce system security. Not recommended for systems with multiple users without virtualization safety restrictions. |
| `mitigations=off` | Disables many security features for a dramatic increase in performance in some cases |
| `pcie_aspm=off` | Disable ASPM power management at the cost of slightly more power usage from the PCIe bus. Strongly recommended. |
| `processor.max_cstate=0` | Limits CPU to active state for better responsiveness |
| `biosdevname=0` | Disables predictable system devices naming. This decreases boot time and has minimal performance increase. |
| `quiet` | Reduces the number of messages logged to dmesg to only the critical messages. |
| `transparent_hugepage=always` | Allows applications to automatically allocate huge (2MB) memory pages without application changes. This allows for faster memory allocation and easier memory management at the cost of increased RAM usage. This feature may reduce performance if RAM is constrained. |
| `tsc=nowatchdog` | The kernel stops periodically checking TSC accuracy, reducing background activity. |
| `nmi_watchdog=0` | Disables the NMI watchdog that detects hard lockups. Disabling this improves high-performance and low-latency workloads. |
