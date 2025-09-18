# Network Configuration for Performance Optimization

Configure your NIC to ensure best performance. The following details the optimization based on a particular NIC.

## AMD Pensando Pollara 400

Several host configurations and NIC configurations should be done to achieve the best performance on the Pollara AI NIC.

### Enable PFC

The uplink port needs to be enabled for RX/TX pause and pause-type as PFC. The configuration can be applied to a single port by specifying the `<port_id>` or all the ports in the system:

```bash
# To get the port_id
# nicctl show port
# nicctl update port -p <port_id> --pause-type pfc --rx-pause enable --tx-pause enable
```

#### Recommended PFC Parameters

Use the script below to update the DCQCN setting of Pollara AI NIC. The DSCP value or the Traffic Class value of your application, ex, TC value of perf-test and RCCL, should match the data_dscp value in the script.

```bash
#!/bin/bash
for i in $(sudo nicctl show port | grep Port | awk {'print $3'}); do sudo nicctl update port -p $i --pause-type pfc --rx-pause enable --tx-pause enable; done
for i in $(sudo nicctl show port | grep Port | awk {'print $3'}); do sudo nicctl update port --port $i --auto-neg enable; done
cts_dscp=46
cts_prio=6
data_dscp=24
data_prio=0
default_prio=3
cnp_dscp=46
cnp_prio=6
sudo nicctl update qos pfc --priority 0 --no-drop disable
sudo nicctl update qos dscp-to-purpose --dscp $cts_dscp --purpose xccl-cts
sudo nicctl update qos dscp-to-purpose $data_dscp --purpose data
sudo nicctl update qos --classification-type pcp
sudo nicctl update qos --classification-type dscp
sudo nicctl update qos dscp-to-priority --dscp 0-63 --priority 0
sudo nicctl update qos dscp-to-priority --dscp 0-23,25-45,47-63 --priority $default_prio
sudo nicctl update qos dscp-to-priority --dscp $cts_dscp --priority strict
sudo nicctl update qos dscp-to-priority --dscp $data_dscp --priority $data_prio
sudo nicctl update qos dscp-to-priority --dscp $cnp_dscp --priority $cnp_prio
sudo nicctl update qos pfc --priority $data_prio --no-drop enable
sudo nicctl update qos scheduling --priority $data_prio,$default_prio,$cts_prio --dwrr 99,1,0 --rate-limit 0,0,10
```

### Configure DCQCN

The DCQCN configuration is crucial to achieve the optimal performance in a bigger cluster. Use the following script to apply the DCQCN parameters that are recommended by AMD:

```bash
#!/bin/bash
TOKEN_BUCKET_SIZE=800000
AI_RATE=160
ALPHA_UPDATE_INTERVAL=1
ALPHA_UPDATE_G=512
INITIAL_ALPHA_VALUE=64
RATE_INCREASE_BYTE_COUNT=431068
HAI_RATE=300
RATE_REDUCE_MONITOR_PERIOD=1
RATE_INCREASE_THRESHOLD=1
RATE_INCREASE_INTERVAL=1
CNP_DSCP=46
ROCE_DEVICES=$(ibv_devices | grep ionic_ | awk '{print $1}' | paste -sd " ")
for roce_dev in $ROCE_DEVICES
do
sudo nicctl update dcqcn -r $roce_dev -i 1 \
--token-bucket-size $TOKEN_BUCKET_SIZE \
--ai-rate $AI_RATE \
--alpha-update-interval $ALPHA_UPDATE_INTERVAL \
--alpha-update-g $ALPHA_UPDATE_G \
--initial-alpha-value $INITIAL_ALPHA_VALUE \
--rate-increase-byte-count $RATE_INCREASE_BYTE_COUNT \
--hai-rate $HAI_RATE \
--rate-reduce-monitor-period $RATE_REDUCE_MONITOR_PERIOD \
--rate-increase-threshold $RATE_INCREASE_THRESHOLD \
--rate-increase-interval $RATE_INCREASE_INTERVAL \
--cnp-dscp $CNP_DSCP
done
```

## Broadcom 400G NIC

For Broadcom 400G NICs, perform the following actions to guarantee proper operation and peak performance:

* Enable PCIe relaxed ordering.
* Enable RDMA support.
* Select the RoCE performance profile.
* Exclude all speeds except 400G from the speed mask.
* Disable unused ports to optimize resources.

For detailed configuration, use the scripts provided in the [cluster networking GitHub repository](https://github.com/ROCm/cluster-networking/tree/main/niccli_scripts)
