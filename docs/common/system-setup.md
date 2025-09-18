# System Setup

This section provides high-level guidance for preparing, installing, and validating the ROCm software stack on AMD Instinct GPU systems.
Always follow the official ROCm installation documentation for current version requirements, supported distributions, and repository configuration.

**ROCm Quick Start:** [https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html](https://rocm.docs.amd.com/projects/install-on-linux/en/latest/install/quick-start.html)

```{note}
[ROCm docs](https://rocm.docs.amd.com) is the single source of truth for supported versions, distribution compatibility, and required dependencies for the ROCm toolkit.
```

## Instinct Driver

Beginning with ROCm 7.0, the Instinct driver release cycle is decoupled from the ROCm toolset.

**Instinct driver documentation:** [https://instinct.docs.amd.com/projects/amdgpu-docs/en/latest/index.html](https://instinct.docs.amd.com/projects/amdgpu-docs/en/latest/index.html)

## Post-Installation Verification

Basic checks (consult ROCm docs for expanded diagnostics):

```bash
# Confirm ROCm version file exists
cat /opt/rocm/.info/version

# Validate installed version
amd-smi --version
```
