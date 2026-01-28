---
name: calculate-code-lines
description: calculate the whole code lines for a project, the code is not include the html, css, xml，txt, etc, only for the pure programming languages's code, which include all the main type code languages.
---

# Colculate Code Lines
To calculate the code lines for current project. The code should be one of the main programming languages (e.g. `java`, `python`， `javascript`, `typescript`, `go`, `C++`, `kotlin`, etc.)

## When to use the skill
- The prompt should include the key words, like "Calculate code lines", "code lines" or the same mean with different nature languages, like Chinese "代码总数", "代码行数".

## How to use it
Calculate the code lines for the current whole project, like **mapleway**, when this skill is triggered, use the script `.\agent\skills\calculate-code-lines\scripts\code_counter.py` to calculate the code lines.
