# BLOC 1 : DATA MANAGEMENT / WEB SCRAPING

### KAYAK

[VIDEO LINK](https://share.vidyard.com/watch/82j4PsLXuh8J5hin2dqBrh?)

Join us in contributing to the creation of an application designed to offer personalized holiday destination recommendations, backed by real-time data on weather conditions and available hotels in specific regions. The goal of this project is to enable the application to suggest the finest travel destinations and accommodations based on these variables at any given moment.

Data for this project is derived from a curated list of 35 "best" cities for travel in France:

["Mont Saint Michel","St Malo","Bayeux","Le Havre","Rouen","Paris","Amiens","Lille","Strasbourg","Chateau du Haut Koenigsbourg","Colmar","Eguisheim","Besancon","Dijon","Annecy","Grenoble","Lyon","Gorges du Verdon","Bormes les Mimosas","Cassis","Marseille","Aix en Provence","Avignon","Uzes","Nimes","Aigues Mortes","Saintes Maries de la mer","Collioure","Carcassonne","Ariege","Toulouse","Montauban","Biarritz","Bayonne","La Rochelle"]

For the purpose of this project, we will exclusively utilize the cities listed above.

Project Steps:

Scrape location coordinates for each destination.
Obtain real-time weather data for each destination.
Gather comprehensive information on available hotels for each destination.
Aggregate all the gathered information into a data lake.
Perform ETL (Extract, Transform, Load) operations to transfer clean data from the data lake into a data warehouse.

Libraries Utilized: Scrapy, Requests, Boto3, SQL Alchemy, Plotly, Pandas