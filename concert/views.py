from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.hashers import make_password

from concert.forms import LoginForm, SignUpForm
from concert.models import Concert, ConcertAttending
import requests as req
from django.conf import settings
from django.shortcuts import redirect


# Create your views here.

def signup(request):
    form = SignUpForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        login(request, user)
        return redirect('index')
    return render(request, 'signup.html', {'form': form})


def index(request):
    return render(request, "index.html")


def songs(request):
    response = req.get(settings.SONGS_SERVICE_URL + '/song', timeout=10)
    response.raise_for_status()
    return render(request, 'songs.html', {'songs': response.json()['songs']})


def photos(request):
    response = req.get(settings.PICTURES_SERVICE_URL + '/picture', timeout=10)
    response.raise_for_status()
    return render(request, 'photos.html', {'photos': response.json()})

def login_view(request):
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('index')
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

def concerts(request):
    attendance = {}
    if request.user.is_authenticated:
        attendance = dict(ConcertAttending.objects.filter(user=request.user).values_list('concert_id', 'attending'))
    rows = [{'concert': concert, 'status': attendance.get(concert.pk, '-')}
            for concert in Concert.objects.order_by('date')]
    return render(request, 'concerts.html', {'concerts': rows})


def concert_detail(request, id):
    if request.user.is_authenticated:
        obj = get_object_or_404(Concert, pk=id)
        try:
            status = obj.attendee.filter(user=request.user).first().attending
        except:
            status = "-"
        return render(request, "concert_detail.html", {"concert_details": obj, "status": status, "attending_choices": ConcertAttending.AttendingChoices.choices})
    else:
        return HttpResponseRedirect(reverse("login"))


def concert_attendee(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            concert_id = request.POST.get("concert_id")
            attendee_status = request.POST.get("attendee_choice")
            get_object_or_404(Concert, pk=concert_id)
            if attendee_status not in ConcertAttending.AttendingChoices.values:
                return HttpResponse('Invalid attendance choice', status=400)
            concert_attendee_object = ConcertAttending.objects.filter(
                concert_id=concert_id, user=request.user).first()
            if concert_attendee_object:
                concert_attendee_object.attending = attendee_status
                concert_attendee_object.save()
            else:
                ConcertAttending.objects.create(concert_id=concert_id,
                                                user=request.user,
                                                attending=attendee_status)

        return HttpResponseRedirect(reverse("concerts"))
    else:
        return HttpResponseRedirect(reverse("index"))
