# Firmware Updates

This page explains the supported ways to update firmware on AMD Instinct GPU systems and points you to the right OEM documentation for anything device-specific. For AMD Instinct accelerators, “firmware” comes in two forms:

- GPU runtime firmware blobs (microcode) that the AMDGPU kernel driver loads at boot from `/lib/firmware/amdgpu`. These are publicly distributed via your Linux distribution’s `linux-firmware` package and/or AMD’s official software repositories. Updating these packages and rebooting is the standard, supported way to update GPU firmware.
- Board VBIOS, platform PLDM bundle components, or other device-level firmware. When an update is required, it is provided through your server OEM’s update mechanisms (Dell, HPE, Lenovo, Supermicro, etc.). Always use the OEMs recommended tools and only updates posted—and qualified—for your exact GPU model.

AMD publishes a hardware / driver / firmware dependency matrix in the ROCm release notes. Always consult the latest matrix when planning upgrades: [ROCm Release Notes](https://rocm.docs.amd.com/en/latest/about/release-notes.html).

## Firmware Update Instructions

### GPU runtime firmware

What it is: Signed firmware files under `/lib/firmware/amdgpu` that the AMDGPU kernel driver loads during boot. These get updated regularly and are the canonical path for GPU firmware updates on Instinct.

How to update:

- RHEL/CentOS/Rocky/Alma
  - Update the OS firmware package: sudo dnf update linux-firmware
  - If you use AMD’s AMDGPU/ROCm packages, updating the kernel driver stack from AMD’s repo may also update the firmware; reboot to take effect.
- Ubuntu/Debian
  - Update the OS firmware package: sudo apt-get update && sudo apt-get install --only-upgrade linux-firmware
  - If you install or upgrade AMDGPU/ROCm from AMD’s repositories, a reboot is required after the driver upgrade.

References:

- linux-firmware upstream repository (reference): [https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/about/](https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/about/)
- AMD SMI (device/driver info): [https://rocm.docs.amd.com/projects/amdsmi/en/latest/](https://rocm.docs.amd.com/projects/amdsmi/en/latest/)

### OEM-provided firmware

What it is: Server vendors publish GPU or platform firmware (for example, VBIOS or bundled PLDM components) to enable platform features or address specific issues. For Instinct, these are applied using the server’s management tools and must align with the versions listed in the ROCm release notes matrix.

Where to find firmware:

- Dell Technologies
  - iDRAC/Lifecycle Controller User’s Guide (firmware update methods, DUP packages): [https://www.dell.com/support/manuals/en-us/oth-r750xs/idrac9_7.xx_ug/firmware-version-7107000](https://www.dell.com/support/manuals/en-us/oth-r750xs/idrac9_7.xx_ug/firmware-version-7107000)
- HPE
  - iLO 5 User Guide and firmware update workflow (SPP/OneView/iLO): [https://support.hpe.com/hpesc/public/docDisplay?docId=a00105236en_us](https://support.hpe.com/hpesc/public/docDisplay?docId=a00105236en_us)
- Lenovo
  - XClarity Essentials UpdateXpress User Guide: [https://pubs.lenovo.com/lxce-ux/ux_book.pdf](https://pubs.lenovo.com/lxce-ux/ux_book.pdf)
- Supermicro
  - Supermicro Update Manager (SUM) and management tools: [https://www.supermicro.com/en/support/resources/downloadcenter/smsdownload](https://www.supermicro.com/en/support/resources/downloadcenter/smsdownload)

Recommendations:

- Only use OEM-posted GPU firmware for your exact server model and GPU option part number.
- If no GPU firmware is posted for your platform, do not attempt to flash anything—contact your OEM or AMD support.

## Other platform firmware (BIOS/UEFI, BMC, NICs, switches, PCIe switches)

For BIOS/UEFI and BMC firmware, always use your server manufacturer’s documented process and validated packages. See the OEM links above for update procedures (iDRAC/Lifecycle Controller for Dell, iLO/OneView/SPP for HPE, XClarity for Lenovo, SUM/Redfish for Supermicro). For recommended settings, refer to the [BIOS Settings](bios-settings.md) guide in this documentation and then apply them using the OEM tool of record.

### Network adapter (NIC) firmware

- NVIDIA/Mellanox adapters: Use NVIDIA Firmware Tools (MFT) and mlxup as documented by NVIDIA. Follow the vendor’s release notes for your exact adapter and OS.
  - NVIDIA Firmware Tools (MFT) documentation: [https://docs.nvidia.com/networking/display/nvidia-firmware-tools-mft-documentation-v4-32-0.0.pdf](https://docs.nvidia.com/networking/display/nvidia-firmware-tools-mft-documentation-v4-32-0.0.pdf)
  - mlxup/MFT download page: [https://network.nvidia.com/support/firmware/mlxup-mft/](https://network.nvidia.com/support/firmware/mlxup-mft/)
- Other NIC vendors: Use the vendor’s official utilities and follow their platform-specific documentation.

### PCIe switch firmware

PCIe switch firmware (e.g., Broadcom/PLX) is platform-specific and typically serviced through the server OEM. Do not attempt to update PCIe switch firmware unless instructed by the OEM with an official package and procedure.

## Minimal verification after updates

- Verify kernel firmware loads: `sudo dmesg | grep amdgpu`
- Confirm ROCm version: `amd-smi version`
- Confirm GPU health: `amd-smi list` and/or `amd-smi monitor`
- Confirm system / BIOS identifiers (when validating against release notes matrix):
  - `sudo dmidecode -s system-product-name`
  - `sudo dmidecode -s bios-version`

## Cluster deployment considerations

- Firmware and config consistency: Keep BIOS/BMC/GPU runtime firmware and system configuration consistent across nodes.
- Use a rolling strategy to minimize downtime.
- Validate each node individually, then perform cluster-level checks.
