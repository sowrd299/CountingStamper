from django.db import models
import datetime

# Create your models here.

'''
Represents players playing in the game
'''
class Player(models.Model):

    id = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return self.id


'''
Represents a question that can be asked of the players
'''
class Question(models.Model):

    question = models.CharField(max_length = 200)
    answer = models.CharField(max_length = 200)

    assign_randomly = models.BooleanField(default = True)

    def __str__(self):
        return "{0}: {1}".format(self.question, self.answer)


'''
Represents a list of questions for the players to go through
Those questions can be tied to specific times,
    at even wait intervals from a specific start time
'''
class Queue(models.Model):

    id = models.CharField(primary_key=True, max_length=200)

    # the timer
    start_time = models.DateTimeField(default = datetime.datetime(1970,1,1))
    wait_per_question = models.DurationField(default = datetime.timedelta(hours = 12))

    def get_first_question(self):
        return QuestionInQueue.objects.get(queue = self, index = 0)

    def __str__(self):
        return self.id#"Queue {0}".format(self.id)


'''
Represents the position of a question in a queue of questions
'''
class QuestionInQueue(models.Model):

    question = models.ForeignKey('Question', on_delete=models.CASCADE)

    queue = models.ForeignKey('Queue', on_delete=models.CASCADE)
    index = models.IntegerField()

    '''
    Returns the amount of time left on the question's timer
    '''
    def get_time_remaining(self):
        return self.queue.start_time + self.queue.wait_per_question * self.index - datetime.datetime.now()

    '''
    Returns the question at the next index
    Returns itself if there is none
    '''
    def get_next_question(self):
        try:
            return QuestionInQueue.objects.get(queue = self.queue, index = self.index + 1)
        except QuestionInQueue.DoesNotExist:
            # TODO: do something more robust
            return self

    def __str__(self):
        return "{0} ({1}, {2})".format(self.queue, self.index, self.question)


'''
Represents a bingo boards of a single user
Also represents the player's larger state in that same game
Allows a player to hypothetically have multiple boards
'''
class Board(models.Model):

    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    current_question = models.ForeignKey('QuestionInQueue', on_delete=models.CASCADE)

    # the size of the board
    rows = models.IntegerField(default=5) # the number of rows of the board
    cols = models.IntegerField(default=5) # the number of cols of the field

    # the cashed game score value of this board
    score = models.IntegerField(default=10)

    def __str__(self):
        return "{0}'s Game Board".format(self.player)


'''
Represents a cell on a player's board
'''
class Cell(models.Model):

    board = models.ForeignKey('Board', on_delete=models.CASCADE)

    x = models.IntegerField()
    y = models.IntegerField()

    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    is_stamped = models.BooleanField(default = False)

    def get_is_stamped(self):
        return self.is_stamped

    def __str__(self):
        return "{0} ({1},{2})".format(self.board, self.x, self.y)


'''
Represents a guess at the answer to a question made by a player
Takes the board it was guessed on, the current question at the time of the guess,
    and the answer guessed
'''
class Guess(models.Model):

    board = models.ForeignKey('Board', on_delete=models.CASCADE)
    question = models.ForeignKey('QuestionInQueue', on_delete=models.CASCADE)
    answer = models.ForeignKey('Question', on_delete=models.CASCADE)

    def get_is_correct(self):
        return self.answer == self.question.question

    def __str__(self):
        return "{0} ({1},{2})".format(self.board, self.question, self.anser)