import time
import csv
import os
import requests
import logging

from logger import logging_setup
from bs4 import BeautifulSoup
from urllib.parse import quote
from typing import Union
from datetime import datetime
from database import models

# 获取当前文件夹路径
__CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))

# create logger
logger = logging.getLogger(__name__)

def __guess_region(market_name: str) -> str:
    three_words_province = ['黑龙江', '内蒙古']
    if market_name[:3] in three_words_province:
        return market_name[:3]
    else:
        return market_name[:2]

def __eval_format_data(data: list[str]) -> dict[str, Union[str, float, datetime]]:
    if not data:
        return None
    try:
        f_l_data = data.copy()
        f_l_data[2:5] = [float(f_l_data[2].strip('￥')), float(f_l_data[3].strip('￥')), float(f_l_data[4].strip('￥'))]
        # 价格为0则返回None
        if f_l_data[2] <= 0 or f_l_data[3] <= 0 or f_l_data[4] <= 0:
            return None
        # 日期为今日则返回今日日期
        if f_l_data[5] == '今日':
            f_l_data[5] = time.strftime("%Y-%m-%d", time.localtime())
        # 日期格式不对则返回None    
        p_date = datetime.strptime(f_l_data[5], "%Y-%m-%d")
    except:
        return None
    return {
        'vegetable_name': f_l_data[0],
        'market_name': f_l_data[1],
        'region': __guess_region(f_l_data[1]),
        'lowest_price': f_l_data[2],
        'highest_price': f_l_data[3],
        'average_price': f_l_data[4],
        'publish_date': p_date,
        'source_url': f_l_data[6]
    }
    

# 爬取数据并写到.csv文件中的函数
def spider(progress_bar,
           v_type="胡萝卜",
           year=2024,
           month=3,
           begin=1,
           end=5,
           folder_path=os.path.join(__CURRENT_FOLDER , 'data'),
           ) -> list[dict[str, Union[str, float, datetime]]]:
    '''
    spider function to get data from http://price.cnveg.com/
    
    params:
        v_type: str, the vegetable type, default is "胡萝卜"
        year: int, the year, default is 2024
        month: int, the month, default is 3
        begin: int, the begin page number, default is 1
        end: int, the end page number, default is 5
        folder_path: str, the folder path to save the data, default is 'data/'
    '''
    logger.info(f"Start to get data for {v_type} in {year} year {month} month")
    res = []
    v_type_base64 = quote(v_type.encode('utf-8')).replace('/', '%2F').replace('+', '%20')
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
    }
    if not folder_path.endswith('/'):
        folder_path += '/'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    with open(folder_path + f'{month}月全国{v_type}价格.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['品种', '批发市场', '最低价格', '最高价格', '平均价格', '发布时间'])
        
        for i in range(begin, end+1):
            # url样例
            # example: http://price.cnveg.com/select/st%E8%83%A1%E8%90%9D%E5%8D%9Cy2024m3d-1cta-1by-1p1.html
            url = f'http://price.cnveg.com/select/st{v_type_base64}y{year}m{month}d-1cta-1by-1p{i}.html'
            re = requests.get(url, headers=headers)
            # 测试是否成功获取网页
            if re.status_code == 200:
                logger.debug(f"Successfully get data from {url}")
            else:
                logger.error(f"Failed to get data from {url}")
                return res
            re.encoding = 'utf-8'   # 设定编码格式为utf8
            soup = BeautifulSoup(re.text, 'html.parser')
            table = soup.find('table', bgcolor="#d8d8d8")  # 价格表 bgcolor="#d8d8d8"
            if not table:
                logger.error(f"Failed to get data from {url}")
                return res
            rows = table.find_all('tr')[1:]  # [1:] 跳过标题行
            
            # print progress bar
            logger.debug(f"Processing '{v_type}' page {i}")

            for row in rows:
                cells = row.find_all('td')
                if cells:
                    cell_texts = ''.join(cell.text.strip() for cell in cells).split(v_type)
                    for record in cell_texts:
                        if record:
                            data = [v_type] + record.split()[:5]
                            if len(data) == 6:
                                # 加上url
                                data.append(url)
                                # logger.debug(data)
                                writer.writerow(data)
                                # 评估格式化数据并添加到结果列表
                                e_f_d = __eval_format_data(data)
                                res.append(e_f_d)
            progress_bar()
    return res


if __name__ == '__main__':
    start = time.time()
    data = spider(v_type="白菜", year=2024, month=3, begin=1, end=5)
    print(data[:10])
    print("Time consumed:", time.time()-start)