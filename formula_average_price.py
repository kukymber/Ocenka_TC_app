import numpy as np

class PriceCalculator:
    def __init__(self):
        self.offer_prices = []

    def update_offer_prices(self, new_prices):
        self.offer_prices = new_prices

    def compute_average_offer_price(self):
        return round(np.mean(self.offer_prices), 2)

    def compute_final_average_offer_price(self):
        average_offer_price = self.compute_average_offer_price()
        final_offers = [price for price in self.offer_prices if abs(price - average_offer_price) / average_offer_price <= 0.2]
        return round(np.mean(final_offers), 2)

    def compute_final_price(self):
        final_average_offer_price = self.compute_final_average_offer_price()
        return round(final_average_offer_price * 0.9, 2)
