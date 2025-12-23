"""
Seed script for Ma3an (NO superuser).
Creates:
- Subscription plans
- Agency users + Agency profiles
- Agency subscriptions
- Travelers
- Languages + TourGuide
- Tour + Schedule + Geofence + GeofenceEvent
- Notifications (event REQUIRED)
"""

from datetime import date, timedelta, time
from django.utils import timezone
from django.contrib.auth import get_user_model

from accounts.models import Agency, Traveler, TourGuide, Language, Notification
from agency.models import (
    Subscription,
    AgencySubscription,
    Tour,
    TourSchedule,
    Geofence,
    GeofenceEvent,
)

User = get_user_model()
today = timezone.localdate()

# -------------------------
# 1) Subscription Plans
# -------------------------
plans_data = [
    ("basic", 199.00, 5, 2, 50),
    ("standard", 399.00, 15, 5, 200),
    ("premium", 799.00, 999, 50, 2000),
]

plans = []
for sub_type, price, tours_lim, sup_lim, trav_lim in plans_data:
    p, _ = Subscription.objects.get_or_create(
        subscriptionType=sub_type,
        defaults={
            "price": price,
            "tours_limit": tours_lim,
            "supervisors_limit": sup_lim,
            "travelers_limit": trav_lim,
        },
    )
    p.price = price
    p.tours_limit = tours_lim
    p.supervisors_limit = sup_lim
    p.travelers_limit = trav_lim
    p.save()
    plans.append(p)

basic, standard, premium = plans

# -------------------------
# 2) Agencies
# -------------------------
agency_rows = [
    ("riyadh_wonders@ma3an.com", "riyadh_wonders", "Riyadh Wonders", "Riyadh", "0500000001", "CL-1001", "pending", ""),
    ("desert_trips@ma3an.com", "desert_trips", "Desert Trips", "Riyadh", "0500000002", "CL-1002", "approved", ""),
    ("sea_breeze@ma3an.com", "sea_breeze", "Sea Breeze Tours", "Jeddah", "0500000003", "CL-1003", "approved", ""),
    ("mountain_escape@ma3an.com", "mountain_escape", "Mountain Escape", "Abha", "0500000004", "CL-1004", "rejected", "Missing documents"),
    ("heritage_walks@ma3an.com", "heritage_walks", "Heritage Walks", "AlUla", "0500000005", "CL-1005", "pending", ""),
    ("city_hoppers@ma3an.com", "city_hoppers", "City Hoppers", "Dammam", "0500000006", "CL-1006", "approved", ""),
]

agencies = []
for email, username, name, city, phone, license_no, status, reject_reason in agency_rows:
    u, _ = User.objects.get_or_create(
        email=email,
        defaults={
            "username": username,
            "role": "agency",
            "is_active": True,
        },
    )
    if not u.has_usable_password():
        u.set_password("1234")
        u.save()

    a, _ = Agency.objects.get_or_create(
        user=u,
        defaults={
            "agency_name": name,
            "city": city,
            "phone_number": phone,
            "commercial_license": license_no,
            "approval_status": status,
            "rejection_reason": reject_reason,
        },
    )

    a.agency_name = name
    a.city = city
    a.phone_number = phone
    a.commercial_license = license_no
    a.approval_status = status
    a.rejection_reason = reject_reason
    a.save()

    agencies.append(a)

# -------------------------
# 3) Agency Subscriptions
# -------------------------
for i, a in enumerate(agencies):
    if a.approval_status != Agency.ApprovalStatus.APPROVED:
        continue

    plan = [basic, standard, premium][i % 3]
    status = "active" if i % 3 != 0 else "expired"
    expiry = today + timedelta(days=30 - i * 2)

    AgencySubscription.objects.update_or_create(
        agency=a,
        defaults={
            "plan": plan,
            "status": status,
            "start_date": today - timedelta(days=10),
            "expiry_date": expiry,
        },
    )

# -------------------------
# 4) Travelers
# -------------------------
traveler_rows = [
    ("trav1@ma3an.com", "trav1", "Sara", "Ahmed", "0551000001"),
    ("trav2@ma3an.com", "trav2", "Noura", "Ali", "0551000002"),
    ("trav3@ma3an.com", "trav3", "Fahad", "Saad", "0551000003"),
]

travelers = []
for email, username, first, last, phone in traveler_rows:
    u, _ = User.objects.get_or_create(
        email=email,
        defaults={
            "username": username,
            "role": "traveler",
            "first_name": first,
            "last_name": last,
        },
    )
    if not u.has_usable_password():
        u.set_password("1234")
        u.save()

    t, _ = Traveler.objects.get_or_create(
        user=u,
        defaults={
            "phone_number": phone,
            "date_of_birth": date(1999, 1, 1),
            "nationality": "SAU",
        },
    )
    travelers.append(t)

# -------------------------
# 5) Languages + TourGuide
# -------------------------
langs = []
for code, name in [("en", "English"), ("ar", "Arabic")]:
    l, _ = Language.objects.get_or_create(code=code, defaults={"name": name})
    l.name = name
    l.save()
    langs.append(l)

approved_agency = Agency.objects.filter(approval_status="approved").first()

guide_user, _ = User.objects.get_or_create(
    email="guide1@ma3an.com",
    defaults={
        "username": "guide1",
        "role": "tourGuide",
        "first_name": "Omar",
        "last_name": "Guide",
    },
)
if not guide_user.has_usable_password():
    guide_user.set_password("1234")
    guide_user.save()

guide, _ = TourGuide.objects.get_or_create(
    user=guide_user,
    defaults={
        "agency": approved_agency,
        "phone": "0552000001",
        "nationality": "SAU",
        "is_active": True,
    },
)
guide.languages.set(langs)

# -------------------------
# 6) Tour + Geofence + Notifications
# -------------------------
tour, _ = Tour.objects.get_or_create(
    name="Riyadh Highlights",
    defaults={
        "description": "City tour",
        "country": "Saudi Arabia",
        "city": "Riyadh",
        "travelers": 40,
        "price": 350,
        "start_date": today + timedelta(days=2),
        "end_date": today + timedelta(days=4),
        "days": 3,
        "tour_guide": guide,
    },
)

sched, _ = TourSchedule.objects.get_or_create(
    tour=tour,
    day_number=1,
    defaults={
        "start_time": time(9, 0),
        "end_time": time(12, 0),
        "activity_title": "Museum Visit",
        "location_name": "National Museum",
        "latitude": 24.6460,
        "longitude": 46.7100,
    },
)

geofence, _ = Geofence.objects.get_or_create(
    schedule=sched,
    defaults={"radius_meters": 200},
)

for t in travelers:
    ev, _ = GeofenceEvent.objects.get_or_create(
        tour_guide=guide,
        traveler=t,
        geofence=geofence,
        event_type="exit",
    )

    Notification.objects.get_or_create(
        user=guide_user,
        event=ev,
        defaults={
            "message": f"{t.user.username} exited geofence",
        },
    )

print("✅ Seed completed")
print("Agencies:", Agency.objects.count())
print("Agency subscriptions:", AgencySubscription.objects.count())
print("Travelers:", Traveler.objects.count())
print("Notifications:", Notification.objects.count())
