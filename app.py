# Importing Necessary Modules
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import logging
import pymongo
import csv

# Logging informations to scrapper.log
logging.basicConfig(filename="scrapper.log" , level=logging.INFO)

# Creating a flask object
app = Flask(__name__)

# Setting route to home page
@app.route("/", methods = ['GET'])
def homepage():
    return render_template("index.html")

# Setting route to review page
@app.route("/review" , methods = ['POST' , 'GET'])
def index():
    if request.method == 'POST':
        try:
            search_key = request.form['content'].replace(" ","")
            # Generating the link to the filpkart page for the specific search key
            flipkart_url = "https://www.flipkart.com/search?q=" + search_key
            uClient = uReq(flipkart_url)

            # Reading the webpage
            flipkartPage = uClient.read()
            uClient.close()
            flipkart_html = bs(flipkartPage, "html.parser")
            bigboxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"})

            # Deleting unecessory captures
            del bigboxes[0:3]
            box = bigboxes[0]

            # Getting product link
            productLink = "https://www.flipkart.com" + box.div.div.div.a['href']
            prodRes = requests.get(productLink)
            prodRes.encoding='utf-8'
            prod_html = bs(prodRes.text, "html.parser")
            print(prod_html)
            commentboxes = prod_html.find_all('div', {'class': "_16PBlm"})

            # Scrapping name, rating, review and comments
            reviews = []
            for commentbox in commentboxes:
                # Name
                try:
                    name = commentbox.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text
                except:
                    logging.info("name")

                # Rating
                try:
                    rating = commentbox.div.div.div.div.text
                except:
                    rating = 'No Rating'
                    logging.info("rating")

                # Review
                try:
                    commentHead = commentbox.div.div.div.p.text
                except:
                    commentHead = 'No Comment Heading'
                    logging.info(commentHead)

                # Comment
                try:
                    comtag = commentbox.div.div.find_all('div', {'class': ''})
                    custComment = comtag[0].div.text
                except Exception as e:
                    logging.info(e)
                
                # Creating a dictionary with captured details
                mydict = {"Product": search_key, "Name": name, "Rating": rating, "CommentHead": commentHead,
                          "Comment": custComment}

                # Storing the dictionary into the list
                reviews.append(mydict)
            logging.info("log my final result {}".format(reviews))

            # Storing all the data in the MongoDB
            # Connecting to the mongo
            # Please add your cluster link
            # client = pymongo.MongoClient(
                # "mongodb+srv://user1:<password>@cluster0.zs8zanp.mongodb.net/?retryWrites=true&w=majority")

            # Creating a databse named review_scrapped_data
            db = client["review_scrapped_data"]

            # Creating respective collection for each search_key
            collection = db[search_key]

            # Inserting all the data at once using insert_many function
            collection.insert_many(reviews)

            # Storing the same data in respective csv file
            filename = search_key + ".csv"
            with open(filename, 'w', newline='', encoding='UTF-8') as fw:
                headers = reviews[0].keys()
                dict_writer = csv.DictWriter(fw, headers)
                dict_writer.writeheader()
                dict_writer.writerows(reviews)

            # Returning the result template
            return render_template('result.html', reviews=reviews[0:(len(reviews)-1)])

        except Exception as e:
            logging.info(e)
            return 'something is wrong'

    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(host="0.0.0.0")
