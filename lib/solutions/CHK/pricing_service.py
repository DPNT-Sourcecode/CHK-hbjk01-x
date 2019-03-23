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

        offers_applied = {
            'freebies_used':  {},
            'prices_used': {}
        }
        for sku, quantity in sku_quantities.items():
            sku_info = self.sku_service.get_sku(sku)

            if quantity > 1 and 'offers' in sku_info and len(sku_info['offers']) > 0:
                best_offer = self._find_best_offer(sku, sku_info['offers'], sku_quantities, offers_applied, quantity, sku_info['price'])

                while quantity > 1 and best_offer is not None:
                    quantity -= best_offer['quantity']
                    total += best_offer['price'] if 'price' in best_offer else best_offer['quantity'] * sku_info['price']
                    if 'price' in best_offer:
                        if sku in offers_applied['prices_used']:
                            offers_applied['prices_used'][sku] += best_offer['quantity']
                        else:
                            offers_applied['prices_used'][sku] = best_offer['quantity']
                    if 'freebies' in best_offer:
                        for freebie in best_offer['freebies']:
                            if freebie['sku'] in sku_quantities:
                                number_already_used = offers_applied['freebies_used'][freebie['sku']] if freebie['sku'] in offers_applied['freebies_used'] else 0
                                if number_already_used + freebie['quantity'] > sku_quantities[freebie['sku']]:
                                    continue

                                number_discountable = sku_quantities[freebie['sku']] - number_already_used
                                freebie_sku_info = self.sku_service.get_sku(freebie['sku'])
                                should_use_freebies = True
                                total_saving = self._get_offer_value(best_offer, sku_quantities, offers_applied, number_discountable, sku_info['price'])
                                if 'offers' in freebie_sku_info and len(freebie_sku_info['offers']) > 0:
                                    freebie_best_offer = self._find_best_offer(freebie['sku'], freebie_sku_info['offers'], sku_quantities, offers_applied, number_discountable, freebie_sku_info['price'])
                                    if freebie_best_offer is not None:
                                        freebie_saving = total_saving
                                        offer_saving = self._get_offer_value(freebie_best_offer, sku_quantities, offers_applied, number_discountable, freebie_sku_info['price'])
                                        if offer_saving > freebie_saving:
                                            should_use_freebies = False
                                        else: 
                                            if freebie['sku'] in offers_applied['prices_used']:
                                                if (sku_quantities[freebie['sku']] - offers_applied['prices_used'][freebie['sku']]) < freebie['quantity']:
                                                    total += offer_saving
                                                offers_applied['prices_used'][freebie['sku']] -= freebie['quantity']
                                
                                if should_use_freebies:
                                    total -= (freebie['quantity'] * freebie_sku_info['price'])
                                    offers_applied['freebies_used'][freebie['sku']] = number_already_used + freebie['quantity']
                    best_offer = self._find_best_offer(sku, sku_info['offers'], sku_quantities, offers_applied, quantity, sku_info['price'])
                
            total += sku_info['price'] * quantity

        return total

    def _find_best_offer(self, sku, offers, sku_quantities_dict, offers_applied, current_quantity, original_price):
        relevant_offers = [
             offer for offer in offers
             if (offer['quantity'] <= current_quantity or
                'anyOf' in offer and offer['quantity'] <= sum([sku_quantities_dict.get(x, 0) for x in offer['anyOf']])
             ) and (
                 'freebies' not in offer or
                 any(freebie for freebie in offer['freebies'] if freebie['sku'] != sku) or
                 any(freebie for freebie in offer['freebies'] if freebie['sku'] == sku and
                    offer['quantity'] + freebie['quantity'] <= current_quantity)
             )]
        sorted_offers = sorted(relevant_offers, key=lambda offer: self._get_offer_value(offer, sku_quantities_dict, offers_applied, current_quantity, original_price), reverse=True)
        return sorted_offers[0] if len(sorted_offers) > 0 else None

    def _get_offer_value(self, offer, sku_quantities_dict, offers_applied, quantity, original_price):
        freebies_used_dict = offers_applied['freebies_used']
        
        total_saving = 0
        if 'anyOf' in offer:
           new_quantity = sum([sku_quantities_dict.get(x, 0) for x in offer['anyOf']])
           if new_quantity > offer['quantity']:
               quantity = new_quantity
        if 'price' in offer and 'anyOf' not in offer:
            while quantity >= offer['quantity']:
                total_saving += (original_price * offer['quantity']) - offer['price']
                quantity -= offer['quantity']
        if 'price' in offer and 'anyOf' in offer:
            sorted_offer_skus = self._get_sorted_anyof_prices(offer)
            used_skus_for_any_of = {}
            while quantity >= offer['quantity']:
                next_sku = next((s for s in sorted_offer_skus
                    if s in sku_quantities_dict and
                    sku_quantities_dict[s] > 0 and
                    (s not in used_skus_for_any_of or sku_quantities_dict[s] > used_skus_for_any_of[s])
                ))
                if next_sku in used_skus_for_any_of:
                    used_skus_for_any_of[next_sku] += 1
                else:
                    used_skus_for_any_of[next_sku] = 1
                sku_price = self.sku_service.get_sku(next_sku)['price']
                total_saving += sku_price
                quantity -= 1
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

    def _get_sorted_anyof_prices(self, offer):
        return sorted(offer['anyOf'], lambda sky: self.sku_service.get_sku(sku)['price'], reverse=True)


