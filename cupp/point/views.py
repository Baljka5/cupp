from datetime import datetime, timedelta
from django.views import generic as g
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse

from .forms import PointForm, PhotoFormset
from .models import Point, District, City ,Type
from .mixins import GroupMixin, StorePlannerMixin


class FormBase(GroupMixin):
    model = Point
    template_name = 'point/form.html'
    form_class = PointForm
    success_url = reverse_lazy('map')

    def form_valid(self, form):
        context = self.get_context_data()
        photo_formset = context['photo_formset']
        if photo_formset.is_valid():
            form.instance.created_by = self.request.user
            instance = form.save()

            photo_formset.instance = instance
            photo_formset.save()

            if form.data.get('next'):
                return redirect('/create/')

            return super(FormBase, self).form_valid(form)

        context['photo_formset'] = photo_formset
        context['form'] = form
        return self.render_to_response(context)


class Create(FormBase, g.CreateView):
    def get_context_data(self, *args, **kwargs):
        context = super(FormBase, self).get_context_data(*args, **kwargs)
        if self.request.method == 'GET':
            context['photo_formset'] = PhotoFormset()
        else:
            context['photo_formset'] = PhotoFormset(self.request.POST, self.request.FILES)
        return context


class Edit(FormBase, StorePlannerMixin, g.UpdateView):
    def get_context_data(self, *args, **kwargs):
        context = super(Edit, self).get_context_data(*args, **kwargs)
        if self.request.method == 'GET':
            context['photo_formset'] = PhotoFormset(instance=self.object)
        else:
            context['photo_formset'] = PhotoFormset(self.request.POST, files=self.request.FILES, instance=self.object)

        return context


class Delete(GroupMixin, StorePlannerMixin, g.DeleteView):
    model = Point
    success_url = reverse_lazy('map')


class AjaxInfo(GroupMixin, StorePlannerMixin, g.DetailView):
    model = Point
    template_name = 'point/ajax_info.html'


class Detail(LoginRequiredMixin, g.DetailView):
    model = Point
    template_name = 'point/detail.html'


class AjaxList(LoginRequiredMixin, g.ListView):
    model = Point
    template_name = 'point/ajax_list.html'

    def get_queryset(self):
        types = self.request.GET.getlist('type')
        grades = self.request.GET.getlist('grade')
        availables = self.request.GET.getlist('availability')
        size = self.request.GET.get('size')
        base_rent_rate = self.request.GET.get('base_rent_rate')
        max_rent_rate = self.request.GET.get('max_rent_rate')
        available_date = self.request.GET.get('available_date')
        created_by = self.request.GET.get('created_by')
        created_date = self.request.GET.get('created_date')

        kwargs = {
            'type': 'PP'
        }

        if grades:
            kwargs['grade__in'] = grades

        if availables:
            kwargs['availability__in'] = [int(i) for i in availables if i.isdigit()]

        if size and size != '0;300':
            sgte, slte = size.split(';')
            kwargs['size__gte'] = sgte
            kwargs['size__lte'] = slte

        if base_rent_rate and base_rent_rate != '0;20000000':
            bgte, blte = base_rent_rate.split(';')
            kwargs['base_rent_rate__gte'] = bgte
            kwargs['base_rent_rate__lte'] = blte

        if max_rent_rate and max_rent_rate != '0;20000000':
            mgte, mlte = max_rent_rate.split(';')
            kwargs['max_rent_rate__gte'] = mgte
            kwargs['max_rent_rate__lte'] = mlte

        if available_date:
            range_value = available_date.replace('/', '-').split(' - ')
            kwargs['available_date__gte'] = datetime.strptime(range_value[0], '%Y-%m-%d')
            kwargs['available_date__lte'] = datetime.strptime(range_value[1], '%Y-%m-%d') + timedelta(days=1)

        if created_date:
            range_value = created_date.replace('/', '-').split(' - ')
            kwargs['created_date__gte'] = datetime.strptime(range_value[0], '%Y-%m-%d')
            kwargs['created_date__lte'] = datetime.strptime(range_value[1], '%Y-%m-%d') + timedelta(days=1)

        if created_by:
            kwargs['created_by__id'] = created_by

        if types:
            qs = Point.objects.filter(Q(**kwargs) | Q(type__in=types))
        else:
            qs = Point.objects.filter(**kwargs)

        user = self.request.user
        if user.groups.filter(name='Store planner').exists():
            qs = qs.filter(Q(created_by=user, type='PP') | Q(type__in=types))

        return qs

def get_districts(request):
    city_id = request.GET.get('city_id')
    districts = list(District.objects.filter(city__id=city_id).values('id', 'district_name'))
    return JsonResponse({'districts': districts})

# def get_type_name(request):
#     type_code = request.GET.get('type_code', '')
#     try:
#         type_obj = Type.objects.get(type_cd=type_code)
#         return JsonResponse({'type_name': type_obj.type_name})
#     except Type.DoesNotExist:
#         return JsonResponse({'type_name': 'Not found'})
