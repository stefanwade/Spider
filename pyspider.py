#!/usr/bin/env python
#encoding:utf-8
#Filename: pyspider.py
'''
-----------------------------------------
Author:	stefan
Version: 2016-9-19
-----------------------------------------
'''
import urllib2
import urllib

post:

values = {"username":"1447792117", "password":"aszx"}

values['username']="1447792117"
values['password']="aszx"
data = urllib.encode(values)
url = "http://www.baidu.com"
request = urllib2.Request(url, data)
response = urllib2.urlopen(request)
html = response.read()
print html

get:

geturl = url + '?' + data
request = urllib2.Request(geturl)
response = urllib2.urlopen(request)
html = response.read()
print html

user_agent = ''
headers = {'User-Agent' : user_agent,
			'Referer' : 'http://www.zhihu.com/articles'}

request = urllib2.urlopen(url, data, headers)


enable_proxy = True   #防止服务器限制多次访问
proxy_handler = urllib2.ProxyHandler({"http" : 'http://'})
null_proxy_handler = urllib2.ProxyHandler({})

if enable_proxy:
	opener = urllib2.build_opener(proxy_handler)
else:
	opener = urllib2.build_opener(null_proxy_handler)

urllib2.install_opener(opener)

# timeout: urlopen传入参数，防止某些网站响应是在太慢


#选择http的请求方式
request.get_method = lambda: 'PUT'


# 捕捉异常
# urlerror
try:
	urllib2.urlopen(request)
except: urllib2.URLError, e:
	print e.reason
# httperror
try:
	urllib2.urlopen(req)
except: urllib2.HTTPError, e:
	print e.code
# httperror是urlerror的子类，一般排除异常父类应该写在子类的后面
# 另外可以用hasattr属性进行判断

try: 
	urllib2.urlopen(req)
except: urllib2.URLError, e:
	if hasattr(e, 'code')：
		print e.code
	elif: hasattr(e, 'reason')
		print e.reason
else:
	print 'ok'

cookielib:提供可存储的cookie对象
CookieJar->派生->FileCookieJar->派生->MoziilaCookieJar和LWPCookieJar

import urllib2
import cookielib

cookie = cookielib.CookieJar()









 
 