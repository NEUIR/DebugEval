# DebugEval
## First we need to deploy the assessment model to the server.
cd DebugEval/src/serve
source source.sh
nohup bash serve_ckpt.sh your_model_path>serve.log 2>&1 &
## model evaluation
cd DebugEval/src/script
## for BUG Localization Task
(1) Inference
    nohup bash error_code_localization.sh
(2) Evaluate
    Run the code by changing the data path in the ".\bug_loc_calculate_acc.py" file.
## for BUG Identification Task
(1) Inference
    nohup bash error_type_identification.sh
(2) Evaluate
    Run the code by changing the data path in the ".\bug_iden_calculate_acc.py" file.
## for Code Review Task
(1) Inference
    nohup bash code_review.sh

    nohup bash code_review_reversh.sh
    
(2) Evaluate
    Run the code by changing the data path in the ".\code_rev_calculate_acc.py" file.
## for Code Repair Task
(1) Inference
    nohup bash code_repair.sh
    
(2) Evaluate
### We use a self-designed OJ evaluation system to evaluate the generated code
#### Due to the large number of test cases of the original data, we could not upload such a large file, so we sample half of the data and keep their test cases for everyone to test. 
1) The results of model inference are processed in the following form
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
3) Adjust the parameters in ".\oj\ CodeError_judger-main \config.yml" and then run pattern2.py.
4) Run the code by changing the data path in the ".\code_rep_calculate_acc.py" file.

# Fine-tune
# For DeepSeek-Coder-6.7B-Ins
cd .\SFT\neural_compiler\src\scripts
nohup bash fine-tune-deepseek-coder.sh>train.log 2>&1 &
# For Llama3-8B-Ins
cd .\SFT\LLaMA-Factory
nohup bash run.sh>train.log 2>&1 &
