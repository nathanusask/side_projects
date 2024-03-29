

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
search_term_var_total_capital = 'var totalcapital'
search_term_var_curr_capital = 'var currcapital'
ten_thousand = 1e4
semicolon = ';'

const_if_model_satisfied = 'if_data_satisfies_model'
const_ch_share_hold_percentage = '持仓比'
const_share_hold_percentage = 'share_hold_percentage'
const_ch_total_buy_in = '累计买入'
const_total_buy_in = 'total_buy_in'
const_ch_stock_code = '股票代码'
const_ch_stock_name = '股票名称'

const_threshold_share_hold_percentage = 0.02
const_threshold_buy_in = 0.005

const_time_frames = [20, 5, 1]
