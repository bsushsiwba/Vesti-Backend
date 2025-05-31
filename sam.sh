#!/bin/bash

# Fail on error
set -e

# Clone repo
git clone https://github.com/bsushsiwba/vesti-backend-sam
cd vesti-backend-sam

# Create and activate venv
python -m venv sam
source sam/bin/activate

# Install dependencies
pip install --upgrade pip
pip install packaging hydra-core scikit-learn wheel iopath onnxruntime rembg
pip install transformers==4.45.2
pip install git+https://github.com/bsushsiwba/grounded-sam-pypi.git

# Set PYTHONPATH so that local modules can be found
export PYTHONPATH=$(pwd)

# Run the script
python main.py
