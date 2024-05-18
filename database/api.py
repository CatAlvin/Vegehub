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
    

# 小功能
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

def getVegetableNameByID(vegetable_id: int) -> str:
    """Get the name of a specific vegetable by its ID

    Args:
        vegetable_id: The ID of the vegetable to get the name of

    Returns:
        str: The name of the vegetable
    """
    vegetable = session.query(models.Vegetable).filter(models.Vegetable.id == vegetable_id).first()
    return vegetable.vegetable_name

def getReviewWordFrequency(vegetable_id: id) -> dict[str, int]:
    """Get the word frequency of customer reviews for a specific vegetable

    Args:
        vegetable_name: The name of the vegetable to get the reviews of
    
    Returns:
        dict: A dict containing the word frequency of the reviews
    """
    wordFrequency = {}
    reviews = session.query(models.CustomerReview).filter(models.CustomerReview.vegetable_id == vegetable_id).all()
    for review in reviews:
        adjs = __handleReviewTextToADJList(review.review_text)
        for adj in adjs:
            adj_capitalized = adj.capitalize()
            if adj_capitalized in wordFrequency.keys():
                wordFrequency[adj_capitalized] += 1
            else:
                wordFrequency[adj_capitalized] = 1
                
    # Sort the word frequency dict by value
    wordFrequency = dict(sorted(wordFrequency.items(), key=lambda item: item[1], reverse=True))
    return wordFrequency

def getVegetableReviews(vegetable_id: id) -> list[str]:
    """Get the reviews of a specific vegetable

    Args:
        vegetable_name: The name of the vegetable to get the reviews of

    Returns:
        list: A list containing the reviews of the vegetable
    """
    reviews = session.query(models.CustomerReview).filter(models.CustomerReview.vegetable_id == vegetable_id).all()
    return [
        {
            'date': review.review_date,
            'text': review.review_text,
            'neg': review.neg,
            'neu': review.neu,
            'pos': review.pos,
            'compound': review.compound
        }
        for review in reviews
    ]