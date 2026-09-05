from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
import json

from main.choices import StatusChoices
from main.models import Advertisement, Category, SavedAd


class ArchiveActiveAdAjaxViewTest(TestCase):

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


    def test_active_to_archive_ajax(self):
    
        # INPUT: отправляем POST-запрос
        response = self.client.post(
            reverse("main:archive_ad_ajax", kwargs={"pk": self.ad.pk})
        )

        # OUTPUT: проверяем, что объявление стало ARCHIVED
        self.ad.refresh_from_db()

        self.assertEqual(self.ad.status, StatusChoices.ARCHIVED)

        # OUTPUT: проверяем JSON
        self.assertEqual(response.json()["status"], "success")
        self.assertEqual(response.json()["ad_id"], self.ad.pk)




    def test_from_archive_to_active_ajax(self):
       

        response = self.client.post(
            reverse("main:from_archive_ajax", kwargs={"pk": self.ad.pk})
        )

        self.ad.refresh_from_db()

        self.assertEqual(self.ad.status, StatusChoices.ACTIVE)

        self.assertEqual(response.json()["status"], "success")
        self.assertEqual(response.json()["ad_id"], self.ad.pk)








class DeleteChangeAdTest(TestCase):

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


    def test_delete_ad_ajax_from_my_ads(self):

        # POST: Тут мы проверяем правильный ли request.method == POST и отправляем на функцию
        response = self.client.post(
            reverse("main:delete_ad_ajax", kwargs={"pk": self.ad.pk})
        )

        # Тут после удаления мы тестим осталось ли то самое ad в БД и это главная проверка в этом тесте
        self.assertFalse(Advertisement.objects.filter(pk=self.ad.pk).exists())

        # Тут проверяет правильно ли без error функция выдаёт success
        self.assertEqual(response.json()["status"], "success")
        self.assertEqual(response.json()["ad_id"], self.ad.pk)



    def test_change_ad_ajax_from_my_ads_GET(self):
        # Тест уже имеет авторизацию с setUp(), user, advertisement подготовили данные для теста
        # И теперь заходим внутрь функции по запросу GET чтобы просто вывести форму
        response = self.client.get(
            reverse("main:change_ad_ajax", kwargs={"pk": self.ad.pk})
        )

        # Проверяем работает ли функция без error + success
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json()["status"], "success")
        # Выводим форму по запросу GET : edit
        self.assertIn("edit", response.json())
        
        
        
        
    
    
    def test_change_ad_ajax_from_my_ads_POST(self):
        
        response = self.client.post(
            reverse("main:change_ad_ajax", kwargs={"pk": self.ad.pk}),
            data={
                "category": self.category.pk,
                "title": "Updated advertisement",
                "price": 200,
                "description": "Updated description for testing the advertisement form",
                "contact_person": "Updated User",
                "phone": "+998901234567",
            }
        )
        
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data["status"], "success")
        self.assertIn("content", data)

        self.ad.refresh_from_db()

        self.assertEqual(self.ad.title, "Updated advertisement")
        self.assertEqual(self.ad.price, 200)
        self.assertEqual(self.ad.description, "Updated description for testing the advertisement form")
        self.assertEqual(self.ad.contact_person, "Updated User")
        self.assertEqual(self.ad.phone, "+998901234567")
        
        
        
        
        
        
        
class MyAdsPageTest(TestCase):
    
    def test_my_ads_list_ajax(self):
        # INPUT: создаём пользователя
        user = User.objects.create_user(
            username="user_a",
            password="password123",
        )

        # INPUT: создаём категорию,
        # потому что Advertisement требует category
        category = Category.objects.create(
            name="Test category",
        )

        # INPUT: создаём ACTIVE-объявление,
        # автором которого является user
        ad = Advertisement.objects.create(
            category=category,
            title="Test advertisement",
            price=100,
            author=user,
            description="Test description",
            status=StatusChoices.ACTIVE,
        )

        # INPUT: пользователь авторизован
        self.client.force_login(user)
        
        response = self.client.get(
            reverse("main:my_ads_list_ajax")
            )
        
        # Проверяем работает ли функция без error + success
        self.assertEqual(response.status_code, 200)
        print(response.json())

        self.assertEqual(response.json()["status"], "success")
        # Выводим форму по запросу GET : content
        self.assertIn("content", response.json())
        
        
        
        
        
        
        
class SaveToFavorite(TestCase):
    
    def test_save_favorite_ad_ajax(self):
        # INPUT: создаём пользователя
        user = User.objects.create_user(
            username="user_a",
            password="password123",
        )

        # INPUT: создаём категорию,
        # потому что Advertisement требует category
        category = Category.objects.create(
            name="Test category",
        )

        # INPUT: создаём ACTIVE-объявление,
        # автором которого является user
        ad = Advertisement.objects.create(
            category=category,
            title="Test advertisement",
            price=100,
            author=user,
            description="Test description",
            status=StatusChoices.ACTIVE,
        )

        # INPUT: пользователь авторизован
        self.client.force_login(user)
        
        self.assertFalse(SavedAd.objects.filter(user=user, advertisement=ad).exists())
        # self.assertTrue(SavedAd.objects.filter(user=user, advertisement=ad).exists())

        
        
        response = self.client.post(
            reverse("main:save_favorite_ad_ajax", kwargs={"pk": ad.pk}),
            data=json.dumps({
                "message": "Успешно добавлено",
            }),
            content_type="application/json",
        )
        
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")
        
        self.assertTrue(SavedAd.objects.filter(user=user, advertisement=ad).exists())
        





class AdDetailTest(TestCase):
    
    def test_ad_detail_view(self):
        # INPUT: создаём пользователя
        user = User.objects.create_user(
            username="user_a",
            password="password123",
        )

        # INPUT: создаём категорию,
        # потому что Advertisement требует category
        category = Category.objects.create(
            name="Test category",
        )

        # INPUT: создаём ACTIVE-объявление,
        # автором которого является user
        ad = Advertisement.objects.create(
            category=category,
            title="Test advertisement",
            price=100,
            author=user,
            description="Test description",
            status=StatusChoices.ACTIVE,
        )

        # INPUT: пользователь авторизован
        self.client.force_login(user)
        
        response = self.client.get(
            reverse("main:ad_detail", kwargs={"pk": ad.pk})
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/ad-detail.html")
        

        
        

        
        
        
        
    