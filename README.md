# DebugEval
## First we need to deploy the assessment model to the server.
cd DebugEval/src/serve
source source.sh
nohup bash serve_ckpt.sh model_path>serve.log 2>&1 &
## model evaluation
cd DebugEval/src/script
## for BUG Localization Task
(1) Inference
(2) Evaluate
## for BUG Identification Task
(1) Inference
(2) Evaluate
## for Code Review Task
(1) Inference
(2) Evaluate
## for Code Repair Task
(1) Inference
(2) Evaluate
### We use a self-designed OJ evaluation system to evaluate the generated code

# Fine-tune
# For DeepSeek-Coder-6.7B-Ins
cd .\SFT\neural_compiler\src\scripts
nohup bash fine-tune-deepseek-coder.sh>train.log 2>&1 &
# For Llama3-8B-Ins
cd .\SFT\LLaMA-Factory
nohup bash run.sh>train.log 2>&1 &
