NBA Management System

This web application is designed to manage various aspects of NBA teams, players, games, standings, news, and more. It utilizes Flask for the backend and MySQL for data storage.

Prerequisites

•	HTML: A basic understanding of HTML for structuring web pages.
•	CSS: Familiarity with CSS for styling web pages.
•	Bootstrap: Familiarity with bootstrap for styling web pages.
•	JQuery: Basic knowledge of JQuery for enhancing the user interface.
•	Flask: Flask is used as the backend framework for this project. 

Features

Team Management:
•	View a list of NBA teams.
•	Add, update, and delete team information.
Player Management:
•	View a list of NBA players.
•	Add, update, and delete player information.
Game Management:
•	View a list of NBA games.
•	Add, update, and delete game information.
Standings:
•	Track team standings, wins, losses, win percentage, and other related statistics.
News Management:
•	Display NBA-related news with date, title, and content.
Schedule:
•	Manage the schedule, including date, time, broadcaster, and participating teams.
Achievements:
•	Record and view team achievements.



File Structure

app.py: Flask application for handling routes and database interactions.
templates: HTML templates for rendering web pages.
static: CSS and JavaScript files.

Database Schema

The application operates on the following database schema:
•	Players (PlayerID, Name_FirstName, Name_LastName, Position, TeamID, Age, BirthDate, PlayerHeight, PlayerWeight, Country, Experience)
•	Team (TeamID, TeamName, HeadCoach, City, GeneralManager, AssistantCoach, Founded)
•	Arena (ArenaID, ArenaName, Location_City, Location_State, Opened, Capacity, TeamID)
•	Games (GamesID, Date, Winner, Arena, Score, HomeTeam, AwayTeam, TeamID)
•	Standings (SID, Wins, Loses, Win%, Road, Last10, Season, Conf, Division, TeamID)
•	News (NewsID, Date, Title, Content)
•	Relates (PlayerID, NewsID)
•	Schedule (ScheduleID, Date, Time, Broadcaster, HomeTeam, AwayTeam, ArenaID)
•	Achievements (AID, AType, TeamID)
•	Achievements_YearsWon(AID, YearsWon)

Database Setup

•	Create a new MySQL database named nba (or choose a different name).
•	Update the database connection details in app.py to match your MySQL setup.
•	Import the provided SQL script (nba.sql) into your MySQL database to create the necessary tables.

Run the Flask Application

•	Make sure all dependencies are installed as mentioned in the requirements.txt file.
•	Navigate to the project root folder and Start the Flask development server with the following command:
     Flask run
•	This command runs the Flask application, and you should see output indicating that the development server is running.

Access the Application

•	Open your web browser and go to http://localhost:5000. The web application should be accessible at this URL.
•	Note: By default, the Flask development server runs on port 5000. If you want to use a different port, you can specify it when running the python app.py command, like python app.py -p 8080 for port 8080.

Interact with the Application

•	Use your web browser to navigate through the different sections of the application. You can perform CRUD (Create, Read, Update, Delete) operations on NBA teams, players, and games.

•	Team Management: View, Add, Edit, Delete Teams
•	Player Management: View, Add, Edit, Delete Players
•	Game Management: View, Add, Edit, Delete Games
•	Team Analytics: Gives information about team and players metrics and administration information
•	News Management: View NBA News 
•	Game Schedule: View Game Schedule

Shutdown the Application

•	To stop the Flask development server, press Ctrl + C in the terminal where the server is running. This will gracefully shut down the server.
