from channels.generic.websockets import JsonWebsocketConsumer
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
import logging
from otree.api import models
import time
from try1.forms import TaskForm, Task2Form
from try1.models import Player, Task, Task2, Constants

logger = logging.getLogger(__name__)


class TaskTracker(JsonWebsocketConsumer):

    def clean_kwargs(self):
        self.player_pk = self.kwargs['player_pk']
        #self.test = self.kwargs['test']

    def get_player(self):
        self.clean_kwargs()
        return Player.objects.get(pk=self.player_pk)

    def process_task(self, content):
        """We get the answer from a client, obtain task id, get it from db, and update it with actual answer."""
        task_id = int(content['task_id'])
        answer = content['answer']
        task = Task.objects.get(pk=task_id)
        task.answer = answer
        #self.clean_kwargs()
        #task.test = self.test
        task.save()

    def feed_task(self):
        """
        We get the task, if it is available, and feed it to the form template. If it is not available we
        send an 'over' signal which forwards player to Results page.
        """
        player = self.get_player()
        task = player.get_or_create_task()
        if player.total_attempts < player.max_quiz:
            task.answered = True
            form_block = mark_safe(render_to_string('try1/includes/q_block.html', {
                'form': self.form(task=task).as_table(),
                'player': player,
            }))

            self.send({'form_block': form_block})
        else:
            self.send({'over': True})
            player.qs_not_available = True
            player.save()

    def connect(self, message, **kwargs):
        """When a new client is connected we find the task and feed it back to him"""
        logger.info('client connected....')
        self.feed_task()

    def receive(self, content, **kwargs):
        """When the new message is receved, we register it (updating current task). and feed him/her back a new task."""
        self.process_task(content)
        self.feed_task()


class Task1Tracker(TaskTracker):
    url_pattern = (r'^/task1/(?P<player_pk>[0-9]+)$')
    form = TaskForm

    def feed_task(self):
        """
        We get the task, if it is available, and feed it to the form template. If it is not available we
        send an 'over' signal which forwards player to Results page.
        """
        player = self.get_player()
        task = player.get_or_create_task()
        if player.total_attempts < player.max_quiz:
            task.answered = True
            form_block = mark_safe(render_to_string('try1/includes/q_block.html', {
                'form': TaskForm(task=task).as_table(),
                'player': player,
            }))

            self.send({'form_block': form_block})
        else:
            self.send({'over': True})
            player.qs_not_available = True
            player.save()


class Task2Tracker(TaskTracker):
    url_pattern = (r'^/task2/(?P<player_pk>[0-9]+)$')
    form = Task2Form

    def process_task(self, content):
        """We get the answer from a client, obtain task id, get it from db, and update it with actual answer."""
        #task_id = int(content['task_id'])
        answer = content['answer']
        task = Task2.objects.latest()
        task.answer = answer
        #self.clean_kwargs()
        #task.test = self.test
        task.save()

    def feed_task(self):
        """
        We get the task, if it is available, and feed it to the form template. If it is not available we
        send an 'over' signal which forwards player to Results page.
        """
        player = self.get_player()
        task2 = player.gen_task2()
        #task.answered = True
        form_block = mark_safe(render_to_string('try1/includes/q2_block.html', {
            'form': Task2Form(task=task2).as_table(),
            'player': player,
        }))

        self.send({'form_block': form_block})

