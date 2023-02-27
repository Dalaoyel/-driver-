import os
from PIL import Image
import re
import time
import random
import string
import threading
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from selenium.webdriver.chrome.service import Service
 
def selelnium_test(url, save_path, num, word):
    # chrome_options = Options() # 模拟器设置
    # chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # driver = webdriver.Chrome(chrome_options=chrome_options) # 将配置文件加载进webdriver
    # executable_path = r"chromedriver.exe"
    # driver = webdriver.Chrome(executable_path=executable_path)

    # s = Service(r"C:\Users\syyyyyw\Desktop\python\爬虫\chromedriver.exe")
    s = r"C:\Users\syyyyyw\Desktop\python\爬虫\chromedriver.exe"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    #chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(executable_path=s,options=chrome_options)
    driver.get(url)

    for i in range(num):
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(0.5)
 
    html = driver.page_source
    bsObj = BeautifulSoup(html,'lxml')
    find_imgs = bsObj.findAll("img", {'src': re.compile(r'http[^\s]*')})

    print("Strat download {} the picture....".format(url[:20]))

    for img in find_imgs:
        try:
            imgurl = img.attrs['src']
            value = ''.join(random.sample(string.ascii_letters + string.digits, 10))
            path = os.path.join(save_path, "%s.jpg" % value)
            urlretrieve(imgurl, path)
            
            #170修改增加            
            image    = Image.open(path)
            image = image.convert('RGB')
            os.remove(path)
            image.save(path)
   

        except:
            print("出现一次问题")

    log_file = open("log.txt", 'a', encoding='utf-8')
    now_time = time.ctime()
    text = now_time + " : " +save_path + " ++ " + word + " == " + url +'\n'
    log_file.write(text) 
    log_file.close()
    driver.quit()
 
 
if __name__ == '__main__':
    # ################ 单网页查找
    # 搜索的网页
    # url = 'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1615262073187_R&pv=&ic=&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&sid=&word=警察'
    # # 图片存放地址
    # save_path = "警察"
    # # 搜索的页数
    # num = 100
    # if not os.path.exists(save_path):
    #     os.mkdir(save_path)
    # selelnium_test(url, save_path, num)

    # #### 多网页查找图片
    url_list = [
        "https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1677159878416_R&pv=&ic=&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&dyTabStr=MCwzLDQsMiw1LDEsNiw3LDgsOQ%3D%3D&ie=utf-8&sid=&word={}"
    # 'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1615262073187_R&pv=&ic=&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&sid=&word={}',
    # 'https://cn.bing.com/images/search?q={}&qs=n&form=QBIR&sp=-1&pq={}&sc=8-2&cvid=16DE4364C909433390F0CE8B1FE322AB&first=1&tsc=ImageBasicHover',
    # 'https://image.so.com/i?q={}&src=srp',
    # 'https://pic.sogou.com/pics?query={}&w=05009900',
    # 'http://www.chinaso.com/newssearch/image?q={}',
    # 'https://www.google.com.hk/search?q={}&tbm=isch&ved=2ahUKEwjxxrjX7NXzAhXlHjQIHQ3hDWUQ2-cCegQIABAA&oq={}&gs_lcp=CgNpbWcQAzoFCAAQgARQq4lNWMamTWDXqE1oA3AAeACAAbUCiAHXG5IBBTItOS4zmAEAoAEBqgELZ3dzLXdpei1pbWewAQDAAQE&sclient=img&ei=72VuYbGTMOW90PEPjcK3qAY&bih=866&biw=1290'
    ]

    content = {"印章背景板":["论文"]}

#170修改
    # big_label = "卫视logo"
    # with open (r"C:\Users\syyyyyw\Desktop\python\爬虫\卫视txt\卫视.txt",encoding="utf-8") as f:
    #     for line in f.readlines():
    #         line = line.strip()
    #         content[big_label+"\\"+line]=[line+"台标"]
    # print("读取要搜索数据已完成")    
    page = 5


    for name in content:
        if not os.path.exists(name):
            os.makedirs(name)

        word_list = content[name]
        for word in word_list:
            threadNum = 10
            threadLoad = [0] * threadNum
            _index = 0
            for url in url_list:
                if "cn.bing.com" in url or "google.com.hk" in url:
                    new_url = url.format(word, word)
                else:
                    new_url = url.format(word)

                threadLoad[_index] = threading.Thread(target=selelnium_test, args=(new_url, name, page, word))
                threadLoad[_index].start()
                _index += 1
                time.sleep(60)
                
