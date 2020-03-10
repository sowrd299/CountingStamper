import random

from .models import Queue, Board, Cell, Question, QuestionInQueue


'''
This file contains methods useful for setting up the game
'''


'''
Creates a brand new queue of questions
'''
def generate_questions(game_id, start_time = None, init_length = 60):

    queue_args = {"id" : game_id}
    if start_time != None:
        queue_args["start_time"] = start_time
    queue = Queue(**queue_args)
    queue.save()

    for i in range(init_length):

        # GENERATES TESTING QUESTIONS
        answer = "A{0}".format(i)
        question = None

        try:
            question = Question.objects.get(answer=answer)
        except Question.DoesNotExist as e:
            question = Question( question = "Tax-related topic #{0}".format(i),  answer=answer)
            question.save()

        q_in_q = QuestionInQueue( question = question, queue = queue, index = i)
        q_in_q.save()

    return queue

'''
Creates a brand new board, associated with the given player
Also takes the queue of questions the board should use
'''
def generate_board(player, queue, rows = 5, cols = 5, free_id = "FREE"):

    board = Board(player = player, current_question = queue.get_first_question(), rows = rows, cols = cols)
    board.save()

    for i in range(cols):
        for j in range(rows):

            question = None
            is_stamped = False

            # ADD THE FREE SPACE
            if i == cols//2 and j == rows//2:
                try:
                    question = Question.objects.get(answer = free_id)
                except Question.DoesNotExist: # create the free space if it doesn't exist
                    question = Question(question = "FREE SPACE", answer = free_id, assign_randomly=False)
                    question.save()
                is_stamped = True

            # ADD NORMAL SPACES
            else:
                question = Question.objects.get(answer = "A{0}".format(random.randrange(60))) # TODO: this is a placeholder question

            cell = Cell(board = board, x = i, y = j, question = question, is_stamped = is_stamped)
            cell.save()

    return board