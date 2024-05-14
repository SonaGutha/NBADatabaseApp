from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL



app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = ''
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'nba'

mysql = MySQL(app)


@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("select * from news")
    news = cur.fetchall()
    cur.execute("select firstname,lastname from players")
    players = cur.fetchall()
    cur.close()
    print(len(players))
    print(players[200])
    players = [players[200][0]+players[200][1],players[143][0]+players[143][1],players[69][0]+players[69][1],players[220][0]+players[220][1],players[17][0]+players[17][1],players[4][0]+players[4][1]]
    news_articles = [
    {"title": news[2][2], "image_url": "static/images/11.jpg.webp"},
    {"title": news[1][2], "image_url": "static/images/12.jpg.webp"},
    {"title": news[19][2], "image_url": "static/images/13.jpg.webp"},
    {"title": news[10][2], "image_url": "static/images/13.jpg.webp"}
    ]
    return render_template('index.html',news=news_articles,players = players)

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        cur = mysql.connection.cursor()
        checkUsername = cur.execute("SELECT username FROM users WHERE username='{0}'".format(username))
        cur.close()
        if checkUsername == 0:
            msg = "username doesn't exist"
            return render_template("login.html",msg = msg)
        else:
            cur = mysql.connection.cursor()
            cur.execute("select password from users where username='{0}'".format(username))
            data = cur.fetchall()
            cur.close()
            print(password)
            print(data[0][0])
            if password == data[0][0]:
                options=['Teams','Players','Games']
                return render_template('admin.html',options = options)
            else:
                msg = "wrong password"
                return render_template("login.html",msg = msg)

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        cur = mysql.connection.cursor()
        checkUsername = cur.execute("SELECT username FROM users WHERE username='{0}'".format(username))
        cur.close()
        if checkUsername == 0:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users (username,password,email) values ('{0}','{1}','{2}');".format(username,password,email))
            mysql.connection.commit()
            msg = "Registered successfully, login to proceed"
            cur.close()
            return render_template('login.html',msg = msg)
        else:
            msg = "username already exists"
            return render_template('register.html',msg = msg)

@app.route('/process',methods=['POST'])
def process():
    option = request.form.get('options')
    if option == "Teams":
        return redirect(url_for('crudteam'))
    if option == "Players":
        return redirect(url_for('crudplayer'))
    if option == "Games":
        return redirect(url_for('crudgame'))

@app.route('/players')
def players_list():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM players")
    players = cur.fetchall()
    cur.close()
    return render_template('players.html', players=players)

@app.route('/teams')
def team_list():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM team")
    teams = cur.fetchall()
    cur.close()
    return render_template('team.html', teams=teams)

@app.route('/games')
def games_list():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM games")
    games = cur.fetchall()
    cur.close()
    return render_template('games.html', games=games)

@app.route('/standings')
def standings_list():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Standings")
    standings = cur.fetchall()
    cur.close()
    return render_template('standings.html', standings=standings)

@app.route('/news')
def news_list():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM news")
    news = cur.fetchall()
    cur.close()
    return render_template('news.html', news=news)

@app.route('/schedules')
def schedules():
    cur = mysql.connection.cursor()
    cur.execute("select * from  schedule")
    schedule = cur.fetchall()
    cur.close()
    return render_template('schedule.html', schedule=schedule)

# *************************************
# ANALYTICS
# *************************************

@app.route('/teamwins')
def teamwins_list():
    cur = mysql.connection.cursor()
    cur.execute("SELECT IFNULL(teamName,'N/A') AS teamName, IFNULL(season,'N/A') AS season , IFNULL(city,'N/A') AS city, Sum(wins) as totalwins FROM standings,team WHERE standings.teamId = team.teamId GROUP BY teamName,season,city WITH ROLLUP")
    teamwins = cur.fetchall()
    cur.close()
    return render_template('teamwins.html', teamwins=teamwins)

@app.route('/playersexp')
def playersexp():
    cur = mysql.connection.cursor()
    cur.execute("select Team.teamId,playerID, firstname, lastname,age, country, experience, ROUND(CUME_DIST() OVER ( PARTITION BY Team.teamID ORDER BY experience), 2) as 'cume_dist',ROUND(ROUND(CUME_DIST() OVER (PARTITION BY Team.teamID ORDER BY experience), 2)*100,2) as 'cume_dist (%age)' FROM Players,Team where Players.teamId=Team.teamId;")
    playersexp = cur.fetchall()
    cur.close()
    return render_template('playersexp.html', playersexp=playersexp)

@app.route('/teamavg')
def teamavg():
    cur = mysql.connection.cursor()
    cur.execute("WITH TeamAvgHeight AS (SELECT TeamID, AVG(PlayerHeight) AS AvgHeight, AVG(age) AS AvgAge FROM Players GROUP BY TeamID) SELECT Team.TeamName, TA.AvgHeight, TA.AvgAge FROM Team JOIN TeamAvgHeight TA ON Team.TeamID = TA.TeamID ORDER BY AvgHeight ,AvgAge ;")
    teamavg = cur.fetchall()
    cur.close()
    return render_template('teamavg.html', teamavg=teamavg)


@app.route('/teamachievements')
def teamach():
    teams = ['WAS','UTA', 'TOR','SAS','SAC','POR','PHX','PHI','ORL','OKC','NYK','NOP','MIN','MIL','MIA','MEM','LAL','LAC','IND','HOU','GSW','DET','DEN','DAL','CLE','CHI','CHA','BOS','BKN','ATL']
    achievements=['Coach of the Year', 'Hustle Award', 'Sixth Man of the Year','Executive of the Year','Clutch Player of the Year','Most Improved Player','MVP','NBA championship trophy','Defensive Player of the Year']
    return render_template('teamach.html', teams=teams, achievements=achievements)

@app.route('/teamachievementsresult', methods=['POST'])
def teamachievementsresult():
    selected_option1 = request.form.get('achievements')
    selected_option2 = request.form.get('teams')

    cur = mysql.connection.cursor()
    try:
        cur.execute("select A.TeamId,A.Atype as AchievementType,TeamName,Headcoach,City,Generalmanager,Assistantcoach,Founded from Achievements AS A JOIN Team AS T ON A.TeamID = T.TeamID where Atype=%s and A.TeamID in (select A.teamid from Achievements AS A JOIN Team AS T ON A.TeamID = T.TeamID where A.TEAMID=%s);", (selected_option1,selected_option2))
        teamachievements = cur.fetchall()
        cur.close()
    except Exception as e:
        flash(str(e))
    return render_template('teamachievements.html', teamachievements=teamachievements)

@app.route('/teamstandings')
def teamstandings():
    year = ['2023','2022', '2021','2020', '2019','2018','2017','2016']
    return render_template('teamstanding.html', year1=year, year2=year)

@app.route('/teamstandingsresult', methods=['POST'])
def teamstandingsresult():
    selected_option1 = request.form.get('year1')
    selected_option2 = request.form.get('year2')

    cur = mysql.connection.cursor()
    try:
        cur.execute("(select * from Standings as TS, Team as T where TS.TeamID=T.TeamID and TS.season=%s) union (select * from Standings as TS, Team as T where TS.TeamID=T.TeamID and TS.season=%s)", (selected_option1,selected_option2))
        teamstandingsresult = cur.fetchall()
        cur.close()
    except Exception as e:
        print(e)
    return render_template('teamstandingsresult.html', teamstandingsresult=teamstandingsresult)

@app.route('/teamcomp')
def teamcomp():
   
    teams = ['WAS','UTA','TOR','SAS','SAC','POR','PHX','PHI','ORL','OKC','NYK','NOP','MIN','MIL','MIA','MEM','LAL','LAC','IND','HOU','GSW','DET','DEN','DAL','CLE','CHI','CHA','BOS','BKN','ATL']
    return render_template('teamcomp.html', teams=teams)

@app.route('/result', methods=['POST'])
def result():
    selected_option = request.form.get('teams')
    cur = mysql.connection.cursor()
    try:
        cur.execute("select teamid,wins, ROUND(win_percentage*100,2) as win_percent,Road, Last10,season, conf,division from standings where wins > all (select wins from standings where teamid='{0}')".format(selected_option))
        teamwincomparision = cur.fetchall()
        cur.close()
    except Exception as e:
        print(e)
    return render_template('teamwincomparision.html', teamwincomparision=teamwincomparision)

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

# *************************************************************
#               CRUD OPERATIONS FOR ADMIN TAB
# *************************************************************


# CRUD FOR TEAMS TABLE

@app.route('/admin/teams')
def crudteam():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM Team")
    data = cur.fetchall()
    cur.close()
    return render_template('editteam.html', teams=data )

@app.route('/admin/team/insert', methods = ['POST'])
def insertteam():

    if request.method == "POST":
        teamid = request.form['teamid']
        teamname = request.form['teamname']
        headcoach = request.form['headcoach']
        city = request.form['city']
        gm = request.form['generalmanager']
        ac = request.form['assistantcoach']
        founded = request.form['founded']
        cur = mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO Team (teamid, teamname, headcoach, city, generalmanager, assistantcoach,founded) VALUES (%s, %s, %s, %s, %s, %s, %s)", (teamid, teamname,headcoach, city, gm, ac, founded))
            mysql.connection.commit()
            flash("Data Inserted Successfully")
        except Exception as e:
            flash(str(e))
        
        return redirect(url_for('crudteam'))

@app.route('/admin/team/delete/<string:id_data>', methods = ['GET'])
def deleteteam(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Team WHERE teamid=%s", (id_data,))
    mysql.connection.commit()
    flash("Record Has Been Deleted Successfully")
    return redirect(url_for('crudteam'))

@app.route('/admin/team/update',methods=['POST','GET'])
def updateteam():

    if request.method == 'POST':
        teamid = request.form['teamid']
        teamname = request.form['teamname']
        headcoach = request.form['headcoach']
        city = request.form['city']
        gm = request.form['generalmanager']
        ac = request.form['assistantcoach']
        founded = request.form['founded']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE Team
               SET teamname=%s, headcoach=%s, city=%s, generalmanager=%s, assistantcoach=%s, founded=%s 
               WHERE teamid=%s
            """,  (teamname,headcoach, city, gm, ac, founded,teamid))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('crudteam'))


# CRUD FOR GAMES

@app.route('/admin/games')
def crudgame():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Games")
    games = cur.fetchall()
    cur.close()
    return render_template('editgame.html', games=games)


@app.route('/admin/game/insert', methods=['POST'])
def insertgame():
    if request.method == "POST":
        games_id = request.form['games_id']
        date = request.form['date']
        winner = request.form['winner']
        arena = request.form['arena']
        score = request.form['score']
        home_team = request.form['home_team']
        away_team = request.form['away_team']
        team_id = request.form['team_id']

        cur = mysql.connection.cursor()
        try:
            cur.execute("""
                INSERT INTO Games (GamesID, Date, Winner, Arena, Score, HomeTeam, AwayTeam, TeamID)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (games_id, date, winner, arena, score, home_team, away_team, team_id))
            mysql.connection.commit()
            flash("Game Data Inserted Successfully")
        except Exception as e:
            flash(str(e))

        return redirect(url_for('crudgame'))


@app.route('/admin/game/delete/<string:games_id>', methods=['GET'])
def deletegame(games_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Games WHERE GamesID=%s", (games_id,))
    mysql.connection.commit()
    flash("Game Record Has Been Deleted Successfully")
    return redirect(url_for('crudgame'))


@app.route('/admin/game/update', methods=['POST', 'GET'])
def updategame():
    if request.method == 'POST':
        games_id = request.form['games_id']
        date = request.form['date']
        winner = request.form['winner']
        arena = request.form['arena']
        score = request.form['score']
        home_team = request.form['home_team']
        away_team = request.form['away_team']
        team_id = request.form['team_id']

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE Games
            SET Date=%s, Winner=%s, Arena=%s, Score=%s, HomeTeam=%s, AwayTeam=%s, TeamID=%s
            WHERE GamesID=%s
        """, (date, winner, arena, score, home_team, away_team, team_id, games_id))
        flash("Game Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('crudgame'))

# CRUD FOR PLAYERS

@app.route('/admin/players')
def crudplayer():
    cur_player = mysql.connection.cursor()
    cur_player.execute("SELECT * FROM Players")
    players = cur_player.fetchall()
    cur_player.close()
    return render_template('editplayer.html',players=players)


@app.route('/admin/player/insert', methods=['POST'])
def insertplayer():
    if request.method == "POST":
        player_id = request.form['player_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        position = request.form['position']
        team_id = request.form['team_id']
        age = request.form['age']
        birth_date = request.form['birth_date']
        height = request.form['height']
        weight = request.form['weight']
        country = request.form['country']
        experience = request.form['experience']

        cur = mysql.connection.cursor()
        try:
            cur.execute("""
                INSERT INTO Players (PlayerID, FirstName, LastName, Position, TeamID, Age, BirthDate, PlayerHeight, PlayerWeight, Country, Experience)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (player_id, first_name, last_name, position, team_id, age, birth_date, height, weight, country, experience))
            mysql.connection.commit()
            flash("Player Data Inserted Successfully")
        except Exception as e:
            flash(str(e))

        return redirect(url_for('crudplayer'))


@app.route('/admin/player/delete/<string:player_id>', methods=['GET'])
def deleteplayer(player_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Players WHERE PlayerID=%s", (player_id,))
    mysql.connection.commit()
    flash("Player Record Has Been Deleted Successfully")
    return redirect(url_for('crudplayer'))


@app.route('/admin/player/update', methods=['POST', 'GET'])
def updateplayer():
    if request.method == 'POST':
        player_id = request.form['player_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        position = request.form['position']
        team_id = request.form['team_id']
        age = request.form['age']
        birth_date = request.form['birth_date']
        height = request.form['height']
        weight = request.form['weight']
        country = request.form['country']
        experience = request.form['experience']

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE Players
            SET FirstName=%s, LastName=%s, Position=%s, TeamID=%s, Age=%s, BirthDate=%s,
            PlayerHeight=%s, PlayerWeight=%s, Country=%s, Experience=%s
            WHERE PlayerID=%s
        """, (first_name, last_name, position, team_id, age, birth_date, height, weight, country, experience, player_id))
        flash("Player Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('crudplayer'))


if __name__ == "__main__":
    app.run(debug=True)
