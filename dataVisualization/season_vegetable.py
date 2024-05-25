import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mysql.connector

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
    if conn is not None:
        cursor = conn.cursor()
        query = "SELECT price, season FROM market_price WHERE vegetable_name = %s"
        cursor.execute(query, (vegetable_name,))
        result = cursor.fetchall()
        conn.close()
        return result
    else:
        return []

def draw_vegetable_season_chart(vege_name, filepath='./frontend/imgs/vegetable_season_chart.png'):
    # 获取数据
    data = fetch_data(vege_name)
    if not data:
        print("No data")
    else:
        df = pd.DataFrame(data, columns=['market_price', 'season'])

        # 设置字体
        plt.rcParams['font.family'] = 'SimHei'  # 设置全局字体为SimHei

        # 绘制散点图
        plt.figure(figsize=(10, 6))
        seasons = df['season'].unique()
        colors = ['orangered', 'deepskyblue', 'gold', 'olivedrab']
        color_dict = {season: colors[i % len(colors)] for i, season in enumerate(seasons)}

        for season in seasons:
            season_data = df[df['season'] == season]
            plt.scatter(season_data['season'], season_data['market_price'], color=color_dict[season], label=season)

        # 自定义图表
        plt.xlabel('Season')
        plt.ylabel('Market Price')
        plt.title(f'{vege_name} Market Prices by Season')
        plt.legend()
        plt.grid(axis='y')

        if filepath:
            plt.savefig(filepath, bbox_inches='tight')
            plt.close()
        else:
            plt.show()
    return filepath