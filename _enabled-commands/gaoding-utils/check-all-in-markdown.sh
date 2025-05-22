#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title check all in markdown
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 🤖
# @raycast.needsConfirmation false

# Documentation:
# @raycast.description Check all todo list in markdown
# @raycast.author wujunchuan
# @raycast.authorURL https://raycast.com/wujunchuan

pbpaste | sed 's/\[ \]/[x]/g' | pbcopy