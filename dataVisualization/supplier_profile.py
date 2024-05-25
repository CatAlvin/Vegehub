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
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("SELECT market_name FROM market")
        result = cursor.fetchall()
        conn.close()
        return result
    else:
        return []

def draw_supplier_profile_chart(filepath='./frontend/imgs/supplier_profile.png'):
    # 获取数据
    data = fetch_data()
    df = pd.DataFrame(data, columns=['market_name'])
    df_counts = df['market_name'].value_counts().to_dict()
    top_10 = dict(sorted(df_counts.items(), key=lambda item: item[1], reverse=True)[:10])

    #print(top_10)

    # 获取 colormap 实例
    color_map = plt.colormaps['Greens']

    # 生成与 top_10 长度相匹配的颜色映射
    colors = color_map(np.linspace(1, 0.2, len(top_10)))

    # 找出系统中可用的合适中文字体
    font_path = None
    for font in fm.fontManager.ttflist:
        if 'SimHei' in font.name:
            font_path = font.fname
            break

    # 设置字体
    if font_path is not None:
        prop = fm.FontProperties(fname=font_path)  # 为xticks和其他文本设置字体
        plt.rcParams['font.family'] = prop.get_name()  # 设置全局字体

    # 创建直方图，并为每个柱子分配颜色
    plt.figure(figsize=(10, 6))
    bars = plt.bar(top_10.keys(), top_10.values(), width=0.5, color=colors)
    plt.xlabel('Supplier name', fontsize=13, fontproperties=prop)
    plt.ylabel('Vegetable count', fontsize=13, fontproperties=prop)
    plt.title('Top 10 supplier', fontsize=25, fontweight='heavy')
    plt.xticks(rotation=60, fontproperties=prop)
    plt.tight_layout()
    if filepath:
        plt.savefig(filepath, bbox_inches='tight')
        plt.close()
    else:
        plt.show()
    return filepath

