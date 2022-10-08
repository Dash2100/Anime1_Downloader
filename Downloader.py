import requests, re
from bs4 import BeautifulSoup
from urllib.parse import unquote
import time

path = "./Downloads/"

def Download(url,cookies,name):
    global title
    headers_cookies ={
        "accept": "*/*",
        "accept-encoding": 'identity;q=1, *;q=0',
        "accept-language": 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        "cookie": cookies,
        "dnt": '1',
        "user-agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    downsize = 0
    r = requests.get(url, headers=headers_cookies, stream=True)
    file_size = round(int(r.headers['content-length'])/1024/1024,2)
    if r.status_code == 200:
        print("Downloading " + title + ' ' + name)
        with open(path+name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    downsize += len(chunk)
                    line = 'Downloading %s %.2f MB / %.2f MB'
                    line = line % (name, downsize / 1024 / 1024, file_size)
                    print(line, end='\r')
            print(line)
    else:
        print("Download Error: " + str(r.status_code))
    print("--------------------")



def Anime(url):
    global title
    r = requests.post(url,headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.34"})

    soup = BeautifulSoup(r.text, 'html.parser')

    title = soup.find('h1', class_='page-title').text

    all_url = []
    videos = soup.find_all("video")
    for video in videos:
        data = {'d':unquote(video['data-apireq'])}
        r = requests.post("https://v.anime1.me/api",data=data)
        t = "https://" + str(r.text).replace('{"s":[{"src":"//','').replace('","type":"video/mp4"}]}','')
        set_cookie = r.headers['set-cookie']
        cookie_e = re.search(r"e=(.*?);", set_cookie, re.M|re.I).group(1)
        cookie_p = re.search(r"p=(.*?);", set_cookie, re.M|re.I).group(1)
        cookie_h = re.search(r"HttpOnly, h=(.*?);", set_cookie, re.M|re.I).group(1)
        cookies = 'e={};p={};h={};'.format(cookie_e, cookie_p, cookie_h)
        name = t.split('/')[-1]
        Download(t,cookies,name)

if __name__ == '__main__':
    Anime("https://anime1.me/category/2017年春季/情色漫畫老師")