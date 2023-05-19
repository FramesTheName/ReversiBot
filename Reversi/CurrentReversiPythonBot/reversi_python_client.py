import reversi
import sys

if __name__ == '__main__':
    server_address = sys.argv[1]
    bot_move_number = int(sys.argv[2])
    print(server_address)
    print(bot_move_number)
    #server_address = "localhost"
    #bot_move_number = 2
    reversi_game = reversi.ReversiGame(server_address, bot_move_number)
    reversi_game.play()
