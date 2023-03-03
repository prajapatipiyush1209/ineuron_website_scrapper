from flask import Flask,render_template,request
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import logging
import socket
import scrap

logging.basicConfig(filename="application.text", level = logging.INFO, format ='%(asctime)s - %(levelname)s-%(message)s {}'.format(socket.gethostbyname(socket.gethostname())))

app = Flask(__name__)


@app.route("/")
def home_page():
    
    try:
        #  creat the instance of the scrap package then call the method of the that class using the object 
        logging.info("Create the instance of the scrap package")
        object1 = scrap.course_name_data()
        logging.info("Successfully created the instance of the scrap package")
        return render_template("index.html", course_list=object1.course_name())
        logging.info("Successfully Execution of the homepage")
    
    except Exception as e :
        logging.error("Find the error in during the fetching the code : {}". format(e))
        return "Error is occured while execution of the code"

    

    
@app.route("/course_details", methods=['POST'])
def course_detail():
    try:
        logging.info("Create the instance of the scrap package")
        object2 = scrap.course_full_data()
        logging.info("Successfully created the instance of the scrap package")
        result =  object2.course_data()
        return render_template("results.html", course_title = result[0],course_description =result[1],course_curriculum = result[2], course_price = result[3], course_duration = result[4], course_requirements = result[5], course_language = result[6])
        
    except Exception as e :
        logging.error("Find the error in during the fetching the code : {}". format(e))
        return "Error is occured while execution of the code"

    
    

    



if __name__=="__main__":
    app.run(debug=True)