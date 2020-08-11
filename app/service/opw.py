from apiwrapper import APIWrapper
import datetime


class Openweather(APIWrapper):

    def __init__(self,api_key):
        self.api_key=api_key

    def _my_callback(self, resp):
        """
        'resp' is a Response object returned from `requests` library
        """
        return resp.json()
        

    def fetch_weather(self,lat,lon):
        """
        @param: latitude and longitude
        Fetch Weather
        """
        url = 'http://api.openweathermap.org/data/2.5/onecall?lat='+str(lat) +'&lon='+str(lon)+'&units=metric&exclude=hourly&appid='+self.api_key
        return self.make_request(url, method='get', headers={'content-type': 'application/json'}, data=None, callback=self._my_callback)

   
