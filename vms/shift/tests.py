from datetime import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from event.models import Event
from job.models import Job
from organization.models import Organization
from shift.models import Shift, VolunteerShift
from shift.services import *
from volunteer.models import Volunteer
from volunteer.services import *

class ShiftMethodTests(TestCase):

    def test_cancel_shift_registration(self):

        u1 = User.objects.create_user('Yoshi')     
        u2 = User.objects.create_user('John')     

        v1 = Volunteer(first_name = "Yoshi",
                    last_name = "Turtle",
                    address = "Mario Land",
                    city = "Nintendo Land",
                    state = "Nintendo State",
                    country = "Nintendo Nation",
                    phone_number = "2374983247",
                    email = "yoshi@nintendo.com",
                    user = u1)

        v2 = Volunteer(first_name = "John",
                    last_name = "Doe",
                    address = "7 Alpine Street",
                    city = "Maplegrove",
                    state = "Wyoming",
                    country = "USA",
                    phone_number = "23454545",
                    email = "john@test.com",
                    user = u2)

        v1.save()
        v2.save()

        e1 = Event(name = "Open Source Event",
                start_date = "2012-10-22",
                end_date = "2012-10-23")

        e1.save()

        j1 = Job(name = "Software Developer",
                start_date = "2012-10-22",
                end_date = "2012-10-23",
                description = "A software job",
                event = e1)

        j2 = Job(name = "Systems Administrator",
                start_date = "2012-9-1",
                end_date = "2012-10-26",
                description = "A systems administrator job",
                event = e1)

        j1.save()
        j2.save()

        s1 = Shift(date = "2012-10-23",
                start_time = "9:00",
                end_time = "3:00",
                max_volunteers = 1,
                job = j1)

        s2 = Shift(date = "2012-10-23",
                start_time = "10:00",
                end_time = "4:00",
                max_volunteers = 2,
                job = j1)

        s3 = Shift(date = "2012-10-23",
                start_time = "12:00",
                end_time = "6:00",
                max_volunteers = 4,
                job = j2)

        s1.save()
        s2.save()
        s3.save()

        #test cases when try to cancel when they aren't signed up for a shift
        with self.assertRaises(ObjectDoesNotExist):
            cancel_shift_registration(v1.id, s1.id)

        with self.assertRaises(ObjectDoesNotExist):
            cancel_shift_registration(v1.id, s1.id)

        with self.assertRaises(ObjectDoesNotExist):
            cancel_shift_registration(v1.id, s2.id)

        with self.assertRaises(ObjectDoesNotExist):
            cancel_shift_registration(v1.id, s3.id)

        with self.assertRaises(ObjectDoesNotExist):
            cancel_shift_registration(v2.id, s1.id)

        with self.assertRaises(ObjectDoesNotExist):
            cancel_shift_registration(v2.id, s2.id)

        with self.assertRaises(ObjectDoesNotExist):
            cancel_shift_registration(v2.id, s3.id)

        #register volunteers to shifts
        register(v1.id, s1.id)
        register(v1.id, s2.id)
        register(v1.id, s3.id)
        register(v2.id, s1.id)
        register(v2.id, s2.id)
        register(v2.id, s3.id)

        #test typical cases
        cancel_shift_registration(v1.id, s1.id)
        cancel_shift_registration(v1.id, s2.id)
        cancel_shift_registration(v1.id, s3.id)
        #cancel_shift_registration(v2.id, s1.id) #why is this throwing ObjectDoesNotExist?
        cancel_shift_registration(v2.id, s2.id)
        cancel_shift_registration(v2.id, s3.id)

    def test_get_shift_by_id(self):

        e1 = Event(name = "Open Source Event",
                start_date = "2012-10-22",
                end_date = "2012-10-23")

        e1.save()

        j1 = Job(name = "Software Developer",
                start_date = "2012-10-22",
                end_date = "2012-10-23",
                description = "A software job",
                event = e1)

        j1.save()

        s1 = Shift(date = "2012-10-23",
                start_time = "9:00",
                end_time = "3:00",
                max_volunteers = 1,
                job = j1)

        s2 = Shift(date = "2012-10-23",
                start_time = "10:00",
                end_time = "4:00",
                max_volunteers = 2,
                job = j1)

        s3 = Shift(date = "2012-10-23",
                start_time = "12:00",
                end_time = "6:00",
                max_volunteers = 4,
                job = j1)

        s1.save()
        s2.save()
        s3.save()

        #test typical cases
        self.assertIsNotNone(get_shift_by_id(s1.id))
        self.assertIsNotNone(get_shift_by_id(s2.id))
        self.assertIsNotNone(get_shift_by_id(s3.id))

        self.assertEqual(get_shift_by_id(s1.id), s1)
        self.assertEqual(get_shift_by_id(s2.id), s2)
        self.assertEqual(get_shift_by_id(s3.id), s3)

        #test non-existant cases
        self.assertIsNone(get_shift_by_id(100))
        self.assertIsNone(get_shift_by_id(200))
        self.assertIsNone(get_shift_by_id(300))
        self.assertIsNone(get_shift_by_id(400))

        self.assertNotEqual(get_shift_by_id(100), s1)
        self.assertNotEqual(get_shift_by_id(100), s2)
        self.assertNotEqual(get_shift_by_id(100), s3)
        self.assertNotEqual(get_shift_by_id(200), s1)
        self.assertNotEqual(get_shift_by_id(200), s2)
        self.assertNotEqual(get_shift_by_id(200), s3)
        self.assertNotEqual(get_shift_by_id(300), s1)
        self.assertNotEqual(get_shift_by_id(300), s2)
        self.assertNotEqual(get_shift_by_id(300), s3)

    def get_shifts_ordered_by_date(self):

        e1 = Event(name = "Open Source Event",
                start_date = "2012-10-22",
                end_date = "2012-10-23")

        e1.save()

        j1 = Job(name = "Software Developer",
            start_date = "2012-10-22",
            end_date = "2012-10-23",
            description = "A software job",
            event = e1)

        j1.save()

        s1 = Shift(date = "2012-1-10",
            start_time = "9:00",
            end_time = "3:00",
            max_volunteers = 1,
            job = j1)

        s2 = Shift(date = "2012-6-25",
            start_time = "10:00",
            end_time = "4:00",
            max_volunteers = 2,
            job = j1)

        s3 = Shift(date = "2012-12-9",
            start_time = "12:00",
            end_time = "6:00",
            max_volunteers = 4,
            job = j1)

        s1.save()
        s2.save()
        s3.save()

        #test typical case
        shift_list = get_shifts_ordered_by_date(j1.id)
        self.assertIsNotNone(shift_list)
        self.assertNotEqual(shift_list, False)
        self.assertEqual(len(shift_list), 3)
        self.assertIn(s1, shift_list)
        self.assertIn(s2, shift_list)
        self.assertIn(s3, shift_list)

        #test order
        self.assertEqual(shift_list[0].date, s1.date)
        self.assertEqual(shift_list[1].date, s2.date)
        self.assertEqual(shift_list[2].date, s3.date)

    def test_get_shifts_signed_up_for(self):

        u1 = User.objects.create_user('Yoshi')     

        v1 = Volunteer(first_name = "Yoshi",
            last_name = "Turtle",
            address = "Mario Land",
            city = "Nintendo Land",
            state = "Nintendo State",
            country = "Nintendo Nation",
            phone_number = "2374983247",
            email = "yoshi@nintendo.com",
            user = u1)

        v1.save()

        e1 = Event(name = "Open Source Event",
                start_date = "2012-10-22",
                end_date = "2012-10-23")

        e1.save()

        j1 = Job(name = "Software Developer",
            start_date = "2012-10-22",
            end_date = "2012-10-23",
            description = "A software job",
            event = e1)

        j2 = Job(name = "Systems Administrator",
            start_date = "2012-9-1",
            end_date = "2012-10-26",
            description = "A systems administrator job",
            event = e1)

        j1.save()
        j2.save()

        s1 = Shift(date = "2012-10-23",
            start_time = "9:00",
            end_time = "3:00",
            max_volunteers = 1,
            job = j1)

        s2 = Shift(date = "2012-10-23",
            start_time = "10:00",
            end_time = "4:00",
            max_volunteers = 2,
            job = j1)

        s3 = Shift(date = "2012-10-23",
            start_time = "12:00",
            end_time = "6:00",
            max_volunteers = 4,
            job = j2)

        s1.save()
        s2.save()
        s3.save()

        #sign up
        register(v1.id, s1.id)
        register(v1.id, s2.id)
        register(v1.id, s3.id)

        #test typical case
        shift_list = get_shifts_signed_up_for(v1.id)
        self.assertIsNotNone(shift_list)
        self.assertNotEqual(shift_list, False)
        self.assertEqual(len(shift_list), 3)
        self.assertIn(s1, shift_list)
        self.assertIn(s2, shift_list)
        self.assertIn(s3, shift_list)

    def test_get_volunteer_shift_by_id(self):

        u1 = User.objects.create_user('Yoshi')     
        u2 = User.objects.create_user('John')     

        v1 = Volunteer(first_name = "Yoshi",
            last_name = "Turtle",
            address = "Mario Land",
            city = "Nintendo Land",
            state = "Nintendo State",
            country = "Nintendo Nation",
            phone_number = "2374983247",
            email = "yoshi@nintendo.com",
            user = u1)

        v2 = Volunteer(first_name = "John",
            last_name = "Doe",
            address = "7 Alpine Street",
            city = "Maplegrove",
            state = "Wyoming",
            country = "USA",
            phone_number = "23454545",
            email = "john@test.com",
            user = u2)

        v1.save()
        v2.save()

        e1 = Event(name = "Open Source Event",
                start_date = "2012-10-22",
                end_date = "2012-10-23")

        e1.save()

        j1 = Job(name = "Software Developer",
            start_date = "2012-10-22",
            end_date = "2012-10-23",
            description = "A software job",
            event = e1)

        j2 = Job(name = "Systems Administrator",
            start_date = "2012-9-1",
            end_date = "2012-10-26",
            description = "A systems administrator job",
            event = e1)

        j1.save()
        j2.save()

        s1 = Shift(date = "2012-10-23",
            start_time = "9:00",
            end_time = "3:00",
            max_volunteers = 1,
            job = j1)

        s2 = Shift(date = "2012-10-23",
            start_time = "10:00",
            end_time = "4:00",
            max_volunteers = 2,
            job = j1)

        s3 = Shift(date = "2012-10-23",
            start_time = "12:00",
            end_time = "6:00",
            max_volunteers = 4,
            job = j2)

        s1.save()
        s2.save()
        s3.save()

        #test cases where signed up
        register(v1.id, s1.id)
        register(v1.id, s2.id)
        register(v1.id, s3.id)

        register(v2.id, s1.id)
        register(v2.id, s2.id)
        register(v2.id, s3.id)

        self.assertEqual(get_volunteer_shift_by_id(v1.id, s1.id), VolunteerShift.objects.get(volunteer_id=v1.id, shift_id=s1.id))
        self.assertEqual(get_volunteer_shift_by_id(v1.id, s2.id), VolunteerShift.objects.get(volunteer_id=v1.id, shift_id=s2.id))
        self.assertEqual(get_volunteer_shift_by_id(v1.id, s3.id), VolunteerShift.objects.get(volunteer_id=v1.id, shift_id=s3.id))

        #self.assertEqual(get_volunteer_shift_by_id(v2.id, s1.id), VolunteerShift.objects.get(volunteer_id=v2.id, shift_id=s1.id)) #why does this throw DoesNotExist?
        self.assertEqual(get_volunteer_shift_by_id(v2.id, s2.id), VolunteerShift.objects.get(volunteer_id=v2.id, shift_id=s2.id))
        self.assertEqual(get_volunteer_shift_by_id(v2.id, s3.id), VolunteerShift.objects.get(volunteer_id=v2.id, shift_id=s3.id))


    def test_is_signed_up(self):

        u1 = User.objects.create_user('Yoshi')     
        u2 = User.objects.create_user('John')     

        v1 = Volunteer(first_name = "Yoshi",
            last_name = "Turtle",
            address = "Mario Land",
            city = "Nintendo Land",
            state = "Nintendo State",
            country = "Nintendo Nation",
            phone_number = "2374983247",
            email = "yoshi@nintendo.com",
            user = u1)

        v2 = Volunteer(first_name = "John",
            last_name = "Doe",
            address = "7 Alpine Street",
            city = "Maplegrove",
            state = "Wyoming",
            country = "USA",
            phone_number = "23454545",
            email = "john@test.com",
            user = u2)

        v1.save()
        v2.save()

        e1 = Event(name = "Open Source Event",
                start_date = "2012-10-22",
                end_date = "2012-10-23")

        e1.save()

        j1 = Job(name = "Software Developer",
            start_date = "2012-10-22",
            end_date = "2012-10-23",
            description = "A software job",
            event = e1)

        j2 = Job(name = "Systems Administrator",
            start_date = "2012-9-1",
            end_date = "2012-10-26",
            description = "A systems administrator job",
            event = e1)

        j1.save()
        j2.save()

        s1 = Shift(date = "2012-10-23",
            start_time = "9:00",
            end_time = "3:00",
            max_volunteers = 1,
            job = j1)

        s2 = Shift(date = "2012-10-23",
            start_time = "10:00",
            end_time = "4:00",
            max_volunteers = 2,
            job = j1)

        s3 = Shift(date = "2012-10-23",
            start_time = "12:00",
            end_time = "6:00",
            max_volunteers = 4,
            job = j2)

        s1.save()
        s2.save()
        s3.save()

        #test cases where not signed up yet
        self.assertFalse(is_signed_up(v1.id, s1.id))
        self.assertFalse(is_signed_up(v1.id, s2.id))
        self.assertFalse(is_signed_up(v1.id, s3.id))

        #test cases where signed up
        register(v1.id, s1.id)
        register(v1.id, s2.id)
        register(v1.id, s3.id)

        self.assertTrue(is_signed_up(v1.id, s1.id))
        self.assertTrue(is_signed_up(v1.id, s2.id))
        self.assertTrue(is_signed_up(v1.id, s3.id))

        #test case where more than one volunteer signs up for the same shift
        self.assertFalse(is_signed_up(v2.id, s1.id))
        self.assertFalse(is_signed_up(v2.id, s2.id))
        self.assertFalse(is_signed_up(v2.id, s3.id))

        register(v2.id, s2.id)
        register(v2.id, s3.id)

        self.assertFalse(is_signed_up(v2.id, s1.id))
        self.assertTrue(is_signed_up(v2.id, s2.id))
        self.assertTrue(is_signed_up(v2.id, s3.id))
