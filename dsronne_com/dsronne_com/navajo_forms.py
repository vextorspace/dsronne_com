from django import forms

class NavajoQuestionForm(forms.Form):
    question = forms.CharField(widget=forms.Textarea, label='Question', max_length=1024)
