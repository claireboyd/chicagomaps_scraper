import lxml.html
import requests

# helper function to streamline two lines of code used a few times
def get_root(url):
    '''
    Returns root element given a URL.
    Inputs: None
    Returns: root (lxml.html.HtmlElement)
    '''
    req = requests.get(url)
    # print(req.text)
    html = req.text
    root = lxml.html.fromstring(html)

    return root

root = get_root("http://chsmedia.org/media/fa/fa/LIB/CityChicagoMapsAccessible_files/sheet001.htm")

def scrape_page(root):
    """
    This function takes a URL of the City of Chicago Maps and re-standardizes
    the data into a workable format

    Inputs: URL
    Returns: CSV file with parsed data
    """
    #url = "http://chsmedia.org/media/fa/fa/LIB/CityChicagoMapsAccessible_files/sheet001.htm"
    #root = get_root(url)

    maps = {}

    # all trs are under this
    all_rows = root.cssselect('body table')[0][11:]
    #print(len(all_rows))

    for i, row in enumerate(all_rows):
        row_number = i
        row_tds = row.getchildren()

        if "mso-yfti-irow" in row.get("style"):
            
            #assignment based on order
            map_dict = {}
            maps[str(row_number)] = {"No.": row_tds[0].text_content()}

            # for element in row_tds:
            #     maps["No."] = element.text_content() 
            # # row_idx = i
            # # print(row.cssselect('td')[0])
            # break

            # print(row.cssselect('td')[0])
            # maps["No."].get(row.cssselect('tr')[0], None)
        else:
            maps[str(row_number)]["Title"] = row_tds[1].text_content()


    return maps

    # column_titles = all_rows[0]

    # for col in column_titles:
    #     print(col.text_content())

    # for tr in all_rows[0:5]:
    #     if 
    #     print(tr.style.text_content())





    # for row in all_rows:
    #     print(row.text_content())

    # return all_rows


    # park_dict["address"] = root.cssselect('p.address')[0].text_content().strip()
    # park_dict["url"] = url

    # # getting root of block text to loop through view-content sections
    # block_text = root.cssselect('div.section')[0].cssselect('div.view-content')

    # for block in block_text:
    #     # read description to dict
    #     if block.cssselect('h3.block-title')[0].text_content().strip() == "Description":
    #         park_dict["description"] = block.cssselect('div.block-text')[0].text_content()

    #     # read history to dict
    #     if block.cssselect('h3.block-title')[0].text_content().strip() == "History":
    #         park_dict["history"] = block.cssselect('div.block-text')[0].text_content()

    # #create key/value pair of history: "" if no history block on webpage
    # park_dict["history"] = park_dict.get("history", "")

    # return park_dict

