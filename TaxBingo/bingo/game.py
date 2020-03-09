from .models import Cell

'''
This file contains functions that implement game logic 
'''


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

    # IF THE PLAYER ANSWERED CORRECTLY
    if question_answered == board.current_question.question:
        for cell in Cell.objects.filter(board = board, question = question_answered):
            # stamp all the relevant cells
            cell.is_stamped = True
            cell.save()

        advance_question(board)

        return True

    # IF THE PLAYER ANSWERED INCORRECTLY
    else:
        return False

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