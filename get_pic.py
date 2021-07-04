import requests
from bs4 import BeautifulSoup
import re

# 从贴吧的帖子的里面get到所有的图片链接然后下载到指定的路径

header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64"}
# url =input("输入帖子链接")
url = "https://tieba.baidu.com/p/6189901499?pn="
findurl = re.compile(r'src="(.*?)"')

url_list = []
html = requests.get(url=url + "1", headers=header).content
response = BeautifulSoup(html, "html.parser")
# 爬取到的页数是网页上实际查看到的2倍，故÷2
page = int(int(response.find_all("span", class_="red")[3].get_text()) / 2)

for i in range(1, page + 2):
    if i != 1:
        html = requests.get(url=url + str(i), headers=header).content
        response = BeautifulSoup(html, "html.parser")
    img_bs = response.find_all("img", class_="BDE_Image")
    print("获取第"+str(i)+"页的图片链接~~~")
    for item in img_bs:
        src = re.findall(findurl, str(item))[0]
        url_list.append(src)
url_list = list(set(url_list))
print("总共有"+str(len(url_list))+"张图片~~~")
download_location = input("请输入下载地址：")
for i in range(1,len(url_list)+1):
    with open(download_location+"\\"+str(i)+".jpg",'wb') as f:
        print("下载第"+str(i)+"张图片~~~")
        f.write(requests.get(url=url_list[i-1],headers = header).content)
