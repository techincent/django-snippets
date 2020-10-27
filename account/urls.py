from django.urls import path

from .views import registration_form_view, RegistrationClassBaseView, user_list_view


urlpatterns = [
    path('signup', registration_form_view, name='register_view'),
    path('signup-classbase', RegistrationClassBaseView.as_view(), name='class_base_register_view'),
    path('ajax/users', user_list_view, name='json_user_list')
]