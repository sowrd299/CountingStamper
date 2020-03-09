from .models import Board, Cell, Question


'''
Creates a brand new queue of questions
'''
def generate_questions(init_length = 100):

    queue = Queue()
    queue.save()

    for i in range(init_length):

        # GENERATES TESTING QUESTIONS
        question = Question( question = "This is tax-related topic {0}!".format(i), answer = "A{0}".format(i) )
        question.save()

        q_in_q = QuestionInQueue( question = question, queue = queue, index = i)
        q_in_q.save()

    return queue

'''
Creates a brand new board, associated with the given player
Also takes the queue of questions the board should use
'''
def generate_board(player, queue, rows = 5, cols = 5):

    board = Board(player = player, queue = queue)
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
                question = Question.objects.get(answer = "A0") # TODO: this is a placeholder question

            cell = Cell(board = board, x = i, y = j, question = question, is_stamped = is_stamped)
            cell.save()

    return board