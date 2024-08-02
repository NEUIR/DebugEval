# DebugEval
## First we need to deploy the assessment model to the server.
cd DebugEval/src/serve
source source.sh
nohup bash serve_ckpt.sh your_model_path>serve.log 2>&1 &
## model evaluation
cd DebugEval/src/script
### for BUG Localization Task
(1) Inference

    #export CUDA_VISIBLE_DEVICES=1,3
    #model ['deepseek_FT_cot','deepseek_FT_no_cot','llama3_FT_cot','llama3_FT_no_cot',other model name]
    python src/inference/main.py \
        --model "deepseek-6.7b" \
        --data_path "debugevalsuite_task124.jsonl" \
        --prompt_dir "src/prompts" \
        --output_dir "Your_output_path" \
        --task "error_code_localization" \
        --prompt_type "zero_shot" \
        --platform "all" \
        --n 1 \
        --temperature 0.2 \
        --top_p 0.95 \
        --max_tokens 1024
        
    execute nohup bash error_code_localization.sh 
    
(2) Evaluate
    Run the code by changing the data path in the ".\bug_loc_calculate_acc.py" file.
### for BUG Identification Task
(1) Inference

    #export CUDA_VISIBLE_DEVICES=1,3
    #model ['deepseek_FT_cot','deepseek_FT_no_cot','llama3_FT_cot','llama3_FT_no_cot',other model name]
    python src/inference/main.py \
        --model "deepseek-6.7b" \
        --data_path "debugevalsuite_task124.jsonl" \
        --prompt_dir "src/prompts" \
        --output_dir "Your_output_path" \
        --task "error_type_identification" \
        --prompt_type "zero_shot" \
        --platform "all" \
        --n 1 \
        --temperature 0.2 \
        --top_p 0.95 \
        --max_tokens 1024
        
    execute nohup bash error_type_identification.sh

(2) Evaluate
    Run the code by changing the data path in the ".\bug_iden_calculate_acc.py" file.
### for Code Review Task
(1) Inference

    #export CUDA_VISIBLE_DEVICES=1,3
    #model ['deepseek_FT_cot','deepseek_FT_no_cot','llama3_FT_cot','llama3_FT_no_cot',other model name]
    python src/inference/main.py \
        --model "deepseek-6.7b" \
        --data_path "debugevalsuite_task124.jsonl" \
        --prompt_dir "src/prompts" \
        --output_dir "Your_output_path" \
        --task "code_review" \
        --prompt_type "zero_shot" \
        --platform "all" \
        --n 1 \
        --temperature 0.2 \
        --top_p 0.95 \
        --max_tokens 1024

    execute nohup bash code_review.sh

    #export CUDA_VISIBLE_DEVICES=1,3
    #model ['deepseek_FT_cot','deepseek_FT_no_cot','llama3_FT_cot','llama3_FT_no_cot',other model name]
    python src/inference/main.py \
        --model "deepseek-6.7b" \
        --data_path "debugevalsuite_task124.jsonl" \
        --prompt_dir "src/prompts" \
        --output_dir "Your_output_path" \
        --task "code_review_reverse" \
        --prompt_type "zero_shot" \
        --platform "all" \
        --n 1 \
        --temperature 0.2 \
        --top_p 0.95 \
        --max_tokens 1024

    execute nohup bash code_review_reversh.sh

(2) Evaluate
    Run the code by changing the data path in the ".\code_rev_calculate_acc.py" file.
### for Code Repair Task
(1) Inference

    #export CUDA_VISIBLE_DEVICES=1,3
    #model ['deepseek_FT_cot','deepseek_FT_no_cot','llama3_FT_cot','llama3_FT_no_cot',other model name]
    python src/inference/main.py \
        --model "llama3_FT_cot" \
        --data_path "debugevalsuite_task3.jsonl" \
        --prompt_dir "src/prompts" \
        --output_dir "Your_output_path" \
        --task "code_repair" \
        --prompt_type "zero_shot" \
        --platform "all" \
        --n 1 \
        --temperature 0.2 \
        --top_p 0.95 \
        --max_tokens 1024

    execute nohup bash code_repair.sh
    
(2) Evaluate
#### We use a self-designed OJ evaluation system to evaluate the generated code.
#### Due to the large number of test cases of the original data, we could not upload such a large file, so we sample 40 pieces of data and keep their test cases for everyone to test, The full test case will be open sourced to Github.. 
1) The results of model inference are processed in the following form
    ```
      atcoder_code_error_judge
    │  
    ├─Python_Code
    │  ├─problem_id abc331_a
    │  │   response.py
    │  │      
    │  ├─problem abc331_b
    │  │   response.py
    │  │
    ├─Cpp_Code
    │  ├─problem_id abc331_a
    │  │   response.cpp
    │  │      
    │  ├─problem abc331_b
    │  │   response.cpp
    │  │
    ├─Java_Code
    │  ├─problem_id abc331_a
    │  │   Main.java
    │  │      
    │  ├─problem abc331_b
    │  │   Main.java
    │  │
    ├─Input
    │          
    └─Output
    ```

3) Adjust the parameters in ".\oj\ CodeError_judger-main \config.yml" and then run pattern2.py.

    ```yml
    # Use parameters in config.yml or in command
    use_config: True # Use parameters in config.yml when it's true, use parameters in command when it's false
    
    # Pattern1: For one problem testing
    problem_name: "abc275_A" # the problem you want to test
    multi_code_dir: D:/_Code_/ABC Data/codes of one user/abc275_A  # one problem, many code for the problem
    
    # Pattern2: For multi-problem testing
    code_dir: ./atcoder_code_error_judge/code  # many problems, many code for each problem
    
    # All the input and output data
    input_dir: ./atcoder_code_error_judge/Input
    answer_dir: ./atcoder_code_error_judge/Output
    
    # timeLimit and memoryLimit for all problems
    timeLimit: 10        # seconds
    memoryLimit: 1024    # MBs
    showDetails: False  # Whether to display the results of each test point
    ```
4) Run the code by changing the data path in the ".\code_rep_calculate_acc.py" file.

# Fine-tune
## For DeepSeek-Coder-6.7B-Ins
cd .\SFT\neural_compiler\src\scripts
```bash
DATA_PATH="fine-tune-data" 
OUTPUT_PATH=""
MODEL_PATH="" 
DS_CONFIG="ds_config_deepseek_coder.json"
deepspeed --include=localhost:1,2 src/finetune/fine-tune-deepseek-coder.py \
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
execute nohup bash fine-tune-deepseek-coder.sh>train.log 2>&1 &
```
## For Llama3-8B-Ins
cd .\SFT\LLaMA-Factory
```bash
CUDA_VISIBLE_DEVICES=2,3  llamafactory-cli train \
    --stage sft \
    --do_train \
    --model_name_or_path MODEL_PATH \
    --dataset  your_data_name\
    --dataset_dir LLaMA-Factory/data \
    --template llama3 \
    --finetuning_type lora \
    --lora_target all \
    --output_dir  Your_output_path\
    --overwrite_cache \
    --overwrite_output_dir \
    --cutoff_len 2048 \
    --preprocessing_num_workers 16 \
    --per_device_train_batch_size 8 \
    --gradient_accumulation_steps 4 \
    --lr_scheduler_type cosine \
    --logging_steps 1 \
    --warmup_steps 30 \
    --save_steps 100 \
    --save_strategy "epoch" \
    --evaluation_strategy "no" \
    --learning_rate 2e-5 \
    --num_train_epochs 1.0 \
    --val_size 0 \
    --plot_loss \
    --fp16
execute nohup bash run.sh>train.log 2>&1 &
```
