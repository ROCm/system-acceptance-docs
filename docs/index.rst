.. meta::
   :description lang=en: AMD Instinct MI300X system validation guide for customer acceptance testing.
   :keywords: validate, CAT

**************************************************
AMD Instinct MI300X customer acceptance test guide
**************************************************

This guide provides detailed instructions for qualified data center
system operators to test the proper functioning and optimal performance
of server systems equipped with AMD Instinct MI300X GPU accelerators.

This document is organized into chapters to follow in sequence to
configure the system, run tests, and interpret results to quickly
determine system health. Links to supporting documentation are also
included for reference.

Before system validation, the system operator should refer to
:doc:`Prerequisites <mi300x/prerequisites>` to ensure the server has a
supported OS installed and is configured with recommended BIOS, GRUB, and OS
settings to ensure proper operation and peak performance operation.

:doc:`Basic system health checks <mi300x/health-checks>` provides the
recommended tests to validate the system health and configuration of the system
across the OS, boot configuration, host memory, and GPU connectivity.

:doc:`System validation tests <mi300x/system-validation>` provides the
recommended tests to validate the system’s Compute (GPUs), Memory, IO, and Power
using the ROCm Validation Suite (RVS).

:doc:`Performance benchmarking <mi300x/performance-bench>` provides a
list of microbenchmarks to validate the performance of the GPUs in the system.
Tests include TransferBench, RCCL, rocBLAS, and BabelStream.

:doc:`Acceptance criteria <mi300x/acceptance-criteria>` provides a summary
of the commands and PASS/FAIL criteria to compare against recently gathered
test results. This comparison is the basis for customer acceptance of a tested
server. Changing one parameter at a time and repeating specific tests in
previous chapters help compare new results to the baseline data gathered and
ensure the best performance for your targeted application(s).

After completing the tests outlined in this guide to determine if the
server/system under test (SUT) meets expected functionality and performance,
review the :doc:`related documentation </reference/related-documentation>` and
move to the next stage of performance validation testing and optimization
outlined in :doc:`Next steps <mi300x/next-steps>`.
