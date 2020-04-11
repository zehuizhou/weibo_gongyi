# -*- coding: utf-8 -*-
import os
import re
import sys
import time
import requests
from parsel import Selector
import pandas as pd


web_header = {
    'Host': 'gongyi.weibo.com',
    'cookie': 'SINAGLOBAL=9039371595693.941.1576205125652; _ga=GA1.2.1684815725.1577155440; wvr=6; _s_tentry=login.sina.com.cn; UOR=,,login.sina.com.cn; Apache=9602868821266.52.1586416476438; ULV=1586416477267:29:2:2:9602868821266.52.1586416476438:1586245592331; gongyi-G0=d99269416c41b8948978c323b1bf51e9; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWES-MGSxVJk.S7AzfIp_iT5JpX5KMhUgL.FoecSKe7Sh-4e0z2dJLoIEXLxKBLBonL1h5LxKqL1-BLB-qLxKqLBo5L1KBLxKnLBoBLBKnLxKqLBo5LBoBt; ALF=1618115108; SSOLoginState=1586579109; SCF=AqURd7rrLbKR6K42oMeW_I-_GcEWkVQLrLN_HSe9iIZfTsvFbX71Vr0n-Xb8BJgFGZAcn57Y2X7s15XePRoKxRU.; SUB=_2A25zlTb1DeRhGeVI7lER9CvFyD6IHXVQ4y89rDV8PUNbmtANLUXmkW9NTAX_rFcREYu9B91dscrexCdr0UkUWVqR; SUHB=04WemHOyc-8USO; webim_unReadCount=%7B%22time%22%3A1586579115031%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A0%7D',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive'
}


def spider(page):
    url = 'https://gongyi.weibo.com/list/personal?on_state=0&donate_type=0&state=1&type=0&location=&title=&open=0&page={}'
    ret = requests.get(url=url.format(page), headers=web_header).content.decode()
    time.sleep(1)
    root = Selector(ret)
    div_list = root.xpath("//div[@class='person_project clearfix']")
    need_list = []
    for div in div_list:
        item = {}
        item['标题'] = div.xpath(".//div[@class='title']/a[1]/text()").get('').strip()
        detail_url = 'https://gongyi.weibo.com' + div.xpath(".//div[@class='title']/a[1]/@href").get('').strip()
        item['链接'] = detail_url
        item['类型'] = div.xpath(".//div[@class='title']/a[2]/text()").get('').strip().replace('【', '').replace('】', '')
        item['发起人'] = div.xpath(".//div[@class='project_info W_linkb']/a[1]/text()").get('').strip()
        rw = div.xpath(".//div[@class='project_more']/a[@class='WF_btn WF_btn3 ']/span/text()").get('').strip()
        item['爱心转发'] = re.findall('\d+', rw)[0]

        det_ret = requests.get(url=detail_url.format(page), headers=web_header).content.decode()
        det_root = Selector(det_ret)
        item['目标筹款'] = det_root.xpath("//div[@class='num-right']/dl/dd/i/text()").get('').strip().replace(',', '')
        item['已筹款'] = det_root.xpath("//div[@class='num-left']/dl/dd/i/text()").get('').strip().replace(',', '')
        item['捐款人次'] = det_root.xpath("//div[@class='num-center']/dl/dd/i/text()").get('').strip().replace(',', '')
        item['完成率'] = det_root.xpath("//h5[@class='bar']/i/text()").get('').strip()
        print(item)
        need_list.append(item)
    return need_list


def save_list_dict(file_name, list_dict):
    path = os.path.join(os.path.dirname(sys.argv[0]), file_name)
    flag = True
    if os.path.isfile(path):
        flag = False
    df = pd.DataFrame(list_dict)
    df.to_csv(path, mode='a', encoding='utf_8_sig', index=False, header=flag)


if __name__ == '__main__':
    for i in range(1, 195):
        data = spider(i)
        save_list_dict('微博公益.csv', data)
        print(f"##############{i}##############保存成功")
        time.sleep(1)
