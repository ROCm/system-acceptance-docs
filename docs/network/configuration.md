# Configure Network Routing

Proper routing is essential to ensure that each backend network interface is used exclusively for high-performance, GPU-driven cluster communications. In a multi-NIC environment, assigning a unique routing domain to each network interface prevents traffic overlap and optimizes throughput and latency.

The following steps and example nmcli commands show how to configure Layer 3 routing for each NIC in your system.

```{note}
Update interface names and IP addresses as appropriate for your cluster.
```

Add Each NIC to Its Own Routing Domain:

```bash
sudo nmcli connection add type ethernet con-name enp83s0np0 ifname enp83s0np0 ipv4.method manual ipv4.addresses 192.168.1.201/31 ipv4.routes "0.0.0.0/0 192.168.1.200 table=101" ipv4.routing-rules "priority 1010 from 192.168.1.201 table 101"
sudo nmcli connection add type ethernet con-name enp105s0np0 ifname enp105s0np0 ipv4.method manual ipv4.addresses 192.168.1.203/31 ipv4.routes "0.0.0.0/0 192.168.1.202 table=102" ipv4.routing-rules "priority 1020 from 192.168.1.203 table 102"
sudo nmcli connection add type ethernet con-name enp35s0np0 ifname enp35s0np0 ipv4.method manual ipv4.addresses 192.168.1.205/31 ipv4.routes "0.0.0.0/0 192.168.1.204 table=103" ipv4.routing-rules "priority 1030 from 192.168.1.205 table 103"
sudo nmcli connection add type ethernet con-name enp9s0np0 ifname enp9s0np0 ipv4.method manual ipv4.addresses 192.168.1.207/31 ipv4.routes "0.0.0.0/0 192.168.1.206 table=104" ipv4.routing-rules "priority 1040 from 192.168.1.207 table 104"
sudo nmcli connection add type ethernet con-name enp241s0np0 ifname enp241s0np0 ipv4.method manual ipv4.addresses 192.168.1.209/31 ipv4.routes "0.0.0.0/0 192.168.1.208 table=105" ipv4.routing-rules "priority 1050 from 192.168.1.209 table 105"
sudo nmcli connection add type ethernet con-name enp205s0np0 ifname enp205s0np0 ipv4.method manual ipv4.addresses 192.168.1.211/31 ipv4.routes "0.0.0.0/0 192.168.1.210 table=106" ipv4.routing-rules "priority 1060 from 192.168.1.211 table 106"
sudo nmcli connection add type ethernet con-name enp143s0np0 ifname enp143s0np0 ipv4.method manual ipv4.addresses 192.168.1.213/31 ipv4.routes "0.0.0.0/0 192.168.1.212 table=107" ipv4.routing-rules "priority 1070 from 192.168.1.213 table 107"
sudo nmcli connection add type ethernet con-name enp156s0np0 ifname enp156s0np0 ipv4.method manual ipv4.addresses 192.168.1.215/31 ipv4.routes "0.0.0.0/0 192.168.1.214 table=108" ipv4.routing-rules "priority 1080 from 192.168.1.215 table 108"
```

Use the following commands to activate each interface:

```bash
nmcli connection up enp83s0np0
nmcli connection up enp105s0np0
nmcli connection up enp35s0np0
nmcli connection up enp9s0np0
nmcli connection up enp241s0np0
nmcli connection up enp205s0np0
nmcli connection up enp143s0np0
nmcli connection up enp156s0np0
```

Set RP filter to 2 (loose mode) for all interfaces for proper asymmetric routing:

```bash
sudo sysctl -w net.ipv4.conf.all.rp_filter=2
```

To make this change permanent, add the following lines to /etc/sysctl.conf:

```bash
net.ipv4.conf.all.arp_ignore=2
net.ipv4.conf.all.arp_announce=1
net.ipv4.conf.all.rp_filter=2
```

For each interface, reload the connection if needed:

```bash
nmcli connection down <con-name> ; nmcli connection reload <con-name> ; nmcli connection up <con-name>
```

Replace `<con-name>` with each interface name.

View the rules:

```bash
ip rule show
```

Check that each custom routing table is active:

```bash
ip route show table 101
ip route show table 102
ip route show table 103
ip route show table 104
ip route show table 105
ip route show table 106
ip route show table 107
ip route show table 108
```

Expected Output Example

```bash
default via 192.168.2.200 dev enp83s0np0 proto static metric 110
```

Result:

PASS: Each routing table shows a default route through the intended NIC.
FAIL: If a table is missing or routes are not as expected, review the configuration for typos or incorrectly assigned NICs.
