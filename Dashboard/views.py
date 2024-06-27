from django.shortcuts import render, redirect
from .models import Workout
from .forms import WorkoutForm
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now, timedelta
from django.db.models import Count


@login_required
def dashboard_view(request):
    workouts = Workout.objects.filter(user=request.user)
    
    # Aggregate the common workout types and their counts
    common_workouts = workouts.values('workout_type').annotate(count=Count('workout_type')).order_by('-count')
    
    return render(request, 'dashboard/dashboard.html', {
        'workouts': workouts,
        'common_workouts': common_workouts
    })

@login_required
def log_workout_view(request):
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user
            workout.save()
            return redirect('dashboard')
    else:
        form = WorkoutForm()
    return render(request, 'dashboard/log_workout.html', {'form': form})

