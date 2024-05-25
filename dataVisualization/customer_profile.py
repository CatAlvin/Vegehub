import matplotlib.pyplot as plt
import pandas as pd
import mysql.connector
import math


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
    cursor.execute("SELECT age, gender FROM customer")
    result = cursor.fetchall()
    conn.close()
    return result

def data_prepocess():
    data = fetch_data()
    df = pd.DataFrame(data, columns=['Age', 'Gender'])
    male_df = df[df['Gender'] == 'male'].copy()
    female_df = df[df['Gender'] == 'female'].copy()
    N = 16
    range_size = df['Age'].max() - df['Age'].min()
    interval_size = math.ceil(range_size / N)
    bins = list(range(df['Age'].min(), df['Age'].max() + interval_size, interval_size))
    group_names = [f'{bins[i]}-{bins[i+1]-1}' for i in range(len(bins)-1)]
    male_df['Age_Group'] = pd.cut(male_df['Age'], bins, labels=group_names, right=False)
    female_df['Age_Group'] = pd.cut(female_df['Age'], bins, labels=group_names, right=False)
    male_age_group_counts = male_df['Age_Group'].value_counts().reindex(group_names, fill_value=0)
    female_age_group_counts = female_df['Age_Group'].value_counts().reindex(group_names, fill_value=0)

    return male_age_group_counts, female_age_group_counts, group_names

def create_butterfly_chart(male_counts, female_counts, labels, filepath=None):
    fig, ax = plt.subplots(figsize=(10, 6))
    bars_male = ax.barh(labels, -male_counts, color='lightblue', edgecolor='black', label='Male')
    bars_female = ax.barh(labels, female_counts, color='lightpink', edgecolor='black', label='Female')
    
    # 显示 x 轴，隐藏 y 轴
    ax.xaxis.set_visible(True)
    ax.yaxis.set_visible(False)
    
    # 设置轴标签和标题
    ax.set_xlabel('Population Count')
    ax.set_title("Customers' Age & Customers' Gender")
    ax.legend(loc='upper right')
    
     # 将 x 轴负方向的数值变为正数
    x_labels = ax.get_xticks()
    ax.set_xticks(x_labels)  # 确保 ticks 是固定的
    ax.set_xticklabels([abs(int(x)) for x in x_labels])
    
    # 在每个条形图上方显示年龄组
    for bar_male, bar_female, label in zip(bars_male, bars_female, labels):
        bar_male_x = abs(bar_male.get_width())
        bar_female_x = bar_female.get_width()
        # 计算标签的位置
        y_position = bar_male.get_y() + bar_male.get_height() / 2

        # 添加标签但不挡住条形图
        ax.text(
            0, y_position, label, 
            va='center', ha='center', fontsize=10, color='mediumslateblue', fontweight='bold',
            bbox=dict(facecolor='none', edgecolor='none')
        )
    
    if filepath:
        plt.savefig(filepath, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def draw_customer_gender_age_butterfly_chart(filepath='./frontend/imgs/customer_gender_age_butterfly_chart.png'):
    male_counts, female_counts, group_names = data_prepocess()
    create_butterfly_chart(male_counts, female_counts, group_names, filepath=filepath)
    return filepath