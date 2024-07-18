import matplotlib.pyplot as plt


# 算法名称
algorithm_names = [
    "MB-WFD", "FFD", "BFD", "1-67-IC-BFD–MB-WFD", "1-67-IC-BFD–MB-FFD", "1-75-IC-BFD–MB-FFD",
    "1-75-IC-BFD–MB-WFD", "1-75-MB-WFD–MB-FFD", "1-100-MB-WFD–MB-FFD", "2-50-MB-FFD–MB-WFD",
    "2-50-MB-FFD–IC-BFD", "2-67-MB-WFD–IC-FFD", "2-67-MB-FFD–IC-FFD", "2-75-MB-FFD–BC",
    "2-50-MB-FFD–BC", "1-67-MB-FFD–BC", "1-75-IC-FFD-IC-BFD", "2-50-IC-FFD-IC-BFD", "2-67-IC-FFD-IC-BFD"
]

# 动态阈值调整数据
dynamic_data = {
    'algorithm': algorithm_names,
    'deviation': [1.46, 1.22, 1.22, 1.46, 1.22, 1.22, 1.79, 1.27, 1.27, 1.79, 1.22, 1.44, 1.22, 1.22, 1.22, 1.22, 1.22, 1.22, 1.22],
    'time': [0.004819, 0.003501, 0.005105, 0.006046, 0.004163, 0.003875, 0.005141, 0.004633, 0.005193, 0.004249, 0.004128, 0.005250, 0.004570, 0.003874, 0.003874, 0.003611, 0.004694, 0.004347, 0.004247]
}

# 固定阈值数据
fixed_data = {
    'algorithm': algorithm_names,
    'deviation': [1.46, 1.22, 1.22, 1.46, 1.22, 1.22, 1.51, 1.22, 1.66, 1.22, 1.22, 1.46, 1.22, 1.22, 1.22, 1.22, 1.22, 1.22, 1.22],
    'time': [0.004819, 0.003501, 0.005105, 0.006046, 0.004163, 0.003875, 0.005141, 0.004633, 0.005193, 0.004249, 0.004128, 0.005250, 0.004570, 0.003874, 0.003874, 0.003611, 0.004694, 0.004347, 0.004247]
}


plt.figure(figsize=(14, 8))

# 绘制固定阈值数据的散点图
plt.scatter(fixed_data['time'], fixed_data['deviation'], color='blue', s=50, label='Fixed Threshold')

# 绘制动态阈值数据的散点图
plt.scatter(dynamic_data['time'], dynamic_data['deviation'], color='red', s=50, label='Dynamic Threshold')

# 中部区域的y坐标
middle_y = (plt.ylim()[0] + plt.ylim()[1]) / 2

# 用于标注标签的y坐标
fixed_label_y_positions = [middle_y + i*0.01 for i in range(len(algorithm_names))]
dynamic_label_y_positions = [middle_y - i*0.01 for i in range(len(algorithm_names))]

# 标注每个点，固定阈值标签放在上方，动态阈值标签放在下方
for i, txt in enumerate(algorithm_names):
    plt.annotate(
        txt,
        xy=(fixed_data['time'][i], fixed_data['deviation'][i]),
        xytext=(fixed_data['time'][i], fixed_label_y_positions[i]),  # 标签放在中部区域不同的y坐标
        textcoords='data',
        ha='right',
        fontsize=8,
        arrowprops=dict(arrowstyle='->', lw=0.5, color='blue')
    )
    plt.annotate(
        txt,
        xy=(dynamic_data['time'][i], dynamic_data['deviation'][i]),
        xytext=(dynamic_data['time'][i], dynamic_label_y_positions[i]),  # 标签放在中部区域不同的y坐标
        textcoords='data',
        ha='left',
        fontsize=8,
        arrowprops=dict(arrowstyle='->', lw=0.5, color='red')
    )

# 设置时间轴的刻度
plt.xticks([0.003501+i * 0.0005 for i in range(7)], rotation=5)

# 增加 y 轴刻度间隔
plt.yticks([i * 0.1 +1 for i in range(10)])

plt.xlabel('Time (sec)')
plt.ylabel('Deviation (%)')
plt.title('Comparison of Fixed and Dynamic Threshold Algorithms for 500 Items in Dataset u')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
