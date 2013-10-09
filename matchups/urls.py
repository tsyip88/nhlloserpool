from django.conf.urls import patterns, url

from matchups.views import matchup_list, scoreboard, submit_picks, update_scores

urlpatterns = patterns('',
    url(r'^submit', submit_picks.submit_picks_for_current_matchup, name='submit_picks'),
    url(r'^(?P<week_number>\d+)/submit', submit_picks.submit_picks_for_week, name='submit_picks_for_week'),
    url(r'^(?P<week_number>\d+)/(?P<user_id>\d+)/admin_submit', submit_picks.admin_submit_picks_for_week, name='admin_submit_picks_for_week'),
    url(r'^(\d+)/admin_scoreboard', scoreboard.admin_scoreboard_for_week, name='admin_scoreboard_for_week'),
    url(r'^$', scoreboard.scoreboard_current_week, name='scoreboard'),
    url(r'^(\d+)/scoreboard', scoreboard.scoreboard, name='scoreboard_for_week'),
    url(r'^matchup$', matchup_list.current_matchups, name='current_matchups'),
    url(r'^(\d+)/matchup', matchup_list.weekly_matchups, name='weekly_matchups'),
    url(r'^update_scores', update_scores.update_current_scores, name='update_current_scores'),
    url(r'^(\d+)/update_scores', update_scores.update_scores_for_week, name='update_scores_for_week'),
)
