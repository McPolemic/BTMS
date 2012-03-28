from django.test import TestCase, Client
from datetime import date
from models import Status,Task
import utils

class TestUtils(TestCase):
    def test_find_start_date_from_date(self):
        t = date(2012, 3, 28)
        d = utils.find_start_date_from_date(t)
        self.assertEquals(d, date(2012, 3, 25))

    def test_string_date_to_date(self):
        d = utils.string_date_to_date('20110101')
        self.assertEquals(d, date(2011,1,1))

class TestModels(TestCase):
    def setUp(self):
        pass

    def test_status_create(self):
        s = Status(co_num = 14456,
                   description = 'Sample Status',
                   role = 'Developer')
        s.save()
        status = str(s)

    def test_status_create(self):
        s = Status(co_num = 14456,
                   description = 'Sample Status',
                   role = 'Developer')
        s.save()
        t = Task(user = "adam",
                 date = date.today(),
                 status = s,
                 total_minutes = 13)
        t.save()
        status = str(s)
        task = str(t)

class TestViews(TestCase):
    def setUp(self):
        s = Status(co_num = 14456,
                   description = 'Sample Status',
                   role = 'Developer')
        s.save()
        t = Task(user = "adam",
                 date = date(2012, 3, 18),
                 status = s,
                 total_minutes = 90)
        t.save()
        t2 = Task(user = "adam",
                  date = date(2012, 3, 19),
                  status = s,
                  total_minutes = 120)
        t2.save()

    def test_index_redirect(self):
        response = self.client.get('/')
        self.assertEquals(302, response.status_code)
        (year, month, day) = response['Location'].split('/')[-4:-1]
        today = date.today()
        self.assertEquals(today.month, int(month))
        self.assertEquals(today.day,   int(day))
        self.assertEquals(today.year,  int(year))

    def test_correct_day_of_week(self):
        # 3/18/2012 is a Sunday (values offset 0)
        # 3/19/2012 is a Monday (values offset 1)
        response = self.client.get('/entry/2012/3/18/')
        self.assertEquals(response.context['week'][0]['status'].co_num, 14456)
        self.assertEquals(response.context['week'][0]['status'].role, 'Developer')
        self.assertEquals(response.context['week'][0]['status'].description, 'Sample Status')
        self.assertEquals(response.context['week'][0]['values'][0]['value'], 1.5)
        self.assertEquals(response.context['week'][0]['values'][1]['value'], 2)

    def test_correct_status_total(self):
        # 3/18/2012 is a Sunday (values offset 0)
        response = self.client.get('/entry/2012/3/18/')
        self.assertEquals(response.context['week'][0]['status'].co_num, 14456)
        self.assertEquals(response.context['week'][0]['status'].role, 'Developer')
        self.assertEquals(response.context['week'][0]['status'].description, 'Sample Status')
        self.assertEquals(response.context['week'][0]['total'], 3.5)

#Expects something like
# [{'total': 0.2, 'values': [0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.0], 'name': '14456 - Developer - Sample Status'},
#  {'values': [0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.0], 'name': 'Total'}]

