from .models import Board, Cell, Question

'''
Creates a brand new board, associated with the given player
'''
def generate_board(player, rows = 5, cols = 5):

    board = Board(player = player)
    board.save()

    for i in range(cols):
        for j in range(rows):

            question = None
            is_stamped = False

            if i == cols//2 and j == rows//2:
                # ADD THE FREE SPACE
                question = Question.objects.get(answer = "FREE")
                is_stamped = True
            else:
                question = Question.objects.get(answer = "Q3") # TODO: this is a placeholder question

            cell = Cell(board = board, x = i, y = j, question = question, is_stamped = is_stamped)
            cell.save()

    return board