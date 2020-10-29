import json, requests, random, os
from os.path import join, dirname
from dotenv import load_dotenv


class chatBot:
    dotenv_path = join(dirname(__file__), 'sql.env')
    load_dotenv(dotenv_path)
    RAPID_API_KEY = os.environ['RAPID_API_KEY']
    
    def yoda(self, input):
        strIn = ""
        for word in input:
            strIn += (" " + word)
        headers = {"Content-Type": "application/json"}
        api_url = "https://api.funtranslations.com/translate/yoda.json?text={}".format(strIn)
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            return json.loads(response.content)
        else:
            return {
                "contents": {
                    "translated": 'Sorry we\'ve run out of API calls for funtranslations. Please try again in an hour :('}}
    
    def joke(self):
        url = "https://rapidapi.p.rapidapi.com/v1/joke"

        headers = {
            'x-rapidapi-host': "joke3.p.rapidapi.com",
            'x-rapidapi-key': "{}".format(self.RAPID_API_KEY)
        }

        response = requests.request("GET", url, headers=headers)
        json_body = response.json()
        joke =  json.dumps(json_body["content"]).replace("\"","").replace("\\", "")
        
        return joke

    def bible(self, params):
        url = "https://ajith-holy-bible.p.rapidapi.com/GetVerseOfaChapter"
        
        querystring = {
            "Verse": params[2],
            "Book": params[0],
            "chapter": params[1]
        }
        headers = {
            'x-rapidapi-host': "ajith-holy-bible.p.rapidapi.com",
            'x-rapidapi-key': "{}".format(self.RAPID_API_KEY)
        }
        
        response = requests.request("GET", url, headers=headers, params=querystring).json()
        book = json.dumps(response['Book'])
        b = (book[1].upper() + book[2:].lower())
        cv = (json.dumps(response['Chapter']) + ":" + json.dumps(response['Verse']))
        text = json.dumps(response['Output'])
        
        verse = (b + " " + cv + " - " + text + " - BBE").replace("\"", "")
        return verse
        
    def command(self, input):
        INVALID_COMMAND = "Command not recognized. Type \'!!help\' to see the commands"
        ABOUT = 'Welcome to "Not Discord"! My name is BimboBOT and I\'m here to help you out with different things. I\'m a bit of a bimbo (hence the name) but I try my best and that\'s what counts! '
        HELP = "All commands start with \"!!\" and are followed by the command and any parameters: !! < about || help || joke || yoda [message] || bible [book] [chapter] [verse] >"
        YODA_FAIL = "Please enter a word or phrase to translate. (Ex: !!yoda The quick brown fox jumped over the lazy dog)"
        
        BIBLE_TOO_MANY = "You\'ve entered too many parameters! The command\'s parameters are as follows: !!bible book chapter verse (Ex: !!bible Luke 1 1)"
        BIBLE_TOO_FEW = "You\'ve entered too few parameters! The command\'s parameters are as follows: !!bible book chapter verse (Ex: !!bible Luke 1 1)"
        
        CMD_PAR = input.split()
        print("\nCMD_PAR: ", CMD_PAR)
        if CMD_PAR[0] == "!!":
            COMMAND = CMD_PAR[1].lower()
            print(COMMAND)
            if len(CMD_PAR) > 2:
                PARAMS = CMD_PAR[2:]
            else:
                PARAMS = ""
        else:
            COMMAND = CMD_PAR[0][2:].lower()
            print("\nCOMMAND: " + COMMAND)
            if len(CMD_PAR) > 1:
                PARAMS = CMD_PAR[1:]
            else:
                PARAMS = ""
        
        if COMMAND == "about":
            if len(PARAMS) > 0:
                return "The command \'about\' doesn\'t need any parameters"
            return ABOUT
        elif COMMAND == "help":
            if len(PARAMS) > 1:
                return "The \'help\' command can take one parameter, a command, or it can take no parameters"
            elif len(PARAMS) == 1:
                if PARAMS[0].lower() == 'about':
                    return "!!about: Tells you about BimboBOT!"
                elif PARAMS[0].lower() == 'joke':
                    return "!!joke: Returns a random joke."
                elif PARAMS[0].lower() == 'help':
                    return "!!help <command>: You're using it right now, I don\'t think you need my help. :p"
                elif PARAMS[0].lower() == 'yoda':
                    return "!!yoda <message>: Translates your inputted message into yoda language!"
                elif PARAMS[0].lower() == 'bible':
                    return "!!bible <book> <chapter> <verse>: Displays the Bible verse inputted. :)"
                return "The command you need help for doesn\'t exist!"
            return HELP
        elif COMMAND == "joke":
            if len(PARAMS) > 0:
                return "The \'joke\' command doesn't take any parameters. Try again with \'!!joke\'"
            return self.joke()
        elif COMMAND == "bible":
            if len(PARAMS) > 3:
                return BIBLE_TOO_MANY
            elif len(PARAMS) < 3:
                return BIBLE_TOO_FEW
            return self.bible(PARAMS)
        elif COMMAND == "yoda":
            if len(PARAMS) == 0:
                return YODA_FAIL
            else:
                return self.yoda(PARAMS)["contents"]["translated"]
        else:
            return INVALID_COMMAND
