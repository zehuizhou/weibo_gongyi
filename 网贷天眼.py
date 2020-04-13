# -*- coding: utf-8 -*-
import os
import re
import sys
import time
import requests
from parsel import Selector
import pandas as pd


web_header = {
    'Host': 'www.p2peye.com',
    'cookie': 'TYID=enANiF5nJIiw+5wdC/s5Ag==; __jsluid_s=0e9786ad85cc2f1574e0aa0a64bb7f27; __firstReferrerKey__=%7B%22%24first_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DGIbxRjGaO7r3eH1twp5P8EzY2amTOwW1yUresGwpfBUUrzgC3KpP95Jf_alqy3KkOBqj34GOjPuaySCYNhR3FK%26wd%3D%26eqid%3Def8d526a0000bccc000000045e672475%22%2C%22%24first_referrer_host%22%3A%22www.baidu.com%22%7D; TJID=enANjV5nJIm6HhWNDEknAg==; A4gK_987c_saltkey=S8sw1178; A4gK_987c_lastvisit=1586741462; A4gK_987c_sendmail=1; PHPSESSID=69dlqpdohmfrj6ntb4g9j1q492; Hm_lvt_556481319fcc744485a7d4122cb86ca7=1586745066; bdp_data2017jssdkcross=%7B%22distinct_id%22%3A%22170c2e6b8c7651-06b1a27bb7421-4313f6a-2073600-170c2e6b8c88ac%22%2C%22props%22%3A%7B%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22user_id%22%3A%22aqTtxytT%22%2C%22target_name%22%3A%22emptyaqTtxytT%7CemptyaqTtxytT%7CemptyaqTtxytT%22%2C%22%24is_first_session%22%3A0%7D%7D; Hm_lpvt_556481319fcc744485a7d4122cb86ca7=1586745312; A4gK_987c_lastact=1586745312%09auth.php%09; __bdpa_session_key__2017__=%7B%22session_time%22%3A1586745318705%2C%22session_id%22%3A%2217171604186806-0cb5c88bd28b98-5313f6f-2073600-17171604187e1%22%2C%22session_hasBeenExpired%22%3A0%2C%22lastSend_sessonId%22%3A%2217171604186806-0cb5c88bd28b98-5313f6f-2073600-17171604187e1%22%7D',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive'
}


def spider(page):
    url = 'https://www.p2peye.com/forumlist-10-{}.html'
    ret = requests.get(url=url.format(page), headers=web_header).text
    print(ret)
    time.sleep(1)
    root = Selector(ret)
    div_list = root.xpath("//div[@class='person_project clearfix']")
    need_list = []
    # for div in div_list:
    #     item = {}
    #     item['标题'] = div.xpath(".//div[@class='title']/a[1]/text()").get('').strip()
    #     detail_url = 'https://gongyi.weibo.com' + div.xpath(".//div[@class='title']/a[1]/@href").get('').strip()
    #     item['链接'] = detail_url
    #     item['类型'] = div.xpath(".//div[@class='title']/a[2]/text()").get('').strip().replace('【', '').replace('】', '')
    #     item['发起人'] = div.xpath(".//div[@class='project_info W_linkb']/a[1]/text()").get('').strip()
    #     rw = div.xpath(".//div[@class='project_more']/a[@class='WF_btn WF_btn3 ']/span/text()").get('').strip()
    #     item['爱心转发'] = re.findall('\d+', rw)[0]
    #
    #     det_ret = requests.get(url=detail_url.format(page), headers=web_header).content.decode()
    #     det_root = Selector(det_ret)
    #     item['目标筹款'] = det_root.xpath("//div[@class='num-right']/dl/dd/i/text()").get('').strip().replace(',', '')
    #     item['已筹款'] = det_root.xpath("//div[@class='num-left']/dl/dd/i/text()").get('').strip().replace(',', '')
    #     item['捐款人次'] = det_root.xpath("//div[@class='num-center']/dl/dd/i/text()").get('').strip().replace(',', '')
    #     item['完成率'] = det_root.xpath("//h5[@class='bar']/i/text()").get('').strip()
    #     print(item)
    #     need_list.append(item)
    # return need_list


def save_list_dict(file_name, list_dict):
    """

    :param file_name:
    :param list_dict: [{},{},{},...]
    :return:
    """
    path = os.path.join(os.path.dirname(sys.argv[0]), file_name)
    flag = True
    if os.path.isfile(path):
        flag = False
    df = pd.DataFrame(list_dict)
    df.to_csv(path, mode='a', encoding='utf_8_sig', index=False, header=flag)


if __name__ == '__main__':
    for i in range(1, 195):
        data = spider(i)
        # save_list_dict('微博公益.csv', data)
        print(f"##############{i}##############保存成功")
        time.sleep(1)
