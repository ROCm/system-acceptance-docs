# BIOS Settings

This section describes the system BIOS configuration settings common to all AMD Instinct GPU models.

## Overview

Some server manufacturers offer tools that allow the current BIOS configuration settings to be exported to a file, modified with needed changes, and loaded back to the system. If the server manufacturer doesn't offer such a tool, the BIOS settings will need to be reviewed and updated manually from the BIOS setup interface before booting the OS.

## Recommended BIOS Settings

For systems with AMD EPYC™ processors, refer to the recommended system BIOS settings for the specific GPU model to ensure the system BIOS is set up correctly for maximum performance. These settings should be set as default values in the system BIOS. Analogous settings for other non-AMI System BIOS providers could be set similarly.

```{note}
The BIOS settings and location given in the following tables may vary by hardware and BIOS vendor; consult your system's documentation for details.
```

```{note}
For systems with Intel processors, some settings might not apply or may be unavailable.
```

### Required BIOS Settings

BIOS settings in the following table are universally required for the AMD Instinct MI3xx product line for proper operation.

| **BIOS setting location** | **Parameter** | **Value** | **Comments** |
| --- | --- | --- | --- |
| Advanced / PCI subsystem settings | Above 4G decoding | Enabled | GPU large BAR support. |
| AMD CBS / DF common options / memory addressing | NUMA nodes per socket | NPS1 | A value of NPS1 is suggested for the general use case, but some workloads may have performance improvements with values greater than 1. **A value of 0 (NPS0) is not allowed.** |
| AMD CBS / DF common options / memory addressing | Memory interleaving | Enabled |  |
| AMD CBS / NBIO common options | PCIe ten bit tag support | Enabled |  |
| AMD CBS / NBIO common options | PCIE ARI Enumeration | Enabled |  |
| AMD CBS / NBIO common options | PCIE ARI Support | Enabled |  |

### BIOS Settings for Virtualization

BIOS settings related to virtualization are required when virtualization features are in use. However, if virtualization is not needed, enabling these settings may reduce performance. Please refer to the tables below for the appropriate configuration for your specific application. For system shipments, AMD recommends using the configuration intended for the virtualization use case.

| **BIOS setting location** | **Parameter** | **Value** | **Comments** |
| --- | --- | --- | --- |
| Advanced / PCI subsystem settings | SR-IOV support | Enabled | Enable single root I/O virtualization. |
| Advanced / PCI subsystem settings | Resizable BAR Support | Enabled | Enabling Resizable BAR Support in the BIOS allows the CPU to access the entire GPU memory space, which is essential for efficiently handling multiple virtual functions. As a result, systems using virtualization or multiple GPU-based virtual functions can share resources more effectively, leading to better performance and responsiveness. Option may not be visible on all system BIOSes. |
| Advanced / CPU Configuration | SVM Mode | Enabled | Secure Virtual Machine feature of AMD processors. For Intel and ARM based CPUs please use the equivalent option. |
| AMD CBS / NBIO common options | IOMMU | Enabled |  |
| AMD CBS / NBIO common options | ACS | Enabled |  |

### BIOS Settings Without Virtualization

If virtualization is not required, the following settings may improve performance.

| **BIOS setting location** | **Parameter** | **Value** | **Comments** |
| --- | --- | --- | --- |
| Advanced / PCI subsystem settings | SR-IOV support | Disabled | Single root IO virtualization. **If this feature is disabled, then the kernel command-line must contain the `pci=realloc=off` parameter.** |
| Advanced / PCI subsystem settings | Resizable BAR Support | N/A | If virtualization is not used, please defer to the system manufacturer for suggested setting. |
| Advanced / CPU Configuration | SVM Mode | N/A | Secure Virtual Machine feature of AMD processors. For Intel and ARM based CPUs please use the equivalent option. If virtualization is not used, please defer to the system manufacturer for suggested setting. |
| AMD CBS / NBIO common options | IOMMU | See comment | This setting is workload-dependent. In some scenarios, performance may improve when it is disabled. However, for general use, **it is recommended to keep the feature enabled**, as certain applications require it. |
| AMD CBS / NBIO common options | ACS | Disabled |  |

### BIOS Settings for Optimal Performance

BIOS settings in the following table are the recommended settings for improved performance with the AMD Instinct MI3xx product line. However, these settings may not be optimal for all platforms or workloads.

| **BIOS setting location** | **Parameter** | **Value** | **Comments** |
| --- | --- | --- | --- |
| Advanced / Power Management | Power Management | Maximum Performance | Optimizes power delivery for GPU workloads. |
| Advanced / PCI subsystem settings | PCIe Generation | Gen 5 enabled | Ensures maximum PCIe bandwidth for GPU performance. |
| Advanced / PCI subsystem settings | PCIe Bifurcation | As required | Configure based on GPU installation requirements. |
| AMD CBS / GPU common options | Global C-state control | Enabled | Global C-states – do not disable this menu item. |
| AMD CBS / GPU common options | CCD/Core/Thread enablement | Accept | May be necessary to enable the SMT control menu. |
| AMD CBS / GPU common options / performance | SMT control | Disable | If the primary application is not compute-bound or if your workload benefits from hyperthreading, then set this to Auto. |
| AMD CBS / DF common options / link | 4-link xGMI max speed | 32 Gbps | Auto results in the speed being set to the lower of the max speed the motherboard is designed to support and the max speed of the CPU in use. |
| AMD CBS / NBIO common options | ASPM | Disable |  |
| AMD CBS / NBIO common options / SMU common options | Determinism control | Manual |  |
| AMD CBS / NBIO common options / SMU common options | Determinism slider | Power |  |
| AMD CBS / NBIO common options / SMU common options | cTDP control | Manual | Set cTDP to the maximum supported by the installed CPU. |
| AMD CBS / NBIO common options / SMU common options | cTDP | Varies by CPU, see comment | Value in watts. Set this to the maximum TDP value supported by the CPU. |
| AMD CBS / NBIO common options / SMU common options | Package power limit control | Manual | Set package power limit to the maximum supported by the installed CPU. |
| AMD CBS / NBIO common options / SMU common options | Package power limit | Varies by CPU, see comment | Value in watts. Set this to the maximum TDP value supported by the CPU. |
| AMD CBS / NBIO common options / SMU common options | xGMI link width control | Manual | Set package power limit to the maximum supported by the installed CPU. |
| AMD CBS / NBIO common options / SMU common options | xGMI force width control | Force |  |
| AMD CBS / NBIO common options / SMU common options | xGMI force link width | 2 | 0: Force xGMI link width to x2  1: Force xGMI link width to x8  2: Force xGMI link width to x16 |
| AMD CBS / NBIO common options / SMU common options | xGMI max speed | 32Gbps | Auto results in the speed being set to the lower of the max speed the motherboard is designed to support and the max speed of the CPU in use. |
| AMD CBS / NBIO common options / SMU common options | GMI Folding | Disabled | Disabling Global Memory Interconnect Folding ensures that all GMI communication links between GPUs remain active instead of being down-clocked or powered down to save energy. With all lanes enabled, the GPUs retain full interconnect bandwidth, which can improve multi-GPU communication performance, especially for workloads that are sensitive to inter-GPU bandwidth or latency. |
| AMD CBS / NBIO common options / SMU common options | APBDIS | 1 | Disables Data Fabric (DF) P-states, contributing to a high-performance power profile. |
| AMD CBS / NBIO common options / SMU common options | DF C-states | Disabled | DF C-states should be disabled to reduce latency unless a power reduction is needed. This is a key C-State setting for performance. |
| AMD CBS / NBIO common options / SMU common options | Fixed SOC P-state | P0 | Sets the System-on-Chip to its highest performance state (P0), ensuring optimal GPU-CPU interaction. |
| AMD CBS / security | TSME | Disabled | Memory encryption. |

```{warning}
Always record existing production system settings before making changes to allow the system to be returned to the original configuration.
```
