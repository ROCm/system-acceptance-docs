# NIC Driver and Supporting Software Installation

This section provides detailed, vendor-specific guidance for installing and configuring the NIC drivers and supporting software. Refer to the appropriate NIC you are using. Before proceeding, ensure that you reference the appropriate documentation for your NIC model and verify all system prerequisites and dependencies are fulfilled. Proper installation and configuration of these components is essential to achieve optimal throughput, low latency, and reliable operation across your cluster.

## AMD Pensando™ Pollara 400 AI NIC

An overview of the driver and software installation steps for the AMD Pensando™ Pollara 400 AI-NIC are given below. However, complete details are given in the following document:

* [AMD AI NIC Pollara 400 Adapter Operations and Troubleshooting User Guide (UG1801)](https://docs.amd.com/r/en-US/ug1801-ai-nic-pollara-400-ops-guide/)

The firmware and software bundles are available on the AMD Pensando Customer Portal at [pensandosupport.amd.com](https://pensandosupport.amd.com/). Additional information and documentation can be obtained by registering on the Pollara registration page at [account.amd.com/en/forms/registration/tip/tip-pollara-pulsar.html](https://account.amd.com/en/forms/registration/tip/tip-pollara-pulsar.html).

### Prerequisites

Root access is required for all software and firmware installations. Install host software that is listed in the [AMD Pensando POLLARA Series Installation Guide (UG1716)](https://docs.amd.com/r/en-US/ug1716-pollara-series-installation-guide).

The Pensando Pollara NIC supports features such as live firmware updates and profile updates, which trigger a PCI reset of the device. If **PCI AER (Advanced Error Reporting) Capability** is enabled in the BIOS, the operating system must be able to handle the resulting link-down notification. If the server does not properly handle this event, please disable PCI AER Capability in the BIOS. Additionally, **Hot Plug support must be enabled** in the BIOS to use profile updates and other reset-related features

#### Download Software

Download and Extract the Software and Driver:

1. Download and unpack the software bundle.
   1. The firmware directory contains the software image for the NIC cards.
   2. `host_sw_pkg.tar.gz` contains the host tools and ionic driver.
2. Extract the host tools and driver package:

   ```bash
   tar -xzvf host_sw_pkg.tar.gz
   ```

#### Install Driver

Install the Driver and Tools:

Install the ionic driver and host utilities, such as nicctl, used to manage AI-NIC cards.

1. Change directory to host_sw_pkg and run the installation script:

   ```bash
   cd /home/user/ainic_bundle/host_sw_pkg
   ./install.sh
   ```

#### Update Firmware

Prerequisite: Driver & Tools version needs to match the firmware version.

1. After installing the driver and tools, install the firmware using the ainic_fw_salina.tar file in the top level of the folder.
2. Use `nicctl` tool to update the firmware. You can update one or all of the cards using the respective command below where `card_uuid` is the unique identifier assigned to a NIC card in the system. If you do not specify a card, all cards will be upgraded by default. To display all the card uuids in the system run the following command:

   ```bash
   # Display the card uuids in the system
   nicctl show card

   # Single card update
   nicctl update firmware -i ainic_fw_salina.tar -c <card_uuid>

   # All cards update
   nicctl update firmware -i ainic_fw_salina.tar
   ```

3. Once the cards are upgraded, reset the card to complete the process and boot to the new firmware version. Reset one or all cards using the respective command:

   ```bash
   # Single card reset
   nicctl reset card -c <card_uuid>

   # or reset all cards
   nicctl reset card –all
   ```

Firmware and software updates are complete.

#### Performance Optimizations

For optimal cluster performance with the Pensando Pollara AI NIC, follow the setup procedures outlined in the [Pollara 400 Configuration and Benchmarking Guide](https://docs.amd.com/v/u/en-US/ug1813-pollara-400-benchmarking-guide).

Ensure that **Priority Flow Control (PFC)** is enabled and that **Dynamic Congestion Notification Control (DCQCN)** and **Quality of Service (QoS)** are correctly configured. These settings are critical for achieving maximum data throughput and minimizing latency in AI workloads. Please see the scripts provided in the Pollara 400 Configuration and Benchmarking Guide. Exact settings in scripts will need to be modified.

Example configuration commands:

```bash
# Enable RDMA on supporting devices
$ niccli_rdma_config.sh

# Enable relaxed ordering
$ niccli_ro_config.sh

# Disable speeds less than 400G
$ niccli_speedmask.sh

# Disable an unused port (replace <index> with the appropriate port index)
$ niccli -i <index> link --port_state --set --port_state_param=down
```

```{note}
Configuration settings will not persist through a system power cycle. Reapply all required parameters after each reboot to maintain proper operation. For persistent settings please see the guide to personas at [https://docs.amd.com/r/en-US/ug1717-ai-nic-pollara-400-user-guide/AI-NICPersonas](https://docs.amd.com/r/en-US/ug1717-ai-nic-pollara-400-user-guide/AI-NICPersonas)
```

## Broadcom 400G Network Adapter

For detailed guidance on updating firmware, drivers, and configuring Broadcom network adapters for optimal performance, refer to the [Broadcom Tech Docs Portal](https://techdocs.broadcom.com/). The [Broadcom Ethernet Network Adapter User Guide](https://techdocs.broadcom.com/content/dam/broadcom/techdocs/us/en/pdf/data-center-solutions/netxtreme/EtherNIC-Ctrl-UG2XX.pdf) is a recommended starting point.

To ensure your AI network cluster is configured for maximum efficiency, it is strongly advised to collaborate with Broadcom support personnel during setup and tuning.

For Broadcom 400G NICs, perform the following actions to guarantee proper operation and peak performance:

* Enable PCIe relaxed ordering.
* Enable RDMA support.
* Select the RoCE performance profile.
* Exclude all speeds except 400G from the speed mask.
* Disable unused ports to optimize resources.

Example configuration commands:

```bash
# Enable RDMA on supporting devices
$ niccli_rdma_config.sh

# Enable relaxed ordering
$ niccli_ro_config.sh

# Disable speeds less than 400G
$ niccli_speedmask.sh

# Set the performance profile to RoCE (Broadcom exclusive feature)
$ niccli_set_profile.sh

# Disable an unused port (replace <index> with the appropriate port index)
$ niccli -i <index> link --port_state --set --port_state_param=down
```

For detailed configuration, use the scripts provided in the cluster networking GitHub repository.

## NVIDIA Mellanox CX-7 400Gx1

To prevent library incompatibilities that could disrupt system operations, it is necessary to follow the specific installation order:

1. ROCm Installation: The ROCm driver must be installed first, because it sets up essential components and libraries that may otherwise conflict with the versions installed by other drivers.
2. Mellanox Driver Installation: The Mellanox driver should be installed before the UCX library because it installs an older version of the UCX library. **If UCX was installed previously, please uninstall UCX before installing the Mellanox driver.**
3. UCX Library Update: Since the Mellanox driver packages an outdated UCX library version, updating the UCX library after completing the Mellanox installation ensures that you are working with the latest features and fixes, thereby maintaining system stability and performance.

```{note}
Ensure that the installation steps are performed in this order.
```

```bash
sudo apt install lsof tk tcl libtool

# Example link is subject to change,
# see https://network.nvidia.com/products/infiniband-drivers/linux/mlnx_ofed/
wget https://content.mellanox.com/ofed/MLNX_OFED-24.10-2.1.8.0/MLNX_OFED_LINUX-24.10-2.1.8.0-ubuntu22.04-x86_64.iso

sudo mkdir -p /mnt/mlnx
sudo mount ./MLNX_OFED_LINUX-24.10-2.1.8.0-ubuntu22.04-x86_64.iso /mnt/mlnx
cd /mnt/mlnx
sudo ./mlnxofedinstall --add-kernel-support
sudo dracut -f

# Before we reboot, edit ulimit by appending to /etc/security/limits.conf
sudo echo “* soft nofile 1048576” >> /etc/security/limits.conf
sudo echo “* hard nofile 1048576” >> /etc/security/limits.conf
sudo echo “* soft memlock unlimited” >> /etc/security/limits.conf
sudo echo “* hard memlock unlimited” >> /etc/security/limits.conf
sudo reboot
```

### MLX Config

```bash
# Need to first run "sudo mst start"
sudo mst start

# then this for loop can queue their current settings:
for MLX in $(lspci -d 15b3:1021 -D | cut -d' ' -f1); do
sudo mlxconfig -y -d ${MLX} q | grep P2P_ORDERING_MODE
sudo mlxconfig -y -d ${MLX} q | grep RDMA_SELECTIVE_REPEAT_EN
sudo mlxconfig -y -d ${MLX} q | grep PCI_WR_ORDERING
sudo mlxconfig -y -d ${MLX} q | grep ATS_ENABLED
done

# and this for loop sets them:
for MLX in $(lspci -d 15b3:1021 -D | cut -d' ' -f1); do
sudo mlxconfig -y -d ${MLX} set P2P_ORDERING_MODE=1
sudo mlxconfig -y -d ${MLX} set RDMA_SELECTIVE_REPEAT_EN=1
sudo mlxconfig -y -d ${MLX} set PCI_WR_ORDERING=1
sudo mlxconfig -y -d ${MLX} set ATS_ENABLED=1
done
```

### Tuning

```bash
sudo su -
echo "net.ipv4.conf.all.arp_ignore=2" >> /etc/sysctl.conf
echo "net.ipv4.conf.all.arp_announce=1" >> /etc/sysctl.conf
echo "net.ipv4.conf.all.rp_filter=2" >> /etc/sysctl.conf
exit
```

### PFC Enable

Set the following script to run every boot to enable PFC.

```bash
#!/usr/bin/bash
for iface in $(rdma link | awk '{print $NF}'); do
sudo mlnx_qos -i $iface --pfc=0,0,0,1,0,0,0,0 # enable PFC on RoCE V2 packets -- priority 3 (TC 3)
sudo mlnx_qos -i $iface --dscp2prio='set,26,3' # set dscp for RoCE V2 packets -- prority 3 (TC 3)
sudo mlnx_qos -i $iface --dscp2prio='set,48,7' # set scp for CNP packets -- priority 7 (TC 7)
done
```
