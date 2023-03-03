# ineuro_website_scraper


# 1.Go to the Ineuron website:
To start with, we will use the requests library to make a request to the Ineuron website and retrieve the HTML content.

# 2.Scrap list of all the listed course name:
We can use BeautifulSoup to parse the HTML content and extract the required data. In this case, we want to get the names of all the listed courses.

# 3.Go to a specific course one by one and then try to scrap all the curriculum and its respective details:
Once we have the list of course names, we can loop through each course and scrape its curriculum and details. We can also store this information in a dictionary for later use.

# 4.Store all the course-related information in MongoDB:
We can use the pymongo library to interact with the MongoDB database and store the course-related information.

# 5.Store all the course name data and its description in MYSQL:
The MySQL connector for Python to connect to a MySQL database and store the course name data.
 
# 6.Logging is mandatory:
We can use the logging library to log information about the application's execution.

# 7.Exception handling is necessary:
We can use try-except blocks to handle exceptions that may occur during the application's execution.

# 8.Modular coding is necessary:
We can break down the application into smaller modules or functions to make the code more readable and maintainable.

# 9.Class and object are must:
We can define classes and objects to encapsulate related data and behavior.
