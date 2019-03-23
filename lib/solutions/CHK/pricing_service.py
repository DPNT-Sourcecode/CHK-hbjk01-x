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
                best_offer = self._find_best_offer(sku_info['offers'], sku_quantities, freebies_used, quantity, sku_info['price'])

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
                                should_use_freebies = True
                                total_saving = self._get_offer_value(best_offer, sku_quantities, freebies_used, number_discountable, sku_info['price'])
                                if 'offers' in freebie_sku_info and len(freebie_sku_info['offers']) > 0:
                                    freebie_best_offer = self._find_best_offer(freebie_sku_info['offers'], sku_quantities, freebies_used, number_discountable, freebie_sku_info['price'])
                                    if freebie_best_offer is not None:
                                        freebie_saving = total_saving
                                        offer_saving = self._get_offer_value(freebie_best_offer, sku_quantities, freebies_used, number_discountable, freebie_sku_info['price'])
                                        if offer_saving > freebie_saving:
                                            should_use_freebies = False
                                        else:
                                            # the offer on this freebie isn't as good, so also counteract that in the price
                                            total_saving -= offer_saving
                                
                                if should_use_freebies:
                                    total -= total_saving
                                    freebies_used[freebie['sku']] = number_already_used + freebie['quantity']
                    best_offer = self._find_best_offer(sku_info['offers'], sku_quantities, freebies_used, quantity, sku_info['price'])
                
            total += sku_info['price'] * quantity

        return total

    def _find_best_offer(self, offers, sku_quantities_dict, freebies_used_dict, current_quantity, original_price):
        relevant_offers = [offer for offer in offers if offer['quantity'] <= current_quantity]
        sorted_offers = sorted(relevant_offers, key=lambda offer: self._get_offer_value(offer, sku_quantities_dict, freebies_used_dict, current_quantity, original_price), reverse=True)
        return sorted_offers[0] if len(sorted_offers) > 0 else None

    def _get_offer_value(self, offer, sku_quantities_dict, freebies_used_dict, quantity, original_price):
        total_saving = 0
        if 'price' in offer:
            while quantity >= offer['quantity']:
                total_saving += (original_price * offer['quantity']) - offer['price']
                quantity -= offer['quantity']
        if 'freebies' in offer:
            for freebie in offer['freebies']:
                if freebie['sku'] not in sku_quantities_dict:
                    continue

                number_already_used = freebies_used_dict[freebie['sku']] if freebie['sku'] in freebies_used_dict else 0
                if number_already_used + freebie['quantity'] > sku_quantities_dict[freebie['sku']]:
                    continue # offer cannot be applied as it's been used on too many items

                number_discountable = sku_quantities_dict[freebie['sku']] - number_already_used
                freebie_sku_info = self.sku_service.get_sku(freebie['sku'])
                while number_discountable >= freebie['quantity'] and quantity >= offer['quantity']:
                    total_saving += freebie['quantity'] * freebie_sku_info['price']
                    number_discountable -= freebie['quantity']
                    quantity -= offer['quantity']

        return total_saving
