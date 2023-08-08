from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.

class InitView(TemplateView):
    
    template_name = 'index.html'