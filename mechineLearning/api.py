import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
import joblib

def predict_price_and_sales(date, vegetable_name):
    # 加载保存的模型
    model_price_rf = joblib.load('model_price_rf.pkl')
    model_sales_rf = joblib.load('model_sales_rf.pkl')

    # 获取输入日期的特征值
    year = date.year
    month = date.month
    day = date.day
    quarter = date.quarter

    # 将输入日期转换为 DataFrame
    input_data = pd.DataFrame({
        'year': [year],
        'month': [month],
        'day': [day],
        'quarter': [quarter],
        'price': np.nan,
        'sale_volume': np.nan
    })

    # 数据预处理
    scaler = MinMaxScaler(feature_range=(0, 1))
    input_scaled = scaler.fit_transform(input_data)

    # 使用加载的模型进行预测
    predicted_price = model_price_rf.predict(input_scaled[:, :-2])
    predicted_sales = model_sales_rf.predict(input_scaled[:, :-2])

    # 反标准化预测结果
    predicted_price_inv = scaler.inverse_transform(np.concatenate((input_scaled[:, :-2], predicted_price.reshape(-1, 1), predicted_sales.reshape(-1, 1)), axis=1))[:, -2]
    predicted_sales_inv = scaler.inverse_transform(np.concatenate((input_scaled[:, :-2], predicted_price.reshape(-1, 1), predicted_sales.reshape(-1, 1)), axis=1))[:, -1]

    # 返回预测结果
    return predicted_price_inv[0], predicted_sales_inv[0]

# 示例调用
date = pd.to_datetime('2024-05-15')
vegetable_name = '南瓜'
predicted_price, predicted_sales = predict_price_and_sales(date, vegetable_name)
print(f"Predicted price of {vegetable_name} on {date}: {predicted_price}")
print(f"Predicted sales volume of {vegetable_name} on {date}: {predicted_sales}")