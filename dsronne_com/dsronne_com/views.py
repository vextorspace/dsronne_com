from django.shortcuts import render
from .stoic_forms import StoicQuestionForm
from .ai_librarian import AiLibrarian
from .navajo_forms import NavajoQuestionForm
from django.http import JsonResponse

def home(request):
    return render(request, 'dsronne_com/home.html')


def stoic(request):
    if request.method == 'POST':
        form = StoicQuestionForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data['question']
            answer = AiLibrarian().question_stoics(question)
            return JsonResponse({
                'result': f'<h3>Sages once said:</h3><p>{answer}</p>'
            })
    else:
        form = StoicQuestionForm()

    return render(request, 'dsronne_com/stoic.html', {'form': form})

def navajo(request, ai_librarian=None):
    if not ai_librarian:
        ai_librarian = AiLibrarian()
    if request.method == 'POST':
        form = NavajoQuestionForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data['question']
            answer = ai_librarian.question_navajo(question)
            return JsonResponse({
                'result': f'<h3>My librarian says:</h3><p>{answer}</p>'
            })
    else:
        form = NavajoQuestionForm()
    return render(request, 'dsronne_com/navajo.html', {'form': form})
