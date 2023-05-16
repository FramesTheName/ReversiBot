# ReversiBot
This project contains all of the code for running a java server with two clients that all connect to engage in a game of reversi. The point of this project is to help develop a reversi AI bot that uses a minimax algorithm with alpha-beta pruning and heuristic evaluation functions.
## Main Components
### Java Server
The [java server](./Reversi/ReversiServer) is the main house for our reversi game. It can be compiled: 
<br> `javac *.java` <br>
Then the server can be run with java \[class name] \[Game length in mins]. For a ten minute game:
<br> `java Reversi 10` <br>
The java server creates a game board that can be used to monitor any game going on between two clients. The board shows all of the tiles currently placed along with the current total points of each side. It will only allow clients to enact fair moves sent in as tuple pair including a \(row, column).
### Human Client
The [human client](./Reversi/ReversiHuman) creates a human client for our reversi game. It can be compiled: 
<br> `javac *.java`. <br>
Then the server can be run with java \[class name] \[the server location] \[whether the client is player 1 or player 2]. For a human client running as player 1:
<br> `java Human localhost 1`. <br>
The human client also creates a reversi GUI for human users to input into.
### Java Random Client
The [java random client](./Reversi/ReversiRandom_Java)  creates a human client for our reversi game. It can be compiled: 
<br> `javac *.java`. <br>
Then the server can be run with java \[class name] \[the server location] \[whether the client is player 1 or player 2]. For a random client running as player 2:
<br>`java RandomGuy localhost 2`. <br>
### Original Python Client
The [original python client](./Reversi/OriginalReversiPythonBot) is a deprecated ai bot input built in Python 2. It is not recommended to use this bot, however, it was created by the original game programmer and can give insights into server client communication details.
To run this client as player 2:
<br> `python RandomGuy.py localhost 2`. <br>
### Current Python Client
The [current python client](./Reversi/CurrentReversiPythonBot) is our working AI bot. The main AI functions are held in the [reversi_bot.py](./Reversi/CurrentReversiPythonBot/reversi_bot.py) file. 
To run this client as player 2:
<br> `python reversi_python_client.py localhost 2`. <br>
The main AI functions are found in our bots make_move function. This function takes in the games current state[^1] and returns the AI's move in a tuple \(row, column).
[^1]: The parameter "state" is of type ReversiGameState and has two useful member variables. The first is "board", which is an 8x8 numpy array of 0s, 1s, and 2s. If a spot has a 0 that means it is unoccupied. If there is a 1 that means the spot has one of player 1's stones. If there is a 2 on the spot that means that spot has one of player 2's stones. The other useful member variable is "turn", which is 1 if it's player 1's turn and 2 if it's player 2's turn.
<br><br>ReversiGameState objects have a nice method called get_valid_moves. When you invoke it on a ReversiGameState object a list of valid moves for that state is returned in the form of a list of tuples.
## Run Files
Each run file follows the same structure of (Player 1)V(Player 2).bat *eg. HumanVRandom.bat*
For each file a java server is started on localhost and two clients are connected via sockets also running on localhost. [^2]
| Filename  | Players |
| ------------- | ------------- |
| HumanVBot.bat  | Starts a 10 minute reversi game with a Human as player 1 and Python AI Bot as player 2  |
| HumanVRandom.bat  | Starts a 10 minute reversi game with a Human as player 1 and Java Bot that plays makes moves randomly as player 2  |
| BotVHuman.bat  | Starts a 10 minute reversi game with a Python AI Bot connection as player 1 and Python AI Bot as player 2  |
| BotVRandom.bat  | Starts a 10 minute reversi game with a Python AI Bot as player 1 and Java Bot that plays makes moves randomly as player 2  |
| RandomVHuman.bat  | Starts a 10 minute reversi game with a Java Bot that plays makes moves randomly as player 1 and Human as player 2  |
| RandomVBot.bat  | Starts a 10 minute reversi game with a Java Bot that plays makes moves randomly as player 1 and Human as player 2  |
[^2]: All .bat files assume a developer has already compiled java programs in their directory. *eg. javac \*.java*
