import unittest
from client3 import getDataPoint, getRatio


class ClientTest(unittest.TestCase):
  def test_getDataPoint_calculatePrice(self):
    quotes = [
      {'top_ask': {'price': 121.2, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 120.48, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'},
      {'top_ask': {'price': 121.68, 'size': 4}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 117.87, 'size': 81}, 'id': '0.109974697771', 'stock': 'DEF'}
    ]
    """ ------------ Add the assertion below ------------ """
    for quote in quotes:
      stock, bid_price, ask_price, _ = getDataPoint(quote)
      price_expected = (bid_price + ask_price) / 2
      self.assertEqual(getDataPoint(quote), (stock, bid_price, ask_price, price_expected))

  def test_getDataPoint_calculatePriceBidGreaterThanAsk(self):
    quotes = [
      {'top_ask': {'price': 119.2, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 120.48, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'},
      {'top_ask': {'price': 121.68, 'size': 4}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 117.87, 'size': 81}, 'id': '0.109974697771', 'stock': 'DEF'}
    ]
    """ ------------ Add the assertion below ------------ """
    # take the ask if bid > ask (in a real scenario)
    # since expect bid to fill at ask price
    # min(quote['top_bid']['price'], quote['top_ask']['price']),
    for quote in quotes:
      stock, bid_price, ask_price, _ = getDataPoint(quote)
      price_expected = (bid_price + ask_price) / 2
      self.assertEqual(getDataPoint(quote), (stock, bid_price, ask_price, price_expected))

  """ ------------ Add more unit tests ------------ """
  def test_getRatio_divByZeroError(self):
    quotes = [
      # no issue
      {'top_ask': {'price': 10.03, 'size': 10}, 'timestamp': '2019-02-11 22:06:30.572453',
       'top_bid': {'price': 10.01, 'size': 10}, 'id': '0.109974697771', 'stock': 'ABC'},
      # denom div by zero error
      {'top_ask': {'price': 0.0, 'size': 10}, 'timestamp': '2019-02-11 22:06:30.572453',
       'top_bid': {'price': 10.01, 'size': 10}, 'id': '0.109974697771', 'stock': 'DEF'},
      # denom div by zero error, both == 0.0
      {'top_ask': {'price': 0.0, 'size': 10}, 'timestamp': '2019-02-11 22:06:30.572453',
       'top_bid': {'price': 0.0, 'size': 10}, 'id': '0.109974697771', 'stock': 'GHI'}
    ]

    for quote in quotes:
      _, bid_price, ask_price, _ = getDataPoint(quote)
      ratio_expected = 0.0
      if ask_price == 0.0:
        ratio_expected = 1e9
      else:
        ratio_expected = bid_price / ask_price

      self.assertEqual(getRatio(bid_price, ask_price), ratio_expected)

  """ Future work if needed
  def test_getRatio_quantityZeroError(self):
    quotes = [
      # normal
      {'top_ask': {'price': 120.48, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453',
       'top_bid': {'price': 119.2, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'},
      # no bids
      {'top_ask': {'price': 120.48, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453',
       'top_bid': {'price': 119.2, 'size': 0}, 'id': '0.109974697771', 'stock': 'ABC'},
      # no asks
      {'top_ask': {'price': 120.48, 'size': 0}, 'timestamp': '2019-02-11 22:06:30.572453',
       'top_bid': {'price': 119.2, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'},
    ]

    self.assertEqual(getRatio(bid_price, ask_price), ratio_expected)
    """

if __name__ == '__main__':
    unittest.main()
