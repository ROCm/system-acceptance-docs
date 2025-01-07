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

Prior to system validation, the system operator should refer to
:ref:`Prerequisites <mi300x-sv-prerequisites>` to ensure the server has a
supported OS installed and is configured with recommended BIOS, GRUB, and OS
settings to ensure proper operation and peak performance operation.

:ref:`Basic system health checks <mi300x-sv-system-health-checks>` provides the
recommended tests to validate the system health and configuration of the system
across the OS, boot configuration, host memory, and GPU connectivity.

:ref:`System validation tests <mi300x-sv-system-validation-tests>` provides the
recommended tests to validate the system’s Compute (GPUs), Memory, IO and Power
using the ROCm Validation Suite (RVS).

:ref:`Performance benchmarking <mi300x-sv-performance-benchmarking>` provides a
list of microbenchmarks to validate the performance of the GPUs in the system.
Tests include TransferBench, RCCL, rocBLAS, and BabelStream.

:ref:`Acceptance criteria <mi300x-sv-acceptance-criteria>` provides a summary
of the commands and PASS/FAIL criteria to compare against recently gathered
test results. This comparison is the basis for customer acceptance of a tested
server. By changing one parameter at a time and repeating specific tests in
earlier chapters, new results can be compared to the baseline data gathered to
ensure the best performance for your targeted application(s).

After completing the tests outlined in this guide to determine if the
server/system under test (SUT) meets expected functionality and
performance, you should proceed to review the recommended referenced
documents in `Appendix B <#appendix-b-reference-documents>`__ and move
to the next stage of performance validation testing and optimization
outlined in :ref:`Next steps <mi300x-sv-next-steps>`.
