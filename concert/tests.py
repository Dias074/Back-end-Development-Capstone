from unittest.mock import patch, Mock
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Concert, ConcertAttending


class WebsiteTests(TestCase):
    def setUp(self):
        self.concert = Concert.objects.create(concert_name='Astana Live', duration=90,
                                              city='Astana', date='2027-06-01')

    def test_home_and_concert_list(self):
        self.assertEqual(self.client.get('/').status_code, 200)
        self.assertContains(self.client.get('/concerts/'), 'Astana Live')

    def test_login_required_for_details(self):
        self.assertEqual(self.client.get('/concert-detail/1').status_code, 302)

    def test_signup_login_logout(self):
        response = self.client.post('/signup/', {'username': 'learner', 'password': 'test-only-password-347'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.get(username='learner').check_password('test-only-password-347'))
        self.client.get('/logout/')
        response = self.client.post('/login/', {'username': 'learner', 'password': 'test-only-password-347'})
        self.assertEqual(response.status_code, 302)
        self.assertIn('_auth_user_id', self.client.session)

    def test_attendance_changes_and_validation(self):
        user = User.objects.create_user('tester')
        self.client.force_login(user)
        response = self.client.post('/concert_attendee/', {'concert_id': self.concert.pk, 'attendee_choice': 'Attending'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ConcertAttending.objects.get(user=user).attending, 'Attending')
        response = self.client.post('/concert_attendee/', {'concert_id': self.concert.pk, 'attendee_choice': 'Invalid'})
        self.assertEqual(response.status_code, 400)

    @patch('concert.views.req.get')
    def test_song_service_rendering(self, get):
        get.return_value = Mock(json=lambda: {'songs': [{'id': 1, 'title': 'Test melody', 'lyrics': 'Words of the song'}]})
        self.assertContains(self.client.get('/songs/'), 'Test melody')
        self.assertContains(self.client.get('/songs/'), 'Words of the song')

    @patch('concert.views.req.get')
    def test_picture_service_rendering(self, get):
        get.return_value = Mock(json=lambda: [{'id': 1, 'pic_url': 'https://example.org/photo.jpg', 'event_city': 'Astana', 'event_country': 'Kazakhstan', 'event_state': '', 'event_date': '2027-06-01'}])
        self.assertContains(self.client.get('/photos/'), 'photo.jpg')

    def test_admin_login_page(self):
        self.assertEqual(self.client.get('/admin/login/').status_code, 200)
