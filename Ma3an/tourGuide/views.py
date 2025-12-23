from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from accounts.models import Agency, TourGuide, Traveler
from django.contrib import messages
from agency.models import Tour
# Create your views here.


@login_required
def all_tourguides_view(request):

    if request.user.role != 'agency':
        return redirect('accounts:profile')

    agency = request.user.agency_profile
    tour_guides = agency.tour_guides.select_related('user')

    return render(request, 'tourGuide/all_tourGuides.html', {
        'agency': agency,
        'tour_guides': tour_guides,
    })
    

@login_required
def delete_tourguide(request, guide_id):
    if request.user.role != 'agency':
        return redirect('accounts:profile')

    agency = request.user.agency_profile
    guide = get_object_or_404(TourGuide, id=guide_id, agency=agency)

    if request.method == 'POST':
        first_name = guide.user.first_name
        last_name = guide.user.last_name

        guide.user.delete()

        messages.success(
            request,
            f'Tour guide "{first_name} {last_name}" has been deleted successfully.'
        )

        return redirect('tourGuide:all_tourguides')

    return redirect('tourGuide:all_guides')


@login_required
def my_tours_view(request):
    tours = []

    if request.user.role == 'tourGuide':
        tours = Tour.objects.filter(tour_guide__user=request.user).order_by('-start_date')

    context = {
        'tours': tours
    }
    return render(request, 'tourguide/my_tours.html', context)


def tour_details_view(request, tour_id):
    # نتأكد أنه Tour Guide
    if request.user.role != 'tourGuide':
        return redirect('accounts:profile')  # أو أي صفحة مناسبة

    # جلب التور المرتبط بالمرشد الحالي
    tour = get_object_or_404(Tour, id=tour_id, tour_guide__user=request.user)

    # قائمة المسافرين المرتبطين بالرحلة
    travelers = Traveler.objects.filter(tour__id=tour.id)  # إذا عندك علاقة ManyToMany أو ForeignKey

    context = {
        'tour': tour,
        'travelers': travelers,
        'today': date.today(),
    }

    return render(request, 'tourguide/tour_detail.html', context)