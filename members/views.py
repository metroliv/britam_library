from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import MemberProfile
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import MemberProfile
import csv
from django.http import HttpResponse
from .models import MemberProfile
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import MemberProfile
from .forms import MemberProfileForm  # we'll create this next



@login_required
def member_dashboard(request):
    return render(request, 'members/dashboard.html')

@login_required
def profile_view(request):
    profile = MemberProfile.objects.get(user=request.user)
    return render(request, 'members/profile.html', {'profile': profile})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'members/register.html', {'form': form})



@login_required
def member_dashboard(request):
    search = request.GET.get("search", "")
    members = MemberProfile.objects.select_related("user").all()

    if search:
        members = members.filter(
            user__first_name__icontains=search
        ) | members.filter(
            user__last_name__icontains=search
        ) | members.filter(
            user__username__icontains=search
        )

    return render(request, "members/dashboard.html", {
        "members": members,
    })


@login_required
def member_profile_view(request, user_id):
    profile = get_object_or_404(MemberProfile, user__id=user_id)
    return render(request, "members/profile_detail.html", {"profile": profile})



def export_members_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="members.csv"'

    writer = csv.writer(response)
    writer.writerow(['Full Name', 'Email', 'Phone', 'Joined At'])

    for profile in MemberProfile.objects.select_related('user').all():
        writer.writerow([
            profile.user.get_full_name(),
            profile.user.email,
            profile.phone,
            profile.joined_at.strftime('%Y-%m-%d'),
        ])

    return response


@login_required
def edit_member_profile(request, user_id):
    profile = get_object_or_404(MemberProfile, user__id=user_id)
    if request.method == 'POST':
        form = MemberProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('member_dashboard')
    else:
        form = MemberProfileForm(instance=profile)
    return render(request, 'members/edit_profile.html', {'form': form})
