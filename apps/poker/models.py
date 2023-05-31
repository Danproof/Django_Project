from django.db import models
import json
import random
from .constants import EMPTY


class TableSize(models.Model):
    name = models.CharField(unique=True, max_length=45)
    seats = models.IntegerField(unique=True)

    def __str__(self):
        return self.name


class BuyIn(models.Model):
    amount = models.IntegerField(unique=True)
    small_blind = models.IntegerField()
    big_blind = models.IntegerField()

    def __str__(self):
        return f'{self.amount} ({self.small_blind}/{self.big_blind})'


class Table(models.Model):
    table_size = models.ForeignKey(TableSize, on_delete=models.CASCADE)
    buy_in = models.ForeignKey(BuyIn, on_delete=models.CASCADE)
    seats = models.JSONField()
    open_seat = models.BooleanField(default=True)
    n_players = models.IntegerField(default=0)

    def __init__(self, *args, **kwargs):
        table_size = kwargs.pop('table_size', None)
        buy_in = kwargs.pop('buy_in', None)

        super(Table, self).__init__(*args, **kwargs)
        if table_size and buy_in:
            self.table_size = table_size
            self.buy_in = buy_in
            seats = [EMPTY for _ in range(table_size.seats)]
            self.seats = json.dumps(seats)
        

    def join(self, player):
        seats = json.loads(self.seats)
        if player.username not in seats:
            empty_seats = [seat for seat, username in enumerate(seats) if username == EMPTY]
            seat = random.choice(empty_seats)
            seats[seat] = player.username
            self.seats = json.dumps(seats)

            self.n_players += 1
            if self.table_size.seats == self.n_players:
                self.open_seat = False
            self.save()

    def sit_out(self, player):
        seats = json.loads(self.seats)
        for seat, username in enumerate(seats):
            if player.username == username:
                seats[seat] = EMPTY 
        self.seats = json.dumps(seats)
        self.n_players -= 1
        self.open_seat = True
        self.save()
        
