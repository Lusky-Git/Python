# 網址：https://maoyan.com/board/4?offset=global      每頁+10，共10頁

import requests
import time
import threading
from bs4 import BeautifulSoup


def main():
    page = 0  # 頁數
    for i in range(0, 4):
        if i != 0:
            page += 10
            url = "https://maoyan.com/board/4?offset="+str(page)
        else:
            url = "https://maoyan.com/board/4"
            page += 10
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
        }

        r = requests.get(url, headers=headers)

        r.encoding = "UTF-8"
        soup = BeautifulSoup(r.text, 'lxml')

        main = soup.find('div', attrs={'class': 'wrapper'}).find(
            'dl', attrs={'class': 'board-wrapper'}).findAll('dd')
        threading.Thread(target=get_information, args=(headers, main)).start()


def get_information(headers, main):
    proxy = {
        'https': '218.60.8.99:3129'
    }
    num = 0  # 排名
    for j in main:
        num += 1
        name = j.find('div', attrs={'class': 'board-item-main'}
                      ).find('p', attrs={'class': 'name'}).find('a').text
        print(str(num)+': '+name)
        # f.write(str(num)+': '+name)
        # f.write('\n')
        star = j.find('div', attrs={'class': 'board-item-main'}
                      ).find('p', attrs={'class': 'star'}).text
        print('    '+star.strip())
        # f.write('    '+star.strip())
        # f.write('\n')/
        releasetime = j.find('div', attrs={
                             'class': 'board-item-main'}).find('p', attrs={'class': 'releasetime'}).text
        print('    '+releasetime+'\r\n')
        # f.write('    '+releasetime)
        # f.write('\n')
        url_child = j.find('div', attrs={'class': 'board-item-main'}).find(
            'p', attrs={'class': 'name'}).find('a').get('href')
        url_child = "https://maoyan.com"+url_child
        r_child = requests.get(url=url_child, headers=headers, proxies=proxy)
        r_child.encoding = "UTF-8"
        # print(r_child.text)
        soup_child = BeautifulSoup(r_child.text, 'lxml')
        Introduction = soup_child.find('span', attrs={'class': 'dra'})
        # print(Introduction)
        print('劇情簡介:'+'\r\n    '+Introduction+'\r\n\r\n')
        # f.write('劇情簡介:'+'\r\n      '+Introduction+'\r\n\r\n')
    time.sleep(0.1)


if __name__ == "__main__":
    main()
