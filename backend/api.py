from database import api as db_api
from dataVisualization import *

def get_review_sentence(vege_id: int):
    vege_name = db_api.getVegetableNameByID(vege_id)
    reviews_data = db_api.getVegetableReviews(vege_id)
    data = {
        'vegetable_name': vege_name,
        'reviews': reviews_data
    }
    return data

def get_review_analyze(vege_id: int):
    vege_name = db_api.getVegetableNameByID(vege_id)
    word_freq = db_api.getReviewWordFrequency(vege_id)
    sentiment_percentage = db_api.getAverageReviewsSentimentPercentage(vege_id)
    sentiment_count = db_api.getReviewsSentimentCount(vege_id)
    sentiment_count_percentage = db_api.getReviewsSentimentCountPercentage(vege_id)
    data = {
        'vegetable_name': vege_name,
        'word_frequency': word_freq,
        'sentiment_percentage': sentiment_percentage,
        'sentiment_count': sentiment_count,
        'sentiment_count_percentage': sentiment_count_percentage
    }
    return data

def get_visualization_img_path(img_name: str, vege_id: int):
    vege_name = None
    if vege_id < 50:
        vege_name = db_api.getVegetableNameByID(vege_id)
    if img_name == "customer_gender_age_butterfly_chart":
        path = draw_customer_gender_age_butterfly_chart()
    elif img_name == "vegetable_season_chart":
        path = draw_vegetable_season_chart(vege_name)
    elif img_name == "sell_cost_chart":
        path = draw_sell_cost_chart(vege_name)
    elif img_name == "supplier_profile_chart":
        path = draw_supplier_profile_chart()
    elif img_name == "vegetable_inventory_chart":
        path = draw_vegetable_inventory_chart()
    elif img_name == "vegetable_region_chart":
        path = draw_vegetable_region_chart(vege_name)
    else:
        path = ""
    data = {
        "vegetable_name": vege_name,
        "img_path": path.replace('./frontend/', '')
    }
    return data