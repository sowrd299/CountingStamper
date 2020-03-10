from django.shortcuts import render
import json
import datetime
import pytz

from .models import Question, Player, Queue, Board, Cell, Guess
from .generation import generate_questions, generate_board
from .game import guess_answer, guess_not_on_board


'''
Renders the bingo gameboard
Takes the id of the player whose board to show
'''
def gameboard(request, board=None):

    question_available = board.current_question.get_time() < datetime.datetime.now(datetime.timezone.utc)

    # HANDLE ANY INCOMING ANSWERS

    if question_available: 
        if "no_answer" in request.POST and request.POST["no_answer"]:
            guess_not_on_board(board)
        elif "answer" in request.POST:
            try:
                guess_answer(board, Question.objects.get(answer = request.POST["answer"]))
            except Question.DoesNotExist as e:
                pass # TODO: post a message about how no guess was made


    # RENDER THE BOARD

    # get all the board data for the website
    # TODO: maybe put this in model?
    cells = []

    for i in range(5):

        row = []
        for j in range(5):
            cell = Cell.objects.get(board = board, x = i, y = j)
            wrong = Guess.objects.filter(board = board, question = board.current_question, answer = cell.question).count()
            row.append({
                "value" : cell.question.answer, # "{0},{1}".format(i,j),
                "stamp" : "HAVE" if cell.get_is_stamped() else ("WRONG" if wrong else "NONE")
            })

        cells.append(row)


    # setup the context and render it
    context = {
        "player_id" : board.player.id,
        "question_prompt" : board.current_question.question.question if question_available else "",
        "timer_prompt" : board.current_question.get_time().astimezone(pytz.timezone('US/Pacific')).strftime("%m/%d, %I:%M %p Pacific"),
        "cell_data" : json.dumps({"cells" : cells}),
        "score" : board.score
    }

    return render(request, 'bingo/gameboard.html', context)


'''
Prompts the user to log in
'''
def login(request):

    context = { "default_game_id" : "Larry Smith's Game" }

    return render(request, 'bingo/login.html', context)


'''
Actually logs in the user
'''
# TODO: this should probably be broken up into two functions
def do_login(request):

    # load or setup the game the user plays is
    game_id = request.POST['game_id']
    queue = None

    try:
        queue = Queue.objects.get(id = game_id)
    except Queue.DoesNotExist as e:
        if 'allow_new_game' in request.POST and request.POST['allow_new_game']:

            # all games count time from 11pm yesterday UTC
            now = datetime.datetime.now(datetime.timezone.utc)
            start_time = datetime.datetime(now.year, now.month, now.day) - datetime.timedelta(hours = 1)

            queue = generate_questions(game_id, start_time)

        else:
            return index(request)

    # load or setup the player
    player_id = request.POST['player_id']
    player = None
    
    try:
        player = Player.objects.get(id = player_id)

    except Player.DoesNotExist as e:
        # IF THE PLAYER DOESN'T EXIST, SET THEM UP
        player = Player(id = player_id)
        player.save()
        generate_board(player, queue)

    # setup the session and return
    request.session['player_id'] = player_id
    request.session['game_id'] = game_id
    return index(request)


'''
Logs out the current player
'''
def do_logout(request):
    request.session.flush()
    return index(request)


'''
Prompts the user to log in if they haven't yet.
Else displayer their bingo board
'''
def index(request):

    if 'player_id' in request.session and 'game_id' in request.session:
        try:
            player = Player.objects.get(id = request.session['player_id'])
            game = Queue.objects.get(id = request.session['game_id'])
            return gameboard(request, Board.objects.get(player = player, current_question__queue = game))
        except (Player.DoesNotExist, Queue.DoesNotExist, Board.DoesNotExist) as e:
            # if something goes wrong with login, just make them log in again
            return login(request)

    else:
        return login(request)