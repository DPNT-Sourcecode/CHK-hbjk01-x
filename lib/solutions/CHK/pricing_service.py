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

        freebies_used = {}
        for sku, quantity in sku_quantities.items():
            sku_info = self.sku_service.get_sku(sku)

            if quantity > 1 and 'offers' in sku_info and len(sku_info['offers']) > 0:
                best_offer = self._find_best_offer(sku_info['offers'], quantity)

                while quantity > 1 and best_offer is not None:
                    quantity -= best_offer['quantity']
                    total += best_offer['price'] if 'price' in best_offer else best_offer['quantity'] * sku_info['price']
                    if 'freebies' in best_offer:
                        for freebie in best_offer['freebies']:
                            if freebie['sku'] in sku_quantities:
                                number_already_used = freebies_used[freebie['sku']] if freebie['sku'] in freebies_used else 0
                                if number_already_used + freebie['quantity'] > sku_quantities[freebie['sku']]:
                                    continue

                                number_discountable = sku_quantities[freebie['sku']] - number_already_used
                                freebie_sku_info = self.sku_service.get_sku(freebie['sku'])
                                if 'offers' in freebie_sku_info and len(freebie_sku_info['offers']) > 0:
                                    freebie_best_offer = self._find_best_offer(freebie_sku_info['offers'], number_discountable)
                                    if freebie_best_offer is not None:
                                        freebie_saving = freebie['quantity'] * freebie_sku_info['price']
                                        offer_saving = (freebie_sku_info['price'] * freebie['quantity']) - freebie_best_offer['price']
                                        if freebie_saving >= offer_saving:
                                            total -= freebie['quantity'] * freebie_sku_info['price']
                                            freebies_used[freebie['sku']] = number_already_used + freebie['quantity']
                                else:
                                    total -= freebie['quantity'] * freebie_sku_info['price']
                                    freebies_used[freebie['sku']] = number_already_used + freebie['quantity']
                    best_offer = self._find_best_offer(sku_info['offers'], quantity)
                
            total += sku_info['price'] * quantity

        return total

    def _find_best_offer(self, offers, current_quantity):
        relevant_offers = [offer for offer in offers if offer['quantity'] <= current_quantity]
        sorted_offers = sorted(relevant_offers, key=lambda key: key['quantity'], reverse=True)
        return sorted_offers[0] if len(sorted_offers) > 0 else None

