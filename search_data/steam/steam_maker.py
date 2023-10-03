import os
import json
import random
import string

import user_data

class SteamMaker():
    def save_quiz(self):
        user_data_location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "/../user_data"

        # lowercase letters + numbers
        options = string.ascii_lowercase + string.digits
        link_id = ''.join(random.choice(options) for i in range(6))
        
        quizes_list = os.listdir(user_data_location)
        
        if link_id in quizes_list:
            self.save_quiz()
            return
        
        self.qstn_dict["qstn_id"] = link_id
        self.qstn_dict["status"] = "Perguntas Salvas!"
        
        with open(f"{user_data_location}/{link_id}.json", "w") as save_file:
            json.dump(self.qstn_dict, save_file, indent=4)

        print("Perguntas Salvas!")

    def make_qstn(self, qstn_dict):
        self.qstn_dict = qstn_dict

        questions_list = [
            self.qstn_created, self.qstn_hours, self.qstn_old_friend, 
            self.qstn_friend_count, self.qstn_recent, self.qstn_games_by_money, self.qstn_level, 
            self.qstn_last_2weeks, self.qstn_library, self.qstn_spent_money]

        # questions_list = [self.qstn_spent_money]

        can_choose = list(range(len(questions_list)))

        for question in range(self.ammount):
            choosed = random.choice(can_choose)
            can_choose.remove(choosed)

            question, options, answer = questions_list[choosed]()

            random.shuffle(options)

            self.qstn_dict["qstn_count"] += 1

            question_info = {
                "Question " + str(self.qstn_dict["qstn_count"]): {
                    "question": question,
                    "options": options,
                    "answer": answer,
                },
            }

            self.qstn_dict.update(question_info)

            print("Questão feita!")
            print(json.dumps(self.qstn_dict, indent=4))

        self.save_quiz()
        self.qstn_dict["status"] = "Quiz Criado!"
        return self.qstn_dict