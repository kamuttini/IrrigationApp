from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Notification


# Create your views here.
def show_notification(request, notification_id):
    n = Notification.objects.get(id=notification_id)
    return render('notification/notification.html', {'notification': n})


def delete_notification(request):
    notfications = Notification.objects.filter(user=request.user, viewed=False)
    for n in notfications:
        n.viewed = True
        n.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
