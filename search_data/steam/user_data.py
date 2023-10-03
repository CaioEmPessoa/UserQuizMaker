import os
from steam import Steam
from decouple import config
from steam_maker import SteamMaker

class GetUserData():
    def __init__(self):
        super().__init__()
        # GET STEAM API KEY FROM .ENV
        KEY = config("STEAM_API_KEY")
        self.steam = Steam(KEY)
        self.qstn_dict = {
            "status":"undefined",
            "qstn_count": 0,
            "qstn_id": "undefined",
        }

    def basic_info(self, username):

        print("pesquisando por id...")
        user = self.steam.users.search_user(username)

        if user == "No match":
            print("nome de usuário '" + username + "' não válido! Tentando busca por id...")
            
            # Tenta pegar os detalhes do usuário pelo ID
            try:
                user = self.steam.users.get_user_details(username)
                print(user["player"]["personaname"] + " encontrado!")
            
            except:
                print("Id também não válido! checar informações.")
                return "O link provido não é de nenhum usuário."

        if user["player"]["communityvisibilitystate"] != 3:
            return "Perfil de usuário é privado!"
                
        try:
            USER_ID = user["player"]["steamid"]
            USER_DETAILS = self.steam.users.get_user_details(USER_ID)
            USER_FRIENDS = self.steam.users.get_user_friends_list(USER_ID)["friends"]
            USER_GAMES = self.steam.users.get_owned_games(USER_ID)["games"]
            status = "Dados coletados."
        except:
            return "Perfil de usuário é privado!"
    
        quiz_maker = SteamMaker()
        quiz_maker.make_qstn(self.qstn_dict)

# get money etc..