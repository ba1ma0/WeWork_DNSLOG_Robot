import json
import datetime
import time
import requests
import json
from datetime import timedelta
############################################################### 人工配置区 ###############################################################
robotAPI                 = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=wework_robot_token"                                    #企业微信机器人token
ceyeDNS                  = "http://api.ceye.io/v1/records?token=ceye_token&type=dns"                                                    #ceye.io注册获取的token
ceyeHTTP                 = "http://api.ceye.io/v1/records?token=ceye_token&type=http"                                                   #ceye.io注册获取的token
staffNoList              = ['01221455']                                                                                                 #机器人发送消息时需要被at的人!01221455为工号,需要at全部人的时候直接@all即可
sleepTime                = 5                                                                                                            #程序每隔5s请求一次ceye.io获取dnslog记录!
############################################################### 人工配置区 ###############################################################
baiduAPI                 = "https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?query=testflagIP&co=&resource_id=6006&oe=utf8"
IPAPI                    = "http://ip-api.com/json/testflagIP"
ceye_dns_previous        = ''
ceye_http_previous       = ''
WeWorktPostheaders       =   {'Content-Type':'application/json'}
WeWorktPostContent       =   ""
WeWorktPostdataTemp      =   {
                    "msgtype": "text",
                    "text": {
                    "content": WeWorktPostContent,
                    "mentioned_list":staffNoList,
    }
}
#WeWorktPostdata          = json.dumps(WeWorktPostdata)

#获取IP的相关详细信息
def getIPLocation(ip):
    try:
        IpInfoResult         =   json.loads(requests.get(baiduAPI.replace("testflagIP",str(ip))).text)
        info                 =   IpInfoResult['data'][0]['location']
        #print(info)    
    except Exception as e:
        try:
            IpInfoResult     =   json.loads(requests.get(IPAPI.replace("testflagIP",str(ip))).text)
            info             =   IpInfoResult['isp'] + "物理地址 "+ IpInfoResult['country'] + " " + IpInfoResult['region'] + " " + IpInfoResult['city']
            #print(info)
        except Exception as e:
            print(e)
            info             =    "IP  :"+str(ip)
            pass
    return info

#UTC时间转换为标准的北京时间字符串
def UTC2BJtime(UTCtimeStr):
    BJTime      =   datetime.datetime.strptime(UTCtimeStr,'%Y-%m-%d %H:%M:%S') + timedelta(hours=8)
    BJTimeStr   =   datetime.datetime.strftime(BJTime,'%Y-%m-%d %H:%M:%S')
    return BJTimeStr

#比较dnslog的结果
def comparePrevious():
    global ceye_dns_previous,ceye_http_previous
    result =  {'dnsChange':False,'dns':'','httpChange':False,'http':''}
    try:
         dnsResult               =  json.loads(requests.get(ceyeDNS).text)
         if dnsResult['data']   !=  []:
             if dnsResult['data'][0]['id'] not in ceye_dns_previous:
                ceye_dns_previous   = str(dnsResult['data'][0])
                #print (ceye_dns_previous)
                result['dnsChange'] = True
                result['dns'] = dnsResult['data'][0]
    except Exception as e:
        print(e)
        pass
    try:
         httpResult           = json.loads(requests.get(ceyeHTTP).text)
         if httpResult['data']   !=  []:
             if httpResult['data'][0]['id'] not in ceye_http_previous:
                 ceye_http_previous   = str(httpResult['data'][0])
                 result['httpChange'] = True
                 result['http'] = httpResult['data'][0]        
    except Exception as e:
        print(e)
        pass
    #print(str(result))
    return result

while True:
    WeWorktPostdata            = WeWorktPostdataTemp
    WeWorktPostdata1           = WeWorktPostdataTemp
    #print(WeWorktPostdata)
    try:
        result = comparePrevious()
        if result['dnsChange'] == True:
            ipInfo                      = getIPLocation(result['dns']['remote_addr'])
            WeWorktPostContent          = "*****************************DNS请求*****************************\n请求ID    : "+result['dns']['id']+ "\n请求时间 : "+UTC2BJtime(result['dns']['created_at'])+"\n"+"请求IP    : "+result['dns']['remote_addr']+"\nIP信息    : "+ipInfo+"\n请求DNS : "+result['dns']['name']+"\n*****************************DNS请求*****************************"
            WeWorktPostdata['text']['content']  = str(WeWorktPostContent)
            WeWorktPostdata             = json.dumps(WeWorktPostdata)
            #print(WeWorktPostdata)
            res                         = requests.post(url=robotAPI, data=WeWorktPostdata, headers=WeWorktPostheaders)
            #print(res)
        if result['httpChange'] == True:
            ipInfo                      = getIPLocation(result['http']['remote_addr'])
            WeWorktPostContent          = "*****************************HTTP请求*****************************\n请求ID    : "+result['http']['id']+ "\n请求时间 : "+UTC2BJtime(result['http']['created_at'])+"\n"+"请求IP    : "+result['http']['remote_addr']+"\nIP信息    : "+ipInfo+"\n请求方法 : "+result['http']['method']+"\nUA信息 : "+str(result['http']['user_agent'])+"\nData : "+str(result['http']['data'])+"\nContent-Type: "+str(result['http']['content_type'])+"\n请求地址 : "+result['http']['name']+"\n*****************************HTTP请求*****************************"
            WeWorktPostdata1['text']['content']  = str(WeWorktPostContent)
            WeWorktPostdata1            = json.dumps(WeWorktPostdata1)
            res                         = requests.post(url=robotAPI, data=WeWorktPostdata1, headers=WeWorktPostheaders)
            #print(res)
    except Exception as e:
        print(e)
        pass
    #print("Sleep 5s")
    time.sleep(sleepTime)
