# Introduce
We use the open source framework LLaMA-Factory (https://github.com/hiyouga/LLaMA-Factory) to train the Llama3-8B-Ins model. Please refer to LLaMA-Factory for relevant environment installation and configuration.

# Fine-tune

1) You need to put `Data/train/fine-tune-dataset.json` into the `LLaMA-Factory/data directory` and add a custom dataset name to `dataset_info.json`.

2) Put the `run.sh` file into the LLaMA-Factory directory, modify the file parameters in run.sh, and then execute the file.

    The bash file contains:
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
    ```
