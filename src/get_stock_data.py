import requests as req

s_code = '600004'
s_url = 'http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get' # the url where to get data should be constant
s_token = '70f12f2f4f091e459a279469fe49eca5' # token is a constant
s_type = 'HSGTHDSTA' # stock type is a constant

def get_stock_data(s_url, url, token, code):
	s_filter = '(SCODE=\'' + s_code + '\')' # s_code shoud be obtained from outside
	params = {'type':type, 'token': token, 'filter': filter}
	resp = req.get(url, params)
	return resp.json()


