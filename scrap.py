from flask import Flask,render_template,request
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import logging
import socket
import json
import pymongo
import pymysql


logging.basicConfig(filename="scraping.log", level = logging.INFO, format ='%(asctime)s - %(levelname)s-%(message)s {}'.format(socket.gethostbyname(socket.gethostname())))


class course_name_data():
    def course_name(self):
        try :
            url = uReq("https://ineuron.ai")
            ineuron_html=url.read()
            logging.info("Successfully read the data from the web page ")
            ineuron_html = bs(ineuron_html, "html.parser")
            course_name = json.loads(ineuron_html.find("script", {"id":"__NEXT_DATA__"}).get_text())
            logging.info("Get the data in the json format")
            all_course_name =list(course_name['props']['pageProps']['initialState']['init']['courses'].keys())
            #The json. load() is used to read the JSON document from file and The json. loads() is used to convert the JSON String document into the Python dictionary.
            logging.info("Success send the all_course_name to the application.py")
            databases.my_sql_datbase(all_course_name)
            return all_course_name
           
        except Exception as e:
            logging.error("Find the error in during the fetching the code : {}". format(e))
            return "Error is occured while execution of the code"

class databases:
    def store_data(course_title, course_description, course_curriculum_details, course_price, course_duration, course_requirements, course_lan):
        client = pymongo.MongoClient("mongodb+srv://<user_name:<password>@cluster0.nnnyytu.mongodb.net/?retryWrites=true&w=majority")
        database = client['scrap_data']
        collection = database['course_data']
        data = {
            "course_title" : course_title,
            "course_description": course_description,
            "course_curriculam": course_curriculum_details,
            "course_price": course_price,
            "course_duration": course_duration,
            "course_requirement": course_requirements,
            "course_lan": course_lan
        }
        count = collection.find({'course_title' : course_title})
        if len(list(count)) >= 1:
            logging.info("Data Is already in database")
            pass
        else :
            collection.insert_one(data)
            logging.info("Now data is added in the MongoDB database")

    def my_sql_datbase(course_title):
        
        conn = pymysql.connect(host='localhost', user='root', password='Dasnadas@0847#')
        my_cursor = conn.cursor()
        my_cursor.execute("USE ineuron_course_data")
        if my_cursor.execute('select count(course_name) from data') >= 1:
            logging.info("Data already haved in the sqldatabase")
            pass
        else :
            query = "INSERT INTO data (course_name) VALUES (%s)"
            my_cursor.executemany(query, course_title)
        conn.commit()
        my_cursor.close()
        conn.close()

class course_full_data(databases) :
    def course_data(self):
        try :
            url = "https://ineuron.ai/course/"
            course_name=request.form['course']
            course_link = uReq(url + course_name.replace(" ","-"))
            ineuron_html=course_link.read()
            ineuron_course_page = bs(ineuron_html, "html.parser")
            course_name = json.loads(ineuron_course_page.find("script", {"id":"__NEXT_DATA__"}).get_text())
            try :
                all_course_data = course_name['props']['pageProps']['data']
            except:
                all_course_data = "No Data"

            try :
                course_title = course_name['props']['pageProps']['data']['title']
            except:
                course_title = "No Title"

            try :    
                course_description  = course_name['props']['pageProps']['data']['details']['description']
            except :
                course_description  = "No Description"
            
            try :
                course_curriculum = course_name['props']['pageProps']['data']['meta']['curriculum']
            except :
                course_curriculum = "No Curriculum"

            course_curriculum_details =[]
            for key, value in course_curriculum.items():
                course_curriculum_details.append(value['title'])
                course = value['items']
                for item in course:
                    course_curriculum_details.append(item["title"])

            try :
                course_price =course_name['props']['pageProps']['data']['details']['pricing']['IN']
            except :
                course_price = "No Course Price"
                
            try :    
                course_duration =course_name['props']['pageProps']['data']['meta']['duration']
            except :
                course_duration = "No Course Duration"
            
            try :
                course_requirements = course_name['props']['pageProps']['data']['meta']['overview']['requirements']
            except :
                course_requirements = "No Requirements"
            
                
            try :    
                course_lan = course_name['props']['pageProps']['data']['meta']['overview']['language']
            except :
                course_lan = "No Language"
            databases.store_data(course_title, course_description , course_curriculum_details, course_price, course_duration, course_requirements, course_lan)
            return course_title, course_description , course_curriculum_details, course_price, course_duration, course_requirements, course_lan
            

        except Exception as e :
            logging.error("Find the error in during the fetching the code : {}". format(e))
            return "Error is occured while execution of the code"
        
