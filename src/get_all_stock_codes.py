from bs4 import BeautifulSoup as bs
from requests import request as req

def get_all_stock_codes(url):
    page_text = req.get(url).text
    soup = bs(page_text, 'html.parser')
    raw_codes = soup.findAll("div", {"class": "mobile-list-body"})
    codes = []
    for raw_code in raw_codes:
        code = raw_code.get_text()
        if code.isnumeric():
            code = '60' + code[1:]  # transform HK codes to SH codes
            if len(code) == 6:  # double check if the code is correct
                codes.append(code)
    return codes
