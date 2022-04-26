

#Make sure to sign up for IEX API token, and paste it here
token = 'Tpk_4d88dfb8d4024e5bbea97f0f1b5ccadf'


import pycurl
import json
from io import BytesIO



response_buffer = BytesIO()
curl = pycurl.Curl()	#Set the curl options which specify the Google API server, the parameters to be passed to the API,
# and buffer to hold the response
curl.setopt(curl.SSL_VERIFYPEER, False)

response_buffer2 = BytesIO()
curl2 = pycurl.Curl()	#Set the curl options which specify the Google API server, the parameters to be passed to the API,
# and buffer to hold the response
curl2.setopt(curl2.SSL_VERIFYPEER, False)


#These are some of the API endpoints you will be using in the assignment.

#curl.setopt(curl.URL, 'https://sandbox.iexapis.com/stable/stock/baba/stats?token='+token)
curl2.setopt(curl2.URL, 'https://sandbox.iexapis.com/stable/stock/baba/quote?token='+token)
#curl.setopt(curl.URL, 'https://sandbox.iexapis.com/stable/ref-data/symbols?token='+token)
#curl2.setopt(curl.URL, 'https://sandbox.iexapis.com/stable/stock/aapl/chart/5y?chartCloseOnly=true&token='+token)

'''
curl.setopt(curl.WRITEFUNCTION, response_buffer.write)

curl.perform()
curl.close()
'''
######################################
curl2.setopt(curl2.WRITEFUNCTION, response_buffer2.write)

curl2.perform()
curl2.close()



body = response_buffer2.getvalue().decode('UTF-8')


body = json.loads(body)

print(body['latestPrice'] - 20.00)







