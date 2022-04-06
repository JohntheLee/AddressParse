# Author: Jeonghoon Lee
# Date: 2021/11/04
# CODG132 - Lab 1 - Ryerson University

def re_province(province):
    """Converts province abbreviations to their full names."""
    
    prov_abbrev = ["ON", "QC", "BC", "AB", "MB", "SK", "NB", "NL", "NS", "PE", "YT", "NT", "NU"]
    prov_name = ["Ontario", "Quebec", "British Columbia", "Alberta", "Manitoba", "Saskatchewan", "New Brunswick", "Newfoundland and Labrador", "Nova Scotia", "Prince Edward Island", "Yukon", "Northwest Territories", "Nunavut"]
    if province in prov_abbrev:
        province = prov_name[prov_abbrev.index(province)]
    return province
