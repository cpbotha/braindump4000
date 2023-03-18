#!/usr/bin/env python3

#%%
import argparse
from pathlib import Path
import re

# this is for testing
s = """+++
title = "shelly-homekit firmware"
author = ["meepzen3"]
date = 2022-03-05T16:36:00+02:00
draft = false
+++

Hello 

[Note-taking]({{< relref "note_taking.md" >}}), [Personal Knowledge Management]({{< relref "personal_knowledge_management.md" >}})

some more links

[Note-taking]({{< relref "note_taking.md" >}}), [Personal Knowledge Management]({{< relref "personal_knowledge_management.md" >}})

some more bleh bleh

{{< figure src="/ox-hugo/2022-12-31_16-17-19_screenshot.png" caption="<span class=\"figure-number\">Figure 2: </span>Random drop-outs in graph below. At least finished strong in last week of year." >}}

"""

def transform(text):
    # replace whole hugo header with "# the title"
    t2 = re.sub('\+\+\+.*title = "([^"]+)".*\+\+\+', "# \\1", text, flags=re.DOTALL)
    # replace all relref links with "normal" [title](localfile) links
    t3 = re.sub('{{< relref "([^"]+)" >}}', '\\1', t2)
    # replace
    # {{< figure src="/ox-hugo/2022-12-31_16-17-19_screenshot.png" caption="<span class=\"figure-number\">Figure 2: </span>Random drop-outs in graph below. At least finished strong in last week of year." >}}
    # with
    # ![](static/ox-hugo/...)
    # BTW obsidian finds the figure even without any prepended path components, as long as it's in the vault
    # until we figure out a better scheme, we rewrite the path to be relative to the site / vault top-level
    t4 = re.sub('{{< figure src="/ox-hugo/([^"]+)".* >}}', '![](static/ox-hugo/\\1)', t3)
    return t4


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


