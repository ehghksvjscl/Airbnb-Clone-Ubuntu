from django.db import models
from django_countries.fields import CountryField
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

    pass


class Amenity(AbstractItem):

    """ Amenity Object Definition """

    pass


class Facility(AbstractItem):

    """ Facility Object Definition """

    pass


class HouseRule(AbstractItem):

    """ HouseRule Object Definition """

    pass


class Room(core_models.TimeStampedModel):

    """ Room Model Definition """

    # DB정의
    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    adddress = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(users_models.User, on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True)
    amenities = models.ManyToManyField(Amenity)
    facilities = models.ManyToManyField(Facility)
    house_rules = models.ManyToManyField(HouseRule)

    # Admin에 보여줄 텍스트 정의
    def __str__(self):
        return self.name
