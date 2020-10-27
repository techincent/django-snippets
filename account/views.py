import json
from django.core import serializers
from django.shortcuts import render, redirect, reverse
from django.http.response import JsonResponse
from django.views.generic import CreateView

from django.contrib.auth import get_user_model

from .forms import UserRegistrationForm


def registration_form_view(request):
    form = UserRegistrationForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            if request.is_ajax():
                return JsonResponse({'success': True}, status=201)
            return redirect(reverse('home'))
        else:
            if request.is_ajax():
                return JsonResponse({'success': False, 'errors': form.errors}, status=406)
    return render(request, 'register_form.html', {'form': form})


class RegistrationClassBaseView(CreateView):
    """ class Base register view, handle with ajax or none ajax"""
    template_name = 'register_form.html'
    form_class = UserRegistrationForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        # other staff
        instance.save()
        if request.is_ajax():
            return JsonResponse({'success': True}, status=201)
        return redirect(reverse('home'))

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        return super().form_invalid(form)        


def user_list_view(request):
    """ get json data """
    users = serializers.serialize(
        'json', 
        get_user_model().objects.all(), 
        fields=('first_name','last_name', 'username', 'email')
    )
    return JsonResponse({'users': users}, status=200)
