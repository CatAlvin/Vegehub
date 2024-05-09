import database.utils as db_utils
import database.models as db_models
import database.api as db_api
import pandas as pd
import numpy as np
import math
#boken库用于画蝴蝶图
#show() 函数用于展示图表。当图表对象被创建和配置完成后，使用 show() 函数将图表显示在输出中
from bokeh.io import output_file, show
#ColumnDataSource 是Bokeh中用来组织和提供图表数据的核心对象。它能够以一种高效的方式存储数据格式，如列式数据，使得Bokeh能在绘图时直接访问。
#FactorRange 用于处理图表olumnDataSource, FactorRange 
from bokeh.models import ColumnDataSource, FactorRange,CDSView, BooleanFilter,LabelSet  
#figure() 函数用于创建一个图表的基础框架。这个函数能够初始化一个新的Figure对象，此对象提供了大量的方法和属性来自定义图表的外观和行为。
from bokeh.plotting import figure
#import mysql.connector

# 创建到MySQL数据库的连接
#def mysql_connect():
    #conn=mysql.connector.connect(
       # host="localhost",
       # user="root",
       # password="1210",
       # database="vegehub"
    #)
    #return conn
#顾客年龄，顾客性别（蝴蝶图）

#def fetch_data():
   #conn = mysql_connect()
   #cursor = conn.cursor()
    #获取男顾客年龄
    #cursor.execute("SELECT age,gender FROM customer")
    #result = cursor.fetchall()
    #conn.close()
    #return result

def data_prepocess():
    data = db_api.getCustomerDataFrame()
    #转换为dataframe方便处理
    df = pd.DataFrame(data)
    print(df.columns)
    # 按性别分组
    male_df = df[df['gender'] == 'male'].copy()
    female_df = df[df['gender'] == 'female'].copy()
    #找最大最小年龄
    min_age = df['age'].min()
    max_age = df['age'].max()
    # 计算间隔大小，这里使用math.ceil向上取整确保覆盖所有年龄
    N=16
    range_size = max_age - min_age
    interval_size = math.ceil(range_size / N)
    # 生成bins
    bins = list(range(min_age, max_age + interval_size, interval_size))  # 确保最大年龄被包含

    # 为最后的区间添加一个额外的点以确保包含最大年龄
    if bins[-1] < max_age:
        bins.append(max_age)

    # 创建分组标签
    group_names = [f'{bins[i]}-{bins[i+1]-1}' for i in range(len(bins)-1)]
    # 分组
    male_df['Age_Group'] = pd.cut(male_df['age'], bins, labels=group_names, right=False)
    female_df['Age_Group'] = pd.cut(female_df['age'], bins, labels=group_names, right=False)

    # 计算每个年龄段的人数
    male_age_group_counts = male_df['Age_Group'].value_counts()
    female_age_group_counts=female_df['Age_Group'].value_counts()
    # 初始化列表以存储整理后的数据
    genders = []
    age_groups = []
    populations = []

    # 为male处理数据添加到列表
    for age_group, count in male_age_group_counts.items():
        genders.append('Male')
        age_groups.append(age_group)
        populations.append(count)

    # 为female处理数据添加到列表
    for age_group, count in female_age_group_counts.items():
        genders.append('Female')
        age_groups.append(age_group)
        populations.append(count)

    # 构建新的DataFrame
    structured_data = {
        'Gender': genders,
        'Age_Group': age_groups,
        'Population': populations
    }
    new_df = pd.DataFrame(structured_data)
    return new_df
def customer_profile():
    data = data_prepocess()
    df = pd.DataFrame(data)
    #数据预处理 保证男性条形向左，女性向右
    df['Population']=df.apply(lambda row:-row['Population'] 
                              if row['Gender']=='Male'
                              else row['Population'],axis=1)
    #df['Age_Group']=abs(df['Population'])
    #为性别创建布尔索引
    male_filter = df['Gender'] == 'Male'
    female_filter = df['Gender'] == 'Female'
    #创建图表
    source = ColumnDataSource(df) 
    output_file("butterfly_chart.html")
    unique_age_groups = sorted(df['Age_Group'].unique())
    p = figure(y_range=FactorRange(*unique_age_groups),height=500, width=900,
                title="Customers' Age & Customers' gender", 
                toolbar_location=None, tools="") 
    # 为女性创建条形，从0开始
    p.hbar(y='Age_Group', left=0, right='Population', height=0.5, source=source,
           color='pink', legend_label='Female',
           view=CDSView(filter=BooleanFilter(female_filter)))

    # 为男性创建条形，从负的Population到0
    p.hbar(y='Age_Group', left='Population', right=0, height=0.5, source=source,
           color='blue', legend_label='Male',
           view=CDSView(filter=BooleanFilter(male_filter)))
     # 添加年龄组标签
    labels = LabelSet(x=0, y='Age_Group', text='Age_Group', level='glyph',text_color='white',
                      source=source, text_align='center', text_baseline='middle')
    p.add_layout(labels)
    #p.hbar(y='Age_Group', left='Population', right=0, height=0.4, source=source, 
          #color='pink', legend_label='Female')
    #p.hbar(y='Age_Group', left=0, right='Population', height=0.4, source=source, 
           #color='blue', legend_label='Male' ) 
    
    p.yaxis.visible = False
    p.xaxis.visible = False
    p.ygrid.grid_line_color = None 
    p.xaxis.axis_label ="Population Count"
    p.title.text_font_size='20pt'
    p.title.align='center'
    # 设置图例位置
    p.legend.location = "top_right"
    # 设置图例背景透明度
    p.legend.background_fill_alpha = 0.0  # 设置背景完全透明
    p.legend.label_text_font_size = '12pt' 
    p.legend.orientation = "vertical" 
    show(p)
customer_profile()