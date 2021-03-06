#coding: utf-8
import requests
import os
import sys
from pandas import DataFrame
from urllib.parse import quote
import json
import pymongo
from pymongo import MongoClient
import random
ua_pc = [ 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
        ' Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
        ' Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
         'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
        ' Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
        ' Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
         'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)']
ua_mobile = ['Mozilla/5.0(iPhone;U;CPUiPhoneOS4_3_3likeMacOSX;en-us)AppleWebKit/533.17.9(KHTML,likeGecko)Version/5.0.2Mobile/8J2Safari/6533.18.5',
                'Mozilla/5.0(iPad;U;CPUOS4_3_3likeMacOSX;en-us)AppleWebKit/533.17.9(KHTML,likeGecko)Version/5.0.2Mobile/8J2Safari/6533.18.5',
                'MQQBrowser/26Mozilla/5.0(Linux;U;Android2.3.7;zh-cn;MB200Build/GRJ22;CyanogenMod-7)AppleWebKit/533.1(KHTML,likeGecko)Version/4.0MobileSafari/533.1',
                 'Opera/9.80(Android2.3.4;Linux;OperaMobi/build-1107180945;U;en-GB)Presto/2.8.149Version/11.10',
                 'Mozilla/5.0(iPhone;U;CPUiPhoneOS4_3_3likeMacOSX;en-us)AppleWebKit/533.17.9(KHTML,likeGecko)Version/5.0.2Mobile/8J2Safari/6533.18.5']
header = {'User-Agent':random.choice(ua_pc)}
url = 'https://movie.douban.com/j/search_subjects?type=tv&tag=%E5%9B%BD%E4%BA%A7%E5%89%A7&sort=rank&page_limit=20&page_start=0'
r = requests.get(url,header)
print(r.status_code)
data = r.json()
class Douban_Movie():
    def __init__(self,path):
        self.base_url = 'https://movie.douban.com/j/search_subjects?type=tv&tag='
        self.sort = ['recommend','time','rank']
        self.movie_type = ['热门','美剧','英剧','韩剧','日剧','国产剧','港剧','日本动画','综艺', '纪录片']
        self.path = path
        self.user_type = ''
        self.user_sort = ''
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        self.data_list = {}
        self.title = []
        self.id = []
        self.url = []
        self.rate = []
        self.cover = []
        self.is_new = []
        self.playable = []
        self.json = None
        self.data = {}
        self.value = []
        self.get_json()
        self.mongo()
        self.download_cover()
    def generate_url(self,tag,sort,page_limit,page_start):
        url_list = []
        for i in range(20,page_limit+20,20):
            url = 'https://movie.douban.com/j/search_subjects?type=tv&tag='+ quote(tag) + '&sort=' + quote(
                sort) + '&page_limit=20'+ '&page_start=' + str(i-20)
            url_list.append(url)
        # print(url_list)
        return url_list
    def get_url(self):
        tag = int(input(" 请输入电影电视剧类型: 热门 (1) 美剧 (2) 英剧 (3) 韩剧 (4) 日剧 (5) 国产剧 (6) 港剧 (7) 日本动画 (8) 综艺 (9) 纪录片 (10)\n"))
        sort = int(input(" 请输入排序方式: 按热度排序 (1) 按时间排序 (2) 按评价排序 (3)\n"))
        tag = self.movie_type[tag-1]
        sort = self.sort[sort-1]
        self.user_type = tag
        self.user_sort = sort
        page_limit = int(input(" 请输入电视剧数量 (电视剧数量应该小于等于 500):\n"))
        page_start = int(input(" 请输入开始页:\n"))
        url = self.generate_url(tag,sort,page_limit,page_start)
        return url
    def get_json(self):
        urls = self.get_url()
        count = 0
        for url in urls:
            try:
                print("capturing %s page" %(count))
                count+=1
                r  =requests.get(url,headers = {'User-Agent':random.choice(ua_pc)},timeout = 50)
                print(r.status_code)
            except:
                pass
            data = r.json()
            value = data.values()
            for i in value:
                for j in i:
                    self.value.append(j)
            self.json = r.json()
            dict = data.values()
            list = []
            for i in dict:
                for j in i:
                    list.append(j)
            for i in list:
                self.title.append(i['title'])
                self.url.append(i['url'])
                self.playable.append(i['playable'])
                self.rate.append(i['rate'])
                self.cover.append(i['cover'])
                self.id.append(i['id'])
                self.is_new.append(i['is_new'])
        print(" 已经获取完所有你选择的豆瓣电影数据, 正在写入 xls 文件 ")
        self.data = {'title':self.title,'id': self.id,'rate':self.rate,'cover':self.cover,
                     'url':self.url,'is_new':self.is_new,'playable':self.playable}
        frame = DataFrame(self.data)
        frame.to_excel(self.path + '\\' + self.user_type + self.user_sort + '.xls',index=True)

    def download_cover(self):
        choice = int(input(" 你要下载刚才获取的电影封面图吗?(1 : 下载，0 : 不用下载)\n"))
        if choice ==0:
            sys.exit()
        if not  os.path.exists(self.path+"\\"+self.user_type+"_" + self.user_sort+"_"+"cover"):
            os.mkdir(self.path+"\\"+self.user_type+"_" + self.user_sort+"_"+"cover")
        count =0
        for i in self.cover:
            try:
                print("downloading %s " %(count))
                r = requests.get(i,headers = header,timeout = 50)
                with open(self.path+"\\"+self.user_type+"_" + self.user_sort+"_"+"cover"+"\\"+str(count)+i[-4:],'wb') as f:
                    f.write(r.content)
                count+=1
            except:
                print("download error")
                pass

    def mongo(self):
        print(len(self.value))
        dict = {"subjects" : self.value}
        data = json.dumps(dict)
        datas = json.loads(data)
        try:
            douban = MongoClient('localhost', 27017)
            douban_db = douban['douban']
            # 连接 douban_movie 这个表，如果不存在则自动创建
            douban_set = douban_db.south_korea
            douban_set.insert(datas)
            douban_set.save(datas)
            print(" 成功存入数据库 ")
        except EnvironmentError:
            print(" 存入数据库失败 ")
            pass
if __name__ == '__main__':
    path = "D:\\douban"
    print(" 豆瓣电影数据默认保存在 D: 盘哦 ")
    douban = Douban_Movie(path)