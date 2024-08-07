# 🕷️DebugEval 
Official repository for the paper "Enhancing the Code Debugging Ability of LLMs via
Communicative Agent Based Data Refinement".

<p align="center">
    <a href="">📜 Paper</a> •
    <a href="https://drive.google.com/file/d/1f7WbR4W_3PwLhLgQWi_0ftegmhXEUMgO/view?usp=drive_link">🤗 Data </a> •
    <a href="https://drive.google.com/file/d/1Xk-qni-o-HXPHXlBfMBby-tp_2MvTMYe/view?usp=drive_link">🤖 Model </a> •
</p>

## 1. Introduction
This paper presents a benchmark, DebugEval, which is used to evaluate the code debugging ability of LLMs (Large Language Models) and proposals a framework for building training data using multiple agents, MASTER.

### 1.1 Benchmark
#### DebugEval designs four task scenarios: BUG Localization, BUG Identification, Code Repair, and Code Review to comprehensively evaluate the code debugging capability of LLMs.

![image](https://github.com/NEUIR/DebugEval/blob/main/Figure/benchmark_00.png)
### 1.2 MASTER
#### MASTER is a framework for making use of multiple agents working together to refine training data to improve code debugging capability in LLMs.

![image](https://github.com/NEUIR/DebugEval/blob/main/Figure/model%20picture_00.png)
## 2. Installation
You can clone the repository using the following command:

```
git clone DebugEval
cd DebugEval
```

## 3. Inference and Evaluation
Download the dataset we provide.

```
cd src
```
Please refer to `src/README.md` for more details.
## 4. Fine-Tuning
We use DeepSeek-Coder-6.7B-Ins and Llama3-8B-Ins as the base model, and train the models with MASTER framework.

### 4.1 For DeepSeek-Coder-6.7B-Ins
```
cd neural_compiler
```
Please refer to `neural_compiler/README.md` for more details.
### 4.2 For Llama3-8B-Ins
```
cd LLaMA-Factory
```
Please refer to `LLaMA-Factory/README.md` for more details.

We provide the trained NeuDebugger models.

## 5. Result

![image](https://github.com/NEUIR/DebugEval/blob/main/Figure/models%20performance_00.png)
## 6. Citation
Please cite the paper and star the repo if you use DebugEval and find it helpful.
```
@article{DebugEval2024,
      title={Enhancing the Code Debugging Ability of LLMs via Communicative Agent Based Data Refinement}, 
      author={},
      year={2024},
}
```
