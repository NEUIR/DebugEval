# Requirements

Install dependencies:

```sh
conda create -n your_env_name python==3.10
conda activate your_env_name
pip install vllm==0.2.7
cd DebugEval/src
```

# Inference and Evaluation of DebugEval

## 1.Deploy the LLM to be evaluated

We use vLLM to deploy the LLM we are going to evaluate, and we will call this model in subsequent tests. In our experiments, 2✖️80G A800 are used for the deployment 7B model and 4✖️80G A800 are used for the deployment 70B model.

Here's the deployment command, replace {your_model_path} with your model path.

```bash
cd DebugEval/src/serve
source source.sh
nohup bash serve_ckpt.sh {your_model_path} > serve.log 2>&1 &
```

## 2. Inference and Evaluation

First, change the directory: `cd DebugEval/src/script`

For different tasks, use the following command to test.

### 2.1 BUG Localization Task
#### (1) Inference Stage

Run the following command: `bash error_code_localization.sh` 

The bash file contains:

```sh
python src/inference/main.py \
    --model "deepseek-6.7b" \
    --data_path "Data/eval/debugevalsuite_task124.jsonl" \
    --prompt_dir "DebugEval/src/prompts" \
    --output_dir "" \
    --task "error_code_localization" \
    --prompt_type "zero_shot" \
    --platform "all" \
    --n 1 \
    --temperature 0.2 \
    --top_p 0.95 \
    --max_tokens 1024
```

#### (2) Evaluate Stage

Run the `bug_loc_calculate_acc.py` file and change the corresponding data and results path.

### 2.2 BUG Identification Task
#### (1) Inference Stage

Run the following command: `bash error_type_identification.sh` 

The bash file contains:

```sh
python src/inference/main.py \
    --model "deepseek-6.7b" \
    --data_path "Data/eval/debugevalsuite_task124.jsonl" \
    --prompt_dir "DebugEval/src/prompts" \
    --output_dir "" \
    --task "error_type_identification" \
    --prompt_type "zero_shot" \
    --platform "all" \
    --n 1 \
    --temperature 0.2 \
    --top_p 0.95 \
    --max_tokens 1024
```

#### (2) Evaluate Stage

Run the `bug_iden_calculate_acc.py` file and change the corresponding data and results path.

### 2.3 Code Repair Task
#### (1) Inference Stage

Run the following command: `bash code_repair.sh` 

The bash file contains:

```sh
python src/inference/main.py \
    --model "deepseek-6.7b" \
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
```

#### (2) Evaluate Stage
We use a self-designed OJ evaluation system to evaluate the generated code.
1) You must put the Input and Output folders in the `Data\test_cases` directory into the `OJ_Evaluation\atcoder_code_error_judge` directory.

2) The results of model inference are processed in the following form:

```yaml
  atcoder_code_error_judge
│  
├─Python_Code
│  ├─abc331_a
│  │   response.py
│  │      
│  ├─abc331_b
│  │   response.py
│  │
├─Cpp_Code
│  ├─abc331_a
│  │   response.cpp
│  │      
│  ├─abc331_b
│  │   response.cpp
│  │
├─Java_Code
│  ├─abc331_a
│  │   Main.java
│  │      
│  ├─abc331_b
│  │   Main.java
│  │
├─Input
│          
└─Output
```

2) Adjust the parameters in `OJ_Evaluate\CodeError_judger-main\config.yml` and then run pattern2.py.

```yaml
# Use parameters in config.yml or in command
use_config: True # Use parameters in config.yml when it's true, use parameters in command when it's false

# Pattern1: For one problem testing
problem_name: "abc275_A" # the problem you want to test
multi_code_dir: D:/_Code_/ABC Data/codes of one user/abc275_A  # one problem, many code for the problem

# Pattern2: For multi-problem testing
code_dir: OJ_Evaluate/atcoder_code_error_judge/code  # many problems, many code for each problem

# All the input and output data
input_dir: OJ_Evaluate/atcoder_code_error_judge/Input
answer_dir: OJ_Evaluate/atcoder_code_error_judge/Output

# timeLimit and memoryLimit for all problems
timeLimit: 10        # seconds
memoryLimit: 1024    # MBs
showDetails: False   # Whether to display the results of each test point
```

3) Run the `code_rep_calculate_acc.py` file and change the corresponding data and results path.
   
4) For the Python data, you can also choose to use our multi-threaded evaluation system, speed up evaluation.
  
  ```sh
  cd src/code_repair_eval_python
  python check.py
  ```

  You just need to change the data path in the `check.py` file.

### 2.4 Code Review Task

#### (1) Inference Stage

Run the following command: `bash code_review.sh` 

The bash file contains:

```sh
python src/inference/main.py \
    --model "deepseek-6.7b" \
    --data_path "Data/eval/debugevalsuite_task124.jsonl" \
    --prompt_dir "DebugEval/src/prompts" \
    --output_dir "" \
    --task "code_review" \
    --prompt_type "zero_shot" \
    --platform "all" \
    --n 1 \
    --temperature 0.2 \
    --top_p 0.95 \
    --max_tokens 1024
```

Run the following command: `bash code_review_reversh.sh` 

```sh
python src/inference/main.py \
    --model "deepseek-6.7b" \
    --data_path "Data/eval/debugevalsuite_task124.jsonl" \
    --prompt_dir "DebugEval/src/prompts" \
    --output_dir "" \
    --task "code_review_reverse" \
    --prompt_type "zero_shot" \
    --platform "all" \
    --n 1 \
    --temperature 0.2 \
    --top_p 0.95 \
    --max_tokens 1024
```

#### (2) Evaluate Stage

Run the `code_rev_calculate_acc.py` file and change the corresponding data and results path.
