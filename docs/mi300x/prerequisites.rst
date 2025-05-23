.. meta::
   :description lang=en: Prerequisites for acceptance testing AMD Instinct MI300X GPU accelerators.
   :keywords: prereq, install

*************
Prerequisites
*************

Before proceeding with the prerequisites in this section, ensure that the
system has been properly installed and is free of visible damage. As the system
administrator, refer to the manufacturer's installation guide to verify that
the system is correctly installed in a rack with sufficient cooling, is
connected to the required power, and is accessible from the network.

If errors or warnings are found during setup, you might need to
troubleshoot the issue by, for example, reseating auxiliary PCBs, checking
internal cable connections, or monitoring the situation. For debugging support,
contact your system manufacturer.

This section describes the server settings to configure before testing,
including:

- :ref:`System BIOS settings <mi300x-prereq-bios-settings>`

- :ref:`Supported operating systems <mi300x-prereq-supported-os>`

- :ref:`GRUB settings <mi300x-prereq-grub-settings>`

- :ref:`Operating system settings <mi300x-prereq-os-settings>`

- :ref:`Updating system firmware <mi300x-prereq-system-firmware>`

- :ref:`ROCm installation <mi300x-prereq-rocm-installation>`

.. note::

   Before changing any system settings and testing, record existing production
   system settings to allow the system to be returned to the original settings.

.. _mi300x-prereq-bios-settings:

System BIOS settings
====================

Some server manufacturers offer tools that allow the current BIOS configuration
settings to be exported to a file, modified with needed changes, and loaded
back to the system. If the server manufacturer doesn't offer such a tool, the
BIOS settings will need to be reviewed and updated manually from the BIOS setup
interface before booting the OS.

Refer to the recommended :ref:`system BIOS settings <rocm:mi300x-bios-settings>`
for MI300X to ensure the system BIOS is set up correctly for maximum performance
prior to validating the system with AMD EPYC™ 9004-series processors and AMI
System BIOS. These settings should be set as default values in the system BIOS.
Analogous settings for other non-AMI System BIOS providers could be set
similarly. For systems with Intel processors, some settings might not apply or
be unavailable.

.. _mi300x-prereq-supported-os:

Supported operating systems
===========================

Refer to the list of Linux :ref:`Supported operating systems
<rocm-install-on-linux:supported_distributions>` and ensure your system is
installed with one. Other distributions might be unable to run ROCm or complete
the validation tests in this document.

To obtain and validate the Linux distribution information for systems
with the OS already installed, refer to the
:doc:`ROCm installation prerequisites <rocm-install-on-linux:install/prerequisites>`.

.. _mi300x-prereq-grub-settings:

GRUB settings
=============

GRUB, or GNU Grand Unified Bootloader, is a boot loader and boot manager for
Linux that allows the operator to select which operating system and kernel
configuration to use when booting the system. MI300X-based servers require
appending strings to the Linux command line and this is done in the GRUB
configuration file as described in the recommended
:ref:`GRUB settings <rocm:mi300x-grub-settings>` for MI300X. After updating GRUB
and rebooting the system, it is recommended to check the GRUB configuration file
before proceeding.

.. _mi300x-prereq-os-settings:

Operating system settings
=========================

To ensure the system is operating at maximum performance prior to running the
validations and performance tests in this document, the operator should ensure
that power gating is disabled, NUMA configuration is set appropriately, and
specific environment variables are exported as outlined in the :ref:`Operating
system settings <rocm:mi300x-os-settings>` for MI300X. For illustration
purposes, this document uses Ubuntu 22.04 for commands and output unless
otherwise specified.

.. _mi300x-prereq-system-firmware:

Updating system firmware
========================

Ensure that the system under test is running the latest firmware
versions by contacting your system manufacturer. Systems with older
firmware versions may not fully be validated, and performance or
functionality could be sub-optimal.

.. _mi300x-prereq-rocm-installation:

ROCm installation
=================

Once the system is properly configured, ROCm software can be installed. Prior to
validating the system, ensure that ROCm version 6.2 or later is installed. For
maximum performance and functionality, it's recommended to always install the
latest ROCm version on the system.

Refer to :doc:`ROCm installation for Linux <rocm-install-on-linux:index>` for
the available options to install ROCm on your system. For operators new to ROCm,
see the :doc:`Quick start installation guide <rocm-install-on-linux:install/quick-start>`
for your supported distribution. Once ROCm is installed, follow the
:doc:`Post-installation instructions <rocm-install-on-linux:install/post-install>`.
To troubleshoot issues encountered when installing ROCm tools or
libraries, see the
:doc:`Installation troubleshooting guide <rocm-install-on-linux:reference/install-faq>`.

Run the following command to check the ROCm version running on the system after
installation.

.. code-block:: shell

   cat /opt/rocm/.info/version

Example output:

.. code-block:: shell-session

   6.2.0-66

.. note::

   Contact your system manufacturer support representative to ensure this
   version of ROCm installed is compatible with the system firmware.
