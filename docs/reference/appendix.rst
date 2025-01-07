********
Appendix
********

Acronyms
========

The following table contains acronyms and definitions used throughout
this document.

+---------------+------------------------------------------------------+
| Acronym       | Description                                          |
+===============+======================================================+
| AMI           | American Megatrends Inc. (BIOS provider)             |
+---------------+------------------------------------------------------+
| BIOS          | Basic Input/Output System                            |
+---------------+------------------------------------------------------+
| CUs           | Compute Units                                        |
+---------------+------------------------------------------------------+
| DGEMM         | Double-precision General Matrix Multiply             |
+---------------+------------------------------------------------------+
| DMA           | Direct Memory Access                                 |
+---------------+------------------------------------------------------+
| GB/s          | Gigabytes per second                                 |
+---------------+------------------------------------------------------+
| GPU           | Graphics Processing Unit                             |
+---------------+------------------------------------------------------+
| GRUB          | GNU Grand Unified Bootloader                         |
+---------------+------------------------------------------------------+
| GST           | GPU Stress Test                                      |
+---------------+------------------------------------------------------+
| HBM3          | High Bandwidth Memory 3                              |
+---------------+------------------------------------------------------+
| HIP           | Heterogeneous-computing Interface for Portability    |
+---------------+------------------------------------------------------+
| IET           | Input Energy Delay Product                           |
+---------------+------------------------------------------------------+
| MB/s          | Megabytes per second                                 |
+---------------+------------------------------------------------------+
| MEM           | Memory                                               |
+---------------+------------------------------------------------------+
| MPI           | Message Passing Interface                            |
+---------------+------------------------------------------------------+
| NVMe          | Non-Volatile Memory Express                          |
+---------------+------------------------------------------------------+
| OAM           | Open Accelerator Module                              |
+---------------+------------------------------------------------------+
| ORC           | Online Resource Center for AMD partners              |
+---------------+------------------------------------------------------+
| OS            | Operating System                                     |
+---------------+------------------------------------------------------+
| PBQT          | P2P Benchmark and Qualification Tool                 |
+---------------+------------------------------------------------------+
| PEBB          | PCIe Bandwidth Benchmark                             |
+---------------+------------------------------------------------------+
| PEQT          | PCIe Qualification Tool                              |
+---------------+------------------------------------------------------+
| PCIe          | Peripheral Component Interconnect Express            |
+---------------+------------------------------------------------------+
| PVG           | Performance Validation Guide                         |
+---------------+------------------------------------------------------+
| RCCL          | ROCm Collective Communications Library               |
+---------------+------------------------------------------------------+
| rocBLAS       | ROCm Basic Linear Algebra Subprograms                |
+---------------+------------------------------------------------------+
| RVS           | ROCm Validation Suite                                |
+---------------+------------------------------------------------------+
| SGEMM         | Single-precision General Matrix Multiply             |
+---------------+------------------------------------------------------+
| SUT           | System Under Test                                    |
+---------------+------------------------------------------------------+
| TFLOPS        | Tera Floating Point Operations Per Second            |
+---------------+------------------------------------------------------+
| xGMI          | Inter-chip (x) Global Memory Interconnect            |
+---------------+------------------------------------------------------+

Reference documentation
=======================

The following table provides the relevant reference documents and links to
setup the system and run the tests in this guide.

+---------------+------------------------------------------------------+
| Document Name | Link                                                 |
+===============+======================================================+
| System BIOS   | https://rocm.docs.amd.com/en/latest/how-to/s         |
| Settings      | ystem-optimization/mi300x.html#mi300x-bios-settings  |
+---------------+------------------------------------------------------+
| Supported     | https://rocm.doc                                     |
| Operating     | s.amd.com/projects/install-on-linux/en/latest/refere |
| Systems       | nce/system-requirements.html#supported-distributions |
+---------------+------------------------------------------------------+
| ROCm          | https://rocm.docs.amd.com/projects/i                 |
| Installation  | nstall-on-linux/en/latest/install/prerequisites.html |
| Prerequisites |                                                      |
+---------------+------------------------------------------------------+
| GRUB Settings | https://rocm.docs.amd.com/en/latest/how-to/          |
|               | system-optimization/mi300x.html#mi300x-grub-settings |
+---------------+------------------------------------------------------+
| Operating     | https://rocm.docs.amd.com/en/latest/how-t            |
| System        | o/system-optimization/mi300x.html#mi300x-os-settings |
| Settings      |                                                      |
+---------------+------------------------------------------------------+
| ROCm          | https://rocm.docs.amd.co                             |
| Compatibility | m/en/latest/compatibility/compatibility-matrix.htmlP |
| Matrix        |                                                      |
+---------------+------------------------------------------------------+
| ROCm Quick    | https://rocm.docs.amd.com/projects                   |
| Start         | /install-on-linux/en/latest/install/quick-start.html |
| Installation  |                                                      |
| Guide         |                                                      |
+---------------+------------------------------------------------------+
| ROCm          | https://rocm.docs.am                                 |
| Installation  | d.com/projects/install-on-linux/en/latest/index.html |
| for Linux     |                                                      |
+---------------+------------------------------------------------------+
| ROCm Post     | https://rocm.docs.amd.com/projects/                  |
| Installation  | install-on-linux/en/latest/install/post-install.html |
| Instructions  |                                                      |
+---------------+------------------------------------------------------+
| ROCm          | https://rocm.docs.amd.com/projects/i                 |
| Installation  | nstall-on-linux/en/latest/reference/install-faq.html |
| Tr            |                                                      |
| oubleshooting |                                                      |
+---------------+------------------------------------------------------+
| RVS           | https://github.com/                                  |
| Configuration | ROCm/ROCmValidationSuite/blob/master/docs/ug1main.md |
| File          |                                                      |
+---------------+------------------------------------------------------+
| RVS User      | https://github.com/                                  |
| Guide         | ROCm/ROCmValidationSuite/blob/master/docs/ug1main.md |
+---------------+------------------------------------------------------+
| RVS Modules   | https://github.                                      |
|               | com/ROCm/ROCmValidationSuite/blob/master/FEATURES.md |
+---------------+------------------------------------------------------+
| TransferBench | https://github.com/ROCm/TransferBench                |
| Repository    |                                                      |
+---------------+------------------------------------------------------+
| TransferBench | `https://ro                                          |
| How To Guide  | cm.docs.amd.com/projects/TransferBench/en/latest/how |
|               | to/use-transferbe                                    |
|               | nch.html <https://rocm.docs.amd.com/projects/Transfe |
|               | rBench/en/latest/how%20to/use-transferbench.html>`__ |
|               |                                                      |
+---------------+------------------------------------------------------+
| TransferBench | https://github.com/                                  |
| Example       | ROCm/TransferBench/blob/develop/examples/example.cfg |
| Configuration |                                                      |
+---------------+------------------------------------------------------+
| RCCL          | https://github.com/ROCm/rccl                         |
| Repository    |                                                      |
+---------------+------------------------------------------------------+
| RCCL Test     | https://github.com/ROCm/rccl-tests/tree/develop      |
| Repository    |                                                      |
+---------------+------------------------------------------------------+
| RCCL          | https://github                                       |
| Performance   | .com/ROCm/rccl-tests/blob/develop/doc/PERFORMANCE.md |
| Guide         |                                                      |
+---------------+------------------------------------------------------+
| RCCL Tests    | h                                                    |
| (All)         | ttps://github.com/ROCm/rccl-tests/tree/develop/test  |
+---------------+------------------------------------------------------+
| rocBLAS       | https://rocm                                         |
| Documentation | .docs.amd.com/projects/rocBLAS/en/develop/index.html |
+---------------+------------------------------------------------------+
| rocBLAS Bench | https://rocm.docs.amd.com/projects/rocBLAS/en        |
| Guide         | /develop/how-to/Programmers_Guide.html#rocblas-bench |
+---------------+------------------------------------------------------+
| BabelStream   | https://github.com/UoB-HPC/BabelStream               |
| Repository    |                                                      |
+---------------+------------------------------------------------------+
| Performance   | https://www.amd.com/content/dam                      |
| Validation    | /amd/en/documents/instinct-tech-docs/product-briefs/ |
| Guide         | amd-instinct-mi300x-performance-validation-guide.pdf |
+---------------+------------------------------------------------------+
| Infinity Hub  | https://                                             |
| Portal        | www.amd.com/en/developer/resources/infinity-hub.html |
+---------------+------------------------------------------------------+
| Cluster       | https://rocm.doc                                     |
| Network       | s.amd.com/projects/gpu-cluster-networking/en/latest/ |
| Performance   |                                                      |
| Validation    |                                                      |
| Guide         |                                                      |
+---------------+------------------------------------------------------+
| Workload      | https://rocm.docs.amd.com                            |
| Optimization  | /en/latest/how-to/tuning-guides/mi300x/workload.html |
| Guide         |                                                      |
+---------------+------------------------------------------------------+

Collecting logs (rocm_techsupport.sh)
=====================================

ROCm Tech Support is a shell utility script that collects logs for
troubleshooting purposes. Information such as ROCm packages installed,
rocm-smi, PCI bridges, system peripherals and more are logged into a
text file. When performing basic checks on the system, it is useful to
first collect the logs as a baseline before making any changes to the
system.

For more information on how to install and use this utility, refer to
the README located at https://github.com/amddcgpuce/rocmtechsupport.

Notices
=======

© Copyright 2025 Advanced Micro Devices, Inc.

The information presented in this document is for informational
purposes only and may contain technical inaccuracies, omissions, and
typographical errors. The information contained herein is subject to
change and may be rendered inaccurate for many reasons, including but
not limited to product and roadmap changes, component and motherboard
version changes, new model and/or product releases, product
differences between differing manufacturers, software changes, BIOS
flashes, firmware upgrades, or

the like. Any computer system has risks of security vulnerabilities
that cannot be completely prevented or mitigated. AMD assumes no
obligation to update or otherwise correct or revise this information.

However, AMD reserves the right to revise this information and to
make changes from time to time to the content hereof without
obligation of AMD to notify any person of such revisions or changes.

THIS INFORMATION IS PROVIDED "AS IS." AMD MAKES NO REPRESENTATIONS OR
WARRANTIES WITH RESPECT TO THE CONTENTS HEREOF AND ASSUMES NO
RESPONSIBILITY FOR

ANY INACCURACIES, ERRORS, OR OMISSIONS THAT MAY APPEAR IN THIS
INFORMATION. AMD SPECIFICALLY DISCLAIMS ANY IMPLIED WARRANTIES OF
NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR ANY PARTICULAR
PURPOSE. IN NO EVENT WILL AMD BE LIABLE TO ANY PERSON FOR ANY
RELIANCE, DIRECT, INDIRECT, SPECIAL, OR OTHER CONSEQUENTIAL DAMAGES
ARISING FROM THE USE OF ANY INFORMATION CONTAINED HEREIN, EVEN IF AMD
IS EXPRESSLY ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

Trademarks
----------

AMD, the AMD Arrow logo, and combinations thereof are trademarks of
Advanced Micro Devices, Inc.

Other product names used in this publication are for identification
purposes only and may be trademarks of their respective companies.

PCIe® is a registered trademark of PCI-SIG Corporation.

.. |A black background with a black square Description automatically generated with medium confidence| image:: media/image1.png
:width: 2.9077in
:height: 0.69771in
.. |Shape| image:: media/image8.png
:width: 7.02084in
