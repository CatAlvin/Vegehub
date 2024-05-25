import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import mysql.connector
from matplotlib import cm

# 创建mysql连接
def mysql_connect():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='wbh53100',
            database='vegehub'
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def fetch_data():
    conn = mysql_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT vegetable_name,purchase_quantity FROM vegetable")
    result = cursor.fetchall()
    conn.close()
    return result

def draw_vegetable_inventory_chart(filepath='./frontend/imgs/vegetable_inventory.png'):
    data = fetch_data()
    df = pd.DataFrame(data)
    vegetable = df[0]
    purchase_quantity = df[1]

    # 找出系统中可用的中文字体
    for font in fm.fontManager.ttflist:
        if 'SimHei' in font.name:
            print(font)
    # 设置字体
    plt.rcParams['font.family'] = 'SimHei'  # 设置全局字体
    # 生成一个颜色映射表
    colormap = plt.colormaps['tab20']  # 获取颜色映射表对象
    colors = [colormap(i / len(vegetable)) for i in range(len(vegetable))]  # 生成颜色


    # 设置图表大小
    plt.figure(figsize=(13,6))


    # 绘制柱形图，设置宽度和颜色
    bars = plt.bar(vegetable, purchase_quantity, width=0.7, color=colors)
    # 替换x轴标签为蔬菜名称， 并竖直显示
    plt.xticks(rotation=60)
  
    # 添加标题和标签
    plt.title('Purchase Quantity of Vegetables')
    plt.xlabel('Vegetables')
    plt.ylabel('Purchase Quantity')

    if filepath:
        plt.savefig(filepath, bbox_inches='tight')
        plt.close()
    else:
        plt.show()
    return filepath