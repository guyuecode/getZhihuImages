#!/usr/bin/env python3
#! _*_ coding:utf-8 _*_

import requests
import re,os,uuid
# from bs4 import BeautifulSoup
import json,random

# 问题id
answer_id = "29024583"

limit = 5
offset = 5
# 存储图片的目录名字
dir_name = "lalalala"
# 创建存储图片的目录
if not os.path.exists(dir_name):
    os.mkdir(dir_name)

UA_list = [
            "Mozilla/5.0 ( ; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
           "Opera/9.80 (Windows NT 6.1; U; en-US) Presto/2.7.62 Version/11.01",
           "Mozilla/5.0 (Windows NT 6.1; rv:1.9) Gecko/20100101 Firefox/4.0",
           "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.3 Safari/534.24",
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.0 Safari/534.24",
           "Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.44 Safari/534.13",
           "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.19 Safari/534.13",
           "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0",
           "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; zh-cn) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
           "Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10gin_lib.cc"
           ]
def UA(ua_list):
    n = random.randint(0,len(ua_list)-1)
    return ua_list[n]

def getImageList(html):
    reg = 'http[^"]*?\.jpg'
    imgre = re.compile(reg)
    imgList = re.findall(imgre,html)
    return imgList


def download_images(ImageList):
    for imgurl in ImageList:
        imgrp = requests.get(imgurl)
        if imgrp.status_code == 200:
            with open(dir_name+'/'+ str(uuid.uuid1()) +'.jpg','wb') as f:
                f.write(imgrp.content)

def get_json(ru):
    headers = {
        "Referer": "https://www.zhihu.com/question/"+answer_id,
        "User-Agent":UA(UA_list),
        "orgin": "https://www.zhihu.com",
        "Accept":"application/json, text/plain, */*",
        "authorization":"oauth c3cef7c66a1843f8b3a9e6a1e3160e20",
    }
    respone = requests.get(ru,headers=headers).content
    return json.loads(respone.decode("utf-8"))


while True:
    print(offset)
    post_data = "data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,upvoted_followees;data[*].mark_infos[*].url;data[*].author.follower_count,badge[?(type=best_answerer)].topics&offset=%s&limit=%s&sort_by=default" % (offset, limit)
    request_json_url = "https://www.zhihu.com/api/v4/questions/%s/answers?include=%s" % (answer_id,post_data)

    que_list = get_json(request_json_url)
    for a in que_list["data"]:
        question_html = a["content"]
        imageList = getImageList(question_html)
        if len(imageList) >0:
            download_images(set(imageList))

    offset += limit

