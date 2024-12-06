from home.models import Products
from django.http import Http404
from django.views.generic import ListView, DetailView


class HomeListView(ListView):
    template_name = 'global/pages/base_page.html'
    model = Products
    context_object_name = 'products'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update({
            'title': 'Home'
        })

        return context


class ViewPageDetailView(DetailView):
    template_name = 'home/pages/view_page.html'
    model = Products
    context_object_name = 'product'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        queryset = queryset.filter(
            pk=self.kwargs.get('pk'),
        )

        if not queryset:
            raise Http404()

        return queryset
