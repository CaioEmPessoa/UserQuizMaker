from flask import Flask, jsonify, request
from waitress import serve

from steam import steam_user

# STARTS FLASK APP
app = Flask(__name__)

# STEAM ROUTES <------------------------------------------------------------------<

@app.route("/steam_app/test")
def server_test():
    return ("sucesso!")

@app.route("/steam_app/create")
def search_steam_data():
    username = request.args.get('username', type = str)
    ammount = request.args.get('ammount', default = '10', type = int)
    
    data = jsonify("request pra user_data")
    return data

@app.route("/steam_app/read")
def open_created(user_id):
    try:
        with open(f"{Start.user_data_location}/{user_id}.json", "r") as load_file:
            data = json.load(load_file)
            data["status"] = "Quiz Carregado!"
            return jsonify(data)
    except:
        return(jsonify({"status":"Esse quiz não existe! Verifique seu código."}))

# >------------------------------------------------------------------> END STEAM ROUTES 


@app.after_request
def header_apply(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] ="True"
    return response

if __name__ == "__main__":
    app.add_url_rule

    app.run(debug=True)

