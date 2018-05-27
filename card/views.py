from django.shortcuts import render
from card.models import UserCard


def display_card(request, pk=None):
    if pk is None:
        cards = UserCard.objects.all()
        args = {
            'cards': cards,
        }
        return render(request, 'card/cards.html', args)
    card = UserCard.objects.get(pk=pk)
    args = {
        'card': card,
    }
    return render(request, 'card/card.html', args)
