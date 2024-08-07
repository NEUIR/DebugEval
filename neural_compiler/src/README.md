# Install

Install dependencies:

```sh
conda create -n your_env_name python==3.10
conda activate your_env_name
pip install -r requirements.txt
cd DebugEval
```

# Configuration

Some package versions are as follows:

```sh
torch 1.13.1 + cu117 
transformers 4.36.2 
deepspeed 0.13.0 
gcc 9.5 
```

# Fine-tune

Change the dir: `cd neural_compiler\src\scripts`

Change the parameters of `neural_compiler/src/scripts/fine-tune-deepseek-coder.sh` then execute the file

Run the following command: `bash fine-tune-deepseek-coder.sh` 

The bash file contains:

```bash
DATA_PATH="Data\train\fine-tune-data" 
OUTPUT_PATH={your output path}
MODEL_PATH={your model path}
DS_CONFIG="ds_config_deepseek_coder.json"
deepspeed --include=localhost:1,2 neural_compiler/src/finetune/fine-tune-deepseek-coder.py \
    --model_name_or_path $MODEL_PATH \
    --data_path $DATA_PATH \
    --output_dir $OUTPUT_PATH \
    --num_train_epochs 1 \
    --model_max_length 2048 \
    --per_device_train_batch_size 8 \
    --per_device_eval_batch_size 1 \
    --gradient_accumulation_steps 4 \
    --evaluation_strategy "no" \
    --save_strategy "epoch" \
    --save_steps 100 \
    --learning_rate 2e-5 \
    --warmup_steps 30 \
    --logging_steps 1 \
    --lr_scheduler_type "cosine" \
    --gradient_checkpointing True \
    --report_to "tensorboard" \
    --deepspeed $DS_CONFIG \
    --bf16 True \
    --use_lora True
```
