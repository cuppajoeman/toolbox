#!/bin/bash

xfce4-terminal --maximize --title='knowledge book' -x bash -c "cd ~/knowledge-book; nvim book.tex; exec bash"

# ... then (these will open as child tabs in the parent terminal window, above):

xfce4-terminal --tab --title='creating'  -x bash -c "cd ~/knowledge-book; python scripts/creator.py -h;  exec bash"
xfce4-terminal --tab --title='finding'  -x bash -c "cd ~/knowledge-book; python scripts/finder.py -h;  exec bash"
