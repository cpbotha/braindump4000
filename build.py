#!/usr/bin/env python

from pathlib import Path

# this is pkb4000: the top-level of my org-mode database
org_dir = Path("..").resolve()
# this is the destination hugo site
hugo_dir = Path("../../pkb4000-web").resolve()

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
