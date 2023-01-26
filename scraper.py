# packages for reading in the html
import lxml.html
import requests

# packages for string manipulation and converting into a dataframe
import regex as re
import pandas as pd

def page_to_dict(url):
    """
    This function takes the URL and restructures the data into a 
    dictionary of dictionaries, parsing by types of text.

    Inputs: URL
    Returns: maps (dict of dicts), with the key as a row number and 
    the value as another dictionary with all cleaned row data.
    """
    # get root HTML object or webpage
    html = requests.get(url).text
    root = lxml.html.fromstring(html)
    
    # initialize a dictionary and set row number (or future dictionary key) to 0
    maps = {}
    row_number = 0

    # collect all table rows (trs) on the webpage, slicing after row 18 where the content of the table begins
    all_rows = root.cssselect('body table')[0][18:]

    # iterate through each row of data to see where/how to save the data to each row's dictionary
    for row in all_rows:
        #unpack all table data points (tds) in the row
        row_tds = row.getchildren()

        # if there are 6 tds in the row, it means that it is a full row of data. save content accordingly.
        if len(row_tds) == 6:
            # increment row number when we hit a new full row of data
            row_number += 1

            # add key/value pair in dictionary, with row_number (integer): {No.: [value]} (dictionary)
            maps[row_number] = {"No.": row_tds[0].text_content()}

            # add the rest of the tds as content to dictionary, with relevant keys
            maps[row_number]["Title"] = row_tds[1].text_content()
            maps[row_number]["Author"] = row_tds[2].text_content()
            maps[row_number]["Size"] = row_tds[3].text_content()
            maps[row_number]["Width (in)"] = ""        #placeholder to add to in parse_strings()
            maps[row_number]["Height (in)"] = ""       #placeholder to add to in parse_strings()
            maps[row_number]["Scale"] = ""             #placeholder to add to in parse_strings()
            maps[row_number]["Description"] = ""       #placeholder to add to in parse_strings()
            maps[row_number]["Provenance"] = ""        #placeholder to add to in parse_strings()
            maps[row_number]["Year"] = row_tds[4].text_content()
            maps[row_number]["Category"] = row_tds[5].text_content()

        # if only one td, then it is a new line of the "contents" column
        elif len(row_tds) == 1:
            
            # extract text from td object, collapsing into one line (without line breaks)
            text = row_tds[0].text_content().strip().replace("\n", "")

            # sort text into the right dict key by text
            if " Scale" in text:
                text, scale = text.split(" Scale")
                maps[row_number]["Description"] += text + " "
                maps[row_number]["Scale"] = "Scale" + scale
            elif "Gift" in text:
                maps[row_number]["Provenance"] = text
            elif "Scale" in text:
                maps[row_number]["Scale"] = text
            elif "\"x" in text:
                maps[row_number]["Size"] += " " + text
            else:
                maps[row_number]["Description"] += text + " "

    # string parsing for additional size columns (width, height)
    for row_dict in maps.values():

        #use parse strings function on each row in maps
        parse_dimensions(row_dict)

    # returns full, restructured dictionary
    return maps


def parse_dimensions(row_dict):
    """
    Takes a row_dict object created by page_to_dict() and parses the dimension values
    (width and height) that are saved within the scale key/value pair.

    Inputs: row_dict (dict)
    Returns: None (changes dict in place)
    """
    row_dict["Size"] = row_dict["Size"].replace(":", ": ")
    row_dict["Size"] = row_dict["Size"].replace("\" x", "\"x")
    row_dict["Size"] = row_dict["Size"].replace("\"x ", "\"x")

    #edge case - if no x in dimensions, so adding an x in when relevant
    strs_to_replace = []
    for integer in range(0, 10):
        string = "\"" + str(integer)
        replacement = "\"x" + str(integer)
        strs_to_replace.append((string,replacement))
    
    for string, replacement in strs_to_replace:
        row_dict["Size"] = row_dict["Size"].replace(string, replacement)

    # separate all words in key "Size"
    for word in row_dict["Size"].split():

        #look at first string that contains "x 
        if ("\"x" or "\" x " or "\" x") in word:
            dimensions = word.replace("\"", "").replace("x", " ").replace(",", "").split()
            
            row_dict["Width (in)"] = float(dimensions[0])
            row_dict["Height (in)"] = float(dimensions[1])
            break
    
    # clean Description to replace two spaces with one.
    row_dict["Description"] = row_dict["Description"].replace("  ", " ")


def get_restructured_data():
    """
    """
    maps_dict = page_to_dict("http://chsmedia.org/media/fa/fa/LIB/CityChicagoMapsAccessible_files/sheet001.htm")

    #convert dictionary to dataframe for analysis
    maps_df = pd.DataFrame.from_dict(maps_dict, orient='index')

    # save to csv in restructured_data folder as an excel file
    maps_df.to_excel("restructured_data/city_of_chicago_maps.xlsx",
                     sheet_name='City of Chicago Maps')
