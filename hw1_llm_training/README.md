# GPT-2 语言模型训练与应用

## 项目概述

本项目实现了基于GPT-2架构的语言模型训练和生成文本的功能。项目使用Hugging Face的Transformers库，在自定义数据集上对GPT-2模型进行微调，并提供了便捷的文本生成接口。

### 主要功能

1. **数据处理**：支持从本地文本、JSON文件或Hugging Face数据集加载和预处理文本数据
2. **模型训练**：提供完整的GPT-2模型训练流程，支持断点续训和参数调整
3. **文本生成**：训练后的模型可用于文本生成，支持单次生成和批量生成
4. **训练监控**：使用Weights & Biases（WandB）进行训练过程监控和可视化

## 项目结构

```
.
├── dataset.py         # 数据集加载与预处理
├── generate.py        # 文本生成功能
├── gpt2_tokenizer/    # GPT-2分词器
├── logs/              # 训练日志和检查点
├── model.py           # 模型定义
├── requirements.txt   # 项目依赖
├── train.py           # 训练脚本
└── wandb/             # WandB日志
```

## 数据集

1. 克隆或下载此仓库到你的本地机器。

   ```bash
   git clone git@github.com:Zhuangjizzz/llm4eda.git
   cd hw1_llm_training
   ```
2. 运行以下Python脚本：

    ```bash
    python download_dataset.py
    ```

这将开始下载数据集，并显示下载进度。脚本会获取以下数据集：

- webtext
- small-117M
- medium-345M
- large-762M
- xl-1542M

每个数据集都被分为以下部分：`train`、`valid` 和 `test`。下载的文件将以 `.jsonl` 格式存储在 `data` 文件夹中。

更多详情，请参考以下链接：[gpt-2-output-dataset](https://github.com/openai/gpt-2-output-dataset.git)

数据集采用JSONL格式，适用于自回归语言模型训练。

## 核心模块

### 1. 数据处理 (dataset.py)

数据处理模块负责加载并预处理数据集，主要功能：

- 支持加载本地文本文件(.txt)或JSON文件(.json/.jsonl)
- 支持直接加载Hugging Face Hub上的数据集
- 使用GPT2TokenizerFast进行高效分词
- 将文本划分为固定长度的块，适用于语言模型训练
- 自动划分训练集和验证集

使用方法：

```python
tokenizer, train_dataset, val_dataset = get_dataset_and_tokenizer(
    dataset_name="small",
    dataset_path="/path/to/dataset/",
    val_split=0.05,
    block_size=128
)
```

### 2. 模型定义 (model.py)

模型模块定义了GPT-2架构的语言模型，支持自定义参数：

- 嵌入维度 (n_embd)
- 层数 (n_layer)
- 注意力头数 (n_head)
- 词表大小 (vocab_size)

使用方法：

```python
model = get_model(
    n_embd=768,
    n_layer=12,
    n_head=12,
    vocab_size=50257
)
```

### 3. 训练流程 (train.py)

训练模块实现了完整的模型训练流程：

- 支持从检查点恢复训练
- 使用WandB监控训练进度
- 自动保存检查点
- 训练后进行模型评估

训练参数：
- 训练轮数：3-5轮
- 批量大小：2
- 学习率：5e-5
- 权重衰减：0.01
- 预热步数：500
- 使用FP16精度加速训练

### 4. 文本生成 (generate.py)

文本生成模块提供了两种生成文本的方法：

1. **单次生成**：使用`model.generate()`方法生成单个文本序列
2. **批量生成**：使用`pipeline`生成多个不同的文本序列

生成参数支持调整：
- 最大生成长度
- top-k 和 top-p 采样
- 温度参数
- 返回序列数量

使用方法：

```python
# 单次生成
result = generate_once(
    tokenizer, model, device,
    prompt="Once upon a time",
    max_new_tokens=100,
    top_k=30,
    top_p=0.8,
    temperature=1.0
)

# 批量生成
choices = generate_batch(
    tokenizer, model, device,
    prompt="In a distant future, humanity has",
    max_length=100,
    num_return_sequences=3,
    top_p=0.8
)
```

## 使用指南

### 环境准备

安装所需依赖：

```bash
pip install -r requirements.txt
```

主要依赖包括：
- transformers
- datasets
- torch
- wandb
- openai
- langchain
- numpy
- matplotlib

### 训练模型

执行以下命令开始训练：

```bash
python train.py
```

训练参数可在脚本内调整。训练过程会自动保存检查点到`logs/`目录。

### 生成文本

使用训练好的模型生成文本：

```bash
python generate.py
```
训练完成后，您可以使用 `generate.py` 脚本通过训练好的模型生成文本：
```bash
python generate.py --model_path ./logs/final_model --length 100
```
这将基于训练好的模型生成100个标记的序列。

默认使用`logs/final_model`目录中的模型，可以通过修改`generate.py`中的`model_directory`变量来使用其他检查点。

## 训练监控

项目使用WandB（Weights & Biases）进行训练监控，训练日志存储在`wandb/`目录中。在离线模式下，可以查看基本的训练指标；如需在线同步，请修改环境变量`WANDB_MODE`。

## 项目扩展方向

1. **扩展数据源**：支持更多数据源和格式
2. **增加评估指标**：实现BLEU、ROUGE等生成文本评估指标
3. **模型量化**：支持INT8/INT4量化以减小模型体积
4. **增加对比实验**：比较不同参数和数据集的训练效果
5. **Web演示界面**：构建简单的Web界面进行在线文本生成演示

## 注意事项

- 训练需要GPU加速，建议使用CUDA环境
- 数据集路径需要根据实际环境调整
- 训练参数如批量大小、学习率等可根据GPU内存和数据集规模进行调整
