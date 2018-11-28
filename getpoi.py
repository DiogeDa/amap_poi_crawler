# 高德地图：http://ditu.amap.com/  
#高德地图poi：http://lbs.amap.com/api/webservice/guide/api/search/#text
#首先得申请一个下载poi数据的key，然后在对应位置填入你的key 
import json
import xlwt
from datetime import datetime
from urllib import request
from urllib.parse import quote
import time
import os


# 获取数据
def get_data(pageindex,url_amap):
    global total_record
    # 暂停500毫秒，防止过快取不到数据
    time.sleep(0.5)
    print('解析页码： ' + str(pageindex) + ' ... ...')
    url = url_amap.replace('pageindex', str(pageindex))
    # 中文编码
    url = quote(url, safe='/:?&=')
    html = ""
    with request.urlopen(url) as f:
        html = f.read()
        rr = json.loads(html)
        if total_record == 0:
            total_record = int(rr['count'])
        return rr['pois']    

def getPOIdata(page_size,json_name,url_amap):
    global total_record
    print('获取POI数据开始')
    josn_data = get_data(1,url_amap)
    if (total_record % page_size) != 0:
        page_number = int(total_record / page_size) + 2
    else:
        page_number = int(total_record / page_size) + 1

    with open(json_name, 'w') as f:
        # 去除最后]
        f.write(json.dumps(josn_data).rstrip(']'))
        for each_page in range(2, page_number):
            html = json.dumps(get_data(each_page,url_amap)).lstrip('[').rstrip(']')
            if html:
                html = "," + html
            f.write(html)
            print('已保存到json文件：' + json_name)
        f.write(']')
    print('获取POI数据结束')


# 写入数据到excel
def write_data_to_excel(json_name,hkeys,bkeys,name):
    # 获取当前日期
    today = datetime.today()
    # 将获取到的datetime对象仅取日期如：2017-4-6
    today_date = datetime.date(today)
    
    # 从文件中读取数据
    fp = open(json_name, 'r')
    result = json.loads(fp.read())
    # 实例化一个Workbook()对象(即excel文件)
    wbk = xlwt.Workbook()
    # 新建一个名为Sheet1的excel sheet。此处的cell_overwrite_ok =True是为了能对同一个单元格重复操作。
    sheet = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)

    # 创建表头
    # for循环访问并获取数组下标enumerate函数
    for index, hkey in enumerate(hkeys):
        sheet.write(0, index, hkey)

    # 遍历result中的每个元素。
    for i in range(len(result)):
        values = result[i]
        n = i + 1
        for index, key in enumerate(bkeys):
            val = ""
            # 判断是否存在属性key
            if key in values.keys():
                val = values[key]
            sheet.write(n, index, val)
    wbk.save(name + str(today_date) + '.xls')
    print('保存到excel文件： ' + name + str(today_date) + '.xls!')

if __name__ == '__main__':
    json_name = 'data_amap.json'
    os.makedirs('data_index')
    # 高德地图poi：http://lbs.amap.com/api/webservice/guide/api/search/#text
    #city = ["北京市","天津市","上海市","重庆市","河北省","山西省","辽宁省","吉林省","黑龙江","江苏省","浙江省",
    #        "安徽省","福建省","江西省","山东省","河南省","湖北省","湖南省","广东省","海南省","四川省","贵州省",
    #        "云南省","陕西省","甘肃省","青海省","台湾省","内蒙古自治区","广西壮族自治区","西藏自治区","宁夏回族自治区","新疆维吾尔自治区","香港特别行政区","澳门特别行政区"]
    
    #解析city.json数据，读取城市列表
    city = []
    data = open("city.json",encoding="utf-8-sig")
    # 转换为python对象
    strJson = json.load(data)
    for i in range(len(strJson)):
        city.append(strJson[i]['n'])
    
    keyword =["派出所"]
    #关键词："加油站","汽车销售","汽车维修","美食","购物","生活服务","体育休闲","医疗保健","宾馆酒店","风景",...等等
    #type具体可以查表http://lbs.amap.com/api/webservice/guide/api/search/#text
    #type = ["010000","020000","030000","050000","060000","070000","080000","090000","100000","110000","140000","150000","160000"]
    type=["130501"]
    
    for i in range(0,len(city)):
        for j in range(0,len(keyword)):
            ##填入你的key
            url_amap = 'http://restapi.amap.com/v3/place/text?key=此处填入你的key&keywords='+ keyword[j] +'&types='+ type[j] +'&city='+ city[i] +'&citylimit=true&children=1&offset=20&page=pageindex&extensions=all'
            page_size = 25  # 每页记录数据，强烈建议不超过25，若超过25可能造成访问报错
            page_index = r'page=1'  # 显示页码
            global total_record
            total_record = 0
            # Excel表头
            hkeys = ['id', '行业类型', '名称', '类型', '地址', '联系电话', 'location', '省份代码', '省份名称', '城市代码', '城市名称', '区域代码', '区域名称',
                     '所在商圈']
            # 获取数据列
            bkeys = ['id', 'biz_type', 'name', 'type', 'address', 'tel', 'location', 'pcode', 'pname', 'citycode', 'cityname',
                     'adcode', 'adname', 'business_area']
            # 写入数据到json文件，第二次运行可注释
            getPOIdata(page_size,json_name,url_amap)
            # 读取json文件数据写入到excel
            #os.makedirs("data_index\\"+city[i])
            write_data_to_excel(json_name,hkeys,bkeys,"data_index\\"+city[i]+keyword[j]+"-高德地图")
            if(i%13==0):
                time.sleep(45)
            elif(i%13!=0):
                time.sleep(15)
    
