###高德地图AMAP爬取POI程序###

###通过城市列表爬取POI###

#缺点：大城市会爬不全！！！

Tips：分块爬取POI详见https://github.com/zhoujungis/Get_amap_poi_by_polygon


1.使用getpoi.py程序获取poi数据表（需要修改城市名，关键词以及对应的编码，编码需要查询）

2.去除所有表头，只保留一个，然后使用excel_merge.py合并所有的excel（修改对应的路径）

3.数据分列，将location分为lon和lat两列

4.使用huoxing2wgs84.py进行坐标转换，转化为wgs1984，然后利用arcgis转化为shape文件，all done！！！（修改对应的路径）
