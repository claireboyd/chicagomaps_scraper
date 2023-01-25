import lxml.html
import requests
import pandas as pd

# helper function to get the root HTML object
def get_root(url):
    '''
    Returns root element given a URL.
    Inputs: None
    Returns: root (lxml.html.HtmlElement)
    '''
    req = requests.get(url)
    html = req.text
    root = lxml.html.fromstring(html)

    return root

# core function
def scrape_page(root):
    """
    This function takes a URL of the City of Chicago Maps and re-standardizes
    the data into a workable format.

    Inputs: URL
    Returns: CSV file with parsed data
    """
    # initialize maps dict and row number
    maps = {}
    row_number = 0

    # all trs are under this. #slicing after row 18 because the first 18 rows are header text for the page
    all_rows = root.cssselect('body table')[0][18:]
    

    for i, row in enumerate(all_rows):
        #unpack all tds in row
        row_tds = row.getchildren()

        # if there are 6 tds, it means that it is a full row of data. save content accordingly
        if len(row_tds) == 6:

            # increment row number when we hit a new full row of data
            row_number += 1

            # create key with row_number and value with a dictionary for that row, starting with No.
            maps[str(row_number)] = {"No.": row_tds[0].text_content()}

            # add all columns to that row dictionary
            maps[str(row_number)]["Title"] = row_tds[1].text_content()
            maps[str(row_number)]["Author"] = row_tds[2].text_content()
            maps[str(row_number)]["Size"] = row_tds[3].text_content()
            maps[str(row_number)]["Scale"] = ""
            maps[str(row_number)]["Description"] = ""
            maps[str(row_number)]["Provenance"] = ""
            maps[str(row_number)]["Year"] = row_tds[4].text_content()
            maps[str(row_number)]["Category"] = row_tds[5].text_content()

        elif len(row_tds) == 1:
            text = row_tds[0].text_content().strip().replace("\n", "")

            if "Gift" in text:
                maps[str(row_number)]["Provenance"] = text
            elif "Scale" in text:
                maps[str(row_number)]["Scale"] = text
            elif "\"x" in text:
                maps[str(row_number)]["Size"] += text
            else:
                maps[str(row_number)]["Description"] += text + " "

    # string parsing for size columns
    for row_dict in maps.values():
        



    return maps

def get_csv(root):
    """
    """
    #root = get_root("http://chsmedia.org/media/fa/fa/LIB/CityChicagoMapsAccessible_files/sheet001.htm")
    maps_dict = scrape_page(root)

    #convert to dataframe
    maps_df = pd.DataFrame.from_dict(maps_dict, orient='index')

    #return maps_df

    # save to csv in filepath folder
    maps_df.to_excel("output/city_of_chicago_maps.xlsx",
                     sheet_name='City of Chicago Maps')
