# models.py
import os
import datetime
import logging
from logger import logging_setup
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import relationship

from sqlalchemy import (
    Date,
    ForeignKey,
    Text,
    create_engine,
    Column,
    Integer,
    String,
    Enum,
    DECIMAL,
    DateTime,
    Boolean,
    UniqueConstraint,
    Index
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database

# 获取当前文件夹路径
__CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))

# create logger
logger = logging.getLogger(__name__)


def __load_database_config(file_name: str = 'database-config.txt'):
    '''load database config from file'''
    file_path = os.path.join(__CURRENT_FOLDER, 'config', file_name)
    with open(file_path, 'r') as f:
        lines = f.readlines()
        config = {}
        for line in lines:
            key, value = line.strip().split(': ')
            config[key] = value
        return config


# 基础类
Base = declarative_base()

# load database config from database-config.txt
database_config = __load_database_config()

# 创建引擎
engine = create_engine(
    # "mysql+pymysql://root:wbh53100@localhost:3306/vegehub?charset=utf8mb4",
    "mysql+pymysql://%s:%s@%s:%s/%s?charset=%s" % (
        database_config['username'],
        database_config['password'],
        database_config['host'],
        database_config['port'],
        database_config['database'],
        database_config['charset']
    ),
    # 超过链接池大小外最多创建的链接
    max_overflow=0,
    # 链接池大小
    pool_size=5,
    # 链接池中没有可用链接则最多等待的秒数，超过该秒数后报错
    pool_timeout=10,
    # 多久之后对链接池中的链接进行一次回收
    pool_recycle=1,
    # 查看原生语句（未格式化）
    echo=False
)


# 绑定引擎
Session = sessionmaker(bind=engine)
# 创建数据库链接池，直接使用session即可为当前线程拿出一个链接对象conn
# 内部会采用threading.local进行隔离
session = scoped_session(Session)

# 管理员账户表


class Admin(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    username = Column(String(255), nullable=False, comment="用户名")
    password = Column(String(255), nullable=False, comment="密码")
    create_time = Column(DateTime, nullable=False,
                         default=datetime.datetime.now, comment="创建时间")

    def __str__(self):
        return f"object : <id:{self.id} username:{self.username} password:{self.password} create_time:{self.create_time}>"


# 市场表
class Market(Base):
    __tablename__ = "market"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    vegetable_name = Column(String(255), nullable=False, comment="蔬菜名称")
    market_name = Column(String(255), nullable=False, comment="市场名称")
    region = Column(String(255), comment="市场所在地区")
    lowest_price = Column(DECIMAL(10, 2), nullable=False, comment="最低价格")
    highest_price = Column(DECIMAL(10, 2), nullable=False, comment="最高价格")
    average_price = Column(DECIMAL(10, 2), nullable=False, comment="平均价格")
    publish_date = Column(Date, nullable=False, comment="发布日期")
    source_url = Column(String(255), comment="数据来源的网页链接")

    __table__args__ = (
        UniqueConstraint("vegetable_name", "market_name", "publish_date"),
    )

    def __str__(self):
        return f"object : <id:{self.id} vegetable_name:{self.vegetable_name} market_name:{self.market_name} region:{self.region} lowest_price:{self.lowest_price} highest_price:{self.highest_price} average_price:{self.average_price} publish_date:{self.publish_date}>"

# 蔬菜表


class Vegetable(Base):
    __tablename__ = "vegetable"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    vegetable_name = Column(String(255), nullable=False, comment="蔬菜名称")
    purchase_quantity = Column(DECIMAL(10, 2), nullable=False, comment="采购数量")
    purchase_price = Column(DECIMAL(10, 2), nullable=False, comment="采购价格")
    supplier_id = Column(Integer, ForeignKey('supplier.id'), comment="供应商ID")
    selling_price = Column(DECIMAL(10, 2), nullable=False, comment="销售价格")
    vip_price = Column(DECIMAL(10, 2), nullable=False, comment="VIP价格")

    __table__args__ = (
        UniqueConstraint("vegetable_name", "supplier_id"),
    )

    def __str__(self):
        return f"object : <id:{self.id} vegetable_name:{self.vegetable_name} purchase_quantity:{self.purchase_quantity} purchase_price:{self.purchase_price} selling_price:{self.selling_price} vip_price:{self.vip_price}>"

# 供应商表


class Supplier(Base):
    __tablename__ = "supplier"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    supplier_name = Column(String(255), nullable=False, comment="供应商名称")
    region = Column(String(255), comment="供应商所在地区")
    contact_info = Column(String(255), nullable=False, comment="供应商联系信息")
    rating = Column(DECIMAL(3, 1), nullable=False, comment="供应商评分")
    availability = Column(String(255), comment="供货状态")
    source_url = Column(String(255), comment="数据来源的网页链接")

    def __str__(self):
        return f"object : <id:{self.id} supplier_name:{self.supplier_name} region:{self.region} contact_info:{self.contact_info} rating:{self.rating} availability:{self.availability}>"

# 消费者评价表


class CustomerReview(Base):
    __tablename__ = "customer_review"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    review_date = Column(Date, nullable=False, comment="评价日期")
    review_text = Column(Text, nullable=False, comment="评价内容")

    # 添加外键关联到蔬菜表
    vegetable_id = Column(Integer, ForeignKey('vegetable.id'), comment="蔬菜ID")
    neg = Column(DECIMAL(6, 4), comment="负面情感")
    neu = Column(DECIMAL(6, 4), comment="中性情感")
    pos = Column(DECIMAL(6, 4), comment="正面情感")
    compound = Column(DECIMAL(6, 4), comment="综合情感")

    def __str__(self):
        return f"object : <id:{self.id} review_date:{self.review_date} review_text:{self.review_text}>"

# 市场价格表


class MarketPrice(Base):
    __tablename__ = "market_price"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    vegetable_name = Column(String(255), nullable=False, comment="蔬菜名称")
    price = Column(DECIMAL(10, 2), nullable=False, comment="价格")
    sale_volume = Column(DECIMAL(10, 2), nullable=False, comment="销售量(kg)")
    season = Column(String(255), comment="蔬菜对应的季节")
    date = Column(Date, nullable=False, comment="日期")

    def __str__(self):
        return f"object : <id:{self.id} date:{self.date} price:{self.price} season:{self.season}>"

# 顾客表


class Customer(Base):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    name = Column(String(255), nullable=False, comment="顾客名称")
    age = Column(Integer, nullable=False, comment="顾客年龄")
    gender = Column(Enum('male', 'female'), nullable=False, comment="顾客性别")
    phone = Column(String(255), nullable=False, comment="顾客联系信息")
    is_vip = Column(Boolean, nullable=False, comment="是否是VIP")

    __table__args__ = (
        UniqueConstraint("name", "age", "phone"),
    )

    def __str__(self):
        return f"object : <id:{self.id} name:{self.name} age:{self.age} phone:{self.phone} is_vip:{self.is_vip}>"
