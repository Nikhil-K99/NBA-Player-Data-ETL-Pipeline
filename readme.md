# NBA Data ETL Pipeline

## Project Overview

The initial objective of this project was to retrieve data from the [NBA_API](https://github.com/swar/nba_api) for analysis. In the NBA community, it is often debated who is truly the greatest player of all time. Most would agree that Michael Jordan is the greatest, however, others argue that it is Kobe Bryant or LeBron James. My original goal was to retrieve the statistics from every game played by these players. However, being a huge NBA fan, I knew that I would most like want to analyze data of different players in the future. Constantly loading the data for many different players and interacting with the API is not conservative or time or memory. This being the case, I decided to create an ETL pipeline that extracts the data from the API, parses the data. and streams it into a postgreSQL database and a CSV file. This stores the the data into disk space so it will not consume too much memory. I can also query a specific subset of the data that only contains the data I need to analyze. When the program is run, it will ask the user which player's data he/she wants. After the user inputs the full name of the player, the pipeline will stream the desired data to the SQL database and also return a CSV file named after the player.

## The Pipeline

The structure of the structure is found in the [`pipeline.py`](https://github.com/Nikhil-K99/NBA-ETL-Pipeline/blob/master/pipeline.py) file. A Directed Acyclic Graph was implement to run the pipeline tasks in the proper and most efficient order. The alogrithm to create and use an efficient Directed Acyclic Graph is known as [Kahn's algorithm](https://www.geeksforgeeks.org/topological-sorting-indegree-based-solution/). The graph is the backbone of the Pipeline class as this class wraps the task functions and treats them as nodes on the graph. These nodes are sorted according to the algorithm and ran in the particular order when the program is ran. The tasks are written and are wrapped by the class in the [`ETL.py`](https://github.com/Nikhil-K99/NBA-ETL-Pipeline/blob/master/ETL.py) file. The player is first searched in the NBA API to retrieve the corresponding player ID. This is then used to retrieve the game log data of the player, which is transformed appropriately. This data is run through a function that streams it to the SQL database and also through a function that saves the data to a CSV file.

## Required Libraries

- collections


- pandas


- sqlalchemy


- psycopg2

