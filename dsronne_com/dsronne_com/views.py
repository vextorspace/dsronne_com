from django.shortcuts import render
from .stoic_forms import StoicQuestionForm
from .ai_librarian import AiLibrarian
from .navajo_forms import NavajoQuestionForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.shortcuts import redirect
from .register_forms import RegistrationForm

def home(request):
    return render(request, 'dsronne_com/home.html')


@login_required
def stoic(request):
    """Handle stoic questions via AJAX or render the form on GET."""
    if request.method == 'POST':
        form = StoicQuestionForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data['question']
            answer = AiLibrarian().question_stoics(question)
            return JsonResponse({
                'result': f'<h3>Sages once said:</h3><p>{answer}</p>'
            })
        else:
            # Return form errors as HTML
            errors = form.errors.as_ul()
            return JsonResponse({
                'result': f'<div class="errorlist">{errors}</div>'
            })
    # GET request
    form = StoicQuestionForm()
    return render(request, 'dsronne_com/stoic.html', {'form': form})

@login_required
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
   
def register(request):
    """Allow a new user to register with email and password."""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'dsronne_com/register.html', {'form': form})
    
def logout_view(request):
    """Log out the user and redirect to home."""
    auth_logout(request)
    return redirect('home')
