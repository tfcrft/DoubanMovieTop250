import requests
from bs4 import BeautifulSoup
import xlwt
import re


def openHTML(url):
    headerua = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
    response = requests.get(url,headers=headerua)
    html = response.content
    return html

def getData(baseurl):
    movie_name = re.compile(r'<span class="title">(.*?)</span>')
    movie_image = re.compile(r'<img.*src="(.*?)"')
    movie_link = re.compile(r'<a href="(.*?)">')
    movie_rating = re.compile(r'<span class="rating_num" property="v:average">(.*?)</span>')
    movie_judgenum = re.compile(r'<span>(\d*?)人评价</span>')
    movie_quote = re.compile(r'<span class="inq">(.*?)</span>')
    datalist = []
    for i in range(0,10):
        url = baseurl + "?start=" + str(i*25) + "&filter="
        html = openHTML(url)
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all("div",attrs={'class':'item'}):
            data = []
            item = str(item)
            name = re.findall(movie_name,item)[0]
            data.append(name)
            image = re.findall(movie_image,item)[0]
            data.append(image)
            link = re.findall(movie_link,item)[0]
            data.append(link)
            rating = re.findall(movie_rating,item)[0]
            data.append(rating)
            judgenum = re.findall(movie_judgenum,item)[0]
            data.append(judgenum)
            quote = re.findall(movie_quote,item)
            data.append(quote)
            datalist.append(data)
    return datalist

def saveData(datalist,savepath):
    book = xlwt.Workbook(encoding='utf-8',style_compression=0)
    sheet = book.add_sheet("豆瓣电影TOP250",cell_overwrite_ok=True)
    cols = ('名称','图片','链接','评分','人数','简介')
    for i in range(0,6):
        sheet.write(0,i,cols[i])
    for i in range(0,250):
        data = datalist[i]
        for j in range(0,6):
            sheet.write(i+1,j,data[j])
    book.save(savepath)

def main():
    print("开始爬取！")
    baseurl = 'https://movie.douban.com/top250'
    datalist = getData(baseurl)
    savepath = r'D:\豆瓣电影TOP250.xls'
    saveData(datalist,savepath)

main()
print("爬取成功！")

