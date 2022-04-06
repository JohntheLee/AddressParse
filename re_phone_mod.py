# Author: Jeonghoon Lee
# Date: 2021/11/03
# CODG132 - Lab 1 - Ryerson University

def re_phone(phone):
    """Inputs a standard 10 digit phone number: xxx-xxx-xxxx.
    Outputs a 10 digit phone number with brackets around the area code: (xxx)xxx-xxxx.
    """
    
    phone_temp = phone.replace("-", "")
    return phone_temp[:0] + "(" + phone_temp[0:3] + ")" + phone_temp[3:6] + "-" + phone_temp[6:]
