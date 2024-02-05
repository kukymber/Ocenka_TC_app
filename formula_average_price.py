import numpy as np
import scipy.stats as stats


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
        return round(final_average_offer_price * 0.95, 2)

    def compute_standard_error(self):
        return round(stats.sem(self.offer_prices), 2)

    def compute_confidence_interval(self, confidence_level=0.95):
        margin_of_error = stats.t.ppf((1 + confidence_level) / 2,
                                      len(self.offer_prices) - 1) * self.compute_standard_error()
        mean = self.compute_final_average_offer_price()
        lower_bound = round(mean - margin_of_error, 2)
        upper_bound = round(mean + margin_of_error, 2)
        return lower_bound, upper_bound

    def compute_accuracy(self):
        mean = self.compute_final_average_offer_price()
        standard_error = self.compute_standard_error()
        accuracy = round(1.96 * standard_error, 2)
        return accuracy