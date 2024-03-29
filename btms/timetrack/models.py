from django.db import models

"""A CO/Status Combination

This represents one unique thing that a user can do."""
class Status(models.Model):
    co_num = models.IntegerField('CO Number', blank=True, null=True)
    description = models.CharField(max_length=50)
    role = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Statuses'

    def __unicode__(self):
        return_string = ''
        if self.co_num:
            return_string += '%d - ' % self.co_num
        if self.role:
            return_string += '%s - ' % self.role
        return_string += self.description
        return return_string

"""Task that happened in a workday"""
class Task(models.Model):
    user = models.CharField(max_length=30)
    date = models.DateField()
    status = models.ForeignKey(Status)
    total_minutes = models.IntegerField()

    def _get_hours(self):
        return self.total_minutes/60

    hours = property(_get_hours)
    
    def _get_minutes(self):
        return self.total_minutes - (self.hours*60)

    minutes = property(_get_minutes)

    def frac_hours(self):
        return round((float(self.total_minutes)/60), 1)
    
    def english_time(self):
        return '%d:%02d' % (self.hours, self.minutes)

    english_time.short_description = "Time"
    frac_hours.short_description = "Hours (Fraction)"

    def __unicode__(self):
        return '%s - %s - %s' % (self.user, self.date, self.status)

"""A MyTask is a Status tied to a user for quick use"""
class MyTask(models.Model):
    user = models.CharField(max_length=30)
    status = models.ForeignKey(Status)

    class Meta:
        verbose_name_plural = 'My Tasks'

    def __unicode__(self):
        return '%s - %s' % (self.user, self.status)
