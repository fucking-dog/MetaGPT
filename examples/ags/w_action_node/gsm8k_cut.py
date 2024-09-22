import numpy as np

import numpy as np
import json


def set_seed(seed=42):
    """
    设置随机种子以确保结果可重复。
    """
    np.random.seed(seed)


def split_jsonl(file_path, n_samples=264, seed=42):
    """
    将JSONL文件分割为训练集和测试集。

    参数：
    - file_path: JSONL文件的路径。
    - n_samples: 训练集的样本数量。
    - seed: 随机种子。

    返回：
    - train_data: 训练集数据列表。
    - test_data: 测试集数据列表。
    """
    # 设置随机种子
    set_seed(seed)

    # 读取JSONL文件
    with open(file_path, 'r', encoding='utf-8') as f:
        data = [json.loads(line) for line in f]

    n = len(data)
    indices = np.arange(n)

    # 打乱索引
    np.random.shuffle(indices)

    # 分割索引为训练集和测试集
    train_indices = indices[:n_samples]
    test_indices = indices[n_samples:]

    # 根据索引获取数据
    train_data = [data[i] for i in train_indices]
    test_data = [data[i] for i in test_indices]

    return train_data, test_data


def save_jsonl(data, output_path):
    """
    将数据保存为JSONL文件。

    参数：
    - data: 数据列表。
    - output_path: 输出文件路径。
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        for entry in data:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')


# 使用示例
file_path = r"D:\PythonProject\MetaGPT-MathAI\examples\ags\w_action_node\data\gsm8k.jsonl"
n_samples = 264  # 设置训练集样本数

# 分割数据
train_data, test_data = split_jsonl(file_path, n_samples=n_samples, seed=42)

# 保存分割后的数据（可选）
save_jsonl(train_data, 'gsm8k_validation.jsonl')
save_jsonl(test_data, 'gsm8k_test.jsonl')

print(f"训练集样本数: {len(train_data)}")
print(f"测试集样本数: {len(test_data)}")
