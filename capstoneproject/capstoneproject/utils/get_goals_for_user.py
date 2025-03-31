from django.core.cache import cache
from LogMyFit.models import Goal


def get_goals(request):
    cache_key = f'goals_{request.user}'
    goals = cache.get(cache_key)
    if goals is None:
        goals = Goal.objects.filter(user=request.user).select_related(
        'fitness_goal', 'nutrition_goal', 'water_goal', 'sleep_goal')

        # Store results in the cache for 5 minutes (300 seconds)
        cache.set(cache_key, goals, 300)
    return goals