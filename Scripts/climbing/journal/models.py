from django.db import models

class Location(models.Model):
    location_type = models.CharField(max_length=200)
    name = models.CharField(max_length=10000)
    parent_location = models.ForeignKey('self',
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL,
                                        related_name='child_location')

    def __str__(self):
        if not self.parent_location:
            return self.name
        return str(self.parent_location) + " * " + self.name

# class Problem(Location):
#     grade = models.CharField(max_length=100)
#     sent = models.BoolField()
#     project = models.BoolField()

#     def __str__(self):
#         if not self.parent_location:
#             return self.name
#         return str(self.parent_location) + " * " + self.name


class Note(models.Model):
    note_type = models.CharField(max_length=200)
    content = models.CharField(max_length=10000)
    location = models.ForeignKey(Location, on_delete=models.CASCADE,
                                 null=True,
                                 blank=True,
                                 related_name='notes')
    date = models.DateField()

    def __str__(self):
        return str(self.location) + ": " + str(self.date) + " - " + self.content


# Create your models here.
