from src.get_all_stock_codes import get_all_stock_codes
import src.constants as constants
from src.get_stock_data import get_stock_data

all_codes = get_all_stock_codes(constants.stock_code_url)

for code in all_codes:
    data = get_stock_data(constants.s_type, constants.s_url, constants.s_token, code)
    refined_data = []
    for item in data:
        refined_item = {}
        for field in constants.fields:
            refined_item[field] = item[field]
        refined_data.append(refined_item)

