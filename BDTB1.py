#-*- coding:utf-8 -*- 
from __future__ import absolute_import

from io import open
import urllib2, urllib
import urllib2, urllib, urlparse
import urllib2, urllib
import urllib2, urllib, urlparse
import urllib2, urllib
import urllib2, urllib
import re
import os



# In[2]:

#处理页面标签类
class Tool(object):
    #去除img标签,7位长空格
    removeImg = re.compile(u'<img.*?>| {7}|')
    #删除超链接标签
    removeAddr = re.compile(u'<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine = re.compile(u'<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile(u'<td>')
    #把段落开头换为\n加空两格
    replacePara = re.compile(u'<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile(u'<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile(u'<.*?>')

    @staticmethod
    def replace(x):
        x = re.sub(Tool.removeImg,u"",x)
        x = re.sub(Tool.removeAddr,u"",x)
        x = re.sub(Tool.replaceLine,u"\n",x)
        x = re.sub(Tool.replaceTD,u"\t",x)
        x = re.sub(Tool.replacePara,u"\n    ",x)
        x = re.sub(Tool.replaceBR,u"\n",x)
        x = re.sub(Tool.removeExtraTag,u"",x)
        #strip()将前后多余内容删除
        return x.strip()


# In[23]:

#百度贴吧爬虫类
class BDTB(object):

    #初始化，传入基地址，是否只看楼主的参数
    def __init__(self, baseUrl, seeLZ=1, floorTag=1):
        #base链接地址
        self.baseURL = baseUrl
        #是否只看楼主
        self.seeLZ = u'?see_lz='+unicode(seeLZ)
        #HTML标签剔除工具类对象
        self.tool = Tool
        #全局file变量，文件写入操作对象
        self.file = None
        #楼层标号，初始为1
        self.floor = 1
        #默认的标题，如果没有成功获取到标题的话则会用这个标题
        path = urllib2.urlparse.urlsplit(u'http://tieba.baidu.com/p/3140626987').path
        tie_id = os.path.split(path)[-1]
        self.defaultTitle = tie_id
        #是否写入楼分隔符的标记
        self.floorTag = floorTag

    #传入页码，获取该页帖子的代码
    def getPage(self,pageNum):
        
        #构建URL
        if pageNum == 0:
            url = self.baseURL
        else:
            url = self.baseURL+ self.seeLZ + u'&pn=' + unicode(pageNum)
            
        try:
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            #返回UTF-8格式编码内容
            return response.read().decode(u'utf-8')
        #无法连接，报错
        except urllib2.URLError, e:
            if hasattr(e,u"reason"):
                print u"连接百度贴吧失败,错误原因",e.reason
                return None

    #获取帖子标题
    def getTitle(self,page):
        #得到标题的正则表达式
        pattern = re.compile(ur'<h(\d)(\W)+class="core_title_txt.*>(.*)</h\1>')
        result = re.search(pattern,page)
        if result:
            #如果存在，则返回标题
            result = result.group(0)
            pattern2=ur'(?<=>)(.*)(?=</h\d>)'
            result2 = re.search(pattern2, result).group(0).strip()
            #bs4.BeautifulSoup(matched_result, 'html.parser').text.strip()
            return result2
        
        else:
            return None

    #获取帖子一共有多少页
    def getPageNum(self, page):
        #获取帖子页数的正则表达式
        pat1=re.compile(ur'<li(\W)+class="l_reply_num.*</span>.*<span.*>(.*)</span>')
        result=re.search(pat1, page).group(0)
        
        pat2=re.compile(ur"回复贴，(\W)*共<span(\W)+.*>(\d)+</span>")
        result2=re.search(pat2, result).group(0)
        
        pat3=ur"(?<=>)(\d)+(?=</span>)"
        result3=re.search(pat3, result2).group(0)
    
        return int(result3)

    #获取每一层楼的内容,传入页面内容
    def getContent(self, page):
        #匹配所有楼层的内容
        pattern = re.compile(u'<div id="post_content_.*?>(.*?)</div>')
        items = re.finditer(pattern,page)
        contents = []
        for item in items:
            #将文本进行去除标签处理，同时在前后加入换行符
            content = u"\n"+self.tool.replace(item.group(0))+u"\n"
            contents.append(content)
        return contents

    def openFile(self,title):
        #如果标题不是为None，即成功获取到标题
        if title is not None:
            self.file = open(title + u".txt",u"w", encoding=u'utf-8')
        else:
            self.file = open(self.defaultTitle + u".txt",u"w", encoding=u'utf-8')
            
            
    def closeFile(self):
        self.file.close()
        
    def __del__(self):
        if hasattr(self, u'file'):
            self.file.close()
            
        
        
    def writeData(self,contents):
        #向文件写入每一楼的信息
        for item in contents:
            if self.floorTag == 1:
                #楼之间的分隔符
                floorLine = u"\n" + unicode(self.floor) + u'='*80 + u'\n'
                
                self.file.write(floorLine)
            self.file.write(item)
            self.floor += 1

    def start(self):
        content = self.getPage(0)
        pageNum = self.getPageNum(content)
        title = self.getTitle(content)
        self.openFile(title)
        if pageNum == None:
            print u"the URL {0:s} might be invalidated".format(self.baseURL)
            return
        try:
            print u"This tie {0:s} has {1:d} pages".format(title, pageNum)
            for i in xrange(1,int(pageNum)+1):
                print u"write to page {0:d}".format(i)
                page = self.getPage(i)
                content = self.getContent(page)
                self.writeData(content)
        #出现写入异常
        except IOError, e:
            print e
        else:
            print u"write successful"
        finally:
            self.closeFile()


# In[24]:

#url='http://tieba.baidu.com/p/3348528950'
#url='http://tieba.baidu.com/p/3138733512'
url=u'http://tieba.baidu.com/p/2640820711'
tb_t1 = BDTB(url, seeLZ=1, floorTag=1)
#page_one = tb_t1.getPage(0)


# In[25]:

tb_t1.start()