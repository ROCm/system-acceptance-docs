.. meta::
   :description lang=en: How to collect logs to troubleshoot AMD Instinct systems.
   :keywords: log, logging, util, linux, docker, troubleshooting, test

************************************************
Collect logs using the ROCm Tech Support utility
************************************************

``rocm_techsupport.sh`` is a shell utility script that collects logs for
troubleshooting purposes. Information such as ROCm packages installed,
``rocm-smi``, PCI bridges, system peripherals and more are logged into a text file.
When performing basic checks on your system, it's useful to first collect the
logs as a baseline before making any changes to the system.

For more information on how to install and use the ROCm Tech Support utility,
see the README at `<https://github.com/amddcgpuce/rocmtechsupport>`__.
