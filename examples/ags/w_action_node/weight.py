import numpy as np


def compute_mixed_probabilities(scores, alpha=0.2, lambda_=0.4):
    """
    计算混合概率分布，结合基础概率和分数加权概率。

    Args:
        scores (list or np.ndarray): 分数列表或数组。
        alpha (float): 控制分数权重敏感度的参数。
        lambda_ (float): 控制基础概率与分数加权概率的混合比例。取值范围 [0, 1]。

    Returns:
        np.ndarray: 归一化后的混合概率分布。
    """
    scores = np.array(scores, dtype=np.float64)
    n = len(scores)

    if n == 0:
        raise ValueError("分数列表为空。")

    # 基础概率（均匀分布）
    uniform_prob = np.full(n, 1.0 / n, dtype=np.float64)
    print(f"基础概率（均匀分布）: {uniform_prob}")

    # 分数加权概率
    max_score = np.max(scores)
    shifted_scores = scores - max_score
    print(f"平移后的分数: {shifted_scores}")

    exp_weights = np.exp(alpha * shifted_scores)
    print(f"指数权重: {exp_weights}")

    sum_exp_weights = np.sum(exp_weights)
    if sum_exp_weights == 0:
        raise ValueError("所有指数权重的和为0，无法归一化。")

    score_prob = exp_weights / sum_exp_weights
    print(f"基于分数的概率分布: {score_prob}")

    # 混合概率分布
    mixed_prob = lambda_ * uniform_prob + (1 - lambda_) * score_prob
    print(f"混合概率分布（未归一化）: {mixed_prob}")

    # 检查混合概率的总和
    total_prob = np.sum(mixed_prob)
    print(f"混合概率总和（未归一化）: {total_prob}")

    # 归一化混合概率
    if not np.isclose(total_prob, 1.0):
        mixed_prob = mixed_prob / total_prob
        print(f"混合概率分布（归一化后）: {mixed_prob}")

    return mixed_prob


def select_item(items, alpha=0.2, lambda_=0.4):
    """
    从项列表中基于混合概率分布选择一个项。

    Args:
        items (list of dict): 包含'round'和'score'键的项列表。
        alpha (float): 控制分数权重敏感度的参数。
        lambda_ (float): 控制基础概率与分数加权概率的混合比例。取值范围 [0, 1]。

    Returns:
        dict: 被选中的项。
    """
    if not items:
        raise ValueError("项列表为空。")

    # 根据'score'字段对项进行降序排序
    sorted_items = sorted(items, key=lambda x: x["score"], reverse=True)
    print("\n排序后的项：")
    for item in sorted_items:
        print(item)

    # 提取分数列表
    scores = [item["score"] for item in sorted_items]
    print(f"分数列表: {scores}")

    # 计算混合概率分布
    probabilities = compute_mixed_probabilities(scores, alpha, lambda_)
    print("\n混合概率分布: ", probabilities)
    print("混合概率总和: ", np.sum(probabilities))

    # 检查概率总和是否为1
    if not np.isclose(np.sum(probabilities), 1.0):
        raise ValueError("混合概率的总和不为1。")

    # 基于概率分布选择一个索引
    selected_index = np.random.choice(len(sorted_items), p=probabilities)
    print(f"\n选择的索引: {selected_index}，选择的项: {sorted_items[selected_index]}")

    # 返回被选中的项
    return sorted_items[selected_index]


# 测试函数
if __name__ == "__main__":
    # 示例数据
    items = [
        {"round": 1, "score": 0.78},
        {"round": 2, "score": 0.83},
        {"round": 3, "score": 0.86},
        {"round": 4, "score": 0.90},
    ]

    # 设置参数
    alpha = 0.2
    lambda_ = 0.3

    # 执行多次选择以观察分布情况
    selection_counts = {item["round"]: 0 for item in items}
    num_trials = 1  # 增加试验次数以更好地观察概率分布

    for _ in range(num_trials):
        selected_item = select_item(items, alpha, lambda_)
        selection_counts[selected_item["round"]] += 1

    # 显示选择分布
    print("\n经过 {} 次试验后的选择分布：".format(num_trials))
    for round_num, count in selection_counts.items():
        print(f"Round {round_num}：{count} 次选择（{(count / num_trials) * 100:.2f}%）")
