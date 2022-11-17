import requests
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import json

#國內政府預算(10年)     
gdp = pd.read_csv('gdp.csv')

x = np.arange(99,109)    
x = [str(i)for i in x]
   
y1 = gdp['占GDP比例(%)'][9:]
y1 = y1.str.strip('%').astype(float)
y2 = gdp['占中央政府總預算比例(%)'][9:]
y2 = y2.str.strip('%').astype(float)

plt.rcParams['font.family']='Microsoft JhengHei'
plt.yticks(np.arange(0.1,1.5,0.1)) 
plt.plot(x,y1,marker = '*',color='#ca6702',label ='占 GDP 比例')
plt.plot(x,y2,marker = '*',color='#005f73',label ='占中央政府總預算比例')
plt.xlabel("年份" )                
plt.ylabel("百分比") 
plt.legend()
plt.savefig('GDP.png',dpi=100) 
plt.show()  




# 國民運動消費支出
spend = pd.read_csv('消費支出.csv',encoding = 'ansi')
s = list(spend.columns)
s = np.array(s[1:7])
spend1 = spend.T[:]
spend1 = spend1[:][1:7]
for i in range(8):
    plt.plot(s,spend1[i],label=spend['年份'][i],marker = '.')
plt.ylabel("運動消費支出比例%") 
plt.legend()
plt.savefig('消費支出.png',dpi=100)
plt.show()  



#規律運動
regular = pd.read_csv('110規律運動.csv',encoding = 'ansi')
regular = regular[:][1:]

plt.plot(regular['年齡別'],regular['男'],label='男' ,marker = '+')
plt.plot(regular['年齡別'],regular['女'],label='女' ,marker = '+')
plt.title("規律運動年齡比" )
plt.xticks(rotation=35)
plt.legend()
plt.savefig('規律運動比.png',dpi=100)
plt.show()  




# 運動目的(使用函數)

def load(file,name1,name2,num):
    pplist =[]
    pplist2=[]
    with open (file,encoding = 'utf8') as pfile:
        ppdata=json.load(pfile)
        for item in ppdata['data']:
                pplist.append(item['analyzeItem'])
                pplist2.append(item['statisticsItemValue'])    
    pplist=np.array(pplist)
    pplist2=np.array(pplist2)

    ppdata = pd.DataFrame(
        {name1:pplist,
         name2:pplist2})   
    ppmean =ppdata.groupby(name1)[name2].mean().sort_values(ascending=False)[:num]      
    plt.rcParams['font.family']='Microsoft JhengHei'
    sns.barplot(ppmean.index, ppmean,palette=("cubehelix"))
    plt.xticks(rotation=35)
    plt.savefig('{}.png'.format(name1),dpi=100)
    plt.show()
    
load('目的.json','目的','各縣市平均比例',6)




# 性別與喜好(爬取API)
api = 'https://isports.sa.gov.tw/Api/Rest/V1/SportsSituation.svc/GetSportsSituation?analyzeYear=110&analyzeTarget=13&statisticsItem=sex&sort=analyzeItem&paging=false'

plt.rcParams['font.family']='Microsoft JhengHei'
r = requests.get(api)
data = r.json()
datalist=[]
datalist1=[]
datalist2=[]
for item in data['data']:
    datalist.append(item['analyzeItem'])
    datalist1.append(item['statisticsItem'])
    datalist2.append(item['statisticsItemValue'])
datalist = np.array(datalist)
datalist1 = np.array(datalist1)
datalist2 = np.array(datalist2)
data = pd.DataFrame(
            {'運動項目':datalist,
             '性別':datalist1,
             '平均比例%':datalist2})   
data = data[data['性別']!='整體']
dmean =data.groupby(['性別','運動項目'])['平均比例%'].agg("mean").reset_index()
dmean= dmean.sort_values(by='平均比例%',ascending=False)[:14]
sns.barplot(x='運動項目',y='平均比例%',hue='性別', data=dmean,palette=("husl"))
plt.xticks(rotation=35)
plt.savefig('性別與喜好.png',dpi=100) 
plt.show()




# 性別與運動訊息來源(爬取API)

api = 'https://isports.sa.gov.tw/Api/Rest/V1/SportsSituation.svc/GetSportsSituation?analyzeYear=110&analyzeTarget=10&statisticsItem=sex&sort=analyzeItem&paging=false'
r = requests.get(api)
data = r.json()

datalist=[]
datalist1=[]
datalist2=[]
for item in data['data']:
    datalist.append(item['analyzeItem'])
    datalist1.append(item['statisticsItem'])
    datalist2.append(item['statisticsItemValue'])
datalist = np.array(datalist)
datalist1 = np.array(datalist1)
datalist2 = np.array(datalist2)

data = pd.DataFrame(
            {'消息來源':datalist,
             '平均比例%':datalist2,
             '性別':datalist1})   
data = data[data['性別']!='整體']
dmean =data.groupby(['性別','消息來源'])['平均比例%'].agg("mean").reset_index()
dmean= dmean.sort_values(by='平均比例%',ascending=False)[:9]

plt.rcParams['font.family']='Microsoft JhengHei'
sns.barplot(x='消息來源',y='平均比例%',hue='性別', data=dmean,palette=("husl"))
plt.xticks(rotation=35)
plt.savefig('消息來源與性別.png',dpi=100) 
plt.show()




# 年齡與運動訊息來源(爬取API)
api = 'https://isports.sa.gov.tw/Api/Rest/V1/SportsSituation.svc/GetSportsSituation?analyzeYear=110&analyzeTarget=10&statisticsItem=age&sort=statisticsItem&paging=false'
r = requests.get(api)
data = r.json()
datalist=[]
datalist1=[]
datalist2=[]
for item in data['data']:
    datalist.append(item['analyzeItem'])
    datalist1.append(item['statisticsItem'])
    datalist2.append(item['statisticsItemValue'])
datalist = np.array(datalist)
datalist1 = np.array(datalist1)
datalist2 = np.array(datalist2)

data = pd.DataFrame(
            {'消息來源':datalist,
             '平均比例%':datalist2,
             '年齡':datalist1})   
data = data[data['年齡']!='拒答']
data = data[data['年齡']!='整體']
data = data[data['消息來源']!='不知道/拒答']
dmean =data.groupby(['消息來源','年齡'])['平均比例%'].agg("mean").reset_index()
dmean= dmean.sort_values(by='年齡',ascending=True)[:]

sns.set(rc={'figure.figsize':(14,8)})
plt.rcParams['font.family']='Microsoft JhengHei'
sns.barplot(x='消息來源',y='平均比例%',hue='年齡', data = dmean, palette=("husl"))
plt.xticks(rotation=35)
plt.savefig('消息來源與年齡.png',dpi=100) 
plt.show()




# 每週次數 (json)

timelist =[]
timelist2=[]
with open ('每週次數.json',encoding = 'utf8') as tfile:
    timedata=json.load(tfile)
    for item in timedata['data']:
            timelist.append(item['analyzeItem'])
            timelist2.append(item['statisticsItemValue'])
timelist=np.array(timelist)
timelist2=np.array(timelist2)

timedata = pd.DataFrame(
    {'每週次數':timelist,
     '各縣市平均比例':timelist2})   

plt.rcParams['font.family']='Microsoft JhengHei'
plt.figure(figsize=(8,8))
sns.violinplot(data=timedata, x='各縣市平均比例', y='每週次數', palette='Set3')
plt.savefig('次數.png',dpi=100)
plt.show()


timedata1 = timedata[timedata.每週次數.isin(['1次','2次','沒有運動'])].shape[0]
timedata2 = timedata[timedata.每週次數.isin(['3次','4次','5次','6次','7次'])].shape[0]

plt.pie([timedata1,timedata2],labels=['少於3次','3次以上(含)'],
         autopct = "%.1f%%",explode = (0.02,0.02),shadow=True,
         colors=['#a8dadc','#fb8500'])
plt.savefig('次數比.png',dpi=100)
plt.show()




# 時間 (json)

minlist =[]
minlist2=[]
with open ('時間.json',encoding = 'utf8') as mfile:
    mindata=json.load(mfile)
    for item in mindata['data']:
            minlist.append(item['analyzeItem'])
            minlist2.append(item['statisticsItemValue'])
minlist=np.array(minlist)
minlist2=np.array(minlist2)
mindata = pd.DataFrame(
    {'每次運動時間':minlist,
     '比例':minlist2})   

minmean =mindata.groupby('每次運動時間')['比例'].mean().sort_values(ascending=False)[:6]     
plt.title('平均運動分鐘數')  
color_1 = ['#5b95b3','#E86C6B','#72d3d8','#A7B88D','#d1b3ea','#93A8E2']
sns.set(rc={'figure.figsize':(10,7)})
plt.rcParams['font.family']='Microsoft JhengHei'
plt.pie(minmean,labels=minmean.index, explode= (0.03,0.03,0.03,0.03,0.03,0.05),
        colors=color_1 ,autopct='%.1f%%') 
x_ = [1, 0, 0, 0, 0]
plt.pie(x_, radius=0.35, colors="w")
plt.xticks(rotation=35)
plt.savefig('每次時間.png',dpi=100)
plt.show()

# 年齡(爬取API)(圓餅圖)
api = 'https://isports.sa.gov.tw/Api/Rest/V1/SportsSituation.svc/GetSportsSituation?analyzeYear=110&analyzeTarget=13&statisticsItem=age&sort=statisticsItem&paging=false'
plt.rcParams['font.family']='Microsoft JhengHei'
r = requests.get(api)
data = r.json()
datalist=[]
datalist1=[]
datalist2=[]
for item in data['data']:
    datalist.append(item['analyzeItem'])
    datalist1.append(item['statisticsItem'])
    datalist2.append(item['statisticsItemValue'])
datalist = np.array(datalist)
datalist1 = np.array(datalist1)
datalist2 = np.array(datalist2)
data = pd.DataFrame(
            {'運動項目':datalist,
             '年齡':datalist1,
             '比例':datalist2})   
data = data[data['年齡']!='拒答']
data = data[data['年齡']!='整體']
data = data[data['運動項目']!='不知道/拒答']
data_age = data.groupby('年齡').count().index

for i in data_age:
    data1 = data[data['年齡']==i].sort_values(by='比例',ascending=False)[:5]
    colors = sns.color_palette('Set2')
    plt.pie(data1['比例'],labels = data1['運動項目'] , colors = colors, 
            autopct='%.0f%%',textprops={'fontsize': 16})
    plt.title('{}偏好從事的運動'.format(i),fontsize=18)
    plt.savefig('{}.png'.format(i),dpi = 100)
    plt.show()

# 匯出資料至數據庫

api ='https://isports.sa.gov.tw/Api/Rest/V1/SportsSituation.svc/GetSportsSituation?analyzeYear=110&analyzeTarget=05&statisticsItem=city&sort=statisticsItem&paging=false'
r = requests.get(api)
data = r.json()
datalist=[]
datalist1=[]
datalist2=[]
for item in data['data']:
    datalist.append(item['analyzeItem'])
    datalist1.append(item['statisticsItem'])
    datalist2.append(item['statisticsItemValue'])
datalist = np.array(datalist)
datalist1 = np.array(datalist1)
datalist2 = np.array(datalist2)
data = pd.DataFrame(
            {'運動次數':datalist,
             '地區':datalist1,
             '比例':datalist2})   
import MySQLdb

try:
    conn = MySQLdb.connect(host='localhost',
                           user = 'root',
                           password = '1004',
                           database = 'project',
                           port =3306,
                           charset = 'utf8')
    cursor = conn.cursor()
    
    sql='''CREATE TABLE IF NOT EXISTS MAP(City VARCHAR(5),
                                          Times VARCHAR(5),
                                          statistics_Value float(5))'''
    
    cursor.execute(sql)
except:
    print('建表失敗')
try:
    for i in range(len(data)):
        sql = '''INSERT INTO MAP (City,Times,statistics_Value)
                         VALUES(%s,%s,%s)'''
        cursor.execute(sql,(datalist1[i],datalist[i],datalist2[i]))
        conn.commit()
except:
    print('匯入失敗')