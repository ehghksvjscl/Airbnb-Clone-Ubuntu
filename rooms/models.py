from django.db import models
from django_countries.fields import CountryField
from django.urls import reverse
from django.utils import timezone

from cal import Calendar
from users import models as users_models
from core import models as core_models


class AbstractItem(core_models.TimeStampedModel):

    """ Abstract Item """

    # DB정의
    name = models.CharField(max_length=80)

    # 추상화
    class Meta:
        abstract = True

    # 문자열
    def __str__(self):
        return self.name


class RoomType(AbstractItem):

    """ Room Type Object Definition """

    class Meta:
        verbose_name_plural = "Room Type"


class Amenity(AbstractItem):

    """ Amenity Object Definition """

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):

    """ Facility Object Definition """

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):

    """ HouseRule Object Definition """

    class Meta:
        verbose_name = "House Rule"


class Photo(core_models.TimeStampedModel):

    """ Photo Objdect Definition """

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="room_photos")

    # Photo가 위에 있는데도 아래에 있는 Room class를 사용하고 싶다면 문자열로 만들면 된다.
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):

    """ Room Model Definition """

    # DB정의
    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField(default=0)
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(
        users_models.User, related_name="rooms", on_delete=models.CASCADE
    )
    room_type = models.ForeignKey(
        RoomType, related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    amenities = models.ManyToManyField(Amenity, related_name="rooms", blank=True)
    facilities = models.ManyToManyField(Facility, related_name="rooms", blank=True)
    house_rules = models.ManyToManyField(HouseRule, related_name="rooms", blank=True)

    # super은 상속하는데 부모의 기능을 살리는 기능이다 부모 + 자식 기능을 모두 할 수 있다.
    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        super().save(*args, **kwargs)

    # Url 오버라이딩 room 관리자 페이지에 바로가기 버튼이 만들어 진다.
    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    # Admin에 보여줄 텍스트 정의
    def __str__(self):
        return self.name

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0

        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += review.rating_average()
            return round(all_ratings / len(all_reviews), 2)
        return 0

    def first_photo(self):
        try:
            (photo,) = self.photos.all()[:1]
            return photo.file.url
        except ValueError:
            return None

    def get_next_four_photos(self):
        photos = self.photos.all()[1:5]
        # print(photos)
        return photos

    def get_beds(self):
        if self.beds == 1:
            return "1 bed"
        else:
            return f"{self.beds} beds"

    def get_calendars(self):
        now = timezone.now()
        this_year = now.year
        this_month = now.month
        next_month = this_month +1
        if this_month == 12:
            next_month = 1
        this_month_cal = Calendar(this_year, this_month)
        next_month_cal = Calendar(this_year, next_month)
        return [this_month_cal, next_month_cal]
