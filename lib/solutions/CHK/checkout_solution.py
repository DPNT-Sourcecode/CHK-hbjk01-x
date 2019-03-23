import logging

from sku_service import SkuService

logging.getLogger().setLevel(logging.INFO)

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    sku_service = SkuService()
    
    try:
        sku_service.load_from_json_file('skus.json')
    except Exception as e:
        logging.error("Unable to load SKUs", exc_info=True)
        return -1

    


