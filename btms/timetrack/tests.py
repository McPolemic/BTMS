from django.utils import unittest
from datetime import date
from models import Status,Task

class TestModels(unittest.TestCase):

    def setUp(self):
        pass

    def test_status_create(self):
        s = Status(co_num = 14456,
                   description = 'Sample Status',
                   role = 'Developer')
        s.save()

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


if __name__=="__main__":
    unittest.main()
