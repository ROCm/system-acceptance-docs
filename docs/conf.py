"""Configuration file for the Sphinx documentation builder."""
import os
import subprocess
import sys

html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "instinct.docs.amd.com")
html_context = {}
if os.environ.get("READTHEDOCS", "") == "True":
    html_context["READTHEDOCS"] = True
project = "AMD Instinct Customer Acceptance Guide"

# Disable external projects to avoid GitHub API issues
external_projects_remote_repository = ""
external_projects_current_project = "system-acceptance-docs"

version = "1.0.0"
release = version
html_title = project
author = "Advanced Micro Devices, Inc."
copyright = "Copyright (c) 2025 Advanced Micro Devices, Inc. All rights reserved."

# Required settings
html_theme = "rocm_docs_theme"
html_theme_options = {
    "flavor": "instinct",
    "link_main_doc": True,
    "nav_secondary_items": {
        "Community": "https://github.com/ROCm/ROCm/discussions",
        "Blogs": "https://rocm.blogs.amd.com/",
        "ROCm&#8482 docs": "https://rocm.docs.amd.com"
    },
    # Add any additional theme options here
}

extensions = ["rocm_docs"]

# Table of contents
external_toc_path = "./sphinx/_toc.yml"

exclude_patterns = ['.venv']
