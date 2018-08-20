# -*- coding: utf-8 -*-


class InputData(object):

    """ Comisión que nos quita el banco 13.5 """
    comission = 13.5

    """ Porcentaje de impuestos %"""
    tax_rate = 18.0

    def __init__(self):
        self.__input_money = 0.0
        self.__buy_price = 0.0

    def __get_tax_multipier(self):
        return 1 + (self.tax_rate / 100)

    tax_mult = property(__get_tax_multipier)

    def _get_input_money(self):
        return self.__input_money

    def _set_input_money(self, money):
        self.__input_money = money

    """ Dinero que vamos a invertir """
    input_money = property(_get_input_money, _set_input_money)

    def _get_buy_price(self):
        return self.__buy_price

    def _set_buy_price(self, price):
        self.__buy_price = price

    """ Precio de compra de la acción """
    buy_price = property(_get_buy_price, _set_buy_price)

    def _get_buy_money(self):
        return self.input_money - self.comission

    """ Dinero real del que disponemos para la compra"""
    buy_money = property(_get_input_money)

    def _get_num_of_shares(self):
        return self.buy_money / self.buy_price

    """ Qty|Size: Número de acciones que vamos a comprar """
    num_of_shares = property(_get_num_of_shares)

    """ Devuelve el precio de venta para obtener el beneficio que pasamos
        como argumento """
    def get_sell_price(self, extra_money):
        return ((extra_money * self.tax_mult) +
            self.buy_money +
            self.comission) / self.num_of_shares

    def _get_sell_price_0_profit(self):
        return self.get_sell_price(0.0)

    """ Precio de venta de nuestras acciones a partir del cual
        empezamos a obtener beneficios """
    sell_price_0_profit = property(_get_sell_price_0_profit)

    def __str__(self):
        return str(self.sell_price_0_profit)

if __name__ == "__main__":
    input_values = InputData()
    input_values.input_money = input("Dinero que vamos a invertir: ")
    input_values.buy_price = input("Precio de compra de la acción: ")
    print ("Empezamos a obtener beneficios si vendemos a partir de: %f" %
        input_values.sell_price_0_profit)
    print ("Si queremos obtener 100 euros de beneficio debemos vender a: %f" %
        input_values.get_sell_price(100.0))