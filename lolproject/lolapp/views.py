from django.shortcuts import render
import requests
import json
from urllib.request import urlopen


# Create your views here.
def home(request):
    # api_key = "RGAPI-3a58d94f-8442-4f65-a3a6-966b44cffaba"
    # username = ''
    # response = requests.get('https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/'+ username +'?api_key='+ api_key)
    # json_response = response.json()
    # encid = json_response['id']

    return render(request, './index.html')

def search(request):
    if request.method == "POST":
        # User searches for name and gets their encrypted ID
        userName = request.POST.get('username')
        api_key = "RGAPI-006b93e8-0346-49ae-8749-ed753a0547b6"

        response = requests.get('https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/'+ userName +'?api_key='+ api_key)
        json_response = response.json()
        encid = json_response['id']

        # Load in the champion data
        url = 'http://ddragon.leagueoflegends.com/cdn/11.23.1/data/en_US/champion.json'
        champ_response = urlopen(url)
        champ_data = json.loads(champ_response.read())

        # Return the mastery data
        mResponse = requests.get('https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/'+ encid+'?api_key=' + api_key)
        mastery = json.loads(mResponse.text)

        
        # for key in champ_data:
        #     for id in mastery:
        #         if key == id:
        #             return key['id']

        return render(request, './index.html', {'mastery':mastery, 'userName': userName})  

    else:
    
        return render(request, './index.html')