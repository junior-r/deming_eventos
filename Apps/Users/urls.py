from django.urls import path

from Apps.Users.views import sign_up, profile, users_staff, assign_perms_user, export_users, info_participant, \
    user_events, delete_user

urlpatterns = [
    path('sing_up/', sign_up, name='sign_up'),
    path('profile/<str:username>/<int:id_user>/', profile, name='profile'),
    path('info_participant/<str:username>/<int:id_user>/', info_participant, name='info_participant'),
    path('user_events/<str:username>/<int:id_user>/', user_events, name='user_events'),
    path('users/<int:id_user>/', users_staff, name='users_staff'),
    path('assign_perms_user/<int:current_profile_user_id>/', assign_perms_user, name='assign_perms_user'),
    path('export_users/<str:user_type>/<int:event_id>/', export_users, name='export_users'),
    path('delete_user/<int:id_user>/', delete_user, name='delete_user'),

]
