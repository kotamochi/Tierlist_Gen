from flask import Flask, render_template, request, jsonify
import json
import rank
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_rank', methods=['GET'])
def start_game():
    #jsからの引数を取得
    name = request.args.get("name")
    level = request.args.get("level")

    #User情報を保管するフォルダを作成
    try:
        os.mkdir(f"./data/temp/{level}")
    except FileExistsError: #既にある時は飛ばす
        pass
    
    #ユーザーデータを読み込み
    try:
        with open("./data/user.json", mode="r", encoding="utf-8") as f:
            Users = json.load(f)
    except json.JSONDecodeError: #ファイルが空の時
        Users = {}
    #同じユーザーが直近に同じレベルで行ってた時は、途中から再開する
    if name in Users and level in Users[f"{name}"]["level"] and 4 != Users[f"{name}"]["counter"]:
        #途中再開フラグを立てる
        is_continue = True
        pass
    else:
        #途中再開フラグを設定
        is_continue = False
        #ユーザーデータ作成
        user = {"level":level, "counter":0}
        Users[f"{name}"] = user
    
        with open("./data/user.json", mode="w", encoding="utf-8") as f:
            json.dump(Users, f, indent=4, ensure_ascii=False)
            
        #データの一時ファイルを作成
        rank.create_data(name, level)

    #楽曲を2曲取得
    name1, img1, name2, img2 = rank.get_music(name, level)

    response_data = {"continue":is_continue,
                     "img1":img1,
                     "name1":name1,
                     "img2":img2,
                     "name2":name2
                     }

    return json.dumps(response_data)

@app.route('/choice', methods=['GET'])
def choice_music():
    #jsからの引数を取得
    name = request.args.get("name")
    level = request.args.get("level")
    s_music = request.args.get("serect_music")
    n_music = request.args.get("non_serect_music")
    point = int(request.args.get("point"))
    
    #ポイント処理とゲームの進行度確認
    flg = rank.set_point(name, level, s_music, n_music, point)
    
    #一連のゲームが終了したか
    if flg:
        #ランキング形式の画像を作成
        response_data = response_data = {"game_flg":False}
        
    else:
        #楽曲を2曲取得
        name1, img1, name2, img2 = rank.get_music(name, level)
        
        #レスポンスデータを作成
        response_data = {"game_flg":True,
                         "img1":img1,
                         "name1":name1,
                         "img2":img2,
                         "name2":name2
                         }

    return json.dumps(response_data)

@app.route('/result', methods=['GET'])
def get_result():
    #jsからの引数を取得
    name = request.args.get("name")
    level = request.args.get("level")
    #Tierリストのデータを取得
    response_data = rank.show_result(name, level)

    return json.dumps(response_data)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)