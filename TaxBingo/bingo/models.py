from django.db import models

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
'''
class Queue(models.Model):

    id = models.CharField(primary_key=True, max_length=200)

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

    def get_next_question(self):
        return QuestionInQueue.objects.get(queue = self.queue, index = self.index + 1)

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