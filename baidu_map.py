import os
import requests
import _thread
from time import sleep
from selenium import webdriver
from browsermobproxy import Server
from selenium.webdriver.chrome.options import Options

# 依赖库 如上 import


def save(res, x, y, z):
    if not os.path.isdir(path):
        print("创建储存环境")
        os.makedirs(path)
    sname = path+"/{z}_{x}_{y}.png".format(z=z, x=x, y=y)
    with open(sname, 'ab') as pngf:
        for chunk in res.iter_content(chunk_size=1024):
            if chunk:
                pngf.write(chunk)
                pngf.flush()


def savePicturesViaUrl(url):
    arr = url.split("&")
    save(requests.get(url),
         arr[1].replace("x=", ""),
         arr[2].replace("y=", ""),
         arr[3].replace("z=", ""))


def initView():
    global server, proxy, browser
    print("环境准备中。。。")
    server = Server('browsermob-proxy.bat')
    server.start()
    proxy = server.create_proxy()
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--proxy-server={0}'.format(proxy.proxy))
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.maximize_window()
    sleep(1)
    proxy.new_har('map', options={
        'captureHeaders': True, 'captureContent': True})

    browser.get("http://api.map.baidu.com/lbsapi/getpoint/index.html")
    print("环境准备 succes！！")
    setConfig()


def setConfig():
    print("设置数据")
    sleep(1)
    browser.find_element_by_id("localvalue").send_keys(addressText)
    sleep(1)
    if addressIs:
        browser.find_element_by_id("pointLabel").click()
        sleep(1)
    browser.find_element_by_id("localsearch").click()
    print("设置完成")
    sleep(2)
    proxyReptile()


ing_b = True


def ing():
    index = ["/", "─", "\\", ]
    while ing_b:
        for i in range(len(index)):
            print("\r"+index[i], end="")
            sleep(0.2)
    print()
    print()


def proxyReptile():
    b = False
    res = proxy.har
    print("开始爬取。。。")
    try:
        _thread.start_new_thread(ing, ())
    except:
        print('error')
    for entry in res['log']['entries']:
        res_url = entry['request']['url']
        if res_url.find('/?qt=s&c=') >= 0 or res_url.find('/?qt=cen&b=') >= 0:
            b = True
        if b and res_url.find('bdimg.com/tile/?qt=vtile') >= 0:
            savePicturesViaUrl(res_url)
    global ing_b
    ing_b = False
    openFile()


def openFile():  # 完成
    print("爬取完成！")
    print("文件已经放在\t"+os.getcwd()+"\\map\\"+addressText+"\\ \t下三秒后打开")
    sleep(3)
    start_directory = os.getcwd()+"\\map\\"+addressText
    os.startfile(start_directory)
    browser.quit()
    server.stop()


if __name__ == '__main__':
    server = browser = proxy = None
    addressIs = False  # 开启坐标查询 False 位置查询
    # addressText = "108.925786,34.478292"  # 坐    标/地址
    addressText = "中华郡"  # 地址
    path = os.getcwd()+"\\map\\"+addressText+"\\"  # 地址
    initView()
