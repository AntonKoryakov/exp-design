import csv
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from django.db import models as djmodels
from django.db.models import F
import json
import random
import string

author = "Philip Chapkovski, chapkovski@gmail.com"

doc = """
Feeding the stream of questions to a player till he dies...

"""


class Constants(BaseConstants):
    name_in_url = 'try1'
    players_per_group = 2
    num_rounds = 8
    # qs = pd.read_csv(r'try1\quiz1.csv', sep=',', encoding='utf8')
    with open('try1/quiz2.csv', encoding='windows-1251') as f:
        qs = list(csv.DictReader(f, delimiter=';', skipinitialspace=True, escapechar='\\'))
    #The matrix for set_matrix
    r1_10 = [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]
    r2_10 = [[4, 5], [6, 9], [8, 2], [7, 1], [10, 3]]
    r3_10 = [[3, 8], [2, 6], [10, 5], [9, 7], [4, 1]]
    r4_10 = [[9, 2], [4, 6], [1, 3], [7, 5], [8, 10]]
    r5_10 = [[5, 3], [9, 4], [2, 10], [1, 8], [7, 6]]
    r6_10 = [[2, 4], [10, 6], [7, 3], [8, 9], [1, 5]]

    r1_12 = [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12]]
    r2_12 = [[1, 6], [8, 4], [5, 10], [3, 9], [7, 12], [11, 2]]
    r3_12 = [[1, 10], [3, 8], [7, 4], [2, 9], [11, 6], [12, 5]]
    r4_12 = [[3, 1], [11, 5], [6, 10], [8, 12], [9, 4], [2, 7]]
    r5_12 = [[2, 12], [1, 9], [3, 6], [4, 5], [10, 8], [11, 7]]
    r6_12 = [[1, 4], [10, 7], [3, 5], [12, 9], [6, 2], [11, 8]]

    r1_14 = [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12], [13, 14]]
    r2_14 = [[3, 2], [12, 8], [6, 4], [10, 1], [7, 11], [13, 9], [14, 5]]
    r3_14 = [[14, 12], [1, 8], [5, 11], [7, 6], [4, 2], [10, 13], [9, 3]]
    r4_14 = [[14, 3], [11, 2], [4, 7], [13, 8], [9, 5], [1, 6], [12, 10]]
    r5_14 = [[12, 5], [14, 8], [2, 7], [1, 3], [13, 6], [4, 9], [10, 11]]
    r6_14 = [[12, 3], [14, 9], [11, 1], [2, 10], [5, 7], [13, 4], [8, 6]]

    r1_16 = [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12], [13, 14], [15, 16]]
    r2_16 = [[4, 11], [1, 3], [2, 16], [13, 7], [14, 9], [10, 15], [8, 6], [12, 5]]
    r3_16 = [[4, 6], [11, 2], [9, 8], [14, 7], [10, 1], [16, 13], [12, 3], [15, 5]]
    r4_16 = [[14, 6], [7, 3], [15, 2], [9, 13], [4, 8], [11, 16], [1, 12], [5, 10]]
    r5_16 = [[3, 11], [12, 14], [7, 1], [10, 16], [15, 8], [9, 2], [5, 4], [13, 6]]
    r6_16 = [[2, 4], [1, 6], [15, 9], [14, 11], [7, 5], [12, 8], [10, 13], [3, 16]]


class Subsession(BaseSubsession):
    def creating_session(self):
        # for index, row in Constants.qs.iterrows():
        #     choices = [row['choice1'], row['choice2'], row['choice3'], row['choice4']]
        #     Q.objects.get_or_create(id=row['id'], text=row['question'],
        #                             chs=json.dumps(choices),
        #                             solution=row['solution'],
        #                             open=row['qtype'])
        for q in Constants.qs:
            choices = [q.get(f'choice{i}') for i in range(1, 5)]

            Q.objects.get_or_create(id=q['id'], defaults={'text': q['question'],
                                                          'chs': json.dumps(choices),
                                                          'solution': q['solution'],
                                                          'open': q['qtype']})

    def do_my_shuffle(self):
        if self.session.num_participants == 10:
            r1 = Constants.r1_10
            r2 = Constants.r2_10
            r3 = Constants.r3_10
            r4 = Constants.r4_10
            r5 = Constants.r5_10
            r6 = Constants.r6_10
        elif self.session.num_participants == 12:
            r1 = Constants.r1_12
            r2 = Constants.r2_12
            r3 = Constants.r3_12
            r4 = Constants.r4_12
            r5 = Constants.r5_12
            r6 = Constants.r6_12
        elif self.session.num_participants == 14:
            r1 = Constants.r1_14
            r2 = Constants.r2_14
            r3 = Constants.r3_14
            r4 = Constants.r4_14
            r5 = Constants.r5_14
            r6 = Constants.r6_14
        elif self.session.num_participants == 16:
            r1 = Constants.r1_16
            r2 = Constants.r2_16
            r3 = Constants.r3_16
            r4 = Constants.r4_16
            r5 = Constants.r5_16
            r6 = Constants.r6_16
        if (self.session.num_participants > 9) and (self.session.num_participants < 17):
            if self.round_number < 4:
                self.set_group_matrix(self.r1)
            elif self.round_number == 4:
                self.set_group_matrix(self.r2)
            elif self.round_number == 5:
                self.set_group_matrix(self.r3)
            elif self.round_number == 6:
                self.set_group_matrix(self.r4)
            elif self.round_number == 7:
                self.set_group_matrix(self.r5)
            elif self.round_number == 8:
                self.set_group_matrix(self.r6)
        else:
            self.group_randomly()

class Group(BaseGroup):
    choice = models.StringField(choices=['Квиз', 'Копирование текста'], widget=widgets.RadioSelectHorizontal)

    choice_foll = models.StringField(choices=['Квиз', 'Копирование текста'], widget=widgets.RadioSelectHorizontal)

    mech2 = models.StringField(choices=['Выбор задания самостоятельно', 'Реализация выбора распределения партнёра'],
                               widget=widgets.RadioSelect)
    mech3 = models.StringField(choices=['Выбор задания самостоятельно', 'Реализация выбора распределения партнёра',
                                        'Демократия'],
                               widget=widgets.RadioSelect)


class Player(BasePlayer):
    # For initial testing
    sex = models.StringField(label="Ваш пол:", choices=['М', 'Ж'],
                             widget=widgets.RadioSelectHorizontal)
    age = models.IntegerField(label="Сколько Вам лет?")
    #Main part
    role = models.StringField()
    real_task = models.StringField()
    max_quiz = models.IntegerField(initial=24)
    leader = models.BooleanField(initial=False)
    current_task = models.IntegerField(initial=0)
    counter = models.IntegerField(initial=0)
    dump_tasks = models.LongStringField(initial='')
    dump_tasks_corr = models.LongStringField(initial='')
    correct_num = models.IntegerField(initial=0)
    correct_num2 = models.IntegerField(initial=0)

    attempt_num = models.IntegerField(initial=0)

    value1 = models.IntegerField(label='Оцените, насколько Вам понравилось первое задание?',
                                 choices=[1, 2, 3, 4, 5], widget=widgets.RadioSelectHorizontal)
    value2 = models.IntegerField(label='Оцените, насколько Вам понравилось второе задание?',
                                 choices=[1, 2, 3, 4, 5], widget=widgets.RadioSelectHorizontal)

    diff1 = models.IntegerField(label='Оцените, насколько трудным Вам показалось первое задание?',
                                choices=[1, 2, 3, 4, 5], widget=widgets.RadioSelectHorizontal)

    diff2 = models.IntegerField(label='Оцените, насколько трудным Вам показалось второе задание?',
                                choices=[1, 2, 3, 4, 5], widget=widgets.RadioSelectHorizontal)

    succ_rate1 = models.IntegerField(label='Оцените, насколько успешно, Вы справились с квизом по сравнению с другими участниками '
                                         '(выберите, в какой квинтиль распределения по выполненным заданиям Вы попали)?',
                                         choices=[20, 40, 60, 80, 100], widget=widgets.RadioSelectHorizontal)
    succ_rate2 = models.IntegerField(label='Оцените, насколько успешно, Вы справились с квизом по сравнению с другими участниками '
                                         '(выберите, в какой квинтиль распределения по выполненным заданиям Вы попали)?',
                                         choices=[20, 40, 60, 80, 100], widget=widgets.RadioSelectHorizontal)

    pref_task = models.StringField(label='Если бы Вам пришлось выбирать, какое из заданий делать на протяжении '
                                         '30 минут, то что бы Вы выбрали?',
                                   choices=['Викторина(квиз)', 'Перепечатывание текста'], widget = widgets.RadioSelectHorizontal)

    qs_not_available = models.BooleanField(initial=False)  # When this is true the user asnwers all questions correctly.


    @property
    def available_qs(self):
        """Here we check for all questions that already correctly answered by a user."""
        # answered_qs_ids = self.tasks.filter(answered=False).values_list('question__id', flat=True)
        q = Q.objects
        for p in self.in_all_rounds():
            answered_qs_ids = p.tasks.filter(answered=False).values_list('question__id', flat=True)
            q = q.exclude(id__in=answered_qs_ids)
        return q
        # Q.objects.exclude(id__in=answered_qs_ids)

    def get_random_question(self):
        """We pick a random question from the list of available ones.
        NB: If the list of questions  is huge it should be done differently. """
        # Get next question from prepared randomized file
        available_qs = self.available_qs
        if available_qs.exists():
            return available_qs.first()
            # return random.choice(available_qs)

    def get_or_create_task(self):
        """We check whether there is unfinished task, if there is we return it. If there is not, we create a new one."""
        unfinished_tasks = self.tasks.filter(answer__isnull=True)
        if unfinished_tasks.exists():
            return unfinished_tasks.latest()
        else:
            q = self.get_random_question()
            if q:
                task = self.tasks.create(question=q)
                return task

    """For second task"""

    def gen_task2(self):
        l1 = random.randint(4, 7)
        w1 = ''.join(random.choice(string.ascii_lowercase) for x in range(l1))
        l2 = random.randint(2, 3)
        w2 = ''.join(random.choice(string.ascii_lowercase) for x in range(l2))
        l3 = random.randint(4, 8)
        w3 = ''.join(random.choice(string.ascii_lowercase) for x in range(l3))
        l4 = random.randint(2, 3)
        w4 = ''.join(random.choice(string.ascii_lowercase) for x in range(l4))
        newstr = w1 + ' ' + w2 + ' ' + w3 + ' ' + w4

        q, _ = Q2.objects.get_or_create(text=newstr, solution=newstr)

        task2 = self.tasks2.create(question=q)

        return task2

    @property
    def correct_answers_trial(self):
        """We get all tasks associated to the current user, to which he provided correct answers."""
        return self.tasks.filter(answer=F('question__solution')).count()

    @property
    def correct_answers2_trial(self):
        """We get all tasks associated to the current user, to which he provided correct answers."""
        return self.tasks2.count() - 1

    @property
    def total_attempts(self):
        """We get all tasks associated to the current user, to which he provided any answers."""
        return self.tasks.filter(answer__isnull=False).count()

    @property
    def correct_answers(self):
        """We get all tasks associated to the current user, to which he provided correct answers."""
        return self.tasks.filter(answer=F('question__solution')).count()

    @property
    def correct_answers2(self):
        """We get all tasks associated to the current user, to which he provided correct answers."""
        return self.tasks2.count() - 1

    @property
    def correct_answersR(self):
        """We get all tasks associated to the current user, to which he provided correct answers."""
        # print(self.tasks.filter(answer=F('question__solution')))
        return self.tasks.filter(answer=F('question__solution')).count()

    @property
    def correct_answers2R(self):
        """We get all tasks associated to the current user, to which he provided correct answers."""
        return self.tasks2.count()

    def get_partner(self):
        return self.get_others_in_group()[0]

class Q(djmodels.Model):
    """This model just to keep the track of all avaialble questions and their correct answers."""
    text = models.StringField()
    chs = models.StringField()
    solution = models.StringField()
    open = models.BooleanField()

    def __str__(self):
        """We do not need this but it is convenient to have when we need to print the object (mostly for debugging."""
        return f'{self.text}: {self.chs}, correct answer: {self.solution}'


class Task(djmodels.Model):
    class Meta:
        """We also do not crucially need this but it is convenient to pick just the most recent unanswered task.
        Ideally there should be just one, but just in case it is better to be safe."""
        get_latest_by = 'created_at'

    player = djmodels.ForeignKey(to=Player, related_name='tasks')
    question = djmodels.ForeignKey(to=Q, related_name='answers')
    answer = models.StringField()
    answered = models.BooleanField(initial=False)
    created_at = models.DateTimeField(auto_now_add=True)  # this and the following field is to track time
    updated_at = models.DateTimeField(auto_now=True)
    test = models.BooleanField()

    def get_answer_time(self):
        """We need this to show the question durations for the user in a nice mode."""
        sec = (self.updated_at - self.created_at).total_seconds()
        return f'{int((sec / 60) % 60):02d}:{int(sec):02d}'


"""For second task"""


class Q2(djmodels.Model):
    """This model just to keep the track of all avaialble questions and their correct answers for Task 2."""
    text = models.StringField()
    solution = models.StringField()

    def __str__(self):
        """We do not need this but it is convenient to have when we need to print the object (mostly for debugging."""
        return f'{self.text}: correct answer: {self.solution}'


class Task2(djmodels.Model):
    class Meta:
        """We also do not crucially need this but it is convenient to pick just the most recent unanswered task.
        Ideally there should be just one, but just in case it is better to be safe."""
        get_latest_by = 'created_at'

    player = djmodels.ForeignKey(to=Player, related_name='tasks2')
    question = djmodels.ForeignKey(to=Q2, related_name='answers')
    answer = models.StringField()
    created_at = models.DateTimeField(auto_now_add=True)  # this and the following field is to track time
    updated_at = models.DateTimeField(auto_now=True)
    test = models.BooleanField()

    def get_answer_time(self):
        """We need this to show the question durations for the user in a nice mode."""
        sec = (self.updated_at - self.created_at).total_seconds()
        return f'{int((sec / 60) % 60):02d}:{int(sec):02d}'
