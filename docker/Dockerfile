# Base: NVIDIA PyTorch 24.01 (Matches CUDA 12.3 requirements for OF3)
FROM nvcr.io/nvidia/pytorch:24.01-py3 AS builder

ENV DEBIAN_FRONTEND=noninteractive

# --- STAGE 1: System Deps ---
RUN apt-get update && apt-get install -y \
    git \
    wget \
    kalign \
    aria2 \
    && rm -rf /var/lib/apt/lists/*

# --- STAGE 2: OpenFold-3 (Pinned) ---
WORKDIR /opt/openfold3
# Pinning to the Oct 2025 Preview Release (v0.3.1)
RUN git clone https://github.com/aqlaboratory/openfold-3.git . \
    && git checkout aeac5fd 

# Install OF3 Dependencies
RUN pip install --no-cache-dir .[cuequivariance]

# --- STAGE 3: AQAffinity (Pinned) ---
# Installing directly from SandboxAQ's official Hugging Face git source
RUN pip install --no-cache-dir \
    "git+https://huggingface.co/SandboxAQ/aqaffinity@main"

# --- STAGE 4: Runtime Setup ---
WORKDIR /app/pipeline

# We COPY the code at runtime or volume mount it to keep image small
# This ensures re-builds are fast when you change python logic
COPY requirements.txt /app/pipeline/requirements.txt
RUN pip install -r requirements.txt

# Entrypoint expects the volume mount at /app/data
ENTRYPOINT ["python", "scripts/run_pipeline.py"]
