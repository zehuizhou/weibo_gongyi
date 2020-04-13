# -*- coding: utf-8 -*-
import os
import sys
import time
import requests
from parsel import Selector
import pandas as pd


web_header = {
    'cookie': 'Hm_lvt_c153f37e6f66b16b2d34688c92698e4b=1586746203; Hm_lpvt_c153f37e6f66b16b2d34688c92698e4b=1586746419',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive'
}


def spider(page):
    url = 'https://www.chunyuyisheng.com/pc/qalist/?page={}&high_quality=1'
    ret = requests.get(url=url.format(page), headers=web_header).text
    root = Selector(ret)
    div_list = root.xpath("//div[@class='hot-qa main-block']/div")

    need_list = []
    for div in div_list:
        item = {}
        item['问题'] = div.xpath("string(.//div[@class='qa-item qa-item-ask']/a)").get('').strip().replace('问', '').replace('\n', '').replace('\t', '')
        detail_url = 'https://www.chunyuyisheng.com/' + div.xpath(".//div[@class='qa-item qa-item-ask']/a/@href").get('').strip()
        item['链接'] = detail_url
        item['日期'] = div.xpath(".//span[@class='date']/text()").get('')
        item['医生'] = div.xpath(".//div[@class='qa-item qa-item-doctor']/em/text()").get('').strip()
        hospital = div.xpath("string(.//div[@class='qa-item qa-item-doctor'])").get('').strip().replace('\t', '')
        item['医院'] = hospital.split('\n')[1]

        det_ret = requests.get(url=detail_url.format(page), headers=web_header).content.decode()
        det_root = Selector(det_ret)
        item['问答内容'] = '\n'.join(det_root.xpath("//div[@class='problem-detail-wrap']//p/text()").getall()).replace('\n', '').replace('\t', '').replace(' ', '')

        print(item)
        need_list.append(item)
    return need_list


def save_list_dict(file_name, list_dict):
    """
    保存字典列表
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
    for i in range(1, 201):
        data = spider(i)
        save_list_dict('春雨医生问答.csv', data)
        print(f"##############{i}##############保存成功")
        time.sleep(1)
