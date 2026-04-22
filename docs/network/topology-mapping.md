# Mapping NIC to GPU NUMA Node

For optimal cluster performance and minimal latency, it's essential to align each GPU with its nearest high-speed NIC—ideally on the same NUMA node and PCIe root complex. This ensures that data traveling to and from each GPU takes the shortest, most efficient path, which is especially critical for RDMA and high-throughput AI/HPC workloads. This section provides step-by-step instructions to map GPUs and NICs using PCIe tools and system commands, ensuring efficient data flow and minimal latency across your AMD Instinct™ cluster.

## Determine Topology to Map the NIC

To properly map each GPU to the NIC, follow these detailed steps:

### Find the Adjacent CPU for Each GPU

Use the corresponding command listed in the following table to identify the adjacent CPU for each GPU. Generally, NUMA node 0 is CPU 0, and NUMA node 1 is CPU 1.

Record the output for mapping purposes; this will be needed later to confirm the GPU-to-CPU association.

### Adjacent GPU Commands

| AMD Instinct Product Name | Command |
| --- | --- |
| MI300X | `lspci -d 1002:74a1 -vvv \| grep -e "Instinct" -e "NUMA node"` |
| MI308X | `lspci -d 1002:74a2 -vvv \| grep -e "Instinct" -e "NUMA node"` |
| MI325X | `lspci -d 1002:74a5 -vvv \| grep -e "Instinct" -e "NUMA node"` |
| MI350X | `lspci -d 1002:75a0 -vvv \| grep -e "Instinct" -e "NUMA node"` |
| MI355X | `lspci -d 1002:75a3 -vvv \| grep -e "Instinct" -e "NUMA node"` |

Run the following command to determine the GPU number for each of the BDF listed from the previous command.

```bash
sudo amd-smi list | grep -e "BDF" -e "GPU"
```

### Determine the PCIe Bus Topology for Each GPU

Use the command from the following table for your product to determine the PCIe bus topology for each GPU to help find the adjacent NIC for each GPU.

#### PCIe Bus Topology Commands

| AMD Instinct Product Name | Command |
| --- | --- |
| MI300X | `lspci -d 1002:74a1 -PP` |
| MI308X | `lspci -d 1002:74a2 -PP` |
| MI325X | `lspci -d 1002:74a5 -PP` |
| MI350X | `lspci -d 1002:75a0 -PP` |
| MI355X | `lspci -d 1002:75a3 -PP` |

Example output:

```bash
$ lspci -d 1002:74a1 -PP
00:01.1/01:00.0/02:00.0/03:00.0/04:00.0/05:00.0 Processing accelerators: Advanced Micro Devices, Inc. [AMD/ATI] Aqua Vanjaram [Instinct MI300X]
18:01.1/19:00.0/1a:04.0/29:00.0/2a:00.0/2b:00.0 Processing accelerators: Advanced Micro Devices, Inc. [AMD/ATI] Aqua Vanjaram [Instinct MI300X]
48:01.1/49:00.0/4a:04.0/59:00.0/5a:00.0/5b:00.0 Processing accelerators: Advanced Micro Devices, Inc. [AMD/ATI] Aqua Vanjaram [Instinct MI300X]
60:01.1/61:00.0/62:00.0/63:00.0/64:00.0/65:00.0 Processing accelerators: Advanced Micro Devices, Inc. [AMD/ATI] Aqua Vanjaram [Instinct MI300X]
78:01.1/79:00.0/7a:00.0/7b:00.0/7c:00.0/7d:00.0 Processing accelerators: Advanced Micro Devices, Inc. [AMD/ATI] Aqua Vanjaram [Instinct MI300X]
98:01.1/99:00.0/9a:03.0/a3:00.0/a4:00.0/a5:00.0 Processing accelerators: Advanced Micro Devices, Inc. [AMD/ATI] Aqua Vanjaram [Instinct MI300X]
c8:01.1/c9:00.0/ca:03.0/d3:00.0/d4:00.0/d5:00.0 Processing accelerators: Advanced Micro Devices, Inc. [AMD/ATI] Aqua Vanjaram [Instinct MI300X]
e0:01.1/e1:00.0/e2:02.0/e5:00.0/e6:00.0/e7:00.0 Processing accelerators: Advanced Micro Devices, Inc. [AMD/ATI] Aqua Vanjaram [Instinct MI300X]
```

Use the following command to list the network adapter PCI vendor ID and device ID:

```bash
lspci -nn | grep -i -e ethernet -e infiniband
```

Using the output from the previous command to determine the vendor and device ID for each backend NIC, capture the network adapter topology to determine the GPU adjacency for each NIC.

#### Pensando Pollara 400

Example for Pensando Pollara 400, 1x400G:

```bash
lspci -d 1dd8:43c6 -PP
```

or

```bash
lspci -d 1dd8:1002 -PP
```

#### Mellanox CX-7

Example for Mellanox CX-7, 1x400G:

```bash
lspci -d 15b3:1021 -PP
```

#### Broadcom Thor2

Example for Broadcom BCM57608 (Thor2):

```bash
lspci -d 14e4:1760 -PP
```

Example output:

```bash
$ lspci -d 15b3:1021 -PP
00:01.1/01:00.0/02:01.0/09:00.0 Ethernet controller: Mellanox Technologies MT2910 Family [ConnectX-7]
18:01.1/19:00.0/1a:03.0/23:00.0 Ethernet controller: Mellanox Technologies MT2910 Family [ConnectX-7]
48:01.1/49:00.0/4a:03.0/53:00.0 Ethernet controller: Mellanox Technologies MT2910 Family [ConnectX-7]
60:01.1/61:00.0/62:01.0/69:00.0 Ethernet controller: Mellanox Technologies MT2910 Family [ConnectX-7]
78:01.1/79:00.0/7a:05.0/8f:00.0 Ethernet controller: Mellanox Technologies MT2910 Family [ConnectX-7]
98:01.1/99:00.0/9a:01.0/9c:00.0 Ethernet controller: Mellanox Technologies MT2910 Family [ConnectX-7]
c8:01.1/c9:00.0/ca:02.0/cd:00.0 Ethernet controller: Mellanox Technologies MT2910 Family [ConnectX-7]
e0:01.1/e1:00.0/e2:04.0/f1:00.0 Ethernet controller: Mellanox Technologies MT2910 Family [ConnectX-7]
```

For the systems used in the examples, GPU 0 has a PCI topology of
`00:01.1/01:00.0/02:00.0/03:00.0/04:00.0/05:00.0`
and the adjacent NIC at 09:00.0 has the same base topology
`00:01.1/01:00.0/02:01.0/09:00.`

## Generate a GPU-NIC Adjacency Table

Use the commands to create a similar table shown below, specifying the correct GPU-NIC adjacency for peer-to-peer RDMA transfers:

### Example of NIC GPUs for Peer-to-Peer RDMA Transfer

Given the examples from this section, generate the following table for adjacency. Using this table, specify the correct GPU for the NIC to test peer-to-peer RDMA transfer.

| GPU | CPU | GPU BDF | NIC BDF | NIC Name |
| --- | --- | --- | --- | --- |
| 0 | 0 | `05:00.0` | `09:00.0` | `enp9s0np0` |
| 1 | 0 | `2b:00.0` | `23:00.0` | `enp35s0np0` |
| 2 | 0 | `5b:00.0` | `53:00.0` | `enp83s0np0` |
| 3 | 0 | `65:00.0` | `69:00.0` | `enp105s0np0` |
| 4 | 1 | `7d:00.0` | `8f:00.0` | `enp143s0np0` |
| 5 | 1 | `a5:00.0` | `9c:00.0` | `enp156s0np0` |
| 6 | 1 | `d5:00.0` | `cd:00.0` | `enp205s0np0` |
| 7 | 1 | `e7:00.0` | `f1:00.0` | `enp241s0np0` |

## Map NIC PCI BDF to NIC Name

Finally, run the following loop to map each NIC PCI BDF to the name of the NIC, as listed in the last column in the table above, ensuring correct identification of network interfaces:

```bash
$ for iface in /sys/class/net/*; do
ls -l ${iface}/device
done
```

Example output:

```bash
$ for iface in /sys/class/net/*; do
ls -l ${iface}/device
done
lrwxrwxrwx 1 root root 0 Jul 27 12:46 /sys/class/net/enp105s0np0/device -> ../../../0000:69:00.0
lrwxrwxrwx 1 root root 0 Jul 27 12:46 /sys/class/net/enp143s0np0/device -> ../../../0000:8f:00.0
lrwxrwxrwx 1 root root 0 Jul 27 12:46 /sys/class/net/enp156s0np0/device -> ../../../0000:9c:00.0
lrwxrwxrwx 1 root root 0 Jul 27 12:46 /sys/class/net/enp205s0np0/device -> ../../../0000:cd:00.0
lrwxrwxrwx 1 root root 0 Jul 27 12:46 /sys/class/net/enp241s0np0/device -> ../../../0000:f1:00.0
lrwxrwxrwx 1 root root 0 Jul 27 12:46 /sys/class/net/enp35s0np0/device -> ../../../0000:23:00.0
lrwxrwxrwx 1 root root 0 Jul 27 12:46 /sys/class/net/enp83s0np0/device -> ../../../0000:53:00.0
lrwxrwxrwx 1 root root 0 Jul 27 12:46 /sys/class/net/enp9s0np0/device -> ../../../0000:09:00.0
lrwxrwxrwx 1 root root 0 Jul 27 12:46 /sys/class/net/enp105s0np0/device -> ../../../0000:69:00.0
lrwxrwxrwx 1 root root 0 Jul 27 12:46 /sys/class/net/enp143s0np0/device -> ../../../0000:8f:00.0
lrwxrwxrwx 1 root root 0 Jul 27 12:46 /sys/class/net/enp156s0np0/device -> ../../../0000:9c:00.0
lrwxrwxrwx 1 root root 0 Jul 27 12:46 /sys/class/net/enp205s0np0/device -> ../../../0000:cd:00.0
lrwxrwxrwx 1 root root 0 Jul 27 12:46 /sys/class/net/enp241s0np0/device -> ../../../0000:f1:00.0
lrwxrwxrwx 1 root root 0 Jul 27 12:46 /sys/class/net/enp35s0np0/device -> ../../../0000:23:00.0
lrwxrwxrwx 1 root root 0 Jul 27 12:46 /sys/class/net/enp83s0np0/device -> ../../../0000:53:00.0
lrwxrwxrwx 1 root root 0 Jul 27 12:46 /sys/class/net/enp9s0np0/device -> ../../../0000:09:00.0
lrwxrwxrwx 1 root root 0 Jul 27 12:46 /sys/class/net/ens99f0np0/device -> ../../../0000:b9:00.0
```

## Rename NIC to Facilitate Mapping to GPU ID

To facilitate the use of the most adjacent NIC to the GPU that is being used, it can be very convenient to use the same enumeration for the network interfaces as the GPUs. For example, NIC `ai0` is the closest network interface to GPU 0, etc. The renaming of NIC can be done through UDEV rules:

### Step 1: Remove Current Pensando Network Rules

```bash
sudo rm /etc/udev/rules.d/81-pensando-net.rules
```

### Step 2: Get the PCI BDF Information for the NICs

```bash
$ lshw -c network -businfo | grep DSC
pci@0000:09:00.0  enp9s0np0    network        DSC Ethernet Controller
pci@0000:23:00.0  enp35s0np0   network        DSC Ethernet Controller
pci@0000:53:00.0  enp83s0np0   network        DSC Ethernet Controller
pci@0000:69:00.0  enp105s0np0  network        DSC Ethernet Controller
pci@0000:8f:00.0  enp143s0np0  network        DSC Ethernet Controller
pci@0000:9c:00.0  enp156s0np0  network        DSC Ethernet Controller
pci@0000:cd:00.0  enp205s0np0  network        DSC Ethernet Controller
pci@0000:f1:00.0  enp241s0np0  network        DSC Ethernet Controller
```

### Step 3: Rename Interface

NIC `enp9s0np0` becomes `ai0` as it is on the same PCIe bus as GPU 0:

```bash
sudo echo "ACTION==\"add\", SUBSYSTEM==\"net\", KERNELS==\"0000:09:00.0\" NAME:=\"ai0\"" >> /etc/udev/rules.d/61-persistent-net.rules
```

Repeat this step for each NIC, adjusting the PCI BDF address and interface name accordingly.

### Step 4: Verify the New Names

After rebooting or reloading the UDEV rules, the final names will be:

```bash
$ lshw -c network -businfo | grep DSC
pci@0000:09:00.0  ai0         network        DSC Ethernet Controller
pci@0000:23:00.0  ai1         network        DSC Ethernet Controller
pci@0000:53:00.0  ai2         network        DSC Ethernet Controller
pci@0000:69:00.0  ai3         network        DSC Ethernet Controller
pci@0000:8f:00.0  ai4         network        DSC Ethernet Controller
pci@0000:9c:00.0  ai5         network        DSC Ethernet Controller
pci@0000:cd:00.0  ai6         network        DSC Ethernet Controller
pci@0000:f1:00.0  ai7         network        DSC Ethernet Controller
```
