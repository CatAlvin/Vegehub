import pandas as pd
from pyecharts.charts import Map
import pyecharts.options as opts
import mysql.connector
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot

# 创建mysql连接
def mysql_connect():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='wbh53100',
            database='vegehub'
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def fetch_data(vegetable_name):
    conn = mysql_connect()
    cursor = conn.cursor()
    query = "SELECT region FROM market WHERE vegetable_name = %s"
    cursor.execute(query, (vegetable_name,))
    result = cursor.fetchall()
    conn.close()
    return [item[0] for item in result]  # 提取元组中的地区名称

# 示例省份列表
provinces = [
    '北京', '天津', '河北', '山西', '内蒙古', '辽宁', '吉林', '黑龙江', 
    '上海', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南',
    '湖北', '湖南', '广东', '广西', '海南', '重庆', '四川', '贵州',
    '云南', '西藏', '陕西', '甘肃', '青海', '宁夏', '新疆', '香港', '澳门', '台湾'
]

# 定义全称映射
province_full_names = {
    '北京': '北京市',
    '天津': '天津市',
    '河北': '河北省',
    '山西': '山西省',
    '内蒙古': '内蒙古自治区',
    '辽宁': '辽宁省',
    '吉林': '吉林省',
    '黑龙江': '黑龙江省',
    '上海': '上海市',
    '江苏': '江苏省',
    '浙江': '浙江省',
    '安徽': '安徽省',
    '福建': '福建省',
    '江西': '江西省',
    '山东': '山东省',
    '河南': '河南省',
    '湖北': '湖北省',
    '湖南': '湖南省',
    '广东': '广东省',
    '广西': '广西壮族自治区',
    '海南': '海南省',
    '重庆': '重庆市',
    '四川': '四川省',
    '贵州': '贵州省',
    '云南': '云南省',
    '西藏': '西藏自治区',
    '陕西': '陕西省',
    '甘肃': '甘肃省',
    '青海': '青海省',
    '宁夏': '宁夏回族自治区',
    '新疆': '新疆维吾尔自治区',
    '香港': '香港特别行政区',
    '澳门': '澳门特别行政区',
    '台湾': '台湾省'
}

def draw_vegetable_region_chart(vege_name, filepath=None):
    # 数据处理删除不是省份的数据并恢复全称
    def filter_provinces(region_list):
        return [province_full_names[region] for region in region_list if region in province_full_names]

    def count_provinces(region_list):
        province_counts = {}
        for region in region_list:
            if region in province_counts:
                province_counts[region] += 1
            else:
                province_counts[region] = 1
        return province_counts

    # 获取数据并进行过滤和统计
    data = fetch_data(vege_name)
    if not data:
        print("please check your input")
    else:
        province_data = filter_provinces(data)
        province_counts = count_provinces(province_data)

        # 构建数据列表，用于 pyecharts 地图
        data_for_chart = [[province, count] for province, count in province_counts.items()]

        # 创建中国地图
        map_chart = (
            Map(init_opts=opts.InitOpts(width="1000px", height="600px"))
            .set_global_opts(
                title_opts=opts.TitleOpts(title="生产"+vege_name+"的省份"),
                visualmap_opts=opts.VisualMapOpts(
                    is_piecewise=True,  # 使用分段颜色配置
                    range_text = ['供应商数量:', ''],
                    pieces=[
                        {"min": 8, "label": '> 8', "color": "#375623"},
                        {"min": 5, "max": 8, "label": '5-8', "color": "#548235"},
                        {"min": 3, "max": 4, "label": '1-4', "color": "#A9D08E"},
                        {"min": 1, "max": 2, "label": '0', "color": "#E2F0D9"}
                    ],
                    pos_left='left',  # 将 visualMap 控件放置在左边
                    pos_top='middle',  # 将 visualMap 控件放置在垂直方向的中间位置
                ),
            )
            .add(
                series_name=vege_name,
                data_pair=data_for_chart,
                maptype="china",
                is_map_symbol_show=False,
                label_opts=opts.LabelOpts(is_show=False),  # 不显示省份名称
            )
            .set_series_opts(
                itemstyle_opts={
                    "normal": {"color": '#375623', "border_color": '#375623'}
                },
            )
        )
    
        # 渲染图表为HTML文件或保存为图片
        if filepath:
            if filepath.endswith('.html'):
                map_chart.render(filepath)
            elif filepath.endswith('.png'):
                map_chart.render('imgs/temp.html')  # 先渲染为临时HTML文件
                make_snapshot(snapshot, 'imgs/temp.html', filepath)
                
            print(f"Map saved to {filepath}")
        else:
            map_chart.render_notebook()
