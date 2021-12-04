from django.shortcuts import render
import os
import requests
import json
from urllib.request import urlopen
from dotenv import load_dotenv


# Load the .env file
load_dotenv()


# Create your views here.
def home(request):
    return render(request, './index.html')

def search(request):
    if request.method == "POST":
        # User searches for name and gets their encrypted ID
        userName = request.POST.get('username')
        api_key = os.getenv("API_KEY")

        response = requests.get('https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/'+ userName +'?api_key='+ api_key)
        json_response = response.json()
        encid = json_response['id']

        # Load in the champion data
        url = 'http://ddragon.leagueoflegends.com/cdn/11.23.1/data/en_US/champion.json'
        champ_response = requests.get(url)
        champ_data = json.loads(champ_response.text)
        champion_id = champ_data['data']
        
        # Part of Champion Data, sort through the JSON and fill championDict var with keys and ids of champions
        champion_ids = []
        champion_names = []
        for champName, champDict in champion_id.items():
            for (champName, value) in champDict.items():
                newDict = {"name": champName, "value": value}
                if newDict['name'] == 'key':
                    champion_ids.append(newDict[('value')])
                if newDict['name'] == 'id':
                    champion_names.append(newDict[('value')])

        champion_ids = [int(n) for n in champion_ids]            

        zip_champs = zip(champion_names, champion_ids)

        championDict = dict(zip_champs)

        # Return the mastery data
        mResponse = requests.get('https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/'+ encid+'?api_key=' + api_key)
        mastery = json.loads(mResponse.text)

        return render(request, './index.html', {'mastery':mastery, 'userName': userName, 'champion_id':champion_id, 'championDict':championDict })  

    else:
    
        return render(request, './index.html')