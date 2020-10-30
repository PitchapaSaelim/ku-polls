"""Views for polls."""
import logging
import logging.config

from django.http import HttpResponseRedirect

from django.shortcuts import get_object_or_404, render, redirect

from django.urls import reverse

from django.views import generic

from django.utils import timezone

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed

from .models import Vote
from .models import Choice, Question

from django.dispatch import receiver

from .settings import LOGGING

logging.config.dictConfig(LOGGING)
log = logging.getLogger("polls")

def get_client_ip(request):
    """ Get the client's ip"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@receiver(user_logged_in)
def get_logging_user_logged_in(sender, request, user, **kwargs):
    log.info(f"IP address: {get_client_ip(request)} USER: {user.username} - has logged in.")

@receiver(user_logged_out)
def get_logging_user_logged_out(sender, request, user, **kwargs):
    log.info(f"IP address: {get_client_ip(request)} USER: {user.username} - has logged out.")

@receiver(user_login_failed)
def get_logging_user_login_failed(sender, request, credentials, **kwargs):
    log.warning(f"IP address: {get_client_ip(request)} USER: {request.POST['username']} - has failed to log in.")


class IndexView(generic.ListView):
    """Class that display index view."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions (not including those set to be published in the future)."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')


class DetailView(generic.DetailView):
    """Class that display detail view."""

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """Class that display results view."""

    model = Question
    template_name = 'polls/results.html'


@login_required
def vote(request, question_id):
    """Show results page when the web visitor vote."""
    user = request.user
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        Vote.objects.update_or_create(user=user, question=question, defaults={'choice': selected_choice})

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

@login_required
def vote_for_poll(request, pk):
    """Show error messages when the question not allowed to vote or render question detail page when it can."""
    question = get_object_or_404(Question, pk=pk)
    already_voted = False
    if not question.can_vote():
        messages.error(request, "Voting is not allowed.")
        return redirect('polls:index')
    try:
        previous_choice = Vote.objects.filter(user=request.user, question=question).first().choice.choice_text
        already_voted = True
    except (AttributeError):
        return render(request, 'polls/detail.html', {'question': question})
    log.info(f"IP address: {get_client_ip(request)} USER: {request.user.username} - has voted on question id: {pk}.")
    return render(request, 'polls/detail.html', {'question': question, 'previous_choice': previous_choice, 'already_voted': already_voted})

