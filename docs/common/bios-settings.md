# BIOS Settings

This section describes the system BIOS configuration settings common to all AMD Instinct GPU models.

## Overview

Some server manufacturers offer tools that allow the current BIOS configuration settings to be exported to a file, modified with needed changes, and loaded back to the system. If the server manufacturer doesn't offer such a tool, the BIOS settings will need to be reviewed and updated manually from the BIOS setup interface before booting the OS.

## Recommended BIOS Settings

For systems with AMD EPYC™ processors, refer to the recommended system BIOS settings for the specific GPU model to ensure the system BIOS is set up correctly for maximum performance. These settings should be set as default values in the system BIOS. Analogous settings for other non-AMI System BIOS providers could be set similarly.

### AMD EPYC BIOS Configuration

The following BIOS settings are recommended for optimal performance with AMD Instinct accelerators. Use this table as a reference to configure each BIOS setting for systems with AMD EPYC™ 9004-series processors and AMI System BIOS to maximize system performance.

```{note}
The BIOS settings and location given in the following table may vary by hardware and BIOS vendor; consult your system's documentation for details.
```

```{note}
For systems with Intel processors, some settings might not apply or may be unavailable.
```

| **BIOS setting location** | **Parameter** | **Value** | **Comments** |
| --- | --- | --- | --- |
| Advanced / Power Management | Power Management | Maximum Performance | Optimizes power delivery for GPU workloads. |
| Advanced / CPU Configuration | SVM Mode | Enabled | Required for GPU virtualization features. |
| Advanced / PCI subsystem settings | Above 4G decoding | Enabled | GPU large BAR support. |
| Advanced / PCI subsystem settings | SR-IOV support | Enabled | Enable single root IO virtualization. |
| Advanced / PCI subsystem settings | PCIe ASPM | Disabled | Prevents PCIe link power state changes during operation. L1 and L2 states should be disabled. |
| Advanced / PCI subsystem settings | PCIe Generation | Gen 5 enabled | Ensures maximum PCIe bandwidth for GPU performance. |
| Advanced / PCI subsystem settings | PCIe Bifurcation | As required | Configure based on GPU installation requirements. |
| AMD CBS / GPU common options | Global C-state control | Auto | Global C-states – do not disable this menu item. For performance, specific C-States are disabled below. |
| AMD CBS / GPU common options | CCD/Core/Thread enablement | Accept | May be necessary to enable the SMT control menu. |
| AMD CBS / GPU common options / performance | SMT control | Disable | Set to Auto if the primary application is not compute-bound. |
| AMD CBS / DF common options / memory addressing | NUMA nodes per socket | Auto | Auto = NPS1. At this time, the other options for NUMA nodes per socket should not be used. This is subject to change. **A value of 0 (NPS0) is not allowed.** |
| AMD CBS / DF common options / memory addressing | Memory interleaving | Auto | Depends on NUMA nodes (NPS) setting. **Required.** |
| AMD CBS / DF common options / link | 4-link xGMI max speed | 32 Gbps | Auto results in the speed being set to the lower of the max speed the motherboard is designed to support and the max speed of the CPU in use. |
| AMD CBS / NBIO common options | IOMMU | Enabled | Used for GPU passthrough and virtualization. **Required.** |
| AMD CBS / NBIO common options | PCIe ten bit tag support | Auto | **Required** |
| AMD CBS / NBIO common options / SMU common options | Determinism control | Manual |  |
| AMD CBS / NBIO common options / SMU common options | Determinism slider | Power |  |
| AMD CBS / NBIO common options / SMU common options | cTDP control | Manual | Set cTDP to the maximum supported by the installed CPU. |
| AMD CBS / NBIO common options / SMU common options | cTDP | Varies by CPU, see comment | Value in watts. Set this to the maximum TDP value supported by the CPU. |
| AMD CBS / NBIO common options / SMU common options | Package power limit control | Manual | Set package power limit to the maximum supported by the installed CPU. |
| AMD CBS / NBIO common options / SMU common options | Package power limit | Varies by CPU, see comment | Value in watts. Set this to the maximum TDP value supported by the CPU. |
| AMD CBS / NBIO common options / SMU common options | xGMI link width control | Manual | Set package power limit to the maximum supported by the installed CPU. |
| AMD CBS / NBIO common options / SMU common options | xGMI force width control | Force |  |
| AMD CBS / NBIO common options / SMU common options | xGMI force link width | 2 | 0: Force xGMI link width to x2  1: Force xGMI link width to x8  2: Force xGMI link width to x16 |
| AMD CBS / NBIO common options / SMU common options | xGMI max speed | Auto | Auto results in the speed being set to the lower of the max speed the motherboard is designed to support and the max speed of the CPU in use. |
| AMD CBS / NBIO common options / SMU common options | APBDIS | 1 | Disables Data Fabric (DF) P-states, contributing to a high-performance power profile. |
| AMD CBS / NBIO common options / SMU common options | DF C-states | Disabled | DF C-states should be disabled to reduce latency unless a power reduction is needed. This is a key C-State setting for performance. |
| AMD CBS / NBIO common options / SMU common options | Fixed SOC P-state | P0 | Sets the System-on-Chip to its highest performance state (P0), ensuring optimal GPU-CPU interaction. |
| AMD CBS / security | TSME | Disabled | Memory encryption. |

```{warning}
Always record existing production system settings before making changes to allow the system to be returned to the original configuration.
```
