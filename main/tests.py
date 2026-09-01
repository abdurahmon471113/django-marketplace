from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from main.choices import StatusChoices
from main.models import Advertisement, Category


class ArchiveAdAjaxViewTest(TestCase):

    def setUp(self):
        # INPUT: создаём пользователя
        self.user = User.objects.create_user(
            username="user_a",
            password="password123",
        )

        # INPUT: создаём категорию,
        # потому что Advertisement требует category
        self.category = Category.objects.create(
            name="Test category",
        )

        # INPUT: создаём ACTIVE-объявление,
        # автором которого является user
        self.ad = Advertisement.objects.create(
            category=self.category,
            title="Test advertisement",
            price=100,
            author=self.user,
            description="Test description",
            status=StatusChoices.ACTIVE,
        )

        # INPUT: пользователь авторизован
        self.client.force_login(self.user)


    def test_archive_active_ad_by_author(self):
    
        # INPUT: отправляем POST-запрос
        response = self.client.post(
            reverse("main:archive_ad_ajax", kwargs={"pk": self.ad.pk})
        )

        # OUTPUT: проверяем, что объявление стало ARCHIVED
        self.ad.refresh_from_db()
        self.assertEqual(self.ad.status, StatusChoices.ARCHIVED)

        # OUTPUT: проверяем HTTP-ответ
        self.assertEqual(response.status_code, 200)

        # OUTPUT: проверяем JSON
        self.assertEqual(response.json()["status"], "success")
        self.assertEqual(response.json()["ad_id"], self.ad.pk)




    def test_from_archive_active_ad_by_author(self):
       

        response = self.client.post(
            reverse("main:from_archive_ajax", kwargs={"pk": self.ad.pk})
        )

        self.ad.refresh_from_db()
        self.assertEqual(self.ad.status, StatusChoices.ACTIVE)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json()["status"], "success")
        self.assertEqual(response.json()["ad_id"], self.ad.pk)




