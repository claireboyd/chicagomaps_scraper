# Scraper for Chicago Maps Archive

The purpose of this scraper is to reconfigure data made publicly available by the Chicago History Museum on [City of Chicago Maps](http://chsmedia.org/media/fa/fa/LIB/CityChicagoMapsAccessible.htm). This reconfigured data will be used to help process and digitize the maps for public use.




In order to streamline the use of this scraper, I used the python package [poetry](https://python-poetry.org/docs/) to create a virtual environment. This package allows users to 

This repository has the following components:

* **scraper.py**: 

* **scraper.py**: 



## A note on the structure of the webpage:

The main content is all built into one table body, with each tr being a new "line" of the webpage content. The core reason why pulling this content is challenging is because each row of the table has multiple trs, so treating that as one text block (especially when the number of lines in each row changes) required additional construction.
