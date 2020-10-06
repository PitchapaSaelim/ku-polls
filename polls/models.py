"""Models for polls."""
import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    """Class named Question for model."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('ending date')

    def __str__(self):
        """Return the question text."""
        return self.question_text

    def was_published_recently(self):
        """Return when the question is recently published."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def is_published(self):
        """Return true if current date is on or after question’s publication date."""
        now = timezone.now()
        if now >= self.pub_date:
            return True
        return False

    def can_vote(self):
        """Return true if voting is currently allowed for this question."""
        now = timezone.now()
        if now <= self.end_date and now >= self.pub_date:
            return True
        return False


class Choice(models.Model):
    """Class named Choice for model."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Return the choice text."""
        return self.choice_text
