#!/usr/bin/env python3

#%%
import argparse
from pathlib import Path
import re

# this is for testing
s = """

+++
title = "shelly-homekit firmware"
author = ["meepzen3"]
date = 2022-03-05T16:36:00+02:00
draft = false
+++

Hello 

[Note-taking]({{< relref "note_taking.md" >}}), [Personal Knowledge Management]({{< relref "personal_knowledge_management.md" >}})

some more links

[Note-taking]({{< relref "note_taking.md#my-anchor" >}}), [Personal Knowledge Management]({{< relref "personal_knowledge_management.md" >}})

some more bleh bleh

{{< figure src="/ox-hugo/2022-12-31_16-17-19_screenshot.png" caption="<span class=\"figure-number\">Figure 2: </span>Random drop-outs in graph below. At least finished strong in last week of year." >}}

## what about pandoc {#what-about-pandoc}

Some text here about why not pandoc.


### Some title {#some-title}

Here we go again.


Another para.

## test section {#test-section}

Skip to [what about pandoc](#what-about-pandoc)

It should not rewrite links like this [google search](https://google.com#something)

"""

# https://regex101.com/ is your friend!
def transform(text):
    # replace whole hugo header with "# the title"
    # note the two strategically placed non-greedy *? operators else this will eat up additional example +++ blocks
    t2 = re.sub(r'^\s*\+\+\+.*?title = "([^"]+)".*?\+\+\+', "# \\1", text, flags=re.DOTALL)

    # 1. replace all relref links with "normal" [title](localfile) links
    # 2. In addition, work around Obsidian's silly lack of user-defined named anchor support:
    #    rewrite all links with anchors to `#^anchor` obs blockrefs; here we do only the relref (otherfile) ones
    #    See t35 next, and t5 below for the rest of this hack
    t3 = re.sub(r'{{< relref "([^"#]+)(#([^"]+))?" >}}', lambda m: m.group(1) + (f"#^{m.group(3)}" if m.group(3) else ''), t2)

    # here we rewrite all local [label](#anchor) to [label](#^anchor)
    t35 = re.sub(r'(\[[^]]+\])\(#([^)]+)\)', '\\1(#^\\2)', t3)

    # replace
    # {{< figure src="/ox-hugo/2022-12-31_16-17-19_screenshot.png" caption="<span class=\"figure-number\">Figure 2: </span>Random drop-outs in graph below. At least finished strong in last week of year." >}}
    # with
    # ![](static/ox-hugo/...)
    # BTW obsidian finds the figure even without any prepended path components, as long as it's in the vault
    # until we figure out a better scheme, we rewrite the path to be relative to the site / vault top-level
    t4 = re.sub('{{< figure src="/ox-hugo/([^"]+)".* >}}', '![](static/ox-hugo/\\1)', t35)

    # here we rewrite e.g. "## Some heading {#some-heading}" into "## Some heading\n^some-heading"
    # in other words, to work around Obsidian's disappointing lack of named anchor support we
    # use a ^block-marker, which means that we also  have to rewrite all links
    # (For obsidian, we would suggest either
    #  1. `<a name="my-named-anchor" />`,
    #  2. a setting to follow github convention in transforming "My Heading" into anchor name "my-heading" or
    #  3. supporting extended "# My heading {#my-heading}" markdown anchors.)
    t5 = re.sub(r'^( *#+ +[^{]+)\s+{#([^}]+)}', '\\1\n^\\2', t4, flags=re.MULTILINE)

    return t5

# uncomment when testing with cell-based execution
#print(transform(s))

#%%
def main():
    parser = argparse.ArgumentParser(description='perform obsidian post-processing on ox-hugo export')
    parser.add_argument('md_file', 
                        help='Markdown file that will be transformed in place')

    args = parser.parse_args()

    p = Path(args.md_file)

    text = p.read_text()
    t_text = transform(text)
    p.write_text(t_text)


if __name__ == "__main__":
    main()


