from bs4 import BeautifulSoup as bs
from requests import request as req
import src.constants as constants


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


def get_stock_data(s_type, url, token, code):
    s_filter = '(SCODE=\'' + code + '\')'  # s_code shoud be obtained from outside
    params = {'type': s_type, 'token': token, 'filter': s_filter}
    resp = req.get(url, params)
    return resp.json()


def get_company_info(s_code):
    company_info_url = constants.company_info_url_prefix + s_code + constants.company_info_url_suffix
    page_text = req.get(company_info_url).text
    soup = bs(page_text, 'html.parser')
    scripts = soup.findAll("script")
    the_script = ''
    for script in scripts:
        tmp_text = script.text
        if tmp_text.find(constants.search_term_var_totalcapital) >= 0:
            the_script = tmp_text
            break
    texts = the_script.split('\n')
    total_capital, curr_capital = 0.0, 0.0
    for text in texts:
        if total_capital > 0.0 and curr_capital > 0.0:
            break
        if text.find(constants.search_term_var_totalcapital) >= 0:
            i_semicolon = text.find(constants.semicolon)
            total_capital = float(text[:i_semicolon].split(constants.split_term)[1]) * constants.ten_thousand
        elif text.find(constants.search_term_var_currcapital) >= 0:
            i_semicolon = text.find(constants.semicolon)
            curr_capital = float(text[:i_semicolon].split(constants.split_term)[1]) * constants.ten_thousand
    return [total_capital, curr_capital]
