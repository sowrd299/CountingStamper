from django.shortcuts import render
import json

from .models import Player, Board, Cell
from .generation import generate_board

# Create your views here.

'''
Renders the bingo gameboard
Takes the id of the player whose board to show
'''
def gameboard(request, player=None, board=None):

    # get all the board data for the website
    # TODO: maybe put this in model?
    cells = []

    for i in range(5):

        row = []
        for j in range(5):
            cell = Cell.objects.get(board = board, x = i, y = j)
            row.append({
                "value" : cell.question.answer, # "{0},{1}".format(i,j),
                "stamp" : "HAVE" if cell.get_is_stamped() else "NONE"
            })

        cells.append(row)


    # setup the context and render it
    context = {
        "player_id" : player.id,
        "prompt" : "Some Kind of Tax!",
        "cell_data" : json.dumps({"cells" : cells})
    }

    return render(request, 'bingo/gameboard.html', context)


'''
Prompts the user to log in
'''
def login(request):

    context = dict()

    return render(request, 'bingo/login.html', context)


'''
Actually logs in the user
'''
def do_login(request):

    player_id = request.POST['player_id']
    player = None
    
    try:
        player = Player.objects.get(id = player_id)

    except Player.DoesNotExist as e:
        # IF THE PLAYER DOESN'T EXIST, SET THEM UP
        player = Player(id = player_id)
        player.save()
        generate_board(player)

    request.session['player_id'] = player_id
    return index(request)


'''
Prompts the user to log in if they haven't yet.
Else displayer their bingo board
'''
def index(request):

    if 'player_id' in request.session:
        try:
            player = Player.objects.get(id = request.session['player_id'])
            return gameboard(request, player, Board.objects.get(player = player))
        except (Player.DoesNotExist, Board.DoesNotExist) as e:
            # if something goes wrong with login, just make them log in again
            return login(request)
    else:
        return login(request)