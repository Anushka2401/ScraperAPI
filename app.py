from flask import Flask, request
from flask_restful import Api, Resource
from bs4 import BeautifulSoup
import json
import requests

app = Flask(__name__)
api = Api(app)

class Rev_test(Resource):
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

api.add_resource(Rev_test, '/')
if __name__ == '__main__':
    app.run(debug=True)