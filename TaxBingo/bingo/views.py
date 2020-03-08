from django.shortcuts import render

# Create your views here.

'''
Renders the bingo gameboard
Takes the id of the player whose board to show
'''
def gameboard(request, player_id = ""):

    context = dict()

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

    # TODO: handle new users
    request.session['player_id'] = request.POST['player_id'];

    return index(request)


'''
Prompts the user to log in if they haven't yet.
Else displayer their bingo board
'''
def index(request):

    if 'player_id' in request.session:
        return gameboard(request, request.session['player_id'])
    else:
        return login(request)