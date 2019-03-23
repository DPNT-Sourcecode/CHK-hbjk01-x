from itertools import groupby

class PricingService(object):
    def __init__(self, sku_service):
        self.sku_service = sku_service

    def get_price(self, basket_string):
        total = 0
        sku_quantities = {}
        
        char_groups = groupby(sorted(basket_string), lambda key: key)

        for group_key, group in char_groups:
            sku_quantities[group_key] = len(list(group))

        for sku, quantity in sku_quantities.items():
            sku_info = self.sku_service.get_sku(sku)

            if quantity > 1 and 'offers' in sku_info and len(sku_info['offers']) > 0:
                relevant_offers = [offer for offer in sku_info['offers'] if offer['quantity'] <= quantity]
                
                while quantity > 1 and len(relevant_offers) > 0:
                    sorted_offers = sorted(relevant_offers, key=lambda key: key['quantity'], reverse=True)
                    offer = sorted_offers[0]
                    quantity -= offer['quantity']
                    total += offer['price']
                    relevant_offers = [offer for offer in sku_info['offers'] if offer['quantity'] <= quantity]
                
            total += sku_info['price'] * quantity

        return total
