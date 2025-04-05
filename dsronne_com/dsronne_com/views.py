from django.shortcuts import render
from .stoic_forms import StoicQuestionForm
from .ai_librarian import AiLibrarian
from .navajo_forms import NavajoQuestionForm
def home(request):
    return render(request, 'dsronne_com/home.html')


def stoic(request):
    answer = None

    if request.method == 'POST':
        form = StoicQuestionForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data['question']
            answer = AiLibrarian().question_stoics(question)
    else:
        form = StoicQuestionForm()

    return render(request, 'dsronne_com/stoic.html',
                  {
                      'form': form,
                      'answer': answer
                  })

def navajo(request):
    answer = None

    if request.method == 'POST':
        form = NavajoQuestionForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data['question']
            answer = AiLibrarian().question_navajo(question)
    else:
        form = NavajoQuestionForm()

    return render(request, 'dsronne_com/navajo.html',
                  {
                      'form': form,
                      'answer': answer
                  })

