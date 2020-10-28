import json, requests, random, os
from os.path import join, dirname
from dotenv import load_dotenv


class chatBot:
    headers = {"Content-Type": "application/json"}

    def get_account_info(self, input):
        api_url = "https://api.funtranslations.com/translate/yoda.json?text={}".format(input)
        response = requests.get(api_url, headers=self.headers)

        if response.status_code == 200:
            return json.loads(response.content)
        else:
            return {
                "contents": {
                    "translated": 'Sorry we\'ve run out of API calls for funtranslations. Please try again in an hour :('}}

    def command(self, input):
        INVALID_COMMAND = "Command not recognized. Please try one of these: !! [about|help|yoda]"
        ABOUT = 'Welcome to "Not Discord"! My name is BimboBOT and I\'m here to help you out with different things. I\'m a bit of a bimbo (hence the name) but I try my best and that\'s what counts! '
        HELP = "All commands start with \"!!\" and are followed by the command and any parameters: !! <about|help|yoda [message]>"
        YODA_FAIL = "Please enter a word or phrase to translate. (Ex: !!yoda The quick brown fox jumped over the lazy dog)"
        
        COMMAND = input.lower()
        
        if COMMAND == "!! about" or COMMAND == "!!about":
            return ABOUT
        elif COMMAND == "!! help" or COMMAND == "!!help":
            return HELP
        elif COMMAND.startswith("!!yoda") or COMMAND.startswith("!! yoda"):
            if len(input[input.find("a") + 1:]) == 0:
                return YODA_FAIL
            else:
                return self.get_account_info(input[input.find("a") + 1 :])["contents"]["translated"]
        else:
            return INVALID_COMMAND
