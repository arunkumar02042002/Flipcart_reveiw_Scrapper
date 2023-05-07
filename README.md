# Flipkart Review Scraper
This project is a web scraper that extracts product reviews from Flipkart, an Indian e-commerce website, using Python and Flask web framework. The extracted data includes the product name, rating, review title, and review comments.

The project is designed as a web application that takes user input as a search key and returns the reviews for the corresponding product. It uses Flask routes to handle requests from the user and Beautiful Soup library to extract data from the Flipkart website. The extracted data is then stored in a MongoDB database and a CSV file.

# Getting Started
To run this project locally, you need to have Python installed on your system. You can follow these steps:

1. Clone this repository on your local machine
2. Install the required Python modules using the following command: pip install -r requirements.txt
3. Run the Flask application using the following command: python app.py
4. Open your browser and go to http://localhost:5000 to access the application.

# How to use
To use this application, follow these steps:

1. First add your cluster link
2. Enter the search key for the product you want to extract reviews for.
3. Click on the "Search" button.
4. The application will extract the reviews for the corresponding product and display them on the results page.

# Technologies Used
This project uses the following technologies:
- Python
- Flask
- Beautiful Soup
- MongoDB
- CSV

# Acknowledgements
This project was inspired by web scraping tutorials of PW Skills team. Special thanks to Flask and Beautiful Soup developers for creating such great tools!
