

s_url = 'http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get' # the url where to get data should be constant
s_token = '70f12f2f4f091e459a279469fe49eca5' # token is a constant
s_type = 'HSGTHDSTA' # stock type is a constant
stock_codes_url = 'https://www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=sh'

fields = [
    'SNAME',
    'SCODE',
    'HKCODE',
    'HDDATE',
    'SHARESRATE',
    'SHAREHOLDPRICE',
    'SHAREHOLDSUM',
    'CLOSEPRICE'
]

company_info_url_prefix = 'https://finance.sina.com.cn/realstock/company/sh'
company_info_url_suffix = '/nc.shtml'
split_term = ' = '
search_term_var_totalcapital = 'var totalcapital'
search_term_var_currcapital = 'var currcapital'
ten_thousand = 1e4
semicolon = ';'