from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    pub_user = models.CharField(max_length=200)
    #add result table later
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    total_bet = models.IntegerField(default=0)
    chance_to_win = models.IntegerField(default=0)
    #votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

class Bet(models.Model):
    choice = models.ManyToManyField(Choice)
    bet_user = models.CharField(max_length=200)
    bet_amount = models.IntegerField(default=0)
    def __str__(self):
        return self.bet_user + ": " + str(self.bet_amount)