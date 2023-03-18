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


# get full names of the el scripts ninja will require
this_dir = Path(__file__).parent.resolve()
init_tiny_el = this_dir / "init-tiny.el"
publish_el = this_dir / "publish.el"
obs_postproc_py = this_dir / "obs_postproc.py"

#  ... as we will be creating build.ninja and everything else in the output dir
out_dir.mkdir(parents=True, exist_ok=True)
os.chdir(out_dir)


files = org_dir.rglob("*.org")

post_proc = f" && {obs_postproc_py} $out" if args.obsidian else ""

# we create build.ninja right here in org_dir/braindump4000/
with Path("build.ninja").open("w") as ninja_file:
    ninja_file.write(
        f"""
rule org2md
  command = emacs --batch -l {init_tiny_el} -l {publish_el} --eval \"(cpb/publish \\"{org_dir}\\" \\"$in\\" \\"{hugo_dir}\\" \\"$out\\" )\"{post_proc}
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
