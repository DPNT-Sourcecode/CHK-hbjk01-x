import json

class SkuService(object):
    def __init__(self):
        self.skus = []

    def load_from_json_file(self, path):
        with open(path, 'r') as f:
            loaded = json.load(f)
            self.skus = loaded

    def get_sku(self, sku):
        return next((sku_entry for sku_entry in self.skus if sku_entry['sku'] == sku), None)