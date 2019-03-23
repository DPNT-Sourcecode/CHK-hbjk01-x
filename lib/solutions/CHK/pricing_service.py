from itertools import groupby

class PricingService(object):
    def __init__(self, sku_service):
        self.sku_service = sku_service

    def get_price(self, basket_string):
        total = 0
        sku_quantities = {}
        
        char_groups = groupby(basket_string, lambda key: key)

        for group_key, group in char_groups:
            sku_quantities[group_key] = len(group)

        for sku, quantity in sku_quantities.items():
            sku_info = self.sku_service.get_sku(sku)

            if 'offers' in sku_info and len(sku_info['offers']) > 0:
                pass

        return total