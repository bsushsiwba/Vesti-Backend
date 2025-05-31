cd SAM

python -m venv sam && source sam/bin/activate && pip install torch==2.5.1 && pip install packaging hydra-core scikit-learn wheel iopath onnxruntime rembg && pip install transformers==4.45.2 && pip install git+https://github.com/bsushsiwba/grounded-sam-pypi.git && python main.py