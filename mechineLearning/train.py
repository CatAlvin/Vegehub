import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from database import api as db_api
import joblib

def train_model():
    # 数据加载
    vegeDF2 = db_api.getMarketPriceDataFrame()

    # 筛选出所有 'vegetable_name' 列中值为指定蔬菜名的行
    vege_rows = vegeDF2.loc[vegeDF2['vegetable_name'] == vegetable_name]

    # 确保日期列是日期格式
    vege_rows['date'] = pd.to_datetime(vege_rows['date'])

    # 数据筛选：选择日期范围内的数据作为训练集
    start_date = pd.to_datetime("2023-05-01")
    end_date = pd.to_datetime("2024-04-30")
    filtered_data = vege_rows[(vege_rows['date'] >= start_date) & (vege_rows['date'] <= end_date)]

    # 按日期排序
    filtered_data = filtered_data.sort_values('date')

    # 特征工程
    filtered_data['year'] = filtered_data['date'].dt.year
    filtered_data['month'] = filtered_data['date'].dt.month
    filtered_data['day'] = filtered_data['date'].dt.day
    filtered_data['quarter'] = filtered_data['date'].dt.quarter  # 添加季度特征

    # 准备数据集
    data = filtered_data[['date', 'year', 'month', 'day', 'quarter', 'price', 'sale_volume']]

    # 划分训练集和测试集
    train_data, test_data = train_test_split(data, test_size=0.3, shuffle=True, random_state=42)

    # 数据预处理
    scaler = MinMaxScaler(feature_range=(0, 1))
    train_scaled = scaler.fit_transform(train_data.drop(columns=['date']))
    test_scaled = scaler.transform(test_data.drop(columns=['date']))

    X_train = train_scaled[:, :-2]
    y_train_price = train_scaled[:, -2]
    y_train_sales = train_scaled[:, -1]
    X_test = test_scaled[:, :-2]
    y_test_price = test_scaled[:, -2]
    y_test_sales = test_scaled[:, -1]

    # 训练随机森林模型
    model_price_rf = RandomForestRegressor(n_estimators=100, random_state=42)
    model_sales_rf = RandomForestRegressor(n_estimators=100, random_state=42)

    model_price_rf.fit(X_train, y_train_price)
    model_sales_rf.fit(X_train, y_train_sales)

    # 保存模型到文件
    joblib.dump(model_price_rf, 'model_price_rf.pkl')
    joblib.dump(model_sales_rf, 'model_sales_rf.pkl')

def predict_vegetable(vegetable_name):
    # 加载保存的模型
    model_price_rf = joblib.load('model_price_rf.pkl')
    model_sales_rf = joblib.load('model_sales_rf.pkl')

    # 数据加载
    vegeDF2 = db_api.getMarketPriceDataFrame()

    # 筛选出所有 'vegetable_name' 列中值为指定蔬菜名的行
    vege_rows = vegeDF2.loc[vegeDF2['vegetable_name'] == vegetable_name]

    # 确保日期列是日期格式
    vege_rows['date'] = pd.to_datetime(vege_rows['date'])

    # 数据筛选：选择日期范围内的数据作为测试集
    start_date = pd.to_datetime("2023-05-01")
    end_date = pd.to_datetime("2024-04-30")
    filtered_data = vege_rows[(vege_rows['date'] >= start_date) & (vege_rows['date'] <= end_date)]

    # 按日期排序
    filtered_data = filtered_data.sort_values('date')

    # 特征工程
    filtered_data['year'] = filtered_data['date'].dt.year
    filtered_data['month'] = filtered_data['date'].dt.month
    filtered_data['day'] = filtered_data['date'].dt.day
    filtered_data['quarter'] = filtered_data['date'].dt.quarter  # 添加季度特征

    # 准备数据集
    data = filtered_data[['date', 'year', 'month', 'day', 'quarter', 'price', 'sale_volume']]

    # 数据预处理
    scaler = MinMaxScaler(feature_range=(0, 1))
    test_scaled = scaler.fit_transform(data.drop(columns=['date']))

    X_test = test_scaled[:, :-2]
    y_test_price = test_scaled[:, -2]
    y_test_sales = test_scaled[:, -1]

    # 使用加载的模型进行预测
    y_pred_price_rf = model_price_rf.predict(X_test)
    y_pred_sales_rf = model_sales_rf.predict(X_test)


# 示例调用
predict_vegetable('南瓜')
