# Network Validation

This section covers essential steps for validating network performance and reliability on AMD Instinct™ platforms. Proper network validation is critical, as misconfigured settings or faulty hardware can significantly impact data throughput and cluster efficiency. The process includes both software and hardware checks—from enabling RDMA (Remote Direct Memory Access) and verifying link speed to running targeted performance benchmarks and evaluating collective GPU operations. By following the outlined procedures, you can quickly identify and resolve network bottlenecks, ensuring your system delivers optimal performance for high-demand workloads.

## Pre-Validation Network Checks

Before initiating network tests, follow the below steps to ensure all backend interfaces are RDMA-enabled and running at the specified speed. These checks confirm that your AMD Instinct™ cluster is prepared for consistent, high-performance networking.

### Enable RDMA on All Backend NICs

All the backend network interfaces should support RDMA. To ensure it is enabled use the command:

```bash
rdma link
```

Result:

* PASSED: All 8 backend NICs should be listed and report status as ENABLED.
* FAILED: One or more of the backend network interfaces is not listed or is DISABLED.

### Check NIC Link Speed

Verify the NICs in your servers are reporting the correct speeds. Several commands and utilities are available to measure speed based on your network type. For the AMD Instinct™ product line 400G network cards are generally advised. 200G cards are not sufficient to avoid bottlenecks and 800G cards and not needed.

#### RoCE / Ethernet

1. Set backend NIC speed

   ```bash
   ethtool -s "<interface>" autoneg off speed 400000 duplex full
   ```

2. Check backend NIC speed

```bash
sudo ethtool <interface> | grep -i speed
cat /sys/class/net/<interface>/speed
```

#### InfiniBand

`ibdiagnet` provides an output of the entire fabric in the default log files. You can verify link speeds here.
`ibstat` or `ibstatus` tells you if the link is up and reports the speed at which it is running for all HCAs in the server.

#### Result

* PASSED: All backend NICs report a speed of 400000
* FAILED: Any result less than 400000
