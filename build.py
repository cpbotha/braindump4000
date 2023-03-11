#!/usr/bin/env python

import os
from pathlib import Path

# we do need to run ninja from the same dir as this script, as it requires
# the bundled init-tiny.el and publish.el
this_dir = Path(__file__).parent.resolve()
os.chdir(this_dir)

# you can reconfigure the below two paths for your setup.
# In my case:
# 1. this resolves to pkb4000: the top-level of my org-mode database
org_dir = Path("..").resolve()
# 2. this is the destination hugo site
hugo_dir = Path("../../web-pkb4000").resolve()

files = org_dir.rglob("*.org")

# we create build.ninja right here in org_dir/braindump4000/
with Path("build.ninja").open("w") as ninja_file:
    ninja_file.write(
        f"""
rule org2md
  command = emacs --batch -l init-tiny.el -l publish.el --eval \"(cpb/publish \\"{org_dir}\\" \\"$in\\" \\"{hugo_dir}\\" \\"$out\\" )\"
  description = org2md $in
"""
    )

    for f in files:
        rf = f.relative_to(org_dir)
        output_file = hugo_dir / "content" / "posts" / rf.with_suffix(".md")
        ninja_file.write(
            f"""
build {output_file}: org2md {org_dir / rf}
"""
        )

import subprocess

subprocess.call(["ninja"])
