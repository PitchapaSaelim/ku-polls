"""Test cases for ku-polls."""
import datetime

from django.test import TestCase

from django.utils import timezone

from polls.models import Question

class QuestionModelTests(TestCase):
    """Class that has tests for questions model."""

    def test_was_published_recently_with_future_question(self):
        """was_published_recently() returns False for questions whose pub_date is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """was_published_recently() returns False for questions whose pub_date is older than 1 day."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """was_published_recently() returns True for questions whose pub_date is within the last day."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_current_date_is_on_publication_date(self):
        """is_published() returns True if current date is on question’s publication date."""
        time = timezone.now()
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.is_published(), True)

    def test_is_published_with_current_date_is_after_publication_date(self):
        """is_published() returns True if current date is after question’s publication date."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.is_published(), True)

    def test_is_published_with_current_date_is_before_publication_date(self):
        """is_published() returns False if current date is before question’s publication date."""
        time = timezone.now() + datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.is_published(), False)

    def test_can_vote_with_current_date_is_before_end_date(self):
        """can_vote() returns True if voting is currently allowed for this question before the end date."""
        time = timezone.now() + datetime.timedelta(hours=23, minutes=59, seconds=59)
        time_of_pub_date = timezone.now() - datetime.timedelta(days=5)
        recent_question = Question(pub_date=time_of_pub_date, end_date=time)
        self.assertIs(recent_question.can_vote(), True)

    def test_can_vote_with_current_date_is_after_end_date(self):
        """can_vote() returns False if voting is currently allowed for this question after the end date."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        time_of_pub_date = timezone.now() - datetime.timedelta(days=5)
        recent_question = Question(pub_date=time_of_pub_date, end_date=time)
        self.assertIs(recent_question.can_vote(), False)
