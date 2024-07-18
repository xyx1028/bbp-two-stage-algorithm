import pandas as pd
import numpy as np
import time

# 载入数据集
def load_data(file_path):
    # 读取CSV文件，假设每行是逗号分隔的
    data = pd.read_csv(file_path, header=None)
    # 将每行转换为列表并包装在外层列表中
    return data.applymap(int).values.tolist()

def calculate_initial_thresholds(items, bin_capacity):
    # 仅使用物品的数量计算阈值
    return int(0.67 * len(items))  # 使用67%的物品数量作为阈值

def dynamic_threshold_adjustment(bins, bin_capacity, index, start_time, threshold, checkpoints):
    # 检查是否达到检查点（基于物品处理的百分比）
    if (index + 1) % checkpoints == 0:
        end_time = time.time()
        # 计算当前所有箱子中的物品总数
        items_packed = sum(len(bin) for bin in bins)
        performance_score = evaluate_performance(bins, bin_capacity, (end_time - start_time) / (index + 1))
        # 调整阈值基于性能评分
        threshold = adjust_threshold(performance_score, threshold)
        # 检查当前已包装的物品数量是否超过动态阈值
        if items_packed >= threshold:
            return bins, True, threshold  # 返回当前箱子列表，超过阈值的标志，和新的阈值
    return None, False, threshold  # 如果没有超过阈值，则返回None，未超过阈值的标志，和当前阈值


def first_stage_algorithm(items, bin_capacity, initial_threshold):

    items_sorted = sorted(items, reverse=True)
    remaining_items = items_sorted[:]  # 复制列表以避免修改原始列表\
    
    bins = []
    start_time = time.time()
    checkpoints = len(items_sorted) // 5  # 每五分之一总物品数调整一次阈值
    threshold = initial_threshold

    for index in range(len(items_sorted)):
        item = remaining_items.pop(0)  # 移除列表中的第一个元素并返回该元素
        placed = False
        for b in bins:
            if sum(b) + item <= bin_capacity:
                b.append(item)
                placed = True
                break
        if not placed:
            bins.append([item])

        # 调用动态阈值调整函数
        adjustment_result, exceeded, threshold = dynamic_threshold_adjustment(bins, bin_capacity, index, start_time, threshold, checkpoints)
        if adjustment_result is not None:
            return adjustment_result, exceeded, remaining_items  # 如果阈值超过，提前返回

    return bins, False, remaining_items  # 返回当前箱子列表和一个标志表示未超过阈值以及剩余物品



# 第二阶段装箱算法 IC-BFD，使用剩余物品列表
def second_stage_algorithm(items, bins, bin_capacity):
    items_sorted = sorted(items, reverse=True)  # 如果需要，可以调整排序方式
    for item in items_sorted:
        best_bin = None
        min_space_left = float('inf')
        for b in bins:
            space_left = bin_capacity - sum(b)
            if space_left >= item and space_left < min_space_left:
                best_bin = b
                min_space_left = space_left
        if best_bin is not None:
            best_bin.append(item)
        else:
            bins.append([item])
    return bins

# 调整阈值
def adjust_threshold(performance_score, current_threshold):
    if performance_score < 0.8:  # 示例性能下限
        return  current_threshold-40 # 降低阈值
    else:
        return current_threshold+40  # 增加阈值
    
# 评估指标计算
def evaluate_performance(bins, bin_capacity, time_spent):
    average_utilization = np.mean([sum(b) / bin_capacity for b in bins])
    # 综合评估量，空间利用率权重为0.8，时间权重为0.2
    performance_score = 0.95* average_utilization - 0.05 * time_spent # 时间越小越好
    return performance_score

def run_experiment(file_path, bin_capacity=1000):
    datasets = load_data(file_path)
    all_deviation_percents = []  # 存储每一行数据的偏差百分比
    all_times = []

    for items in datasets:
        start_time = time.time()
        total_capacity = sum(items)
        lower_bound = np.ceil(total_capacity / bin_capacity)  # 计算KLB
        
        # 进行第一阶段装箱
        bins, threshold_exceeded, remaining_items = first_stage_algorithm(items, bin_capacity, calculate_initial_thresholds(items, bin_capacity))
        if threshold_exceeded:
            # 如果第一阶段已超过阈值，立即切换到第二阶段
            bins = second_stage_algorithm(remaining_items, bins, bin_capacity)
        
        end_time = time.time()
        time_spent = end_time - start_time

        kalgebra = len(bins)  # KALG是算法所需的箱子数
        deviation_percent = ((kalgebra - lower_bound) / lower_bound) * 100 if lower_bound != 0 else 0
        all_deviation_percents.append(deviation_percent)
        all_times.append(time_spent)
        
        # print(f"Dataset processed, time spent: {time_spent} seconds")
        # print(f"Total bins used: {kalgebra}, Lower Bound: {lower_bound}, Deviation: {deviation_percent:.2f}%")
        # print("结束---------------------------------------------------结束")
        # print()

    average_time_spent = np.mean(all_times)  # 计算所有处理时间的平均值
    average_deviation_percents = np.mean(all_deviation_percents)  # 计算所有处理时间的平均值
    return average_deviation_percents, average_time_spent

# 运行实验
file_path = 'class_t_120.csv'  # 确保路径正确
average_deviation_percents, average_time_spent = run_experiment(file_path)
print("--------------------------------------------------------------------------------")
print(f"Total average time spent: {average_time_spent} seconds")
print(f"Total average Deviation: {average_deviation_percents}%")
print("--------------------------------------------------------------------------------")