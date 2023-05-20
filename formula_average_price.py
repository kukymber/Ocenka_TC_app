import numpy as np

class PriceCalculator:
    def __init__(self, offer_prices):
        self.offer_prices = offer_prices

    def compute_average_offer_price(self):
        return np.mean(self.offer_prices)

    def compute_final_average_offer_price(self):
        average_offer_price = self.compute_average_offer_price()
        final_offers = [price for price in self.offer_prices if abs(price - average_offer_price) / average_offer_price <= 0.2]
        return np.mean(final_offers)

    def compute_final_price(self):
        final_average_offer_price = self.compute_final_average_offer_price()
        return final_average_offer_price * 0.9

# Создаем экземпляр класса PriceCalculator и передаем ему цены предложений
price_calculator = PriceCalculator([396000, 350000, 199000, 255000, 240000])

# Вычисляем итоговую цену
final_price = price_calculator.compute_final_price()

# Выводим итоговую цену
print(f"Итоговая цена: {final_price}")