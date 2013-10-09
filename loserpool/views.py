from django.shortcuts import render, redirect
from django import forms
import django.contrib.auth
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import PasswordChangeForm
from matchups.utilities import current_week_number
import matchups.matchup_data_retriever
import teams.team_data_retriever
import teams.models
class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)

def login(request):
    redirect_to = request.GET.get('next', None)
    form = LoginForm()
    error_message = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = django.contrib.auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    django.contrib.auth.login(request, user)
                    if redirect_to:
                        return redirect(redirect_to)
                    return render(request, 'successful_login.html')
                else:
                    error_message = "Unable to login due to disabled account."
            else:
                error_message = "Failed to log in. Please try again."
        else:
            error_message = "Failed to log in. Please try again."
    context = {'login_form':form,
               'error_message':error_message,
               'redirect_to':redirect_to}
    return render(request, 'login.html', context)

def logout(request):
    django.contrib.auth.logout(request)
    return render(request, 'successful_logout.html')

def index(request):
    return render(request, "index.html")

@login_required
def user_options(request):
    context = {'week_number':current_week_number()}
    return render(request, "user_options.html", context)

@login_required
def change_password(request):
    error_message = ''
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            print "Change!"
        else:
            error_message = "Failed to change password. Please try again."
    else:
        form = PasswordChangeForm(request.user)
    context = {'form':form,
               'error_message':error_message}
    return render(request, "change_password.html", context)

class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(max_length=50, widget=forms.PasswordInput)
    new_password = forms.CharField(max_length=50, widget=forms.PasswordInput)
    verify_new_password = forms.CharField(max_length=50, widget=forms.PasswordInput)

@permission_required('matchups.add_matchup')
def admin_actions(request):
    if request.method == 'POST':
        if request.POST.has_key('load_matchups'):
            matchups.matchup_data_retriever.MatchupDataRetriever.load_matchups()
        if request.POST.has_key('load_teams'):
            sport_name = "hockey"
            league_name = "nhl"
            teams.team_data_retriever.TeamDataRetriever.load_teams(sport_name, league_name)
        if request.POST.has_key('load_images'):
            team_list = teams.models.Team.objects.all()
            for team in team_list:
                team.image_location = team.full_name().replace(' ','').replace('.','') + '.png'
                team.save()
    return render(request, "admin_actions.html")