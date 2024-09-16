################################################################################
#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to whom the
#  Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#  OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.

import json
import random
import urllib.request
import sys
# Server API URLs
QUERY = "http://localhost:8080/query?id={}"

# 500 server request
N = 500


def getDataPoint(quote: str) -> tuple:
    """ Produce all the needed values to generate a datapoint
    price = avg(bid_price, ask_price)
    input:
        quote: dict
    returns:
        tuple: (stock, bid_price, ask_price, price)
    ------------- Update this function ------------- """

    stock = quote['stock']
    """
    # would expect in real market behavior
    # if no quantity of bids or asks, set the price to 0.0
    bid_price = max(float(quote['top_bid']['price']), 0.0)
    ask_price = max(float(quote['top_ask']['price']), 0.0)
    # would expect in real market behavior
    bid_price = min(bid_price, ask_price)
    """
    bid_price = float(quote['top_bid']['price'])
    ask_price = float(quote['top_ask']['price'])

    price = (bid_price + ask_price) / 2
    """ 2 points past decimal place
    return (stock,
            float(f"{bid_price:.2f}"),
            float(f"{ask_price:.2f}"),
            float(f"{price:.2f}"))
    """
    return stock, bid_price, ask_price, price

def getRatio(price_a: float, price_b: float) -> float:
    """ Get ratio of price_a and price_b
    input:
        price_a, price_b: float, float
    returns:
        price_b <= 0.0 then 1e9 to avoid div by 0 error
        else: price_a / price_b
    ------------- Update this function ------------- """
    if price_b <= 0.0:
        return 1e9

    # 2 places past decimal
    # ratio = float(f"{(price_a / price_b):.2f}")
    ratio = price_a / price_b

    # print(f"{price_a = }, {price_b = }, {ratio = }")
    return ratio

# Main
if __name__ == "__main__":
    # Query the price once every N seconds.
    for _ in iter(range(N)):
        quote = None
        try:
            quotes = json.loads(urllib.request.urlopen(QUERY.format(random.random())).read())
        except Exception as e:
            print(f"Error fetching data: {e = }")
            continue

        """ ----------- Update to get the ratio --------------- """
        for quote in quotes:
            stock, bid_price, ask_price, price = getDataPoint(quote)
            print("Quoted %s at (bid:%s, ask:%s, price:%s)" % (stock, bid_price, ask_price, price))

        print("Ratio %s" % getRatio(bid_price, ask_price))
