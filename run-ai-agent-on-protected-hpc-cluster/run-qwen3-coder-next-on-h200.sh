#!/bin/bash
#SBATCH --job-name=run-qwen3-coder-next-on-h200
#SBATCH --nodes=1
#SBATCH --account=rai-gpu-rw
#SBATCH --partition=rai-gpu-rw
#SBATCH --time=7-00:00:00        # Request 7 days
#SBATCH --gres=gpu:h200:1
#SBATCH --cpus-per-task=16       # Multiple CPUs for snappy model loading and prompt processing
#SBATCH --mem=128G               # System RAM (separate from GPU VRAM)
#SBATCH --nodelist=rw236
#SBATCH --output=run-qwen3-coder-next-on-h200.log
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=peterm@genetics.utah.edu

# the above config is appropriate for https://ollama.com/library/qwen3-coder-next:q8_0
# c.f., https://gemini.google.com/share/90c73e1c3bb9

module load ollama 

export OLLAMA_CONTEXT_LENGTH=128000 

# https://www.chpc.utah.edu/documentation/software/genai.php#ollamamodels
export OLLAMA_MODELS="/scratch/ucgd/lustre-labs/quinlan/data-shared/ollama-models" 

ollama serve

