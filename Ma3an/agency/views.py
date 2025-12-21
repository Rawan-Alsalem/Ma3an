from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Tour, TourGuide, TourSchedule
from datetime import datetime


# -------------------------
# Tour Guide Views
# -------------------------
def add_tour_guide_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('add_tour_guide')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        TourGuide.objects.create(user=user)
        messages.success(request, 'TourGuide account created successfully ✅')
        return redirect('dashboard')

    return render(request, 'agency/add_tour_guide.html')


def all_tour_guides_view(request):
    tour_guides = TourGuide.objects.all()
    return render(request, 'agency/all_tour_guides.html', {'tour_guides': tour_guides})


# ✏️ Edit Tour Guide
def edit_tour_guide_view(request, pk):
    tour_guide = get_object_or_404(TourGuide, pk=pk)
    user = tour_guide.user

    if request.method == "POST":
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()

        messages.success(request, "Tour Guide updated successfully")
        return redirect('all_tour_guides')

    return render(request, 'agency/edit_tour_guide.html', {
        'tour_guide': tour_guide
    })


# 🗑️ Delete Tour Guide
def delete_tour_guide_view(request, pk):
    tour_guide = get_object_or_404(TourGuide, pk=pk)
    user = tour_guide.user

    if request.method == "POST":
        user.delete()
        messages.success(request, "Tour Guide deleted successfully")
        return redirect('all_tour_guides')

    return render(request, 'agency/delete_tour_guide.html', {
        'tour_guide': tour_guide
    })


# -------------------------
# Agency Views
# -------------------------
def dashboard_view(request):
    return render(request, 'agency/agency_dashboard.html')


def subscription_view(request):
    return render(request, 'agency/agency_subscription.html')


def agency_payment_view(request):
    return render(request, 'agency/agency_payment.html')


# -------------------------
# Tour Views
# -------------------------
def add_tour_view(request):
    guides = TourGuide.objects.all()
    available_guides = guides

    # نقرأ التواريخ من GET (مو POST)
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    start_date = end_date = None

    if start_date_str and end_date_str:
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "❌ تنسيق التواريخ غير صحيح")
            start_date = end_date = None

        if start_date and end_date:
            if start_date > end_date:
                messages.error(request, "❌ تاريخ البداية لا يمكن أن يكون بعد تاريخ النهاية")
            else:
                # تصفية المرشدين فقط بعد اختيار التاريخ
                available_guides = [
                    g for g in guides if g.is_available(start_date, end_date)
                ]

    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        country = request.POST.get('country')
        city = request.POST.get('city')
        travelers = int(request.POST.get('travelers') or 0)
        price = float(request.POST.get('price') or 0)

        try:
            start_date = datetime.strptime(request.POST.get('start_date'), "%Y-%m-%d").date()
            end_date = datetime.strptime(request.POST.get('end_date'), "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "❌ تنسيق التواريخ غير صحيح")
            return render(request, 'agency/add_tour.html', {
                'guides': available_guides,
                'name': name,
                'description': description,
                'country': country,
                'city': city,
                'travelers': travelers,
                'price': price,
                'start_date': request.POST.get('start_date'),
                'end_date': request.POST.get('end_date'),
            })

        if start_date > end_date:
            messages.error(request, "❌ تاريخ البداية لا يمكن أن يكون بعد تاريخ النهاية")
            return render(request, 'agency/add_tour.html', {
                'guides': available_guides,
                'name': name,
                'description': description,
                'country': country,
                'city': city,
                'travelers': travelers,
                'price': price,
                'start_date': request.POST.get('start_date'),
                'end_date': request.POST.get('end_date'),
            })

        tour_guide = get_object_or_404(TourGuide, id=request.POST.get('tour_guide'))

        # حماية إضافية
        if not tour_guide.is_available(start_date, end_date):
            messages.error(request, "❌ هذا المرشد لديه رحلة في نفس التاريخ")
            return render(request, 'agency/add_tour.html', {
                'guides': available_guides,
                'name': name,
                'description': description,
                'country': country,
                'city': city,
                'travelers': travelers,
                'price': price,
                'start_date': request.POST.get('start_date'),
                'end_date': request.POST.get('end_date'),
            })

        # إنشاء الرحلة
        Tour.objects.create(
            name=name,
            description=description,
            country=country,
            city=city,
            travelers=travelers,
            price=price,
            start_date=start_date,
            end_date=end_date,
            tour_guide=tour_guide
        )

        messages.success(request, "✅ تم إنشاء الرحلة")
        return redirect('all_tours')

    return render(request, 'agency/add_tour.html', {
        'guides': available_guides,
        'start_date': start_date_str,
        'end_date': end_date_str,
    })


def all_tours_view(request):
    tours = Tour.objects.all()
    tours_with_duration = []
    for tour in tours:
        duration_days = (tour.end_date - tour.start_date).days + 1
        tours_with_duration.append({
            'tour': tour,
            'duration': duration_days
        })
    return render(request, 'agency/all_tours.html', {'tours': tours_with_duration})


def edit_tour_view(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    guides = TourGuide.objects.all()

    if request.method == "POST":
        tour.name = request.POST.get('tourName')
        tour.description = request.POST.get('description')
        tour.country = request.POST.get('country')
        tour.city = request.POST.get('city')
        tour.travelers = request.POST.get('travelers') or 0
        tour.price = request.POST.get('price') or 0
        tour.start_date = request.POST.get('startDate')
        tour.end_date = request.POST.get('endDate')

        tour_guide_id = request.POST.get('tourGuide')
        tour.tour_guide = TourGuide.objects.filter(id=tour_guide_id).first() if tour_guide_id else None

        if 'tourImage' in request.FILES:
            tour.image = request.FILES['tourImage']

        tour.save()
        messages.success(request, "✅ Tour updated successfully!")
        return redirect('all_tours')

    return render(request, 'agency/edit_tour.html', {'tour': tour, 'guides': guides})


def delete_tour_view(request, tour_id):
    tour = Tour.objects.filter(id=tour_id).first()
    if tour:
        tour.delete()
        messages.success(request, "✅ Tour deleted successfully!")
    else:
        messages.error(request, "Tour not found")
    return redirect('all_tours')


def tour_detail_view(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    schedules = tour.schedules.all()
    return render(request, 'agency/tour_detail.html', {
        'tour': tour,
        'schedules': schedules
    })


# -------------------------
# Tour Schedule Views
# -------------------------
def add_schedule_view(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)

    if request.method == "POST":
        number_of_days = int(request.POST.get("number_of_days", 0))

        # إذا المستخدم اختار عدد الأيام فقط
        if "set_days" in request.POST:
            days = range(1, number_of_days + 1)
            return render(request, "agency/add_schedule.html", {
                "tour": tour,
                "days": days,
                "number_of_days": number_of_days
            })

        # إذا المستخدم أرسل الأنشطة
        else:
            days = range(1, number_of_days + 1)
            for day in days:
                start_times = request.POST.getlist(f"day_{day}_start_time[]")
                end_times = request.POST.getlist(f"day_{day}_end_time[]")
                titles = request.POST.getlist(f"day_{day}_activity_title[]")
                locations = request.POST.getlist(f"day_{day}_location_name[]")
                urls = request.POST.getlist(f"day_{day}_location_url[]")
                descriptions = request.POST.getlist(f"day_{day}_description[]")

                for i in range(len(titles)):
                    TourSchedule.objects.create(
                        tour=tour,
                        day_number=day,
                        start_time=start_times[i],
                        end_time=end_times[i],
                        activity_title=titles[i],
                        location_name=locations[i],
                        location_url=urls[i],
                        description=descriptions[i],
                    )

            messages.success(request, "✅ Schedule saved successfully!")
            return redirect("tour_detail", tour_id=tour.id)

    # الصفحة قبل اختيار الأيام
    return render(request, "agency/add_schedule.html", {"tour": tour})


def delete_schedule_view(request, schedule_id):
    schedule = get_object_or_404(TourSchedule, id=schedule_id)
    tour_id = schedule.tour.id
    schedule.delete()
    messages.success(request, "✅ Activity deleted successfully!")
    return redirect("tour_detail", tour_id=tour_id)
