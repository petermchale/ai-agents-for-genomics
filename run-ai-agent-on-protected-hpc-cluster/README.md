# How to run the a coding agent on a protected HPC cluster 

## Run a 80B-parameter open-source coding LLM on a H200 GPU compute node

1. Determine whether GPUs are available on compute node `rw236` (say) by issuing `scontrol show node rw236` and looking for: 
* CfgTRES: The total resources configured on the node (e.g., gres/gpu=4).
* AllocTRES: The resources currently allocated to running jobs. If you see gres/gpu=2, it means 2 GPUs are taken and the rest are free.
* GresUsed: This often lists the specific indices (e.g., gpu:2(IDX:0-1)) so you know exactly which physical cards are busy.
2. Submit a batch job to run `ollama` on the H200 with enough resources to accommodate `qwen3-coder-next`: 
```
sbatch run-qwen3-coder-next-on-h200.sh
``` 
3. Confirm the ollama server is running by inspecting its logs (`run-qwen3-coder-next-on-h200.log`), and then download `qwen3-coder-next:q8_0` as follows:
```
salloc --nodes=1 --ntasks=1 --account=rai-gpu-rw --partition=rai-gpu-rw --time=1:00:00 --nodelist=rw236
module load ollama 
export OLLAMA_MODELS="/scratch/ucgd/lustre-labs/quinlan/data-shared/ollama-models" 
ollama pull qwen3-coder-next:q8_0 
```
4. One can monitor GPU and CPU usage at https://portal.chpc.utah.edu/

## Connect the H200 node to an agent node

1. Log into an interactive node and start a named `tmux` session:
```
tmux new -s reverse_ssh_tunnel
```
2. Request an allocation on the H200 node, by running: 
```
salloc --nodes=1 --ntasks=1 --account=rai-gpu-rw --partition=rai-gpu-rw --time=7-00:00:00 --nodelist=rw236
```     
3. Set up a reverse ssh tunnel from the H200 node to the agent node (the interactive machine you wish to run the coding agent on; `father` in this example): 
```
ssh -f -N -R 11434:localhost:11434 father
```
4. To leave the ssh tunnel running, and log out of the H200 node, press `Ctrl + b`, then let go and press `d`. You are now back on the interactive node's "bare" shell. The allocation, and therefore the tunnel between the H200 node and the agent node, will stay active, even if you logout of the interactive node. 
5. Check that the connection was successful by running, on the agent node: 
```
echo $(curl localhost:11434 2> /dev/null)
```
which should give: 
```
Ollama is running
```
6. When you log back into the interactice node running the `tmux` session, you can jump right back into your session:
```
tmux attach -t reverse_ssh_tunnel
```
At this point, one can kill the background ssh process on the H200 node: 
```
pgrep -f "ssh.*11434" | xargs kill
```

## Install, configure, and run Pi coding agent on the "agent node"

https://buildwithpi.ai

1. Download Node.js (https://nodejs.org/en/download), using the Linux instructions, reproduced here as of Feb 10, 2026:
```
# Download and install nvm:
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash

# In lieu of restarting the shell
\. "$HOME/.nvm/nvm.sh"

# Download and install Node.js:
nvm install 24

# Verify the Node.js version:
node -v # Should print "v24.13.1".

# Verify npm version:
npm -v # Should print "11.8.0".
```
3. Install Pi, without `-g` option (https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent#quick-start):
  ```
  npm install @mariozechner/pi-coding-agent
  ```
3. Add Pi CLI entry point to `PATH`:
```
export PATH="$HOME/node_modules/.bin:$PATH"
```
4. Open and close `pi` to establish the directory structure required for configuration (see next step)
```
pi # followed by ctrl-d to shut down
```

5. Configure `pi` to use `qwen3-coder-next:q8_0` by pasting the following into `$HOME/.pi/agent/models.json` (from: https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/models.md#full-example)
```
{
  "providers": {
    "ollama": {
      "baseUrl": "http://localhost:11434/v1",
      "api": "openai-completions",
      "apiKey": "ollama",
      "models": [
        {
          "id": "qwen3-coder-next:q8_0",
          "name": "qwen3-coder-next:q8_0 (Local)",
          "reasoning": false,
          "input": ["text"],
          "contextWindow": 128000,
          "maxTokens": 32000,
          "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
        }
      ]
    }
  }
}
```
6. Run the agent by typing `pi` at the command line. Your coding agent should now be connected to `qwen3-coder-next:q8_0`. 
