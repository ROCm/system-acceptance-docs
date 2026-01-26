# Kernel Parameters

This section describes the GRUB and kernel parameter settings common to all AMD Instinct GPU models.

## Overview

Configuring the correct kernel command-line parameters is essential for stable operation and optimal performance of AMD Instinct™-based systems. These parameters are set using GRUB (GNU Grand Unified Bootloader), which controls how the Linux kernel initializes hardware during system startup. This section outlines the required and recommended kernel boot parameters to be appended in the GRUB configuration file (typically `/etc/default/grub`) required by AMD Instinct-based servers.

## GRUB Configuration Steps

The following steps are for Ubuntu-based systems:

1. Open `/etc/default/grub` with root privileges.
2. Locate the line starting with `GRUB_CMDLINE_LINUX`.
3. Append all required and recommended parameters to this line.
4. Save the file and apply changes:

   ```bash
   sudo update-grub
   ```

5. Reboot the system for changes to take effect.
6. Verify the active kernel parameters:

   ```bash
   cat /proc/cmdline
   ```

```{note}
For RHEL-based systems, use the grubby tool instead of editing GRUB directly:

    sudo grubby --update-kernel=ALL --args="pci=bfsort pci=realloc=off iommu=pt numa_balancing=disable modprobe.blacklist=amdgpu"
```

## Kernel Parameters

### Required Kernel Parameters

| Parameter | Comments |
|---|---|
| `pci=realloc=off` | Disables automatic reallocation of PCI resources, enabling Linux to clearly detect all GPUs in Instinct™-based systems. This setting is useful when Single Root I/O Virtualization (SR-IOV) Base Address Registers (BARs) have not been allocated by the BIOS, helping to avoid potential hardware configuration issues. |
| `pci=bfsort` | Forces the kernel to enumerate all devices on a bus in a breadth-first manner before proceeding to the next bus. This ensures predictable device ordering, important for devices with persistent naming schemes such as network interfaces, and results in improved performance. Using this parameter prevents accessing an unintended GPU over the network. |
| `iommu=pt` | Enables IOMMU pass-through mode, which allows the adapter to bypass DMA translation to memory, thereby improving performance. IOMMU is a system-specific IO mapping useful for DMA mapping and isolation, particularly in virtualization and device assignments to virtual machines. It is recommended to enable IOMMU support. |
| `intel_iommu=on` | Necessary for systems with Intel host CPUs; not required for systems with AMD CPUs. |
| `numa_balancing=disable` | **Optional.** NUMA balancing allows the OS to scan memory and attempt to migrate to a DIMM logically closer to accessing cores. While beneficial in some scenarios, it adds overhead because the OS is only estimating NUMA allocations, which may be useful if the NUMA locality access is not ideal. |
| `modprobe.blacklist=amdgpu` | **Optional.** For some system configurations, it is necessary to blacklist the amdgpu driver to prevent instances where the DCGPU may not be ready when the driver loads, or if the system BIOS settings are not optimally configured. If this parameter is used, the amdgpu driver must be loaded post-boot for the system to function properly. Alternatively, configuring the AMD DCGPU with recommended system-optimized BIOS settings might make it possible to remove driver blacklisting. However, blacklisting the driver is considered the safest option since the AMD DCGPU may not be ready during system boot if a firmware update is in progress. |

```{note}
If `modprobe.blacklist=amdgpu` is used, the amdgpu module must be loaded after booting:

    sudo modprobe amdgpu

For deployment, adding a sysctl task to load the amdgpu driver immediately after boot is recommended.
```

### Optional Kernel Parameters

Depending on your specific environment and workload requirements, additional kernel command line parameters can further enhance performance and system responsiveness. The table below lists optional GRUB settings to consider for AMD Instinct implementations. Evaluate and apply those that best fit your deployment scenario.

| Parameter | Comments |
|---|---|
| `nokaslr` | Disables KASLR (Kernel Address Space Layout Randomization) to reduce boot time and increase cache locality. |
| `norandmaps` | Disables random memory allocation, which increases performance, but can reduce system security. Not recommended for systems with multiple users without virtualization safety restrictions. |
| `mitigations=off` | Disables many security features, resulting in an increase in performance in some scenarios. |
| `pcie_aspm=off` | Disables ASPM power management at the cost of slightly higher power usage from the PCIe bus. This setting is highly recommended when prioritizing performance. |
| `processor.max_cstate=0` | Limits the CPU to the active state, making the CPU more responsive. This setting is highly recommended when prioritizing performance. |
| `biosdevname=0` | Disables predictable system devices naming. This decreases boot time and has minimal performance increase. |
| `quiet` | Reduces the number of messages logged to dmesg to only the critical messages. |
| `transparent_hugepage=always` | Allows applications to automatically allocate huge (2MB) memory pages without application changes. This allows for faster memory allocation and easier memory management at the cost of increased RAM usage. This feature may reduce performance if RAM is constrained. |
| `tsc=nowatchdog` | The kernel stops periodically checking TSC accuracy, reducing background activity and optimizing performance. |
| `nmi_watchdog=0` | Disables the NMI watchdog that detects hard lockups. Disabling this improves high-performance and low-latency workloads. |
| `nowatchdog` | Disables the kernel's soft and hard lockup watchdog timers, which are normally used to detect and recover from CPU hangs. While this can slightly improve performance by reducing monitoring overhead, it removes a key safeguard against system lockups, making debugging and stability tracking more difficult. |
