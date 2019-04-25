from django import forms
import json


class TaskForm(forms.Form):
    def __init__(self, task, *args, **kwargs):
        """
        We get the task here, we get the choices from the corresponding question.
        and we render the form based on the task type (open/multiplechoice).
        We also need to pass task_id there so the consumers can process it when the user delivers answer.
        """
        super().__init__(*args, **kwargs)
        q = task.question
        if task.question.open:
            self.fields['question'] = forms.CharField(label=q.text,
                                                      required=True
                                                      )
        else:
            choices = json.loads(q.chs)
            choices = ((c, c,) for c in choices)
            self.fields['question'] = forms.ChoiceField(label=q.text, choices=choices,
                                                        widget=forms.RadioSelect(),
                                                        required=True
                                                        )

        self.fields['question'].widget.attrs.update({'data-task': task.id})


class Task2Form(forms.Form):
    def __init__(self, task, *args, **kwargs):
        """
        We get the task here, we get the choices from the corresponding questin.
        and we render the form based on the task type (open/multiplechoice).
        We also need to pass task_id there so the consumers can process it when the user delivers answer.
        """
        super().__init__(*args, **kwargs)
        q = task.question
        self.fields['question'] = forms.CharField(label=q.text,
                                                  required=True,
                                                  widget=forms.Textarea,
                                                  )

        #self.fields['question'].widget.attrs.update({'data-task': task.id})
