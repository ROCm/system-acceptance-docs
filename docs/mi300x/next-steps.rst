.. meta::
   :description lang=en: AMD Instinct MI300X post-acceptance optimization.
   :keywords: performance, optimize, AI, HPC, cluster, mpi, LLM, learning, tutorial

**********
Next steps
**********

After successfully completing the tests mentioned in this guide, the System
Under Test (SUT) meets the customer acceptance criteria. The test results
related to performance serve as a baseline for further enhancements. To further
optimize the system, it is recommended to make incremental changes to individual
parameters noted in the pre-requisites and repeat the tests. Once complete, AMD
recommends proceeding with AI model validation and cluster network validation
using the guides mentioned below. Refer to the list of
:doc:`related documentation </reference/related-documentation>` for a list of
links to all referenced documentation in this guide.

MI300X AI model performance validation
======================================

Larger AI applications, such as LLMs, are beyond the scope of this document for
system acceptance guidance. However, the SUT should be ready to run these large
models. For reference, please see the AMD Instinct MI300X Performance Validation
Guide (PVG) which has detailed platform configuration information, application
instructions, and guidance for AI application performance validation. Models are
available on `AMD Infinity Hub
<https://www.amd.com/en/developer/resources/infinity-hub.html>`_ and the
`Performance Validation Guide
<https://www.amd.com/content/dam/amd/en/documents/instinct-tech-docs/product-briefs/amd-instinct-mi300x-performance-validation-guide.pdf>`_
is available on the AMD Documentation Hub.

MI300X cluster network performance validation
=============================================

After validating single node performance, it is now time to configure each
server for maximum data transfer and bandwidth. It's essential to test both host
and device performance in single-node and multi-node setups using targeted
benchmarks. The `Cluster network performance validation guide
<https://instinct.docs.amd.com/projects/gpu-cluster-networking/en/latest/>`_ for
single-node networking and multi-node networking provides step-by-step
instructions on configuring network settings, devices, and running performance
tests to ensure AMD Instinct MI300X based GPU clusters operate at peak speed and
bandwidth.

MI300X workload optimization
============================

Once the system and networking have been fully validated, it is recommended to
review the `Workload optimization guide
<https://rocm.docs.amd.com/en/latest/how-to/tuning-guides/mi300x/workload.html>`__
to learn more about how to take advantage of workload tuning strategies to
further improve performance and efficiency of the workloads operating on the
MI300X-based systems.
