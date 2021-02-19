'''
Author: MGod_wu
Date: 2021-02-06 10:02:48
LastEditTime: 2021-02-07 16:54:57
LastEditors: Please set LastEditors
Description: 数据分析及可视化，可生成前25位人气主播分析网页，直播类型平均人气值排名网页，
主播人气值与数量关系网页，生成的网页数据均在./result目录下
'''

# import json
from pyecharts import options as opts
from pyecharts.charts import Bar,Pie,Page,Grid
from pyecharts.globals import ThemeType
import json


# 全局变量
data_path = r'./result'  # 存储数据的路径


def analys_of_data(datas):
    """
    对主播类型进行分类，统计
    (dict)type_dict : {
        'type' : {
            'count': int,
            'popularity': int,
        }
        'type' : str(popularity*10000 + count)
    }
    """
    type_dict = dict()
    for data in datas:
        if data['type'] not in type_dict.keys():
            type_dict[data['type']] = data['popularity'] * 100000 + 1
        else:
            type_dict[data['type']] += data['popularity'] * 100000 + 1

    num_list = sorted([num%100000 for num in list(type_dict.values())], reverse=True)     # 获得类型数量的降序列表
    popul_list = sorted([int(num/100000) for num in list(type_dict.values())], reverse=True)     # 获得类型人气值的降序列表
    # 人气前25名的直播内容统计
    data_list = sorted(datas, key=lambda x: x['popularity'], reverse=True)
    popul_dict = dict()
    for data in data_list[:25]:
        if data['type'] not in popul_dict.keys():
            popul_dict[data['type']] = data['popularity'] * 100 + 1
        else:
            popul_dict[data['type']] += data['popularity'] * 100 + 1

    # 创建统计前25位人气主播的网页
    page_1 = Page(page_title='关于前25位人气主播分析')
    a = (
        Bar(init_opts=opts.InitOpts(width='100%'))
        .add_xaxis([data_list[num]['name'] for num in range(25)])
        .add_yaxis('',[round(data_list[num]['popularity']/10000,1) for num in range(25)], color='#fa0000')
        .set_global_opts(
            title_opts=opts.TitleOpts(title="前25位人气主播排名\n(单位：万)"),
            datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
        )
        .set_series_opts(
            xaxis_opts=opts.AxisOpts(name='主播名称'),
            title_opts=opts.TitleOpts(title="人气值占比",pos_left='10%',pos_top='2%'),
            legend_opts=opts.LegendOpts(is_show=False),
        )
    )
    b = (
        Pie(init_opts=opts.InitOpts(width='100%'))
        .add(
            series_name="数量占比",
            data_pair=[(list(popul_dict.keys())[num],list(popul_dict.values())[num]%100) for num in range(popul_dict.__len__())],
            radius=50,
            center=['90%','15%'],
        )
        .add(
            series_name="人气占比",
            data_pair=[(list(popul_dict.keys())[num],int(list(popul_dict.values())[num]/100)) for num in range(popul_dict.__len__())],
            radius=50,
            center=['90%','40%'],
        )
        .set_series_opts(
            title_opts=opts.TitleOpts(title='数量占比情况'),
            legend_opts=opts.LegendOpts(type_='scroll',pos_left="50%", pos_top="2%",is_show=True),
        )
    )
    grid = (
        Grid(init_opts=opts.InitOpts(width='100%',height='720px',theme=ThemeType.DARK))
        .add(a, grid_opts=opts.GridOpts(pos_top="10%", pos_right="10%"))
        .add(b, grid_opts=opts.GridOpts(pos_left="90%", pos_top='10%'))
    )
    page_1.add(grid)
    page_1.render(f'{data_path}/analys_of_25.html')
    # 提取类型前32（数量）的进行分类
    source_num_1 = list()
    source_num_2 = list()
    source_num_3 = list()
    source_num_4 = list()
    source_num_1.append(["数量", "人气", "类型"])
    source_num_2.append(["数量", "人气", "类型"])
    source_num_3.append(["数量", "人气", "类型"])
    source_num_4.append(["数量", "人气", "类型"])
    for num in range(type_dict.__len__()):
        type_num = list(type_dict.values())[num]%100000
        type_popul = int(list(type_dict.values())[num]/100000)
        type_name = list(type_dict.keys())[num]
        if num_list[8] < type_num <= num_list[0]:
            source_num_1.append([type_num, type_popul, type_name])
        elif num_list[16] < type_num <= num_list[8]:
            source_num_2.append([type_num, type_popul, type_name])
        elif num_list[24] < type_num <= num_list[16]:
            source_num_3.append([type_num, type_popul, type_name])
        elif num_list[32] < type_num <= num_list[24]:
            source_num_4.append([type_num, type_popul, type_name])

    # 提取类型前32（人气）的进行分类
    source_popul_1 = list()
    source_popul_2 = list()
    source_popul_3 = list()
    source_popul_4 = list()
    source_popul_other = {
        'type': '其他',
        'popularity': 0,
        'num': 0,
    }
    source_popul_1.append(["人气", "数量", "类型"])
    source_popul_2.append(["人气", "数量", "类型"])
    source_popul_3.append(["人气", "数量", "类型"])
    source_popul_4.append(["人气", "数量", "类型"])
    for num in range(type_dict.__len__()):
        type_num = list(type_dict.values())[num]%100000
        type_popul = int(list(type_dict.values())[num]/100000)
        type_name = list(type_dict.keys())[num]
        if popul_list[8] < type_popul <= popul_list[0]:
            source_popul_1.append([type_popul, type_num, type_name])
        elif popul_list[16] < type_popul <= popul_list[8]:
            source_popul_2.append([type_popul, type_num, type_name])
        elif popul_list[24] < type_popul <= popul_list[16]:
            source_popul_3.append([type_popul, type_num, type_name])
        elif popul_list[32] < type_popul <= popul_list[24]:
            source_popul_4.append([type_popul, type_num, type_name])
        else:
            source_popul_other['popularity'] += type_popul
            source_popul_other['num'] += type_num
    # # 创建一个网页实例，用于整合多张图表
    page_2 = Page(page_title='直播类型一览图1')
    page_3 = Page(page_title='直播类型一览图2')

    # 创建横向柱状图
    def create_bar(source,page,x_type,x_name,y_type,title,range,range_text,split_num=8):
        c = (
            Bar(init_opts=opts.InitOpts(width='100%',height='480px',theme=ThemeType.DARK))
            .add_dataset(source=source)
            .add_yaxis(
                series_name="",
                y_axis=[],
                encode={"x": x_type, "y": y_type},
                label_opts=opts.LabelOpts(is_show=False),
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(title=title),
                xaxis_opts=opts.AxisOpts(name=x_name),
                yaxis_opts=opts.AxisOpts(type_="category"),
                visualmap_opts=opts.VisualMapOpts(
                    orient="horizontal",
                    pos_left="center",
                    min_=range[0],
                    max_=range[1],
                    range_text=range_text,
                    dimension=0,
                    range_color=["#D7DA8B", "#E15457"],
                    is_piecewise=True,
                    split_number=split_num,
                ),
            )
        )
        page.add(c)

    create_bar(source_num_1,page_2,'人气','人气','类型','类型人气(数量:前8名)',(num_list[7],num_list[0]),('数量高','数量低'))
    create_bar(source_num_2,page_2,'人气','人气','类型','类型人气(数量:第8~16名)',(num_list[15],num_list[8]),('数量高','数量低'))
    create_bar(source_num_3,page_2,'人气','人气','类型','类型人气(数量:第16~24名)',(num_list[23],num_list[16]),('数量高','数量低'))
    create_bar(source_num_4,page_2,'人气','人气','类型','类型人气(数量:第24～32名)',(num_list[31],num_list[24]),('数量高','数量低'))
    page_2.render(f'{data_path}/type_of_num.html')

    create_bar(source_popul_1,page_3,'数量','数量','类型','类型数量(人气:前8名)',(popul_list[7],popul_list[0]),('人气高','人气低'),split_num=5)
    create_bar(source_popul_2,page_3,'数量','数量','类型','类型数量(人气:第8~16名)',(popul_list[15],popul_list[8]),('人气高','人气低'),split_num=5)
    create_bar(source_popul_3,page_3,'数量','数量','类型','类型数量(人气:第16~24名)',(popul_list[23],popul_list[16]),('人气高','人气低'),split_num=5)
    create_bar(source_popul_4,page_3,'数量','数量','类型','类型数量(人气:第24～32名)',(popul_list[31],popul_list[24]),('人气高','人气低'),split_num=5)
    page_3.render(f'{data_path}/type_of_popular.html')

    # 类型平均人气一览图
    source = list()
    for s in source_popul_1[1:]:
        source.append([s[2],round(s[0]/s[1]/100000,1)])
    for s in source_popul_2[1:]:
        source.append([s[2],round(s[0]/s[1]/100000,1)])
    for s in source_popul_3[1:]:
        source.append([s[2],round(s[0]/s[1]/100000,1)])
    source.append([source_popul_other['type'],round(source_popul_other['popularity']/100000/source_popul_other['num'],1)])
    d = (
        Bar(init_opts=opts.InitOpts(width='100%',height='720px',theme=ThemeType.DARK,page_title='直播平均人气排名'))
        .add_xaxis([s[0] for s in source])
        .add_yaxis('人气值(单位：万)',[s[1] for s in source], color='#fa0000')
        .set_global_opts(
            title_opts=opts.TitleOpts(title="直播类型平均人气排名"),
            datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
        )
        .set_series_opts(
            xaxis_opts=opts.AxisOpts(name='直播类型'),
            legend_opts=opts.LegendOpts(is_show=False),
        )
        .render(f'{data_path}/avg_of_popular.html')
    )

# with open('./result/datas[210218].json', 'r') as fp:
#     datas = json.loads(fp.read())['datas_222300']

# print(datas)

# a = analys_of_data(datas)
