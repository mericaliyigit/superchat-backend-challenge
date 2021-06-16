import requests


class SuperchatPlugin:
    bitcoin_url = 'https://api.coindesk.com/v1/bpi/currentprice.json'
    cached_last_price = '0'

    def get_current_price(self):

        try:
            response=requests.get(self.bitcoin_url)
            data = response.json()
            self.cached_last_price = data['bpi']['USD']['rate'].replace(',','')
            return self.cached_last_price
        except Exception as e :
            if self.cached_last_price == '0':
                return '0'
            else:
                return self.cached_last_price

    def __init__(self):
        print('Initializing superchat plugin')
        self.get_current_price()


    def token_replace_name(self, a_message, receiver_name):
        #receiver_name = ''
        a_message = a_message.replace('#name#', receiver_name)
        return a_message

    def token_replace_btc(self, a_message):
        a_message = a_message.replace('#btc#', self.get_current_price())
        return a_message

    def message_fix(self,a_message,receiver_name):
        with_name=self.token_replace_name(a_message,receiver_name)
        finished = self.token_replace_btc(with_name)
        return finished





