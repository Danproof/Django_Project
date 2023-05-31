import json
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import TableSize, BuyIn, Table
from .forms import NewTable
from .constants import EMPTY

def home(request):
    return render(request, 'poker/home.html')

def demo(request):
    return render(request, 'poker/demo.html')

def one(request):
    return render(request, 'poker/1.html')

def two(request):
    return render(request, 'poker/2.html')


def new_game(request):
    if request.method == 'POST':
        form = NewTable(request.POST)
        if form.is_valid():
            table = Table.objects.get_or_create(**form.cleaned_data,
                                                open_seat=True)[0]
            table.join(request.user)
            return redirect('poker-table', table_id=table.id)
    else:
        form = NewTable()
        context = {
            'form': form,
        }
        return render(request, 'poker/new_game.html', context)


def table(request, table_id):
    table = Table.objects.get(id=table_id)
    if request.method == 'POST':
        player = request.user
        table.sit_out(player)
        return redirect('poker-home')
    else:
        context = {
            'table_id': table_id
        }
        return render(request, 'poker/table.html', context)