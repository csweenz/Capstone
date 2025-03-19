from django.core.cache import cache
from datetime import date, timedelta
from LogMyFit.models import Activity


def get_all(request):
    cache_key = f'activities_{request.user}'
    activities = cache.get(cache_key)
    if activities is None:
        print("empty cache")
        activities = Activity.objects.filter(user=request.user).select_related(
        'workout_activity', 'meal_activity', 'water_activity', 'sleep_activity')

        # Store results in the cache for 5 minutes (300 seconds)
        cache.set(cache_key, activities, 300)
    else:
        print("cache hit")
    return activities

def get_monthly(request):
    # 30 days of data for visualization
    month_cache_key = f'activities_{request.user}_30_days'
    monthly_activities = cache.get(month_cache_key)
    if monthly_activities is None:
        series_30_date = date.today() - timedelta(days=30)
        monthly_activities = Activity.objects.filter(user=request.user, activity_date__gte=series_30_date)
        cache.set(month_cache_key, monthly_activities, 300)
    else:
        print("cache hit")

    return monthly_activities
