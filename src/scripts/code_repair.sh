#export CUDA_VISIBLE_DEVICES=1,3
#model ['deepseek_FT_cot','deepseek_FT_no_cot','llama3_FT_cot','llama3_FT_no_cot',other model name]

python src/inference/main.py \
    --model "deepseek-6.7b" \
    --data_path "Data/eval/debugevalsuite_task3.jsonl" \
    --prompt_dir "DebugEval/src/prompts" \
    --output_dir "" \
    --task "code_repair" \
    --prompt_type "zero_shot" \
    --platform "all" \
    --n 1 \
    --temperature 0.2 \
    --top_p 0.95 \
    --max_tokens 1024