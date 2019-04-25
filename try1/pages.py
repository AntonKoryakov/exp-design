from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants, Player, Task
import random


class Instructions(Page):
    """Introduction and task 1 representation"""

    def before_next_page(self):
        self.player.max_quiz = self.session.config['max_quiz']

    def is_displayed(self):
        return self.round_number == 1


class Instr2(Page):
    """Overview of task 2"""

    def before_next_page(self):
        if self.player.total_attempts < self.player.max_quiz:
            for i in range(1, 1 + self.player.max_quiz - self.player.total_attempts):
                task = self.player.get_or_create_task()
                task_obj = Task.objects.get(id=task.id)
                task_obj.answered = True

    def is_displayed(self):
        return self.round_number == 1


class Inter(Page):
    """Introduction and task 1 representation"""

    def is_displayed(self):
        return self.round_number == 2


class Inter2(Page):
    """Overview of task 2"""

    def before_next_page(self):
        if self.player.total_attempts < self.player.max_quiz:
            for i in range(1, 1 + self.player.max_quiz - self.player.total_attempts):
                task = self.player.get_or_create_task()
                task_obj = Task.objects.get(id=task.id)
                task_obj.answered = True

    def is_displayed(self):
        return self.round_number == 2


class Values(Page):
    """Include form about comparative value of the tasks"""
    form_model = 'player'

    form_fields = ['value1',
                   'value2',
                   'diff1',
                   'diff2',
                   'succ_rate1',
                   'succ_rate2',
                   'pref_task']

    def is_displayed(self):
        return self.round_number == 2

    # def before_next_page(self):
    #    if self.round_number == 1:
    #        self.participant.vars['corr1'] = self.player.correct_answers
    #        self.participant.vars['corr2'] = self.player.correct_answers2


class GroupWaitPage(WaitPage):
    wait_for_all_groups = True

    def is_displayed(self) -> bool:
        return self.round_number > 2

    def after_all_players_arrive(self):
        self.subsession.do_my_shuffle()
    #    Or we can set up group matrix for each round therefor we'll have groups already
    #    So here we set the roles


class StartWaitPage(WaitPage):
    def is_displayed(self) -> bool:
        return self.round_number > 2

    def after_all_players_arrive(self):
        for p in self.group.get_players():
            partner = p.get_partner()
            selected_task = random.randint(0, 1)
            if selected_task == 0:
                if partner.in_round(2).correct_answers > p.in_round(2).correct_answers:
                    p.role = 'follower'
                elif partner.in_round(2).correct_answers == p.in_round(2).correct_answers:
                    p.role = 'leader'
                    partner.role = 'follower'
                else:
                    p.role = 'leader'
            else:
                if partner.in_round(2).correct_answers2 > p.in_round(2).correct_answers2:
                    p.role = 'follower'
                elif partner.in_round(2).correct_answers2 == p.in_round(2).correct_answers2:
                    p.role = 'leader'
                    partner.role = 'follower'
                else:
                    p.role = 'leader'
        for p in self.group.get_players():
            print(p.role)


class Instructions2(Page):

    def is_displayed(self):
        check = bool((self.round_number > 2) and (self.round_number < 5))
        return check


class Instructions3(Page):

    def is_displayed(self):
        check = bool((self.round_number > 4) and (self.round_number < 7))
        return check


class Instructions4(Page):
    def is_displayed(self):
        check = bool(self.round_number > 6)
        return check


class LeaderChoice(Page):
    """Include form about task choice"""
    form_model = 'group'

    form_fields = ['choice']

    def is_displayed(self):
        check = bool((self.player.role == 'leader') and (self.round_number < 5) and (self.round_number > 2))
        return check


class LeaderChoice2(Page):
    """Include form about task choice in second treatment"""
    form_model = 'group'

    form_fields = ['choice',
                   'mech2']

    def is_displayed(self):
        return (self.player.role == 'leader') and (self.round_number > 4) and (self.round_number < 7)


class LeaderChoice3(Page):
    """Include form about task choice"""
    form_model = 'group'

    form_fields = ['choice',
                   'mech3']

    def is_displayed(self):
        return (self.player.role == 'leader') and (self.round_number > 6)


class FollowerChoice(Page):
    """Include form about task choice"""
    form_model = 'group'

    form_fields = ['choice_foll']

    def is_displayed(self):
        check = bool((self.player.role == 'follower') and (self.round_number > 2))
        return check


class TaskWaitPage(WaitPage):
    def is_displayed(self):
        return self.round_number > 2

    def after_all_players_arrive(self):
        if self.round_number > 4:
            if self.round_number < 7:
                if self.group.mech2 == 'Реализация выбора распределения партнёра':
                    if self.group.choice_foll == 'Квиз':
                        self.group.choice = 'Копирование текста'
                    else:
                        self.group.choice = 'Квиз'
            else:
                if self.group.mech3 == 'Реализация выбора распределения партнёра':
                    if self.group.choice_foll == 'Квиз':
                        self.group.choice = 'Копирование текста'
                    else:
                        self.group.choice = 'Квиз'
                elif self.group.mech3 == 'Демократия':
                    if self.group.choice == self.group.choice_foll:
                        self.group.choice = random.choice(['Квиз', 'Копирование текста'])
        for p in self.group.get_players():
            if self.group.choice == 'Квиз':
                if p.role == 'leader':
                    p.real_task = 'Квиз'
                else:
                    p.real_task = 'Копирование текста'
            else:
                if p.role == 'leader':
                    p.real_task = 'Копирование текста'
                else:
                    p.real_task = 'Квиз'
            print(p.role)


# class ShuffleWaitPage(WaitPage):
#     """Reshuffle the groups after the round has ended"""
#     wait_for_all_groups = True
#
#     def after_all_players_arrive(self):
#         self.subsession.do_my_shuffle()


# class ResultsWaitPage(WaitPage):
#     def after_all_players_arrive(self):
#         self.group.set_payoffs()


class TaskTrial(Page):
    template_name = 'try1/Task.html'
    timeout_seconds = 10

    def before_next_page(self):
        self.player.correct_num = self.player.correct_answers
        self.player.attempt_num = self.player.total_attempts
        if self.player.total_attempts < self.player.max_quiz:
            for i in range(1, 1 + self.player.max_quiz - self.player.total_attempts):
                task = self.player.get_or_create_task()
                task_obj = Task.objects.get(id=task.id)
                task_obj.answered = True

    def vars_for_template(self) -> dict:
        return {'channel_stem': 'task1', 'test': 1}

    def is_displayed(self) -> bool:
        # return not self.player.qs_not_available
        return self.player.round_number == 1


class Task2Trial(Page):
    timer_text = "Time left to complete the task:"
    timeout_seconds = 10

    template_name = 'try1/Task2.html'

    def before_next_page(self):
        self.player.correct_num2 = self.player.correct_answers2

    def vars_for_template(self) -> dict:
        return {'channel_stem': 'task2', 'test': 1}

    def is_displayed(self) -> bool:
        # return not self.player.qs_not_available
        return self.player.round_number == 1


class Task1(Page):
    template_name = 'try1/Task1.html'
    timer_text = "Время, оставшееся на выполнение задания:"
    timeout_seconds = 10

    def vars_for_template(self) -> dict:
        return {'channel_stem': 'task1', 'test': 1}

    def before_next_page(self):
        self.player.correct_num = self.player.correct_answers
        self.player.attempt_num = self.player.total_attempts
        for t in self.player.tasks.all().filter(answer__isnull=False):
            self.player.dump_tasks += str(t.answer) + ';'
            if t.answer == t.question.solution:
                self.player.dump_tasks_corr += '1;'
            else:
                self.player.dump_tasks_corr += '0;'

        if self.player.total_attempts < self.player.max_quiz:
            for i in range(1, 1 + self.player.max_quiz - self.player.total_attempts):
                task = self.player.get_or_create_task()
                task_obj = Task.objects.get(id=task.id)
                task_obj.answered = True

    def is_displayed(self) -> bool:
        # return not self.player.qs_not_available
        return self.player.round_number == 2


class Task2(Page):
    timer_text = "Время, оставшееся на выполнение задания:"
    timeout_seconds = 20

    template_name = 'try1/Task2.html'

    def before_next_page(self):
        self.player.correct_num2 = self.player.correct_answers2


    def vars_for_template(self) -> dict:
        return {'channel_stem': 'task2', 'test': 1}

    def is_displayed(self) -> bool:
        # return not self.player.qs_not_available
        return self.player.round_number == 2


class TaskReal1(Page):
    timer_text = "Time left to complete the task:"
    timeout_seconds = 15

    def before_next_page(self):
        self.player.correct_num = self.player.correct_answers
        self.player.attempt_num = self.player.total_attempts

        if self.player.total_attempts < self.player.max_quiz:
            for i in range(1, 1 + self.player.max_quiz - self.player.total_attempts):
                task = self.player.get_or_create_task()
                task_obj = Task.objects.get(id=task.id)
                task_obj.answered = True



    def vars_for_template(self) -> dict:
        return {'channel_stem': 'task1', 'test': 0}

    def is_displayed(self):
        check = bool((self.player.round_number > 2) and (self.player.real_task == 'Квиз'))
        return check


class TaskReal2(Page):
    timer_text = "Time left to complete the task:"
    timeout_seconds = 20

    def before_next_page(self):
        self.player.correct_num2 = self.player.correct_answers2

    def vars_for_template(self) -> dict:
        return {'channel_stem': 'task2', 'test': 0}

    def is_displayed(self):
        check = bool((self.player.round_number > 2) and (self.player.real_task == 'Копирование текста'))
        return check


class Results(Page):
    pass


class FinalResults(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class Questionary(Page):
    form_model = "player"

    form_fields = ["sex",
                   "age"]

    def is_displayed(self) -> bool:
        return self.round_number == 2


page_sequence = [
    # Instructions,
    # TaskTrial,
    # Instr2,
    # Task2Trial,
    Inter,
    Task1,
    Inter2,
    Task2,
    Values,
    # GroupWaitPage,
    # StartWaitPage,
    # Instructions2,
    # Instructions3,
    # Instructions4,
    # LeaderChoice,
    # LeaderChoice2,
    # LeaderChoice3,
    # FollowerChoice,
    # TaskWaitPage,
    # TaskReal1,
    # TaskReal2,
    # ReaultsWaitPage,
    # Results,
    # GroupWaitPage,
    # ShuffleWaitPage,
    # FinalResults,
    Questionary,
]
