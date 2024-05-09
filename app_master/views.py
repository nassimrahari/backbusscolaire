from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.db import transaction
from django import forms

class HomeViewPage(View):
    template_name = 'index.html'
    def get(self,request):
        context={}

        return render(request, self.template_name, context)

