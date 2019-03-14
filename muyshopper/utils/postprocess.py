# -*- coding: utf-8 -*-
"""Utils to process all item fields and attributes."""
import re


class PostProcess:
    def __init__(self):
        pass

    def find_float_in_string(self, value, limit=None, keep_right_zeros=True):
        if value:
            if '.' in value and ',' in value:
                value = value.replace('.', '')
            else:
                value = value.replace(',', '.')
        
            value = str(value).lower()

            try:
                value = value.replace(',', '.')
                number = re.findall(r"[-+]?\d*\.\d+|\d+", value)[0]
                # number = re.findall(r"\d+\.\d+", value)[0] # ONLY FLOAT, NO INT

                number = float(number)

                if not keep_right_zeros:
                    if float(number) % 1 == 0:
                        number = int(number)

                if limit and number > limit:
                    return None

                return number
            except IndexError:
                return None

    def process_item(self, item):
        price = item.get('precio')
        normalized_price = self.find_float_in_string(price)
        item['precio'] = normalized_price

        if item['precio']:
            return item
        else:
            return None
