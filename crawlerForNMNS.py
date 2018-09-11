
# coding: utf-8

# In[ ]:

import selenium
from selenium import webdriver
import urllib.request
import ssl
import datetime

uploadDate = "2018-07-29"
aliveMonth = 3
localtime = datetime.datetime.today()

uploadDatetime = datetime.datetime.strptime(uploadDate,"%Y-%m-%d")
replaceMonth = uploadDatetime.month + aliveMonth

urlInvalidDate = uploadDatetime.replace(month = replaceMonth)

xpath_attribute = {
    '//div[@data-swiper-slide-index]':'style',
    '//div[@data-swiper-slide-index]/img':'src'
}

# urls to be get
url_dict = {}

driver = webdriver.Chrome(r'D:\pyLadies\2018_0805_nmnsCrawler\chromedriver.exe')
totalDays = 3

# method findURL() : get the clean URLs, and put in url_dict{}
def findURL(xpath,attribute):
    images = driver.find_elements_by_xpath(xpath)
    picNumber = 0 # 圖片張數計算 picture number to count how many pictures in this album

    for image in images:
        tagContent = image.get_attribute(attribute)
        
        if tagContent.find('\"') == -1: pass              
        else: 
            tagContent = tagContent.split('\"')[-1]
            # ↑split the string if it comes from attribute "style" 

        if tagContent.find("https://") == -1: return False            
        else:
            url = tagContent.split('\"')[0]
            # ↑split to get clear url from attribute "style"
            if url in url_dict: pass
            else: 
                picNumber += 1
                url_dict[url] = "Day" + str(day) + "_" + str(picNumber).zfill(3) + ".jpg"
            

# main
if localtime > urlInvalidDate: # check the date, future/now is larger than past
    print("相簿已逾期！請手動確認檔案是否仍存在。")
else:
    for day in range(1,totalDays+1): # get the url of the day
        urlDay = 'http://www.nmns.edu.tw/web/learn/feature/photo.htm?id={idNo}'.format(idNo=12+day)
             # ↑url of day 1 = http://www.nmns.edu.tw/web/learn/feature/photo.htm?id=13
        driver.get(urlDay)

        for xpath,attribute in  xpath_attribute.items(): # get url from xpath
            if findURL(xpath,attribute) != False:
                print("Day",day,"取得網址！","目前字典長度:",len(url_dict))
            else:
                print( "注意：「", xpath, " + ", attribute, "」的組合失敗。" )
                  
    for key,value in url_dict.items(): #download images from url,and save in file name
#        print(key,value)
        ssl._create_default_https_context = ssl._create_unverified_context
            # ↑ to pass the SSL certificate verify
        resource = urllib.request.urlopen(key)
        output = open(value,"wb") # write binary
        output.write(resource.read())
        output.close()
    print("下載結束")
    
    
driver.close()

