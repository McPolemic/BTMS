from django.db import models

"""A CO/Status Combination

This represents one unique thing that a user can do."""
class Status(models.Model):
    STATUS_ROLES = (('D', 'Developer'),
                    ('T', 'TFAL'),
                    ('P', 'PM'),
                    ('B', 'Business Analyst'),
                    ('E', 'Tester'),
                   )
    role = models.CharField(max_length=1, choices=STATUS_ROLES)

    co_num = models.IntegerField('CO Number', blank=True, null=True)
    description = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Statuses'

    def __unicode__(self):
        if self.co_num:
            return '%d - %s - %s' % (self.co_num, self.role, self.description)
        else:
            return '%s - %s' % (self.role, self.description)

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
