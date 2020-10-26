import json,requests,random,os
from os.path import join, dirname
from dotenv import load_dotenv

class chatBot:
    headers = {'Content-Type': 'application/json'}

    def get_account_info(self, input):
        api_url = 'https://api.funtranslations.com/translate/yoda.json?text={}'.format(input)
        response = requests.get(api_url, headers=self.headers)

        if response.status_code == 200:
            return json.loads(response.content)
        else:
            return None

    
    def command(self, input):
        if(input.lower().startswith("!! about") or input.lower().startswith("!!about")):
            return ("Welcome to \"Not Discord\"! " +
                    "My name is BimboBOT and I'm here to help you out with different things." +
                    " Just type [!!help] to learn more about what I can do!")
        elif(input.lower().startswith("!! help") or input.lower().startswith("!!help")):
            return "All commands start with !! and are followed by the command with or without a space: !! about: Tells you about me! I'm not very interesting though :(, !! yoda [message] : Translates your message to yoda!"
        elif (input.startswith("!!yoda") or input.startswith("!! yoda")):
            return self.get_account_info(input[input.find('a') + 1:])['contents']['translated']
        else:
            return "Command not recognized. Please try one of these: !! [about|help|yoda]"
