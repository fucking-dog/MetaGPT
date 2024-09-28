import pandas as pd
import json

# 1. 读取Excel文件
# 假设Excel文件名为 'data.xlsx'，并且数据在第一个工作表中
df = pd.read_excel(r'C:\Users\13761\Downloads\humaneval.xlsx')

dataset = 'HumanEval'

# 2. 过滤“数据集”为“HumanEval”的记录
filtered_df = df[df['数据集'] == dataset]

# 3. 选择所需列
selected_columns = [
    '方法', '模型', '模型-其他-补充内容',
    '数据集', 'Performance',
    '数据集Settings', '生成文件', 'Total Cost'
]
filtered_df = filtered_df[selected_columns]

# 4. 分组汇总并计算统计量
grouped = filtered_df.groupby(['方法', '模型'])

# 创建一个字典来存储结果
result = {}

for (method, model), group in grouped:
    key = f"{method} - {model}"
    if key not in result:
        result[key] = {
            '方法': method,
            '模型': model,
            '数据集': dataset,
            'Performance': group['Performance'].tolist(),
            'Performance_stats': {
                'avg': group['Performance'].mean(),
                'std': group['Performance'].std() if len(group) > 1 else None
            },
            '数据集Settings': group['数据集Settings'].dropna().unique().tolist(),
            'Total Cost': group['Total Cost'].tolist(),
            'Total Cost_stats': {
                'avg': group['Total Cost'].mean(),
                'std': group['Total Cost'].std() if len(group) > 1 else None
            }
        }

# 5. 将结果写入JSON文件
output_filename = 'data_result.json'  # 可以根据需要更改文件名
with open(output_filename, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)

print(f"数据已成功保存到 {output_filename}")



