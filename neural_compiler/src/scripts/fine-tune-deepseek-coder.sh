DATA_PATH="Data/train/fine-tune-data" 
OUTPUT_PATH=""
MODEL_PATH="" 
DS_CONFIG="neural_compiler\src\finetune\zero2.json""
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