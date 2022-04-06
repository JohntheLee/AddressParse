# Author: Jeonghoon Lee
# Date: 2021/11/03
# Business in query = McDonalds

import urllib.request
import win32com.client
import re_phone_mod # My own module that changes Yellow Page's phone number format to a custom format.
import re_province_mod # My own module that converts province abbreviations to their full names.

def parse (searchstring, leader, trailer):
    """Parses a source page for geospatial information between leading and trailing strings.
    Returns a custom error message if the parse produces a ValueError.
    This custom error message differs depending on the geospatial information being parsed.
    """
    
    try:
        end_leader = searchstring.index(leader) + len(leader)
        start_trailer = searchstring.index(trailer, end_leader)
        return searchstring[end_leader:start_trailer]
    except ValueError:
        if "addressLocality" in leader:
            return "No city available"
        if "addressRegion" in leader:
            return "No province available"
        if "postalCode" in leader:
            return "No postal code available"
        if "data-phone" in leader:
            return "No phone number available"
        else:
            return ""

def returnpages(s):
    """Returns the number of pages."""
    
    try:
        returnpages = parse(s, 'yp_searchTotalPages" : "', '",')
        return int(returnpages)
    except:
        return 0

# Download the McDonald's restaurant entries.
page = 1
mcd_file = urllib.request.urlopen("https://www.yellowpages.ca/search/si/1/McDonalds/Canada")
s = mcd_file.read()

# Geospatial information values (city, province, postal, phone) will be linked to a key (the address) in this dictionary as a tuple.
# A dictionary will prevent duplicate address entries.
mcd_dict = {}

pages = returnpages(s.decode())

# A for loop that iterates through all of the search pages found in the querystring and splits the address information.
for page in range(1, pages):
    mcd_file = urllib.request.urlopen("https://www.yellowpages.ca/search/si/" + str(page) + "/McDonalds/Canada")
    s = mcd_file.read()
    add_split = s.decode().split('<div class="listing__address address mainLocal noNum">')

    # A for loop that iterates through the sets of leading and trailing strings and parses the information between them.
    for item in add_split:
        address = parse(item, '<span class="jsMapBubbleAddress"  itemprop="streetAddress" >', '</span>')
        city = parse(item, '<span class="jsMapBubbleAddress"  itemprop="addressLocality" >', '</span>')
        province = re_province_mod.re_province(parse(item, '<span class="jsMapBubbleAddress"  itemprop="addressRegion" >', '</span>'))
        postal = parse(item, '<span class="jsMapBubbleAddress"  itemprop="postalCode" >', '</span>')
        phone = parse(item, 'data-phone="', '">')

        # If the address exists, then the address will serve as the newest key entry into the dictionary, with the other geospatial information serving as values.
        if len(address) > 0:
            mcd_dict[address] = city, province, postal, phone

    mcd_file = urllib.request.urlopen("https://www.yellowpages.ca/search/si/" + str(page) + "/McDonalds/Canada")
    s = mcd_file.read()

row = 2

# A new excel workbook is created with appropriate headers.
mcd_excel = win32com.client.Dispatch("Excel.Application")
mcd_excel.Visible = 1
mcd_excel.Workbooks.Add()
sh = mcd_excel.ActiveSheet
sh.Cells(1,1).Value = "Address"
sh.Cells(1,2).Value = "City"
sh.Cells(1,3).Value = "Province"
sh.Cells(1,4).Value = "Postal Code"
sh.Cells(1,5).Value = "Phone Number"

# The header row is bolded.
for i in range(1,6):
    sh.Cells(1,i).Font.Bold = True

# A for loop that populates each new row with a unique geospatial entry.
# The first column is reserved for the key ([0] in the dictionary entry).
# The other four columns are reserved for the value ([1] in the dictionary entry as tuple - second index is used to return specific elements within the tuple).
for business in mcd_dict.items():
    sh.Cells(row,1).Value = business[0]
    sh.Cells(row,2).Value = business[1][0]
    sh.Cells(row,3).Value = business[1][1]

    # Existing postal codes will be reformatted. Nonexisting postal codes will retain their custom error message.
    if len(business[1][2]) < 10:
        sh.Cells(row,4).Value = business[1][2].replace(" ", "")
    else:
        sh.Cells(row,4).Value = business[1][2]

    # Existing phone numbers will be reformatted. Nonexisting phone numbers will retain their custom error message.
    if len(business[1][3]) < 15:
        sh.Cells(row,5).Value = re_phone_mod.re_phone(business[1][3])
    else:
        sh.Cells(row,5).Value = business[1][3]
    
    row += 1

# The number of unique address entries (keys in the dictionary) will be printed.
print(str(len(mcd_dict.keys())) + " rows written to excel.")
