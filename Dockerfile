FROM python:3.10.12-slim

# Install required packages
RUN apt-get update && apt-get install -y \
    bash tmux && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy scripts to container
COPY sam.sh cat.sh idm.sh start-all.sh ./

# Make sure scripts are executable
RUN chmod +x sam.sh cat.sh idm.sh start-all.sh

# Run tmux-based script on container start
CMD ["bash", "start-all.sh"]
