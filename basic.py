from flask import Flask, request
from flask_restful import Api, Resource
from audioop import reverse
from operator import itemgetter
from textwrap import indent
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selectorlib import Extractor
from bs4 import BeautifulSoup 
import requests
import pandas as pd

import requests
import json
import time

app = Flask(__name__)
api = Api(app)

class url_scraper(Resource):
    def get(self, item):
        main_url = []
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.get("https://www.amazon.in/")
        search = driver.find_element(By.ID,"twotabsearchtextbox")
        search.send_keys(item)
        search_button = driver.find_element(By.ID, "nav-search-submit-button").click()
        
        main_url.append(driver.current_url)
        HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/90.0.4430.212 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

        name = []
        link = []
        stars = []
        reviews = []
        prices = []
        images =[]

        data_str =""

        time.sleep(10)
        page = requests.get(main_url[0], headers=HEADERS)
        soup = BeautifulSoup(page.text,'html.parser')
        print(page)

        product_names = soup.find_all('h2', class_='a-size-mini a-spacing-none a-color-base s-line-clamp-2')
        for i in product_names:
            data_str = i.get_text()
            name.append(data_str)
        nm = (len(name))
        


        link_tags = soup.find_all('a', class_= 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
        for j in link_tags:
            product_links = 'http://amazon.in'+(j.get('href'))
            link.append(product_links)
        urlss = (len(link))
        


        star_rating = soup.find_all('span', class_='a-icon-alt')
        for k in star_rating:
            rating = k.get_text().replace(' out of 5 stars','')
            stars.append(rating)
        rate = (len(stars))
        
        #for l in stars:
        #   if('4 Stars & Up'  or "3 Stars & Up" or '2 Stars & Up' or '1 Star & Up'):
        #      stars.remove(l)

        review_no = soup.find_all('span', class_='a-size-base s-underline-text')
        for m in review_no:
            no = m.get_text()
            reviews.append(no)
        rev = (len(reviews))
        


        price_tag = soup.find_all('span', class_='a-price-whole')
        for n in price_tag:
            price = n.get_text()
            prices.append(price)
        prc = len(prices)
        

        product_image = soup.find_all('img', class_="s-image")
        for o in product_image:
            img = o['src']
            images.append(img)
        imgs = len(images)
        

        num = [nm,urlss,rate,rev,prc,imgs]
        num.sort()
        n = num[0]
        array =[]
        for i in range(0,n):
            array.append({'Product Name':name[i], 'URL':link[i], 'Ratings':stars[i], 'Reviews':reviews[i], 'Price':prices[i], 'Image':images[i]}) 

        dict = sorted(array, key=itemgetter('Ratings'), reverse=True)
        newdict =sorted(dict, key=itemgetter('Reviews'), reverse=True)

        

        data = json.dumps(newdict)
        return data

'''class Rev_test(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        product_link = json_data['link']
        
        HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/90.0.4430.212 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
        htmldata = requests.get(product_link, headers=HEADERS)
        soup = BeautifulSoup(htmldata.text, 'html.parser')
        data_str = ""     
        cus_list = []
    
        for item in soup.find_all("span", class_="a-profile-name"):
            data_str = data_str + item.get_text()
            cus_list.append(data_str)
            data_str = ""
        
        data1_str = ""
  
        for item in soup.find_all("div", class_="a-expander-content reviewText review-text-content a-expander-partial-collapse-content"):
            data1_str = data1_str + item.get_text()
    
        result = data1_str.split("\n")

        rev_result = []
        for i in result:
            if i == "":
                pass
            else:
                rev_result.append(i)

        data = {"Name":cus_list, "Review":rev_result}
        dict = json.dumps(data) 
        return dict

api.add_resource(Rev_test, '/')'''



api.add_resource(url_scraper, '/<string:item>')

if __name__ == '__main__':
    app.run(debug=True)