# NIC Driver and Supporting Software Installation

This section provides detailed, vendor-specific guidance for installing and configuring the NIC drivers and supporting software. Refer to the appropriate NIC you are using. Before proceeding, ensure that you reference the appropriate documentation for your NIC model and verify all system prerequisites and dependencies are fulfilled. Proper installation and configuration of these components is essential to achieve optimal throughput, low latency, and reliable operation across your cluster.

## AMD Pensando™ Pollara 400 AI NIC

An overview of the driver and software installation steps for the AMD Pensando™ Pollara 400 AI-NIC are given below. However, complete details are given in the following document:

* [AMD Pensando Pollara Series Installation Guide (UG1716)](https://docs.amd.com/r/en-US/ug1716-pollara-series-installation-guide)
* [AMD Pensando Pollara Series User Guide (UG1717)](https://docs.amd.com/r/en-US/ug1717-pollara-series-user-guide)

The firmware and software bundles are available on the AMD Pensando Customer Portal at [pensandosupport.amd.com](https://pensandosupport.amd.com/). Additional information and documentation can be obtained by registering on the Pollara registration page at [account.amd.com/en/forms/registration/tip/tip-pollara-pulsar.html](https://account.amd.com/en/forms/registration/tip/tip-pollara-pulsar.html).

### Prerequisites

Root access is required for all software and firmware installations. Install host software that is listed in the [AMD Pensando POLLARA Series Installation Guide (UG1716)](https://docs.amd.com/r/en-US/ug1716-pollara-series-installation-guide)

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

## NVIDIA Mellanox CX-7 400Gx1

Install ROCm first, and then UCX, and the NVIDIA Mellanox driver last.

```{note}
Ensure that the installation steps are performed in this order.
```

```bash
sudo apt install gcc-gfortran lsof tk tcl createrepo kernel-rpm-macros perl-sigtrap libtool

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
