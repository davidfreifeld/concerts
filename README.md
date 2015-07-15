# concerts
Performs a data analysis on concert ticketing data 

### Current Functionality
1. Saves concert ticketing data from the internet as html pages
2. Compiles the html pages into a csv file
3. Loads the data into R and cleans it (planning on changing this implementation to Python)

### Planned Functionality
1. Loads additional data about artists from the dataset (spotify plays, last.fm scrobbles, etc. Using an api)
2. Performs exploratory analysis on the compiled set of data, plots graphs, etc.
3. Builds a model to predict something (how much money a band can make at a particular time and location?)
4. Saves the analysis as an IPython Notebook
5. Build a web app where a user can enter a band (and time, location?) and get the model output.

### Files
- ca_page_saver.py - Uses a webdriver to log in to the data source's website, and save each html page from a db query
- ca_scaper.py - Parses the html pages and compiles all of the records into a csv file
- data/BoxOfficeData.csv - The compiled concert data
- boxOfficeAnalysis.R - First crack at loading the data for analysis. Done in R, but planning to switch to Python
