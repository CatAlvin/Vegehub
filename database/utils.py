import sys
import os
import random
import hashlib
import logging

import database.models as models

from time import sleep
from faker import Faker
from spider import api as spider_api
from sqlalchemy import and_
from logger import logging_setup
from alive_progress import alive_bar, alive_it

# create logger
logger = logging.getLogger(__name__)
# create faker
faker = Faker()

VEGETABLES = [
    '西红柿',
    '黄瓜',
    '茄子',
    '土豆',
    '胡萝卜',
    '白菜',
    '青菜',
    '芹菜',
    '莴苣',
    '生菜',
    '菠菜',
    '苋菜',
    '香菜',
    '芫荽',
    '葱',
    '姜',
    '蒜',
    '辣椒',
    '椒',
    '豆角',
    '豆芽',
    '豆苗',
    '甜椒',
    '苦瓜',
    '南瓜',
    '冬瓜',
    '丝瓜',
    '黄花菜',
    '莲藕',
    '荸荠',
    '芋头',
    '山药',
    '花生',
    '蚕豆',
    '豌豆',
    '扁豆',
]

CRAWLER_VEGETABLES = [
    '胡萝卜',
    '白菜',
    '土豆',
    '西红柿',
    '芹菜',
    '黄瓜',
    '青椒',
    '韭菜',
    '大葱',
    '白萝卜',
    '葱头'
]

__CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))


def create_database():
    '''create database'''
    try:
        if not models.database_exists(models.engine.url):
            models.create_database(models.engine.url)
            logger.info('Database created successfully.')
        else:
            logger.warning('Database already exists.')
    except Exception as e:
        logger.error('Error occurred while creating database:', e)
        logger.error('>> Please check the database configuration. <<')


def create_tables():
    '''create tables'''
    try:
        models.Base.metadata.create_all(models.engine)
        logger.info('Tables created successfully.')
    except Exception as e:
        logger.error('Error occurred while creating tables:', e)


def drop_tables():
    '''drop tables'''
    try:
        models.Base.metadata.drop_all(models.engine)
        logger.info('Tables dropped successfully.')
    except Exception as e:
        logger.error('Error occurred while dropping tables:', e)


def get_session():
    '''get the session for database operations'''
    return models.scoped_session(models.Session)


def close_session():
    '''close the session'''
    models.session.close()
    logger.info('Session closed successfully.')


def fetch_all(model: models.Base):
    '''fetch all data from a table
    params:
        model: the model class
    '''
    return models.session.query(model).all()


def fetch_by_id(model: models.Base, id: int):
    '''fetch data by id from a table

    params:
        model: the model class
        id: the id to filter
    '''
    return models.session.query(model).filter_by(id=id).first()


def fetch_by_condition(model: models.Base, condition):
    '''fetch data by condition from a table

    params:
        model: the model class
        condition: the condition to filter
    '''
    return models.session.query(model).filter(condition).all()


def fetch_specific_columns(model: models.Base, columns: list[models.Column]):
    '''fetch specific columns from a table

    params:
        model: the model class
        columns: list of columns to fetch
    '''
    return models.session.query(*columns).all()


def fetch_specific_columns_by_condition(model: models.Base, columns: list[models.Column], condition):
    '''fetch specific columns by condition from a table

    params:
        model: the model class
        columns: list of columns to fetch
        condition: the condition to filter
    '''


def execute_query(query: str):
    '''execute a query

    params:
        query: the query to be executed
    '''
    return models.session.execute(query)


def add_data(data: models.Base):
    '''add data to a table

    params:
        data: models.Base object
    '''
    models.session.add(data)
    models.session.commit()
    # logger.debug(f'Successfully added data {data}')


def add_multiple_data(data: list[models.Base]):
    '''add multiple data to a table

    params:
        data: list of models.Base objects
    '''
    models.session.add_all(data)
    models.session.commit()
    logger.debug(f'Successfully added {len(data)} data.')
    

def hash_password(password: str, hash_obj):
    '''hash the password

    params:
        password: the password to be hashed
    '''
    hash_obj.update(password.encode('utf-8'))
    return hash_obj.hexdigest()


def __load_admin_data_from_file(file_name: str = 'admin.txt'):
    '''load admin data from file

    params:
        file_path: the file path
    '''
    # example data
    # admin_id: 1
    # username: admin
    # password: admin
    # admin_id: 2
    # username: chenglan
    # password: 53100
    # admin_id: 3
    # username: neneliu
    # password: 200499Dd
    file_path = os.path.join(__CURRENT_FOLDER, 'config', file_name)
    data = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 3):
            d = {}
            username = lines[i + 1].strip().split(': ')[1]
            password = lines[i + 2].strip().split(': ')[1]
            
            # password hash use md5
            hash_obj = hashlib.md5()
            password = hash_password(password, hash_obj)
            d['username'] = username
            d['password'] = password
            
            data.append(d)
            
    return data

# data maker
def __discontinues_probability_maker(items: list, probabilities: list):
    '''make a random choice based on the probabilities'''
    return random.choices(items, probabilities)[0]

def __make_admin_data():
    '''make admin data'''
    data = __load_admin_data_from_file()
    m_data = []
    total_task_num = len(data)
    with alive_bar(total_task_num, title='Adding Admin Data') as bar:
        for item in data:
            m_data.append(models.Admin(
                username=item['username'],
                password=item['password']
            ))
            bar()
    add_multiple_data(m_data)
    logger.info('Admin data added successfully.')


def __make_customer_data(numOfData: int):
    '''make customer data use faker

    params:
        numOfData: the number of data to be generated
    '''
    data = []
    total_task_num = numOfData
    with alive_bar(total_task_num, title='Adding Customer Data') as bar:
        
        for _ in range(numOfData):
            data.append(models.Customer(
                name=faker.name(),
                age=random.randint(18, 80),
                gender=random.choice(['male', 'female']),
                phone=faker.phone_number(),
                is_vip=__discontinues_probability_maker([True, False], [0.1, 0.9])
            ))
            bar()
    add_multiple_data(data)
    logger.info('Customer data added successfully.')


def __make_supplier_data(numOfData: int):
    '''make supplier data use faker

    params:
        numOfData: the number of data to be generated
    '''
    data = []
    total_task_num = numOfData
    with alive_bar(total_task_num, title='Adding Supplier Data') as bar:
        for _ in range(numOfData):
            data.append(models.Supplier(
                supplier_name=faker.company(),
                contact_info=faker.phone_number(),
                rating=__discontinues_probability_maker(
                    [1, 2, 3, 4, 5], [0.1, 0.1, 0.2, 0.4, 0.2]),
                availability=__discontinues_probability_maker(
                    ['available', 'not available'], [0.8, 0.2]),
                source_url=faker.url()
            ))
            bar()
    add_multiple_data(data)
    logger.info('Supplier data added successfully.')


def __make_vegetable_data(supplier_num: int = 20,
                          vegetable_list: list = VEGETABLES,
                          pq_items: list = [10, 50, 100, 200],
                          pq_probabilities: list = [0.1, 0.5, 0.3, 0.1],
                          pp_range: tuple = (0.5, 5.0),
                          profit_rate: float = 0.2,
                          vip_discount: float = 0.9
                          ):
    '''make vegetable data use faker

    params:
        supplier_num: number of suppliers
        vegetable_list: list of vegetables
        pq_items: list of purchase quantity items
        pq_probabilities: list of purchase quantity probabilities
        pp_range: tuple of purchase price range
        profit_rate: profit rate, default is 0.2 (20%)
        vip_discount: discount rate for VIP, default is 0.9 (10% off)
    '''
    data = []
    total_task_num = len(vegetable_list)
    with alive_bar(total_task_num, title='Adding Vegetable Data') as bar:
        for vegetable in vegetable_list:
            p_price = random.uniform(*pp_range)
            s_price = p_price * (1 + profit_rate)
            data.append(models.Vegetable(
                vegetable_name=vegetable,
                purchase_quantity=__discontinues_probability_maker(
                    pq_items, pq_probabilities),
                purchase_price=p_price,
                supplier_id=random.randint(1, supplier_num),
                selling_price=s_price,
                vip_price=s_price * vip_discount
            ))
            bar()
    add_multiple_data(data)
    logger.info('Vegetable data added successfully.')


def __make_customer_review_data(numOfData: int,
                                vegetable_list: list = VEGETABLES,
                                review_list: list = ['It was a great shopping experience and allowed me to eat fresh vegetables',
                                                     'The vegetables are fresh. Good reviews',
                                                     'Some dishes are not very fresh',
                                                     'It\'s worse, not as good as expected',
                                                     'The vegetables are not fresh. Not recommended',
                                                     'Great shopping experience, fresh vegetables, good reviews',
                                                     'The vegetables are fresh, good reviews',
                                                     'Some dishes are not very fresh',
                                                     'Very Good!',
                                                     'Recommended!',
                                                     'Wow! Fresh vegetables!',
                                                     'I will buy again!',
                                                     'I will not buy again!',
                                                     'Good experience!',
                                                     'Good quality!',
                                                     'Good service!']):
    '''make customer review data use faker

    params:
        numOfData: the number of data to be generated
        vegetable_num: the number of vegetables
        review_list: list of review text
    '''
    data = []
    total_task_num = numOfData
    with alive_bar(total_task_num, title='Adding Customer Review Data') as bar:
        for _ in range(numOfData):
            data.append(models.CustomerReview(
                review_date=faker.date_this_year(),
                review_text=random.choice(review_list),
                vegetable_id=random.randint(1, len(vegetable_list))
            ))
            bar()

    add_multiple_data(data)
    logger.info('Customer review data added successfully.')


def __make_market_price_data(numOfData: int,
                             vegetable_list: list = VEGETABLES):
    '''make market price data use faker

    params:
        numOfData: the number of data to be generated
        vegetable_num: the number of vegetables
    '''
    data = []
    total_task_num = numOfData
    with alive_bar(total_task_num, title='Adding Market Price Data') as bar:
        for _ in range(numOfData):
            date = faker.date_between(start_date='-1y', end_date='today')
            # get the season based on the month
            month = date.month
            if month in [3, 4, 5]:
                season = 'spring'
            elif month in [6, 7, 8]:
                season = 'summer'
            elif month in [9, 10, 11]:
                season = 'autumn'
            else:
                season = 'winter'
            # get the season price influence factor
            if season == 'spring':
                p_factor = 1.2
            elif season == 'summer':
                p_factor = 1.5
            elif season == 'autumn':
                p_factor = 1.0
            else:
                p_factor = 0.8
            # get the season sale volume influence factor
            if season == 'spring':
                v_factor = 0.8
            elif season == 'summer':
                v_factor = 1.2
            elif season == 'autumn':
                v_factor = 1.5
            else:
                v_factor = 0.8
            # get the vegetable breed influence factor
            vege_name = random.choice(vegetable_list)
            if '菜' in vege_name:
                p_factor *= 1.0
                v_factor *= 1.2
            elif '瓜' in vege_name:
                p_factor *= 1.5
                v_factor *= 0.6
            elif '豆' in vege_name:
                p_factor *= 1.2
                v_factor *= 1.0

            # add the data
            data.append(models.MarketPrice(
                vegetable_name=vege_name,
                price=random.uniform(0.5, 5.0) * p_factor,
                sale_volume=random.uniform(10, 100) * v_factor,
                season=season,
                date=date
            ))
            bar()

    add_multiple_data(data)
    logger.info('Market price data added successfully.')


def __make_market_data(vegetable_list: list = CRAWLER_VEGETABLES,
                       year: int = 2024,
                       month: int = 3,
                       begin: int = 1,
                       end: int = 5):
    '''make market price data use spider'''
    data = []
    total_task_num = len(vegetable_list) * (end - begin + 1)
    with alive_bar(total_task_num, title='Crawling Market Data') as bar:
        for vegetable in vegetable_list:
            s_data = spider_api.spider(bar, vegetable, year, month, begin, end)
            if not s_data:
                return data
            data.extend(s_data)
            sleep(1)
        for item in data:
            if not item:
                continue
            record = models.Market(
                vegetable_name=item['vegetable_name'],
                market_name=item['market_name'],
                region=item['region'],
                lowest_price=item['lowest_price'],
                highest_price=item['highest_price'],
                average_price=item['average_price'],
                publish_date=item['publish_date'],
                source_url=item['source_url']
                )
            add_data(record)
            
    logger.info('Market data added successfully.')


def fake_table_data(numOfSupplier: int = 20,
                    numOfCustomer: int = 1000,
                    numOfReview: int = 1000,
                    numOfMarketPrice: int = 1000,
                    crawler_begin: int = 1,
                    crawler_end: int = 10,
                    crawler_year=2024,
                    crawler_month=3):
    '''fake table data'''
    # make admin data
    __make_admin_data()
    # make supplier data
    __make_supplier_data(numOfData=numOfSupplier)
    # make vegetable data
    __make_vegetable_data(supplier_num=numOfSupplier,
                          vegetable_list=VEGETABLES,
                          pq_items=[10, 50, 100, 200],
                          pq_probabilities=[0.1, 0.5, 0.3, 0.1],
                          pp_range=(0.5, 5.0))
    # make customer data
    __make_customer_data(numOfData=numOfCustomer)
    # make customer review data
    __make_customer_review_data(numOfData=numOfReview,
                                vegetable_list=VEGETABLES,
                                review_list=['It was a great shopping experience and allowed me to eat fresh vegetables',
                                             'The vegetables are fresh. Good reviews',
                                             'Some dishes are not very fresh',
                                             'It\'s worse, not as good as expected',
                                             'The vegetables are not fresh. Not recommended',
                                             'Great shopping experience, fresh vegetables, good reviews',
                                             'The vegetables are fresh, good reviews',
                                             'Some dishes are not very fresh',
                                             'Very Good!',
                                             'Recommended!',
                                             'Wow! Fresh vegetables!',
                                             'I will buy again!',
                                             'I will not buy again!',
                                             'Good experience!',
                                             'Good quality!',
                                             'Good service!'])
    # make market price data
    __make_market_price_data(numOfData=numOfMarketPrice,
                             vegetable_list=VEGETABLES)
    # make market data
    __make_market_data(begin=crawler_begin,
                       end=crawler_end,
                       vegetable_list=CRAWLER_VEGETABLES,
                       year=crawler_year,
                       month=crawler_month)
    logger.info('Fake data generated successfully.')


def init_database():
    # create_database
    create_database()
    # drop_tables to avoid duplicate data
    drop_tables()
    # create tables
    create_tables()
    # fake table data
    fake_table_data(crawler_begin=1, 
                    crawler_end=5, 
                    crawler_year=2024, 
                    crawler_month=3)
    logger.info('Database initialized successfully.')