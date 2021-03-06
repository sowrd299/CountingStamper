from django.db.models import F

from .models import Guess, Cell

'''
This file contains functions that implement game logic 
'''


'''
Returns the number of bingos on the given board
'''
def calc_bingos(board):

    r = 0
    cells = Cell.objects.filter(board = board)

    # find all the potenital bingo lines
    lines = [ cells.filter(x = i) for i in range(board.cols) ] # cols
    lines += [ cells.filter(y = i) for i in range(board.rows) ] # rows
    lines += [ cells.filter(x = F('y')) ] # back slash
    lines += [ cells.filter(x = board.cols - 1 - F('y')) ] # forward slash

    for line in lines:
        if all(map(lambda x : x.get_is_stamped(), line)):
            r += 1

    return r
    
'''
Re-calculates and returns the current score of the given board
Takes the number of bingos found from calc_bingos, for efficiency
'''
def calc_score(board, bingos = None):

    if bingos == None:
        bingos = calc_bingos(board)

    score = 0 # the base score

    for guess in Guess.objects.filter(board = board):
        # give points for correct guesses
        if guess.get_is_correct():
            score += 15
        # deduct points for wrong guesses
        else:
            score -= 5

    # score points for BINGO'S
    score += bingos * 200 # the score per bingo

    return score


'''
Calculates and cashes the score on the given board
    including the number of bingos they have
'''
def set_score(board):
    bingos = calc_bingos(board)
    board.bingos = bingos
    board.score = calc_score(board, bingos)
    board.save()


'''
Advances the the given board to the next question in the queue
'''
def advance_question(board):
    board.current_question = board.current_question.get_next_question()
    board.save()


'''
Handles a player making a guess at a question
Take the player's current board, and the answer they gave (as an entire question)
Returns if the player guessed correctly
'''
def guess_answer(board, question_answered):

    # add the guess to the record
    guess = Guess(board = board, question = board.current_question, answer = question_answered)
    guess.save()

    # IF THE PLAYER ANSWERED CORRECTLY
    if guess.get_is_correct():
        for cell in Cell.objects.filter(board = board, question = question_answered):
            # stamp all the relevant cells
            cell.is_stamped = True
            cell.save()

        advance_question(board)

    # update the cashes score and return
    set_score(board)
    return guess.get_is_correct()

'''
Handles a player guessing that nothing on their board matches their question
Returns if false if the question is on the board
'''
def guess_not_on_board(board):

    r = True

    for cell in Cell.objects.filter(board = board):
        if cell.question == board.current_question.question:
            r = False
            break

    advance_question(board)

    return r