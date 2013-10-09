from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from matchups import utilities
from django.contrib.auth.models import User
from matchups.forms import PickForm
from matchups.models import Pick

def submit_picks_for_current_matchup(request):
    return submit_picks_for_week(request, utilities.current_submit_picks_week_number())

@permission_required('matchups.add_matchup')
def admin_submit_picks_for_week(request, week_number, user_id):
    user = get_object_or_404(User, id=user_id)
    return submit_picks_for_user(request, week_number, user, True)

@login_required
def submit_picks_for_week(request, week_number):
    return submit_picks_for_user(request, week_number, request.user)

@login_required
def submit_picks_for_user(request, week_number, user, is_admin = False):
    if request.method =="POST" and request.POST.has_key('user_select'):
        selected_username = request.POST.get('user_select')
        selected_user = User.objects.get(username=selected_username)
        return redirect('matchups:admin_submit_picks_for_week', week_number=week_number, user_id=selected_user.id)
    week_date = str(utilities.game_day(week_number).strftime("%b %d, %Y"))
    matchup_list = None
    form_list = list()
    error_message = ''
    if utilities.has_first_matchup_of_week_started(week_number) and not is_admin:
        error_message = 'Cannot change picks, first game of the week has already started.'
    else:
        matchup_list = utilities.matchups_for_week(week_number)
        pick_sets = utilities.pick_sets_for_user(user)
        failed_to_save_field = False
        for pick_set in pick_sets:
            form, failed_to_save = create_or_get_form_for_pick(request, week_number, pick_set)
            form_list.append(form)
            if failed_to_save:
                failed_to_save_field = True
        if failed_to_save_field:
            error_message = 'Failed to save picks. See below for details.'
    context = {'matchup_list' : matchup_list,
               'form_list' : form_list,
               'error_message' : error_message,
               'week_number': int(week_number),
               'submitted_picks': request.method=="POST",
               'week_date' : week_date,
               'submit_user' : user,
               'is_admin' : is_admin}
    return render(request, 'submit_picks.html', context)

def create_or_get_form_for_pick(request, week_number, pick_set):
    failed_to_save_field = False
    pick = utilities.get_or_create_pick(week_number, pick_set)
    if request.method == "POST":
        form = PickForm(request.POST, prefix=pick_set.id, instance=pick)
        if form.is_valid():
            form.save()
        else:
            failed_to_save_field = True
        picks = Pick.objects.filter(week_number=week_number, pick_set=pick_set)
        utilities.update_winning_picks_for_week(week_number, picks)
    else:
        form = PickForm(prefix=pick_set.id, instance=pick)
    return form, failed_to_save_field