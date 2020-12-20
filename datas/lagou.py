# coding: utf-8
import requests
from lxml.html import etree
import json
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
import os
from pandas import DataFrame
from pymongo import MongoClient

header = {
    'Host':'m.lagou.com',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A366 Safari/600.1.4'
}
client = MongoClient()
db = client['lagou']

start_url = 'https://m.lagou.com/search.json'
# response = requests.get(start_url,params=params,headers = header)
# data = response.json()
# for i in data['content']['data']['page']['result']:

# print(data['content']['data']['page']['totalCount'])

class LagouJob():
    def __init__(self,language,path,**position):
        self.start_url = 'https://m.lagou.com/search.json'
        self.path = path
        self.job_list = []
        self.total_job = None
        self.json_url = []
        self.language = language
        self.params = {
            'positionName': language,
            'pageNo': 1,
            'pageSize': 15,
        }
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        self.collection = db[self.language]
        self.getJobNum()
        self.generate_url()
        self.get_data()
        self.save_to_excel()

    def getJobNum(self):
        print("Fetching {}".format(self.language))
        try:
            response = requests.get(self.start_url,params=self.params,headers = header)
            print(response.status_code)
            data = response.json()
            self.total_job = int(data['content']['data']['page']['totalCount'])
            print("Total job {}".format(self.total_job))
        except requests.ConnectionError as e:
            print('Error', e.args)

    def generate_url(self):
        for i in range(1,int(self.total_job/15)+1):
            self.params = {
                'positionName': language,
                'pageNo': i,
                'pageSize': 15,
            }
            self.json_url.append(self.params)
        print("Total page {}".format(len(self.json_url)))

    def get_data(self):
        count = 0
        for i in self.json_url:
            try:
                response = requests.get(self.start_url,params = i,headers = header,timeout=50)
                data = response.json()
                for i in data['content']['data']['page']['result']:
                    self.job_list.append(i)
                    if self.collection.insert(i):
                        print("Saved to Mongo {}".format(i))
                    else:
                        print("Fail to save data")
                print("page {}".format(count))
                count+=1
            except requests.ConnectionError as e:
                print("Error",e.args)

    def save_to_excel(self):
        companyFullName = []
        createTime = []
        positionId = []
        companyId = []
        companyName = []
        city = []
        positionName = []
        salary = []
        companyLogo = []
        for job in self.job_list:
            companyFullName.append(job['companyFullName'])
            createTime.append(job['createTime'])
            positionId.append('//lagou.com/jobs/'+str(job['positionId'])+".html")
            companyId.append('//lagou.com/gongsi/'+str(job['companyId'])+".html")
            companyName.append(job['companyName'])
            city.append(job['city'])
            positionName.append(job['positionName'])
            salary.append(job['salary'])
            companyLogo.append('//www.lagou.com/'+job['companyLogo'])
        data = {'companyFullName' : companyFullName,'createTime' : createTime,
                'positionId' : positionId,'companyId' : companyId,
                'companyName':companyName,'city':city,
                'positionName':positionName,'salary':salary,'companyLogo':companyLogo}
        frame = DataFrame(data)
        frame.to_excel(self.path + '\\' +self.language +'_job.xls', index=True)
        print("Saved to excel")
if __name__ == '__main__':
    path = "D:\\lagou"
    language = ['Java', 'C++', 'PHP','数据挖掘', '搜索算法',
                '精准推荐', 'C', '全栈工程师', 'C#', 'Hadoop',
                'Python', 'Delphi', 'VB', 'Perl', 'Ruby',
                'Node.js', 'Go', 'ASP', 'Shell', '后端开发','机器学习']
    for i in language:
        job = LagouJob(i,path)

