from django.contrib import admin

from rating.models import StarRating


class StarRatingAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'research', 'user_type', 'time_score', 'attitude_score')

admin.site.register(StarRating, StarRatingAdmin)