from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post, Profil
from django.test import TestCase, Client
from django.urls import reverse
from .forms import PostForma
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

class PostModelTest(TestCase):
    """Post modeli testlari"""

    def setUp(self):
        """Har bir test dan oldin ishga tushadi"""
        self.user = User.objects.create_user(
            username='test_user',
            password='test_parol123'
        )

        self.post = Post.objects.create(
            sarlavha='Test Post',
            matn='Bu test uchun post',
            muallif=self.user,
            nashr_etilgan=True
        )

    def test_post_yaratildi(self):
        """Post yaratilganini tekshirish"""
        self.assertEqual(self.post.sarlavha, 'Test Post')
        self.assertEqual(self.post.muallif.username, 'test_user')
        self.assertTrue(self.post.nashr_etilgan)

    def test_post_str(self):
        """Post __str__ metodi"""
        self.assertEqual(str(self.post), 'Test Post')

    def test_post_soni(self):
        """Jami postlar soni"""
        postlar_soni = Post.objects.count()
        self.assertEqual(postlar_soni, 1)





class BoshSahifaTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='test_user',
            password='test_parol123'
        )

        # Test postlar yaratish
        for i in range(5):
            Post.objects.create(
                sarlavha=f'Post {i+1}',
                matn=f'Bu {i+1}-post matni',
                muallif=self.user,
                nashr_etilgan=True
            )

    def test_bosh_sahifa_ochiladi(self):
        """Bosh sahifa ochilishini tekshirish"""
        response = self.client.get(reverse('bosh_sahifa'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/bosh.html')

    def test_postlar_korsatiladi(self):
        """Postlar sahifada ko'rinishini tekshirish"""
        response = self.client.get(reverse('bosh_sahifa'))

        self.assertEqual(len(response.context['postlar']), 5)
        self.assertContains(response, 'Post 1')
        self.assertContains(response, 'Post 5')

    def test_nashr_etilmaganlar_korinmaydi(self):
        """Nashr etilmagan postlar ko'rinmasligi"""
        post = Post.objects.create(
            sarlavha='Post nash etilmagan',
            matn='Bu post nashr etilmagan',
            muallif=self.user,
            nashr_etilgan=False
        )

        response = self.client.get(reverse('bosh_sahifa'))

        self.assertNotContains(response, 'Post nash etilmagan')



class PostFormaTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            password='test_parol123'
        )

    def test_forma_togri_maydonlar(self):
        """Forma to'g'ri maydonlarga ega"""
        forma = PostForma()
        self.assertIn('sarlavha', forma.fields)
        self.assertIn('matn', forma.fields)

    def test_forma_togri_malumot(self):
        """To'g'ri ma'lumot bilan forma valid"""
        forma = PostForma(data={
            'sarlavha': 'Test sarlavha',
            'matn': 'Test matn'
        })
        self.assertTrue(forma.is_valid())

    def test_forma_bosh_sarlavha(self):
        """Bo'sh sarlavha bilan forma invalid"""
        forma = PostForma(data={
            'sarlavha': '',
            'matn': 'Test matn'
        })
        self.assertFalse(forma.is_valid())
        self.assertIn('sarlavha', forma.errors)

    def test_forma_uzun_sarlavha(self):
        """Juda uzun sarlavha (200+ belgi) invalid"""
        forma = PostForma(data={
            'sarlavha': 'a' * 201,  # 201 ta 'a' harfi
            'matn': 'Test matn'
        })
        self.assertFalse(forma.is_valid())


class PostAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            password='test_parol123'
        )
        self.token = Token.objects.create(user=self.user)

        self.post = Post.objects.create(
            sarlavha='API Test Post',
            matn='API uchun test post',
            muallif=self.user,
            nashr_etilgan=True
        )

    def test_postlar_olish(self):
        """GET /api/{version}/postlar/ - barcha postlar"""
        url = reverse('post-list', kwargs={'version': 'v1'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_bitta_post_olish(self):
        """GET /api/{version}/postlar/{id}/ - bitta post"""
        url = reverse('post-detail', kwargs={'version': 'v1', 'pk': self.post.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['sarlavha'], 'API Test Post')

    def test_post_yaratish_tokensiz(self):
        """POST /api/{version}/postlar/ - tokensiz (xato)"""
        url = reverse('post-list', kwargs={'version': 'v1'})
        data = {
            'sarlavha': 'Yangi post',
            'matn': 'Yangi post matni'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_yaratish_token_bilan(self):
        """POST /api/{version}/postlar/ - token bilan"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        url = reverse('post-list', kwargs={'version': 'v1'})
        data = {
            'sarlavha': 'Token bilan yaratilgan',
            'matn': 'Bu post token bilan yaratildi'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)

    def test_boshqa_muallif_ozgartira_olmaydi(self):
        """Boshqa foydalanuvchi postni o'zgartira olmaydi"""
        boshqa_user = User.objects.create_user(
            username='boshqa_user',
            password='parol123'
        )
        boshqa_token = Token.objects.create(user=boshqa_user)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + boshqa_token.key)

        url = reverse('post-detail', kwargs={'version': 'v1', 'pk': self.post.id})
        data = {'sarlavha': 'O\'zgartirilgan'}
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


