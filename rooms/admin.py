from django.contrib import admin
from . import models


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    pass


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ Room Admin Definition """

    list_display = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "adddress",
        "guests",
        "beds",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
    )

    list_filter = ("instant_book", "city", "country")

    search_fields = ("=city", "^host__username")


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Definition """

    pass
