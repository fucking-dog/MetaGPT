import json
import os
from collections import defaultdict
import pandas as pd
import re
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from networkx.drawing.nx_agraph import graphviz_layout


def _load_experience(path):
    rounds_dir = os.path.join(path, "graphs_0")
    experience_data = defaultdict(lambda: {"score": None, "success": {}, "failure": {}})

    # 遍历所有轮次的文件夹
    for round_dir in os.listdir(rounds_dir):
        if os.path.isdir(os.path.join(rounds_dir, round_dir)) and round_dir.startswith("round_"):
            round_path = os.path.join(rounds_dir, round_dir)
            try:
                # 提取轮次的数字
                round_number = int(round_dir.split("_")[1])

                # 查找 experience.json 文件
                json_file_path = os.path.join(round_path, "experience.json")
                if os.path.exists(json_file_path):
                    with open(json_file_path, "r", encoding="utf-8") as json_file:  # 指定 UTF-8 编码
                        data = json.load(json_file)
                        father_node = data["father node"]

                        # 如果这是该父节点的第一条记录，设置其分数
                        if experience_data[father_node]["score"] is None:
                            experience_data[father_node]["score"] = data["before"]

                        # 根据成功与否，将数据添加到相应的字典中
                        if data["succeed"]:
                            experience_data[father_node]["success"][round_number] = {
                                "modification": data["modification"],
                                "score": data["after"]
                            }
                        else:
                            experience_data[father_node]["failure"][round_number] = {
                                "modification": data["modification"],
                                "score": data["after"]
                            }
                else:
                    print(f"experience.json not found for round {round_dir}")
            except Exception as e:
                print(f"Error processing {round_dir}: {str(e)}")

    # 将 defaultdict 转换为普通 dict
    experience_data = dict(experience_data)

    # 保存为 JSON 文件
    output_path = os.path.join(path, "processed_experience.json")
    with open(output_path, "w", encoding="utf-8") as outfile:  # 指定 UTF-8 编码
        json.dump(experience_data, outfile, indent=4, ensure_ascii=False)  # ensure_ascii=False 以正确保存中文字符

    print(f"Processed experience data saved to {output_path}")
    return experience_data


def draw_experience_tree(json_data):
    G = nx.DiGraph()

    def add_edges(father_node, node_data):
        for round_number, success_data in node_data.get("success", {}).items():
            child_node = f'{round_number}'
            G.add_node(child_node, score=success_data["score"], color='green')
            G.add_edge(father_node, child_node)
            if child_node in json_data:
                add_edges(child_node, json_data[child_node])

        for round_number, failure_data in node_data.get("failure", {}).items():
            child_node = f'{round_number}'
            G.add_node(child_node, score=failure_data["score"], color='red')
            G.add_edge(father_node, child_node)
            if child_node in json_data:
                add_edges(child_node, json_data[child_node])

    # 添加所有的节点和边
    for father_node, details in json_data.items():
        if father_node not in G:
            G.add_node(father_node, score=details["score"], color='blue')
        add_edges(father_node, details)

    pos = nx.shell_layout(G)  # 使用 shell_layout 布局

    # 创建图形对象并设置大小
    plt.figure(figsize=(30, 30))  # 修改这里的参数来调整图的大小

    # 绘制节点
    node_colors = [nx.get_node_attributes(G, 'color')[node] for node in G.nodes()]
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=1000, font_size=12, font_color='white',
            font_weight='bold', edgecolors='black')

    # 绘制边
    nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle='-|>', arrowsize=20, edge_color='gray')

    # 在节点上标注分数
    for node in G.nodes():
        score = G.nodes[node]['score']
        plt.text(pos[node][0], pos[node][1] + 0.1, f'{score:.3f}', fontsize=10, ha='center', fontweight='bold')

    plt.title("Experience Tree", fontsize=16, fontweight='bold')
    plt.show()


import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def get_highest_score_per_round(json_data):
    # Create a dictionary to store the highest score for each round
    highest_scores = {}
    for data in json_data:
        round_number = data['round']
        score = data['score']
        # Store the highest score for each round
        if round_number not in highest_scores:
            highest_scores[round_number] = score
        else:
            highest_scores[round_number] = max(highest_scores[round_number], score)
    return highest_scores


def get_top_five_average_per_round(json_data):
    # Create a dictionary to store all scores for each round
    round_scores = {}
    for data in json_data:
        round_number = data['round']
        score = data['score']
        if round_number not in round_scores:
            round_scores[round_number] = [score]
        else:
            round_scores[round_number].append(score)

    # Calculate the average of the top 5 scores for each round
    top_five_averages = {}
    for round_number, scores in round_scores.items():
        sorted_scores = sorted(scores, reverse=True)
        top_five_averages[round_number] = np.mean(sorted_scores[:5]) if len(sorted_scores) >= 5 else np.mean(
            sorted_scores)

    return top_five_averages


def plot_score_evolution(json_data, round_0_score, validation, test):
    import numpy as np
    import matplotlib.pyplot as plt

    # 获取原始数据中各轮次的最高分和前五均值
    highest_scores = get_highest_score_per_round(json_data)
    # highest_scores["0"] = round_0_score
    top_five_averages = get_top_five_average_per_round(json_data)

    rounds = sorted([int(r) for r in highest_scores.keys()])

    # 计算每个轮次的历史最高分
    highest_scores_list = [max([highest_scores[str(round_number)] for round_number in rounds[:i + 1]]) for i in
                           range(len(rounds))]

    # 计算前五均值
    top_five_avg_list = [
        np.mean(sorted([highest_scores[str(round_number)] for round_number in rounds[:i + 1]], reverse=True)[:5]) for i
        in range(len(rounds))]

    # validation布林带计算
    bollinger_rounds = sorted(validation.keys(), key=int)
    bollinger_rounds = bollinger_rounds[:20]
    bollinger_means = {k: np.mean(v) for k, v in validation.items()}
    bollinger_stds = {k: np.std(v) for k, v in validation.items()}
    bollinger_upper = {k: bollinger_means[k] + 2 * bollinger_stds[k] for k in bollinger_rounds}
    bollinger_lower = {k: bollinger_means[k] - 2 * bollinger_stds[k] for k in bollinger_rounds}

    # test布林带计算
    t_bollinger_rounds = sorted(test.keys(), key=int)
    t_bollinger_means = {k: np.mean(v) for k, v in test.items()}
    t_bollinger_stds = {k: np.std(v) for k, v in test.items()}
    t_bollinger_upper = {k: t_bollinger_means[k] + 2 * t_bollinger_stds[k] for k in t_bollinger_rounds}
    t_bollinger_lower = {k: t_bollinger_means[k] - 2 * t_bollinger_stds[k] for k in t_bollinger_rounds}

    # 计算综合评分（例如信噪比）
    snr_scores = {}
    for k in bollinger_rounds:
        if bollinger_stds[k] != 0:
            mean_values = np.array(list(bollinger_means.values()))
            std_values = np.array(list(bollinger_stds.values()))

            mean_zscores = (mean_values - mean_values.mean()) / mean_values.std()
            std_zscores = (std_values - std_values.mean()) / std_values.std()

            # 结合标准化后的均值和标准差
            alpha = 0.7  # 控制均值的权重
            snr_scores = {k: alpha * mean_zscores[i] - (1 - alpha) * std_zscores[i] for i, k in
                          enumerate(bollinger_rounds)}

        else:
            snr_scores[k] = np.inf  # 如果标准差为0，信噪比设为正无穷

    # 选出评分最高的几个轮次（例如前5名）
    top_rounds = sorted(snr_scores, key=snr_scores.get, reverse=True)
    print("均值高且方差小的轮次：", top_rounds)

    # 创建图形和子图
    fig, axs = plt.subplots(1, 2, figsize=(14, 7))
    ax1 = axs[0]
    ax2 = axs[1]

    # 在第一个子图中绘制
    ax1.plot(rounds, highest_scores_list, label='Highest Score', marker='o')
    ax1.plot([int(k) for k in bollinger_rounds], [bollinger_means[k] for k in bollinger_rounds], '-',
             label='Bollinger Mean',
             color='orange')
    ax1.fill_between([int(k) for k in bollinger_rounds], [bollinger_lower[k] for k in bollinger_rounds],
                     [bollinger_upper[k] for k in bollinger_rounds], color='orange', alpha=0.5,
                     label='Bollinger Band')

    ax1.plot([int(k) for k in t_bollinger_rounds], [t_bollinger_means[k] for k in t_bollinger_rounds], '-',
             label='Test Bollinger Mean',
             color='red')
    ax1.fill_between([int(k) for k in t_bollinger_rounds], [t_bollinger_lower[k] for k in t_bollinger_rounds],
                     [t_bollinger_upper[k] for k in t_bollinger_rounds], color='red', alpha=0.5,
                     label='Test Bollinger Band')

    ax1.set_xlabel('Round', fontsize=12)
    ax1.set_ylabel('Score', fontsize=12)
    ax1.set_title('Highest Score Evolution', fontsize=14)
    # ax1.set_ylim(0.7, 1)
    ax1.set_xlim(1, 20)
    ax1.set_xticks(range(1, 20))  # 明确指定刻度为 1 到 19
    ax1.legend()
    ax1.grid(True)
    ax1.set_xticks(np.arange(min(rounds), max(rounds) + 1, 5))

    # 标注选出的轮次
    for k in top_rounds[:5]:
        ax1.annotate(
            f'{k}',
            xy=(int(k), bollinger_means[k]),
            xytext=(int(k), bollinger_means[k] + 0.03 * (
                    max(bollinger_means.values()) - min(bollinger_means.values()))),
            arrowprops=dict(
                facecolor='black',
                arrowstyle='->',
                mutation_scale=15  # 调整箭头大小
            ),
            fontsize=10,
            color='red',
            horizontalalignment='center'
        )

    # 在第二个子图中绘制
    ax2.plot(rounds, top_five_avg_list, label='Top 5 Average Score', marker='o')
    ax2.set_xlabel('Round', fontsize=12)
    ax2.set_ylabel('Score', fontsize=12)
    ax2.set_title('Top 5 Average Score Evolution', fontsize=14)
    ax2.legend()
    ax2.grid(True)
    ax2.set_xticks(np.arange(min(rounds), max(rounds) + 1, 5))

    plt.tight_layout()
    plt.show()


# 示例 JSON 数据
# 假设 JSON 文件的路径是 path_to_json


def read_scores_and_costs(a_folder_path):
    results = []

    for round_folder in os.listdir(a_folder_path):
        round_folder_path = os.path.join(a_folder_path, round_folder)

        # 确保它是一个文件夹
        if os.path.isdir(round_folder_path):
            # 使用正则表达式提取轮次文件夹名称中的纯数字部分
            round_number_match = re.search(r'\d+', round_folder)
            if round_number_match:
                round_number = round_number_match.group()  # 提取到的纯数字轮次

                # 遍历该轮次文件夹下的所有文件
                for file in os.listdir(round_folder_path):
                    file_path = os.path.join(round_folder_path, file)

                    # 确保文件是csv文件，且文件名是以数字开头（表示分数）
                    if file.endswith('.csv') and file[:-4].replace('.', '').isdigit():
                        # 提取文件名中的分数
                        score = float(file[:-4])

                        # 读取csv文件
                        df = pd.read_csv(file_path)

                        # 获取 'cost' 列的最大值
                        if 'cost' in df.columns:
                            cost = df['cost'].max()
                        else:
                            cost = None

                        # 将该轮次的分数和对应的cost记录下来
                        results.append({'round': round_number, 'score': score, 'cost': cost})

    return results


def plot_pareto(results, save_path=None):
    # 提取分数、成本和轮次，并筛选符合条件的结果
    filtered_results = [r for r in results]
    scores = [r['score'] for r in filtered_results]
    costs = [r['cost'] for r in filtered_results]
    rounds = [r['round'] for r in filtered_results]

    # 绘制成本和分数的散点图（轴反转）
    plt.figure(figsize=(8, 6))
    plt.scatter(costs, scores, color='blue', label='Graph')

    # 标题和标签
    plt.title('Pareto Front of Cost vs Score(Gsm8K)')
    plt.xlabel('Cost($)')
    plt.ylabel('Score(Pass@1)')

    # 计算帕累托前沿
    pareto_front = []
    sorted_results = sorted(filtered_results, key=lambda x: x['cost'])
    current_pareto_score = float('-inf')

    for result in sorted_results:
        if result['score'] > current_pareto_score:
            pareto_front.append(result)
            current_pareto_score = result['score']

    pareto_costs = [p['cost'] for p in pareto_front]
    pareto_scores = [p['score'] for p in pareto_front]
    pareto_rounds = [p['round'] for p in pareto_front]

    plt.plot(pareto_costs, pareto_scores, color='red', label='Pareto Front', linestyle='--')

    # 在帕累托前沿点上标注轮次信息
    for cost, score, round_num in zip(pareto_costs, pareto_scores, pareto_rounds):
        plt.annotate(f'{round_num}', xy=(cost, score), textcoords="offset points", xytext=(5, 5), ha='center')

    # 图例
    plt.legend()

    # 如果提供了保存路径，保存高分辨率图像
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    # 显示图形
    plt.show()


experience = r"D:\PythonProject\MetaGPT-MathAI\examples\ags\w_action_node\optimized\MATH\graphs\processed_experience.json"
validation_result = r"D:\PythonProject\MetaGPT-MathAI\examples\ags\w_action_node\optimized\MATH\graphs\results.json"
test_result = r"D:\PythonProject\MetaGPT-MathAI\examples\ags\w_action_node\optimized\MATH\graphs\results.json"

# 打开文件并加载 JSON 数据
with open(experience, 'r', encoding='utf-8') as file:
    json_data = json.load(file)
with open(validation_result, 'r', encoding='utf-8') as file:
    validation_data = json.load(file)
with open(test_result, 'r', encoding='utf-8') as file:
    test_data = json.load(file)

# 生成树图
draw_experience_tree(json_data)

# test = {1: [0.92607, 0.92891, 0.93081, 0.93175, 0.93270]}
test = {}
# , 3:[0.91848, 0.92038, 0.92133, 0.92607, 0.93175], 14:[0.92701, 0.92796, 0.93081,0.93081, 0.93460]


df = pd.DataFrame(validation_data)
scores_per_round = df.groupby('round')['score'].apply(list).to_dict()
df_t = pd.DataFrame(test_data)
t_scores_per_round = df_t.groupby('round')['score'].apply(list).to_dict()
print(t_scores_per_round)

# 检查和转换数据类型
df['score'] = pd.to_numeric(df['score'], errors='coerce')
df['avg_cost'] = pd.to_numeric(df['avg_cost'], errors='coerce')
# 只保留需要计算的列
df_filtered = df[['round', 'score', 'avg_cost']]

# 计算每轮的均值
result = df_filtered.groupby('round').mean().reset_index()

# 将结果整理为所需的格式
formatted_result = result.rename(columns={'round': 'round', 'score': 'score', 'avg_cost': 'cost'})
formatted_result['round'] = formatted_result['round'].astype(str)  # 将 round 转换为字符串
results = formatted_result.to_dict(orient='records')
# 直接添加 test 中的内容到 scores_per_round
for key, value in test.items():
    t_scores_per_round.setdefault(key, []).extend(value)

a_folder_path = r"D:\PythonProject\MetaGPT-MathAI\examples\ags\w_action_node\optimized\Gsm8K\graphs"
save_path = r"C:\Users\13761\Desktop\a"

# results = read_scores_and_costs(a_folder_path)
print(scores_per_round)
print(results)
# t_scores_per_round = {}
plot_score_evolution(results, 0.81, scores_per_round, t_scores_per_round)
plot_pareto(results, save_path)

# _load_experience(r'D:\PythonProject\MetaGPT-MathAI\examples\ags\w_action_node\optimized\Gsm8K')
