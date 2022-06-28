# WeWork_DNSLOG_Robot 自动监测dnslog并推送到企业微信群 

# 0x01 第一步
按照DNSLOG.py脚本中提示填写相关配置信息
```
###该工具的主要作用是每隔5s请求一次ceye.io,如果有新的dnslog记录则推送到企业微信
#####################################################人工配置#####################################################
robotAPI                 = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=wechat_robot_token"                    #wechat_robot_token是在企业微信群中申请的机器人链接
ceyeDNS                  = "http://api.ceye.io/v1/records?token=ceye_token&type=dns"                                    #ceye_token是在ceye.io申请的token
ceyeHTTP                 = "http://api.ceye.io/v1/records?token=ceye_token&type=http"                                   #ceye_token是在ceye.io申请的token
staffNoList              = ['01221455']                                                                                 #机器人发送消息时需要被at的人!需要at全部人的时候直接@all即可
sleepTime                = 5                                                                                            #程序每隔5s请求一次ceye.io获取dnslog记录!
#####################################################人工配置#####################################################
```
# 0x02 第二步
后台运行监控命令
```
nohup python3 DNSLOG.py 
```
# 0x03 第三步
配合https://github.com/ba1ma0/SDLC_Vuln_Auto_Find 组合进行使用,然后在企业微信中静待ssrf,或者其他漏洞
![](https://raw.githubusercontent.com/ba1ma0/WeWork_DNSLOG_Robot/main/1.png)
