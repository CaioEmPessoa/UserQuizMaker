
def qstn_hours(self):
    question = f"Qual o jogo mais jogado de {self.user['player']['personaname']}?"
    print("pergunta: " + question)
    sort_by_hours = []


    # get the list sorted by most played games
    for game in self.games:
        sort_by_hours.append([game["playtime_forever"], game["name"]])

    sort_by_hours.sort(reverse=True)
    sort_by_hours = sort_by_hours[:4]

    games_name = []
    for game_name in sort_by_hours:
        games_name.append(game_name[1])

    # the first item of the list is the right
    return question, games_name, sort_by_hours[0][1]

def qstn_last_2weeks(self):
    question = f"Qual o jogo mais jogado nas últimas duas semanas por {self.user['player']['personaname']}?"
    print("pergunta: " + question)

    sort_by_2weeks = []

    # get the list sorted by most played games
    for game in self.games:
        try:
            sort_by_2weeks.append([game["playtime_2weeks"], game["name"]])
        except:
            pass
    
    while len(sort_by_2weeks) <= 4:
        sort_by_2weeks.append([0, random.choice(self.games)["name"]])

    sort_by_2weeks.sort(reverse=True)
    sort_by_2weeks = sort_by_2weeks[:4]

    games_name = []
    for game_name in sort_by_2weeks:
        games_name.append(game_name[1])

    # the first item of the list is the right
    return question, games_name, sort_by_2weeks[0][1]

def qstn_recent(self):
    question = f"Qual foi o último jogo jogado por {self.user['player']['personaname']}?"
    print("pergunta: " + question)

    sort_by_last = recent_games(self.user["player"]["profileurl"])
    sort_by_last.append(random.choice(self.games)["name"])

    # the first item of the list is the right
    return question, sort_by_last, sort_by_last[0]

    # the correct answer is the smallest number on "rtime_last_played", under the "games" list

def qstn_games_by_money(self):
    question = f"Qual o jogo mais caro da biblioteca de {self.user['player']['personaname']}?"
    print("pergunta: " + question)

    # creating lists
    sort_by_money = []
    id_list = []

    # get a list of all games id's
    for game in self.games:
        id_list.append(str(game["appid"]))

    # make a request abt all the prices of the games
    games_price_dict = self.steam.apps.get_app_details(",".join(id_list), "BR", "price_overview")
    # for each game
    for game in self.games:
        
        # It tryies to found the initial price of the game, in case it has somed discount
        try:
            game_price = games_price_dict[str(game["appid"])]["data"]["price_overview"]["initial_formatted"]
            
            # If the game isn't in promotion, it gets only the final price of it
            if game_price == 0 or game_price == "":
                game_price = games_price_dict[str(game["appid"])]["data"]["price_overview"]["final_formatted"]
                
        except:
            # If the game isn't on the dict, it is "free"
            game_price = "R$ 0"

        if game_price == "Free":
            game_price = "R$ 0"

        # The game price comes like "R$ xx,xx" so I had to convert to "xx.xx"
        sort_by_money.append([float(game_price[3:].replace(",", ".")), game["name"]])

    sort_by_money.sort(reverse=True)
    sort_by_money = sort_by_money[:4]

    games_name = []
    for game_name in sort_by_money:
        games_name.append(game_name[1])

    return question, games_name, sort_by_money[0][1]

def qstn_spent_money(self):
    question = f"Quanto {self.user['player']['personaname']} já gastou em sua biblioteca da steam? (sem contar descontos)"
    print("pergunta: " + question)

    id_list = []
    spent_money = []

    # get a list of all games id's
    for game in self.games:
        id_list.append(str(game["appid"]))

    # make a request abt all the prices of the games
    games_price_dict = self.steam.apps.get_app_details(",".join(id_list), "BR", "price_overview")
    # for each game
    for game in self.games:
        
        # It tryies to found the initial price of the game, in case it has somed discount
        try:
            game_price = games_price_dict[str(game["appid"])]["data"]["price_overview"]["initial_formatted"]
            
            # If the game isn't in promotion, it gets only the final price of it
            if game_price == 0 or game_price == "":
                game_price = games_price_dict[str(game["appid"])]["data"]["price_overview"]["final_formatted"]
                
        except:
            # If the game isn't on the dict, it is "free"
            game_price = "R$ 0"

        if game_price == "Free":
            game_price = "R$ 0"

        # The game price comes like "R$ xx,xx" so I had to convert to "xx.xx"
        spent_money.append([float(game_price[3:].replace(",", ".")), game["name"]])

    sum_total = 0
    for item in spent_money: 
        sum_total = item[0] + sum_total

    # arredonda o valor :)
    sum_total = round(sum_total)
    spent_range = list(range(round(sum_total/1.5), round(sum_total*1.5)))

    spent_optn = []
    spent_range.remove(sum_total)
    spent_optn.append(sum_total)
    for r in range(3): 
        sum_total = random.choice(spent_range)
        spent_range.remove(sum_total)
        spent_optn.append(sum_total)

    formatted_spent_optn = ["R$ " + str(item) for item in spent_optn]
    
    return question, formatted_spent_optn, formatted_spent_optn[0]

def qstn_achievements(self): # not working
    question = f"Qual o jogo com mais conquistas de {self.user['player']['personaname']}?"
    print("pergunta: " + question)


    # this code is unoptimized, it makes a request for each game, wich takes a lot of time.
    sort_by_achievements = []
    for game in self.games:
        try:
            # request to the API, for the current game of games list and the user's id
            game_achievements = self.steam.apps.get_user_achievements(self.id, game["appid"])["playerstats"]["achievements"]
            
            # sum 1 for each achievement achieved
            how_many = sum(1 for achievement in game_achievements if achievement["achieved"] == 1)
            sort_by_achievements.append([how_many, game["name"]])

        # if the game doesn't have achievements
        except:
            pass

    sort_by_achievements.sort(reverse=True)
    sort_by_achievements = sort_by_achievements[:4]


    games_name = []
    for game_name in sort_by_achievements:
        games_name.append(game_name[1])

    return question, games_name, sort_by_achievements[0][1]

def qstn_level(self): # steam level
    question = f"Qual level de {self.user['player']['personaname']}?"
    print("pergunta: " + question)

    level = self.steam.users.get_user_steam_level(self.id)["player_level"]

    level_range = list(range(round(level/1.5), round(level*1.5)))

    level_optn = []
    level_optn.append(level)
    level_range.remove(level)
    for r in range(3): 
        level = random.choice(level_range)
        level_range.remove(level)
        level_optn.append(level)
    
    return question, level_optn, level_optn[0]

def qstn_created(self):
    question = f"Quando {self.user['player']['personaname']} criou sua conta?"
    print("pergunta: " + question)

    # gets the unix time the user created its account and convert it to common years
    year_created = self.user["player"]["timecreated"]
    year_created = int(datetime.utcfromtimestamp(year_created).strftime('%Y'))

    year_range = list(range(year_created-3, year_created+3))

    year_optn = []
    year_optn.append(year_created)
    year_range.remove(year_created)
    for r in range(3): 
        year = random.choice(year_range)
        year_range.remove(year)
        year_optn.append(year)

    return question, year_optn, year_optn[0]
    
def qstn_old_friend(self):
    question = f"Quem é o amigo mais antigo de {self.user['player']['personaname']}?"
    print("pergunta: " + question)

    oldest_friends = []
    for friend in self.friends:
        oldest_friends.append([friend["friend_since"], friend["personaname"]])

    oldest_friends.sort()
    oldest_friends = oldest_friends[:4]

    friends_name = []
    for friend_name in oldest_friends:
        friends_name.append(friend_name[1])

    return question, friends_name, friends_name[0]
    
def qstn_friend_count(self):
    question = f"Quantos amigos {self.user['player']['personaname']} tem?"
    print("pergunta: " + question)

    friends_count = len(self.friends)

    friends_range = list(range(round(friends_count/1.3), round(friends_count*1.3)))

    friends_optn = []
    friends_optn.append(friends_count)
    friends_range.remove(friends_count)
    for r in range(3): 
        friends_count = random.choice(friends_range)
        friends_range.remove(friends_count)
        friends_optn.append(friends_count)

    return question, friends_optn, friends_optn[0]

def qstn_library(self):
    question = f"Quantos jogos {self.user['player']['personaname']} possui em sua biblioteca?"
    print("pergunta: " + question)

    library_count = len(self.games)

    library_range = list(range(round(library_count/1.5), round(library_count*1.5)))

    library_optn = []
    library_optn.append(library_count)
    library_range.remove(library_count)
    for r in range(3): 
        library_count = random.choice(library_range)
        library_range.remove(library_count)
        library_optn.append(library_count)

    # the first item of the list is the right
    return question, library_optn, library_optn[0]