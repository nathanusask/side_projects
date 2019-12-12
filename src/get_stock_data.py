import requests as req

def get_stock_data(s_type, url, token, code):
    s_filter = '(SCODE=\'' + code + '\')'  # s_code shoud be obtained from outside
    params = {'type': s_type, 'token': token, 'filter': s_filter}
    resp = req.get(url, params)
    return resp.json()
