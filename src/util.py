from bs4 import BeautifulSoup as bs
import requests as req
import src.constants as constants
from operator import itemgetter
import os
import datetime
from pandas import DataFrame, ExcelWriter


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
    try:
        resp = req.get(url, params)
    except:
        return []
    try:
        return resp.json()
    except:
        return []


def get_company_info(s_code):
    company_info_url = constants.company_info_url_prefix + s_code + constants.company_info_url_suffix
    page_text = req.get(company_info_url).text
    soup = bs(page_text, 'html.parser')
    scripts = soup.findAll("script")
    the_script = ''
    for script in scripts:
        tmp_text = script.text
        if tmp_text.find(constants.search_term_var_total_capital) >= 0:
            the_script = tmp_text
            break
    texts = the_script.split('\n')
    total_capital, curr_capital = 0.0, 0.0
    for text in texts:
        if total_capital > 0.0 and curr_capital > 0.0:
            break
        if text.find(constants.search_term_var_total_capital) >= 0:
            i_semicolon = text.find(constants.semicolon)
            total_capital = float(text[:i_semicolon].split(constants.split_term)[1]) * constants.ten_thousand
        elif text.find(constants.search_term_var_curr_capital) >= 0:
            i_semicolon = text.find(constants.semicolon)
            curr_capital = float(text[:i_semicolon].split(constants.split_term)[1]) * constants.ten_thousand
    return [total_capital, curr_capital]


def write_code_and_company_info():
    all_codes = get_all_stock_codes(constants.stock_codes_url)
    records = []
    file_code_and_company_info = open(constants.filename_code_company_info_records, 'w')
    for code in all_codes:
        record = {}
        company_info = get_company_info(code)
        record[constants.const_s_code] = code
        record[constants.const_s_total_capital] = company_info[0]
        record[constants.const_s_curr_capital] = company_info[1]
        records.append(record)
        file_code_and_company_info.write(record[constants.const_s_code] + '\t'
                                         + str(record[constants.const_s_total_capital]) + '\t'
                                         + str(record[constants.const_s_curr_capital]) + '\n')
    file_code_and_company_info.close()
    return records


def read_code_and_company_info():
    file_code_and_company_info = open(constants.filename_code_company_info_records, 'r')
    records = []
    for line in file_code_and_company_info:
        record = {}
        entries = line.rstrip('\n').split('\t')
        record[constants.const_s_code] = entries[0]
        record[constants.const_s_total_capital] = float(entries[1])
        record[constants.const_s_curr_capital] = float(entries[2])
        records.append(record)
    file_code_and_company_info.close()
    return records


def get_stock_data_for_past_twenty_days_of_one_company(code):
    data = get_stock_data(constants.s_type, constants.s_url, constants.s_token, code)
    if len(data) == 0:
        return []
    refined_data = []
    for item in data:
        refined_item = {}
        for field in constants.fields:
            refined_item[field] = item[field]
        refined_data.append(refined_item)
    return sorted(refined_data, key=itemgetter(constants.HD_DATE))


def if_data_satisfies_model(data, record,
                            threshold_share_hold_percentage=constants.const_threshold_share_hold_percentage,
                            threshold_buy_in=constants.const_threshold_buy_in,
                            timeframe=20):
    resp = {}
    false_resp = {constants.const_if_model_satisfied: False}
    if len(data) < timeframe:
        return false_resp
    if record[constants.const_s_curr_capital] > 0:
        index = timeframe if timeframe < len(data) else timeframe - 1
        share_hold_sum_today = float(data[0][constants.SHARE_HOLD_SUM])
        share_hold_sum_range = float(data[index][constants.SHARE_HOLD_SUM]) if index > 0 else 0.0
        curr_capital = record[constants.const_s_curr_capital]
        buy_in = (share_hold_sum_today - share_hold_sum_range) / curr_capital
        share_hold_percentage = share_hold_sum_today / curr_capital
        resp[constants.const_if_model_satisfied] = buy_in > threshold_buy_in \
                                                   and share_hold_percentage > threshold_share_hold_percentage
        resp[constants.const_total_buy_in] = buy_in
        resp[constants.const_share_hold_percentage] = share_hold_percentage
        return resp
    return false_resp


def process(
        threshold_share_hold_percentage=constants.const_threshold_share_hold_percentage,
        threshold_buy_in=constants.const_threshold_buy_in):
    entries = os.listdir()
    records = []
    if constants.filename_code_company_info_records not in entries:
        print('Getting stock codes...')
        records = write_code_and_company_info()
        print('Finish getting stock codes')
    else:
        print(constants.filename_code_company_info_records, 'already exists. Now start reading from the file...')
        records = read_code_and_company_info()
        print('Finish loading data')

    today = datetime.datetime.today()
    headers = [
        constants.const_ch_stock_code,
        constants.const_ch_stock_name,
        constants.const_ch_share_hold_percentage,
        constants.const_ch_total_buy_in
    ]
    time_frames = constants.const_time_frames
    xls_filename = today.strftime("%y_%m_%d") + ".xlsx"
    sheet_names = ["past_%d" % time_frame for time_frame in time_frames]
    excel_writer = ExcelWriter(xls_filename, engine='xlsxwriter', date_format='YYYY-MM-DD')
    len_time_frames = len(time_frames)
    rows_by_time_frame = [[] for _ in range(len_time_frames)]
    for record in records:
        print('Now for stock', record[constants.const_s_code])
        data = get_stock_data_for_past_twenty_days_of_one_company(record[constants.const_s_code])
        if len(data) == 0:
            continue
        for i, time_frame in enumerate(time_frames):
            resp = if_data_satisfies_model(data,
                                           record,
                                           threshold_share_hold_percentage=threshold_share_hold_percentage,
                                           threshold_buy_in=threshold_buy_in,
                                           timeframe=time_frame
                                           )
            if resp[constants.const_if_model_satisfied]:
                row = {
                    constants.const_ch_stock_code: record[constants.const_s_code],
                    constants.const_ch_stock_name: data[0][constants.STOCK_NAME],
                    constants.const_ch_share_hold_percentage: resp[constants.const_share_hold_percentage],
                    constants.const_ch_total_buy_in: resp[constants.const_total_buy_in]
                }
                rows_by_time_frame[i].append(row)

    for i, sheet_name in enumerate(sheet_names):
        df = DataFrame.from_records(rows_by_time_frame[i])
        df.to_excel(excel_writer, sheet_name=sheet_name)
    excel_writer.save()
