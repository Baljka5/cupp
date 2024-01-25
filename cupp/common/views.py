from django.views import generic as g
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages

from cupp import constants as c
from cupp.point.models import Type

from cupp.common.forms import MySettingsForm


class Map(LoginRequiredMixin, g.TemplateView):
    template_name = 'common/map.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['types'] = Type.objects.all()
        context['types'] = c.CHOICES_POINT_TYPE
        context['grades'] = c.CHOICES_POINT_GRADE

        context['users'] = User.objects.all()
        return context


class MySettings(LoginRequiredMixin, g.FormView):
    template_name = 'common/my_settings.html'
    form_class = MySettingsForm
    success_url = reverse_lazy('my_settings')

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user

        initial['first_name'] = user.first_name
        initial['last_name'] = user.last_name

        return initial

    def form_valid(self, form):
        user = self.request.user

        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()

        messages.add_message(self.request, messages.INFO, c.MSG_SAVED)

        return super().form_valid(form)
