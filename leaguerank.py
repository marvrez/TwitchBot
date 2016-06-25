import requests

#Check for errors
class LoLException(Exception):
    def __init__(self, error, response):
        self.error = error
        self.headers = response.headers

    def __str__(self):
        return self.error

    def __eq__(self, other):
        if isinstance(other, "".__class__):
            return self.error == other
        elif isinstance(other, self.__class__):
            return self.error == other.error and self.headers == other.headers
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return super(LoLException).__hash__()


error_400 = "Bad request"
error_401 = "Unauthorized"
error_403 = "Blacklisted key"
error_404 = "Game data not found"
error_429 = "Too many requests"
error_500 = "Internal server error"
error_503 = "Service unavailable"
error_504 = 'Gateway timeout'


def raise_status(response):
    if response.status_code == 400:
        raise LoLException(error_400, response)
    elif response.status_code == 401:
        raise LoLException(error_401, response)
    elif response.status_code == 403:
        raise LoLException(error_403, response)
    elif response.status_code == 404:
        raise LoLException(error_404, response)
    elif response.status_code == 429:
        raise LoLException(error_429, response)
    elif response.status_code == 500:
        raise LoLException(error_500, response)
    elif response.status_code == 503:
        raise LoLException(error_503, response)
    elif response.status_code == 504:
        raise LoLException(error_504, response)
    else:
        response.raise_for_status()


region_list = ['br', 'eune', 'euw', 'kr', 'lan', 'las', 'na', 'oce', 'ru', 'tr']  
#get league given region and and summoner name
class get_summoner_league(object):
    def __init__(self,api_key,region = "euw"):
        self.api_key = api_key
        self.region = region
    URL = {
        "base": "https://{proxy}.api.pvp.net/api/lol/{region}/{url}",
        "summonerName": "v1.4/summoner/by-name/{name}?api_key={API}",
        "summonerRank": "v2.5/league/by-summoner/{summoner_id}/entry?api_key={API}",
}
    def getSummonerData(self,summonerName):
        api_url = self.URL["summonerName"].format(name = summonerName, API = self.api_key)
        response = requests.get(
            self.URL["base"].format(
                proxy = self.region,
                region = self.region,
                url = api_url)
                )
        print (response)
        return response.json()
        
    def getRankData(self,ID):
        api_url = self.URL["summonerRank"].format(region=self.region,summoner_id = ID, API = self.api_key)
        response = requests.get(
            self.URL["base"].format(
                proxy = self.region,
                region = self.region,
                url = api_url)
                )
        print (response)
        return response.json()
   
    def getLeagueRank(self,message):
        if message: #"!rank REGION SUMMONER_NAME"
            summoner_name = str(message.split()[2])
            try:
                region = message.split()[1].lower()
            except IndexError:
                region = self.region
        if region not in region_list:
            return "Region is not valid. Please enter a valid region, region is optional and the default region is {}".format(region.upper())

        try:
            summoner = self.getSummonerData(summoner_name)
            print (summoner)
            summonerID = str(summoner[summoner_name]['id'])
            summoner_name = summoner[summoner_name]["name"]

        except LoLException as e:
            if e == error_429:
                return "Too many requests, STFU for some seconds DansGame"
            elif e == error_404:
                return "The summoner not found. Use a valid summoner name (remove spaces) and region FailFish"
            else:
                return "Something unknown went wrong FeelsBadMan"
        try:
            summoner_league = self.getRankData(summonerID)
            print (summoner_league)
            tier = summoner_league[summonerID][0]["tier"]
            division = summoner_league[summonerID][0]["entries"][0]["division"]
            leaguePoints = summoner_league[summonerID][0]["entries"][0]["leaguePoints"]

            return "The summoner {} on region {} is currently in {} {} with {} LP 4Head".format(summoner_name, self.region.upper(),tier, division,leaguePoints)
        except LoLException as e:
            if e == error_429:
                return "Too many requests, STFU for some seconds DansGame"
            elif e == error_404:
                return "Rank data not found cmonBruh"
            else:
                return "Trouble fetching summoner rank.. KKona Try again later!"
    
