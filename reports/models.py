import datetime

from django.db import models


class ReportModel(models.Model):
    """
    The Report is the sum of all the emissions. It should be done once a year
    """
    name = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateField()


class SourceModel(models.Model):
    """
    An Emission is every source that generates GreenHouse gases (GHG).
    It could be defined as source x emission_factor = total
    """
    report = models.ForeignKey(ReportModel, on_delete=models.CASCADE, blank=True,
                               null=True)
    description = models.CharField(max_length=250, blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    emission_factor = models.FloatField(blank=True, null=True)
    total_emission = models.FloatField(blank=True, null=True, help_text="Unit in kg")
    lifetime = models.PositiveIntegerField(blank=True, null=True)
    acquisition_year = models.PositiveSmallIntegerField(blank=True, null=True)
