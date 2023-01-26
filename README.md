# Scraper for Chicago Maps Archive

The purpose of this scraper is to reconfigure data made publicly available by the Chicago History Museum on [City of Chicago Maps](http://chsmedia.org/media/fa/fa/LIB/CityChicagoMapsAccessible.htm). This reconfigured data will be used to help process and digitize the maps for public use by [University of Chicago Library's Preservation Department](https://www.lib.uchicago.edu/about/directory/departments/pres/).

In order to streamline the use of this scraper, I used the python package [poetry](https://python-poetry.org/docs/) to create a virtual environment. This approach allows users to work more flexibility across machines, not needing to worry about installing all the appropriate packages needed to run this program.

**scraper.py** is the core module of this program, and is composed of three core functions:

* *page_to_dict()*: This function takes the URL and restructures the data into a dictionary of dictionaries, parsing by types of text.

* *parse_dimensions()*: This function takes a row_dict object created by page_to_dict() and parses the dimension values (width and height) that are saved within the scale key/value pair.

* *get restructured_data()*: This function takes no inputs, calls the two functions above using the [City of Chicago Maps](http://chsmedia.org/media/fa/fa/LIB/CityChicagoMapsAccessible.htm) URL. The core use of this function is to convert the maps dictionary into a dataframe, and then export the dataframe as an xlsx file. This is output is saved as "city_of_chicago_maps.xlsx" within the restructured_data folder.

### A note on the structure of the webpage:

The main content is all built into one table body, with each tr being a new "line" of the webpage content. The core reason why pulling this content is challenging is because each row of the table has multiple trs, so treating that as one text block (especially when the number of lines in each row changes) required additional construction.
