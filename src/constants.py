

s_url = 'http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get' # the url where to get data should be constant
s_token = '70f12f2f4f091e459a279469fe49eca5' # token is a constant
s_type = 'HSGTHDSTA' # stock type is a constant
stock_codes_url = 'https://www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=sh'

const_s_code = 'code'
const_s_total_capital = 'total_capital'
const_s_curr_capital = 'total_curr_capital'

filename_code_company_info_records = 'code_company_info_records.txt'

STOCK_NAME = 'SNAME'
STOCK_CODE = 'SCODE'
HK_CODE = 'HKCODE'
HD_DATE = 'HDDATE'
SHARES_RATE = 'SHARESRATE'
SHARE_HOLD_PRICE = 'SHAREHOLDPRICE'
SHARE_HOLD_SUM = 'SHAREHOLDSUM'
CLOSE_PRICE = 'CLOSEPRICE'

fields = [
    STOCK_NAME,
    STOCK_CODE,
    HK_CODE,
    HD_DATE,
    SHARES_RATE,
    SHARE_HOLD_PRICE,
    SHARE_HOLD_SUM,
    CLOSE_PRICE
]

company_info_url_prefix = 'https://finance.sina.com.cn/realstock/company/sh'
company_info_url_suffix = '/nc.shtml'
split_term = ' = '
search_term_var_totalcapital = 'var totalcapital'
search_term_var_currcapital = 'var currcapital'
ten_thousand = 1e4
semicolon = ';'