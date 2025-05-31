#!/bin/bash

# Start tmux session in detached mode
tmux new-session -d -s multisession

# First pane: sam.sh
tmux send-keys -t multisession "bash sam.sh" C-m

# Split horizontally and run cat.sh
tmux split-window -h -t multisession
tmux send-keys -t multisession:0.1 "bash cat.sh" C-m

# Split vertically and run idm.sh
tmux split-window -v -t multisession:0.1
tmux send-keys -t multisession:0.2 "bash idm.sh" C-m

# Attach to the session so user sees it
tmux attach -t multisession
