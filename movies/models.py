from django.db import models

class Movie(models.Model):
    title=models.CharField(max_length=250)
    price=models.IntegerField()
    booked_seats=models.ManyToManyField('Seat',blank=True)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.title} ${self.price}"


class Seat(models.Model):
    seat_no=models.IntegerField()
    occupant_first_name=models.CharField(max_length=250)
    occupant_last_name=models.CharField(max_length=250)
    occupant_email=models.EmailField(max_length=500)
    purchase_time=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.occupant_first_name} {self.occupant_last_name} seat_no {self.seat_no}"

