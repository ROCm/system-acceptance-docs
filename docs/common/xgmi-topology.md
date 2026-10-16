<!--
description: How to read amd-smi topology output on AMD Instinct GPUs, including the distinction between abstracted topology hops and physical xGMI hops, and how link weights are derived.
keywords: AMD Instinct, amd-smi, topology, xGMI, hops, link weight, Infinity Fabric, NUMA, MI300X
-->

# Interpreting GPU fabric topology

The `amd-smi topology` command reports the fabric connections between the GPUs in a node. It is the primary tool for verifying that the AMD Infinity Fabric™ (xGMI) mesh is fully cabled and that every GPU can reach every other GPU over the expected link type. This page explains how to read its output, with particular attention to what the **hops** and **weight** tables actually count, because both are easily misread.

## Run the topology query

```bash
amd-smi topology
```

The command emits several square matrices. Each matrix is indexed by PCIe BDF (domain:bus:device.function); the diagonal corresponds to a GPU paired with itself. The example below is from a fully-cabled 8x MI300X system.

```text
$ amd-smi topology
ACCESS TABLE:
             0000:0c:00.0 0000:22:00.0 0000:38:00.0 0000:5c:00.0 0000:9f:00.0 0000:af:00.0 0000:bf:00.0 0000:df:00.0
0000:0c:00.0 ENABLED      ENABLED      ENABLED      ENABLED      ENABLED      ENABLED      ENABLED      ENABLED
0000:22:00.0 ENABLED      ENABLED      ENABLED      ENABLED      ENABLED      ENABLED      ENABLED      ENABLED
0000:38:00.0 ENABLED      ENABLED      ENABLED      ENABLED      ENABLED      ENABLED      ENABLED      ENABLED
0000:5c:00.0 ENABLED      ENABLED      ENABLED      ENABLED      ENABLED      ENABLED      ENABLED      ENABLED
0000:9f:00.0 ENABLED      ENABLED      ENABLED      ENABLED      ENABLED      ENABLED      ENABLED      ENABLED
0000:af:00.0 ENABLED      ENABLED      ENABLED      ENABLED      ENABLED      ENABLED      ENABLED      ENABLED
0000:bf:00.0 ENABLED      ENABLED      ENABLED      ENABLED      ENABLED      ENABLED      ENABLED      ENABLED
0000:df:00.0 ENABLED      ENABLED      ENABLED      ENABLED      ENABLED      ENABLED      ENABLED      ENABLED
WEIGHT TABLE:
             0000:0c:00.0 0000:22:00.0 0000:38:00.0 0000:5c:00.0 0000:9f:00.0 0000:af:00.0 0000:bf:00.0 0000:df:00.0
0000:0c:00.0 0            15           15           15           15           15           15           15
0000:22:00.0 15           0            15           15           15           15           15           15
0000:38:00.0 15           15           0            15           15           15           15           15
0000:5c:00.0 15           15           15           0            15           15           15           15
0000:9f:00.0 15           15           15           15           0            15           15           15
0000:af:00.0 15           15           15           15           15           0            15           15
0000:bf:00.0 15           15           15           15           15           15           0            15
0000:df:00.0 15           15           15           15           15           15           15           0
HOPS TABLE:
             0000:0c:00.0 0000:22:00.0 0000:38:00.0 0000:5c:00.0 0000:9f:00.0 0000:af:00.0 0000:bf:00.0 0000:df:00.0
0000:0c:00.0 0            1            1            1            1            1            1            1
0000:22:00.0 1            0            1            1            1            1            1            1
0000:38:00.0 1            1            0            1            1            1            1            1
0000:5c:00.0 1            1            1            0            1            1            1            1
0000:9f:00.0 1            1            1            1            0            1            1            1
0000:af:00.0 1            1            1            1            1            0            1            1
0000:bf:00.0 1            1            1            1            1            1            0            1
0000:df:00.0 1            1            1            1            1            1            1            0
LINK TYPE TABLE:
             0000:0c:00.0 0000:22:00.0 0000:38:00.0 0000:5c:00.0 0000:9f:00.0 0000:af:00.0 0000:bf:00.0 0000:df:00.0
0000:0c:00.0 SELF         XGMI         XGMI         XGMI         XGMI         XGMI         XGMI         XGMI
0000:22:00.0 XGMI         SELF         XGMI         XGMI         XGMI         XGMI         XGMI         XGMI
0000:38:00.0 XGMI         XGMI         SELF         XGMI         XGMI         XGMI         XGMI         XGMI
0000:5c:00.0 XGMI         XGMI         XGMI         SELF         XGMI         XGMI         XGMI         XGMI
0000:9f:00.0 XGMI         XGMI         XGMI         XGMI         SELF         XGMI         XGMI         XGMI
0000:af:00.0 XGMI         XGMI         XGMI         XGMI         XGMI         SELF         XGMI         XGMI
0000:bf:00.0 XGMI         XGMI         XGMI         XGMI         XGMI         XGMI         SELF         XGMI
0000:df:00.0 XGMI         XGMI         XGMI         XGMI         XGMI         XGMI         XGMI         SELF
```

## Hops: abstracted topology steps, not physical xGMI links

The **hops** table is the most commonly misinterpreted output. Its value is an *abstracted topological step count* describing the class of route between two GPUs. **It is not the number of physical xGMI links the route traverses.**

| Hops value | Meaning |
| --- | --- |
| `1` | The two endpoints are reachable over xGMI, **regardless of how many physical xGMI links the route actually traverses**. This applies to both GPU-to-GPU and GPU-to-CPU xGMI connections. |
| `2` | The endpoints share a CPU NUMA node and communicate through it over PCIe. This applies to both GPU-to-GPU and GPU-to-CPU PCIe connections. |
| `3` | The endpoints sit on different CPU NUMA nodes, so the route traverses both. |
| `4` | Fallback value used when the inter-CPU io_link weight cannot be read. |

The key consequence: any two GPUs on the same xGMI fabric report `1` hop **even if the data physically crosses several xGMI links** to get there. On a fully-connected 8x MI300X system every off-diagonal entry is `1`, but on a fabric where some GPU pairs are only reachable through an intermediate GPU, the value is still `1` despite the longer physical path.

```{warning}
Do not use the **hops** table to determine the physical distance between two GPUs. A value of `1` means "reachable over xGMI", not "one xGMI link away".
```

### Reading the physical xGMI hop count

The literal number of physical xGMI links between devices is exposed separately by the `amdgpu` driver, not by `amd-smi topology`. Read it from sysfs:

```bash
for f in /sys/class/drm/card*/device/xgmi_num_hops; do echo "$f: $(cat "$f")"; done
```

This is the value to consult when you need the actual hop count for a GPU pair — for example, when reasoning about latency or bandwidth between specific devices.

## Weight: a qualitative cost metric

The **weight** table is a qualitative cost metric the kernel assigns to each link, similar in spirit to the NUMA distances reported by `numactl`. Lower values indicate closer or faster connections.

Each value comes from the KFD io_link `weight` property exposed at `/sys/class/kfd/kfd/topology/nodes/<n>/io_links/<m>/properties`. For multi-segment PCIe routes, the SMI library sums the segment weights (GPU→CPU + CPU→CPU + CPU→GPU). The `amdgpu` driver computes each xGMI io_link weight as `KFD_CRAT_XGMI_WEIGHT × num_hops` — 15 per physical xGMI hop on a single-partition system — while PCIe segments contribute a fixed cost of 20.

Because the weight is derived from the physical hop count, it carries distance information that the abstracted **hops** table does not. On an 8x MI300X system every GPU pair is one physical xGMI hop apart, so every off-diagonal weight is `15`. On a non-uniform fabric, larger weights (for example `30` or `45`) indicate pairs separated by two or three physical xGMI hops respectively.

## Access and link type

* The **access** table reports whether each GPU can directly access every other GPU. On a fully-cabled platform every off-diagonal entry is `ENABLED`.
* The **link type** table reports the link technology between each pair: `SELF` on the diagonal, `XGMI` for AMD Infinity Fabric links, or `PCIE` for PCIe links. A system without an Infinity Fabric bridge installed reports `PCIE` for every off-diagonal entry.

## Result

* **PASSED:** Every off-diagonal **access** entry is `ENABLED`, every off-diagonal **link type** entry is `XGMI`, and the **hops** and **weight** tables match the expected pattern for your platform (for a fully-cabled 8x MI300X system, all off-diagonal hops are `1` and all off-diagonal weights are `15`).
* **FAILED:** Any off-diagonal pair reports `DISABLED` access, a `PCIE` link type where xGMI is expected, or weights higher than expected for the platform.
  * **Action:** A `PCIE` link type or `DISABLED` access between GPUs that should be xGMI-connected usually indicates a missing or improperly seated Infinity Fabric bridge. Verify the physical fabric cabling and reseat the bridges, then rerun the query.
