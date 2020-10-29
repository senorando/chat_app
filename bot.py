import json, requests, random, os
from os.path import join, dirname
from dotenv import load_dotenv


class chatBot:
    def funtranslate(self, input):
        headers = {"Content-Type": "application/json"}
        api_url = "https://api.funtranslations.com/translate/yoda.json?text={}".format(input)
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            return json.loads(response.content)
        else:
            return {
                "contents": {
                    "translated": 'Sorry we\'ve run out of API calls for funtranslations. Please try again in an hour :('}}
    
    def joke(self):
        dotenv_path = join(dirname(__file__), 'sql.env')
        load_dotenv(dotenv_path)
        JOKE_KEY =  os.environ['JOKE_KEY']
        url = "https://rapidapi.p.rapidapi.com/v1/joke"

        headers = {
            'x-rapidapi-host': "joke3.p.rapidapi.com",
            'x-rapidapi-key': "{}".format(JOKE_KEY)
        }

        response = requests.request("GET", url, headers=headers)
        json_body = response.json()
        joke =  json.dumps(json_body["content"]).replace("\"","").replace("\\", "")
        
        return joke

    def command(self, input):
        INVALID_COMMAND = "Command not recognized. Please try one of these: !! [about|help|yoda]"
        ABOUT = 'Welcome to "Not Discord"! My name is BimboBOT and I\'m here to help you out with different things. I\'m a bit of a bimbo (hence the name) but I try my best and that\'s what counts! '
        HELP = "All commands start with \"!!\" and are followed by the command and any parameters: !! <about|help|joke|yoda [message]>"
        YODA_FAIL = "Please enter a word or phrase to translate. (Ex: !!yoda The quick brown fox jumped over the lazy dog)"
        
        COMMAND = input.lower()
        
        if COMMAND == "!! about" or COMMAND == "!!about":
            return ABOUT
        elif COMMAND == "!! help" or COMMAND == "!!help":
            return HELP
        elif COMMAND == "!! joke" or COMMAND == "!!joke":
            return self.joke()
        elif COMMAND.startswith("!!yoda") or COMMAND.startswith("!! yoda"):
            if len(input[input.find("a") + 1:]) == 0:
                return YODA_FAIL
            else:
                return self.funtranslate(input[input.find("a") + 1 :])["contents"]["translated"]
        else:
            return INVALID_COMMAND
