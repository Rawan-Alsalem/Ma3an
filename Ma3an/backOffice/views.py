from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import TravelAgency, Subscription, Notification, Profile

from django.contrib.auth.models import User


# @login_required
def dashboard(request):
    context = {
        'pending_agencies': TravelAgency.objects.filter(profile__user__is_active=False).count(),
        'active_agencies': TravelAgency.objects.count(),
        'total_users': Profile.objects.count(),
        'active_subscriptions': Subscription.objects.filter(status='active').count(),
        'recent_notifications': Notification.objects.order_by('-created_at')[:5]
    }
    return render(request, 'backOffice/dashboard.html', context)


# @login_required
def manage_agencies(request):
    agencies = TravelAgency.objects.all()
    return render(request, 'backOffice/agencies.html', {'agencies': agencies})


# @login_required
def approve_agency(request, agency_id):
    agency = get_object_or_404(TravelAgency, id=agency_id)
    agency.approved = True
    agency.save()
    return redirect('manage_agencies')


# @login_required
def manage_subscriptions(request):
    subscriptions = Subscription.objects.all()
    return render(request, 'backOffice/subscriptions.html', {'subscriptions': subscriptions})


# @login_required
def users_list(request):
    users = User.objects.all()
    return render(request, 'backOffice/users.html', {'users': users})


# @login_required
def system_security(request):
    return render(request, 'backOffice/security.html')
