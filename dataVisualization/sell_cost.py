import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
import numpy as np
import matplotlib.font_manager as fm

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

def fetch_data(vegetable_name):
    conn = mysql_connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT v.vegetable_name, v.selling_price, v.purchase_price,v.vip_price, m.price
        FROM vegetable as v
        INNER JOIN market_price as m ON v.vegetable_name = m.vegetable_name
        WHERE v.vegetable_name = %s
    """, (vegetable_name,))
    result = cursor.fetchall()
    conn.close()
    return result


def draw_sell_cost_chart(vege_name, filepath="./frontend/imgs/sell_cost_chart.png"):
    # 获取合并后的数据
    data = fetch_data(vege_name)
    if not data:
        print("Please check your input")
    else:
        df = pd.DataFrame(data, columns=['vegetable_name', 'selling_price', 'purchase_price','vip_price', 'market_price'])

        # 提取数据，只获取第一个 vegetable_name 的记录
        vegetable = df['vegetable_name'][0]
        selling_price = float(df['selling_price'][0])
        purchase_price = float(df['purchase_price'][0])
        vip_price = float(df['vip_price'][0])
        
        # 获取所有市场价格并转换为浮点数
        market_prices = df['market_price'].astype(float).to_list()

        # 设置字体
        plt.rcParams['font.family'] = 'SimHei'  # 设置全局字体为SimHei
        plt.figure(figsize=(10, 5))
        
        # 定义渐变的绿色系列颜色
        #colors = ['slategray','#375623', '#548235', 'sage', '#A9D08E','honeydew'] # 深绿色到浅绿色的渐变
        colors =['#90EE90', '#3CB371', '#008000', '#228B22', '#006400','#E2F0D9']
        # 创建箱型图并显示平均数
        box = plt.boxplot(market_prices, patch_artist=True, showmeans=True, meanline=False,
                        meanprops=dict(marker='D', markeredgecolor='black', markerfacecolor=colors[4]))
        
        # 设置箱型图的颜色
        for median in box['medians']:
            median.set(color='black', linewidth=1)
        for box_patch in box['boxes']:
            box_patch.set(facecolor=colors[5])
        for whisker in box['whiskers']:
            whisker.set(color='black', linewidth=1.2)
        for cap in box['caps']:
            cap.set(color='black', linewidth=1.2)
        for flier in box['fliers']:
            flier.set(marker='o', alpha=0.5)
        # 标注售价和成本价，稍微移动位置使其偏离箱型图的中间线
        plt.plot(1.02, selling_price, 'o', label='selling price', color=colors[1], markersize=5)  # 稍微右移
        plt.plot(1.02,vip_price,'o',label='vip price',color=colors[2],markersize=5)
        plt.plot(0.98, purchase_price, 'o', label='cost price', color=colors[3], markersize=5)  # 稍微左移
        plt.plot(1, np.mean(market_prices), 'D', label='average market price', color=colors[4])  # 维持原位置

        # 添加x轴、y轴和图例
        plt.ylabel('价格 (元)')
        plt.xticks([1], [vegetable])
        plt.legend()

        # 展示图表
        plt.tight_layout()
        
        if filepath:
            plt.savefig(filepath, bbox_inches='tight')
            plt.close()
        else:
            plt.show()
    return filepath