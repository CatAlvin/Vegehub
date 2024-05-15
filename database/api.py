import database.models as models
import database.utils as utils
import pandas as pd
import re
from spider import api as spider_api
from nltk import pos_tag, word_tokenize

session = utils.get_session()

# 获取DataFrame
def __getDataFrame(model) -> pd.DataFrame:
    """Get the DataFrame of a specific model in the database

    Args:
        model: The model to get the DataFrame of

    Returns:
        pd.DataFrame: A pandas DataFrame containing the data of the model
    """
    query = session.query(model)
    dataFrames = pd.read_sql(query.statement, query.session.bind, index_col='id')
    return dataFrames

def getAdminDataFrame() -> pd.DataFrame:
    """Get the DataFrame of all admins in the database

    Returns:
        pd.DataFrame: A pandas DataFrame containing all admins
    """
    return __getDataFrame(models.Admin)

def getCustomerDataFrame() -> pd.DataFrame:
    """Get the DataFrame of all customers in the database

    Returns:
        pd.DataFrame: A pandas DataFrame containing all customers
    """
    return __getDataFrame(models.Customer)

def getCustomerReviewsDataFrame() -> pd.DataFrame:
    """Get the DataFrame of all customer reviews in the database

    Returns:
        pd.DataFrame: A pandas DataFrame containing all customer reviews
    """
    return __getDataFrame(models.CustomerReview)

def getMarketDataFrame() -> pd.DataFrame:
    """Get the DataFrame of all markets in the database

    Returns:
        pd.DataFrame: A pandas DataFrame containing all markets
    """
    return __getDataFrame(models.Market)

def getMarketPriceDataFrame() -> pd.DataFrame:
    """Get the DataFrame of all market prices in the database

    Returns:
        pd.DataFrame: A pandas DataFrame containing all market prices
    """
    return __getDataFrame(models.MarketPrice)

def getSupplierDataFrame() -> pd.DataFrame:
    """Get the DataFrame of all suppliers in the database

    Returns:
        pd.DataFrame: A pandas DataFrame containing all suppliers
    """
    return __getDataFrame(models.Supplier)

def getVegetableDataFrame() -> pd.DataFrame:
    """Get the DataFrame of all vegetables in the database

    Returns:
        pd.DataFrame: A pandas DataFrame containing all vegetables
    """
    return __getDataFrame(models.Vegetable)
    

# 小功能（画图用）
def getCustomerAges() -> pd.Series:
    """Get the ages of all customers in the database

    Returns:
        np.array: An pandas Series containing the ages of all customers
    """
    ages = pd.Series(utils.fetch_specific_columns(models.Customer, models.Customer.age))
    return ages

def getCustomerGenderCounts() -> dict[str, int]:
    """Get the counts of male and female customers in the database
    
    Returns:
        dict: A dict containing the counts e.g. {'male': maleCount, 'female': femaleCount}
    """
    maleCount = session.query(models.Customer).filter(models.Customer.gender == 'male').count()
    femaleCount = session.query(models.Customer).filter(models.Customer.gender == 'female').count()
    return {
        'male': maleCount,
        'female': femaleCount   
    }

def __handleReviewTextToADJList(review_text: str) -> list[str]:
    """Convert the review text to a list of adjectives use nltk

    Args:
        review_text (str): The review text to convert

    Returns:
        str: The converted list of adjectives
    """
    text = word_tokenize(review_text)
    return [word for word, tag in pos_tag(text) if tag in ['JJ', 'JJR', 'JJS', 'UH', 'WRB']]

def getReviewWordFrequency(vegetable_name: str) -> dict[str, int]:
    """Get the word frequency of customer reviews for a specific vegetable

    Args:
        vegetable_name: The name of the vegetable to get the reviews of
    
    Returns:
        dict: A dict containing the word frequency of the reviews
    """
    wordFrequency = {}
    reviews = session.query(models.CustomerReview).join(models.Vegetable).filter(models.Vegetable.vegetable_name == vegetable_name).all()
    for review in reviews:
        adjs = __handleReviewTextToADJList(review.review_text)
        for adj in adjs:
            if adj in wordFrequency:
                wordFrequency[adj] += 1
            else:
                wordFrequency[adj] = 1
                
    # Sort the word frequency dict by value
    wordFrequency = dict(sorted(wordFrequency.items(), key=lambda item: item[1], reverse=True))
    return wordFrequency