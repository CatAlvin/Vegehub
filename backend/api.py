from database import api as db_api

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