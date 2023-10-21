from django.test import TestCase

class TestHome(TestCase):
    def test_index(self):
        res = self.client.get('')
        self.assertEquals(res.status_code, 200)
