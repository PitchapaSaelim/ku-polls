"""Test cases for ku-polls."""
import datetime

from django.test import TestCase

from django.utils import timezone

from django.urls import reverse

from django.contrib.auth.models import User

from polls.models import Question


def create_question(question_text, days):
    """
    Create a question with the given arguments.

        * question_text: the question text.
        * days: days offset to now.
    """
    time_of_pub_date = timezone.now() + datetime.timedelta(days=days)
    time_of_end_date = datetime.timedelta(
        days=30) + time_of_pub_date
    return Question.objects.create(question_text=question_text, pub_date=time_of_pub_date, end_date=time_of_end_date)


class QuestionDetailViewTests(TestCase):
    """Class that has tests for questions detail view."""

    def test_future_question(self):
        """The detail view of a question with a pub_date in the future returns a 404 not found."""
        future_question = create_question(
            question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """The detail view of a question with a pub_date in the past displays the question's text."""
        past_question = create_question(
            question_text='Past Question.', days=-5)
        User.objects.create_user(username='Pitchapa', password='@jeejee19')
        url = reverse('polls:detail', args=(past_question.id,))
        self.client.login(username='Pitchapa', password='@jeejee19')
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

