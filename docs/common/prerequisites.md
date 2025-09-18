# Prerequisites

This section describes the system prerequisites and requirements common to all AMD Instinct GPU models.

## System Requirements

Before proceeding with the prerequisites in this section, ensure that the system has been properly installed and is free of visible damage. As the system administrator, refer to the manufacturer's installation guide to verify that the system is correctly installed in a rack with sufficient cooling, is connected to the required power, and is accessible from the network.

If errors or warnings are found during setup, you might need to troubleshoot the issue by, for example, reseating auxiliary PCBs, checking internal cable connections, or monitoring the situation. For debugging support, contact your system manufacturer.

## Prerequisite Areas

This section covers the following configuration areas:

- [Supported Operating Systems](#supported-operating-systems)
- [BIOS Settings](bios-settings.md)
- [Kernel Parameters](kernel-parameters.md)
- [OS Tuning](os-tuning.md)
- [Firmware Updates](firmware-updates.md)
- [System setup](system-setup.md)

## Supported Operating Systems

For the most up-to-date information on supported operating systems and distributions, please refer to the official ROCm documentation:

[ROCm System Requirements - Supported Distributions](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html#supported-distributions)

**Note**: This external resource is always the most current and authoritative source for OS compatibility information.

To obtain and validate the Linux distribution information for systems with the OS already installed, refer to the [ROCm installation prerequisites](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/prerequisites.html).

### System Requirements

- **CPU**: AMD EPYC™ 9004-series or later processors recommended
- **Memory**: Refer to the [table below](#system-memory-requirements) for specific model recommendations
- **Storage**: Minimum 1TB free space for operating system and data
- **Network**: High-speed networking (100GbE recommended for multi-GPU configurations)
- **Cooling**: Datacenter-grade cooling solution with sufficient airflow

### Hardware Configuration

For optimal performance with AMD Instinct accelerators, systems should be configured according to the following guidelines:

#### Expected GPU Configuration

A typical AMD Instinct GPU-based server should have:

- **GPU Count**: 8x GPU accelerators (standard configuration)
- **Processors**: Dual-socket AMD EPYC 9004-series processors
- **Cooling**: Proper cooling and power infrastructure
- **Network**: High-speed connectivity (100-400 GbE or InfiniBand)

#### System Memory Requirements

The recommended minimum system memory for AMD Instinct products is as follows:

| Product | Minimum System Memory (TB) |
|---|---|
| MI300X | 2.0 |
| MI308X | 2.0 |
| MI325X | 2.5 |
| MI350X | 3.0 |
| MI355X | 3.0 |

> **Note**: System memory requirements scale with GPU count and workload complexity. Systems with larger memory configurations provide better performance for memory-intensive AI and HPC workloads.

## Configuration Workflow

1. **System Installation**: Install a [supported operating system](#supported-operating-systems)
2. **BIOS Configuration**: Apply recommended [BIOS settings](bios-settings.md)
3. **Firmware Updates**: Update system firmware per [firmware guidance](firmware-updates.md)
4. **Kernel Parameters**: Configure GRUB and kernel parameters as described in [kernel parameters](kernel-parameters.md)
5. **System Setup**: Install GPU driver and ROCm toolkit instructions in [System setup](system-setup.md)
6. **OS Tuning**: Apply operating system optimizations from [OS tuning](os-tuning.md)
7. **Validation**: Run [health checks](health-checks.md) and perform [system validation tests](system-validation.md)

```{note}
Before changing any system settings and testing, record existing production system settings to allow the system to be returned to the original settings.
```

```{warning}
Ensure all firmware and software versions are compatible with your specific GPU model. Contact your system manufacturer support representative to verify compatibility.
```
