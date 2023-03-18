#!/usr/bin/env python

import argparse
import os
from pathlib import Path

parser = argparse.ArgumentParser(description='Convert Emacs Org mode database to Hugo / Obsidian')
parser.add_argument('org_dir', 
                    help='Directory containing your nested org mode database')
parser.add_argument('out_dir', 
                    help='Output directory. This must take the form hugo-site/content/something, where "something" is usually posts')
parser.add_argument('--obsidian', action='store_true',
                    help='Perform Obsidian-targeted link rewrite. Default: Hugo only.')

args = parser.parse_args()

# we do need to run ninja from the same dir as this script, as it requires
# the bundled init-tiny.el and publish.el
this_dir = Path(__file__).parent.resolve()
os.chdir(this_dir)

# you can reconfigure the below two paths for your setup.
# In my case:
# 1. this resolves to pkb4000: the top-level of my org-mode database
org_dir = Path(args.org_dir).resolve()
# 2. this is the destination hugo site SECTION, e.g. hugo-site/content/posts/ OR the obsidian vault
out_dir = Path(args.out_dir).resolve()

# we need to determine the hugo site dir based on the specified section dir
# ox-hugo has some logic that relies on the "content/<something>" convention
try:
    # find last occurrence of "content" -- everything before that is hugo-site dir
    ci = next((i for i in range(len(out_dir.parts)-1,-1,-1) if out_dir.parts[i] == 'content'))
except StopIteration:
    print("Your out_dir argument should contain the 'content' path component, e.g. hugo_site/content/posts/")
    exit()

hugo_dir = Path(*out_dir.parts[0:ci])

files = org_dir.rglob("*.org")

post_proc = " && sed -i 's/{{< relref \"\([^\"]*\)\" >}}/\\1/g' $out" if args.obsidian else ""

# we create build.ninja right here in org_dir/braindump4000/
with Path("build.ninja").open("w") as ninja_file:
    ninja_file.write(
        f"""
rule org2md
  command = emacs --batch -l init-tiny.el -l publish.el --eval \"(cpb/publish \\"{org_dir}\\" \\"$in\\" \\"{hugo_dir}\\" \\"$out\\" )\"{post_proc}
  description = org2md $in
"""
    )

    for f in files:
        rf = f.relative_to(org_dir)
        output_file = out_dir / rf.with_suffix(".md")
        ninja_file.write(
            f"""
build {output_file}: org2md {org_dir / rf}
"""
        )

import subprocess

#subprocess.call(["ninja"])
