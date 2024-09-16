import pandas as pd
import glob

# 设置文件路径（假设所有 CSV 文件在同一个目录下）
file_path = r'D:\PythonProject\MetaGPT-MathAI\examples\ags\w_action_node\answer\*.csv'  # 请替换为你的实际路径

# 读取所有 CSV 文件
all_files = glob.glob(file_path)
df_list = [pd.read_csv(file) for file in all_files]

# 获取文件的总行数（假设所有文件的行数都相同）
num_rows = len(df_list[0])

# 初始化一个包含零的计数列表用于统计每个索引的score为0的次数
zero_counts = [0] * num_rows

# 遍历所有文件的每一行，统计score为0的次数
for df in df_list:
    for idx in range(num_rows):
        if df.loc[idx, 'score'] == 0:
            zero_counts[idx] += 1

# 创建一个DataFrame来存储索引和对应的零计数
index_counts = pd.DataFrame({'index': range(num_rows), 'zero_count': zero_counts})

# 根据零计数降序排序并选择前100个
top_100_indices = index_counts.sort_values(by='zero_count', ascending=False).head(100)


# 输出前50个索引的列表
top_50_index_list = top_100_indices['index'].tolist()
# 输出结果
print("前100个容易出错的索引位置及其对应的出错次数：")
print(top_100_indices)

# 如果你只想打印索引和出错数的列表，也可以这样做：
for index, count in zip(top_100_indices['index'], top_100_indices['zero_count']):
    print(f"索引: {index}, 出错次数: {count}")

print(top_50_index_list)