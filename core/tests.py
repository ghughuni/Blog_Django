from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .models import Post, Comment, ReplyComments, Likes_Unlikes, User_profiles
from .views import index, postDetails, index_by_tag, register, loginView, logout_view
from .forms import UserLoginForm, PostForm, UserProfileForm, CommentForm, UserProfileAddForm
from django.core.paginator import Paginator

#  Tests of models
# class PostModelTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             username="testuser", password="testpassword"
#         )
#         self.post = Post.objects.create(
#             author=self.user,
#             title="Test Post",
#             body="This is a test post",
#             slug="test-post",
#         )

#     def test_post_creation(self):
#         self.assertEqual(str(self.post), "Test Post|testuser")
#         self.assertIsNotNone(self.post.post_id)

# class CommentModelTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             username="testuser", password="testpassword"
#         )
#         self.post = Post.objects.create(
#             author=self.user,
#             title="Test Post",
#             body="This is a test post",
#             slug="test-post",
#         )
#         self.comment = Comment.objects.create(
#             post=self.post, author=self.user, content="This is a test comment"
#         )

#     def test_comment_creation(self):
#         self.assertEqual(
#             str(self.comment), "testuser - " + str(self.comment.created)
#         )

# class ReplyCommentsModelTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             username="testuser", password="testpassword"
#         )
#         self.post = Post.objects.create(
#             author=self.user,
#             title="Test Post",
#             body="This is a test post",
#             slug="test-post",
#         )
#         self.comment = Comment.objects.create(
#             post=self.post, author=self.user, content="This is a test comment"
#         )
#         self.reply = ReplyComments.objects.create(
#             parent_comment=self.comment,
#             post=self.post,
#             author=self.user,
#             content="This is a test reply",
#         )

#     def test_reply_creation(self):
#         self.assertEqual(
#             str(self.reply), "testuser - " + str(self.reply.created)
#         )

# class LikesUnlikesModelTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             username="testuser", password="testpassword"
#         )
#         self.post = Post.objects.create(
#             author=self.user,
#             title="Test Post",
#             body="This is a test post",
#             slug="test-post",
#         )
#         self.like_unlike = Likes_Unlikes.objects.create(
#             post=self.post, author=self.user, like=1, unlike=0
#         )

#     def test_likes_unlikes_creation(self):
#         self.assertEqual(self.like_unlike.like, 1)
#         self.assertEqual(self.like_unlike.unlike, 0)

# class UserProfilesModelTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             username="testuser", password="testpassword"
#         )
#         self.user_profile = User_profiles.objects.create(
#             author=self.user,
#             phone="(123) 456-7890",
#         )

#     def test_user_profile_creation(self):
#         self.assertEqual(str(self.user_profile), "testuser")


# Tests of views
class ViewsTest(TestCase):
    def setUp(self):
        # Create test user data for registration and login tests
        self.test_user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword', 
        }
        self.test_user = User.objects.create_user(
            username=self.test_user_data['username'],
            email=self.test_user_data['email'],
            password=self.test_user_data['password'],
        )
        for i in range(4):
            Post.objects.create(
                slug=f"TestSlug_{i}",
                author=self.test_user,
                title=f'Test Post {i}',
                body=f'Test Body {i}',
                views=i,
            )

        User_profiles.objects.create(author=self.test_user)     
    
    def test_post_details_view(self):
        self.client.login(username='testuser', password='testpassword')
        post = Post.objects.first()
        url = reverse('postDetails', args=[post.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_index_view_without_search(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)  

    def test_index_view_with_search(self):
        search_query = 'Test Post 0'
        response = self.client.get(reverse('index'), {'q': search_query})
        self.assertEqual(response.status_code, 200)  

    def test_index_view_authenticated_user(self):
        self.client.login(username='testuser', password='testpassword')
        tag_slug = 'TestSlug_2'
        response = self.client.get(reverse('index_by_tag', args=[tag_slug]))
        self.assertEqual(response.status_code, 200)

    def test_index_view_pagination(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)  
        self.assertTrue('page_obj' in response.context)
    
    def test_index_by_tag_view(self):
        response = self.client.get(reverse('index_by_tag', args=['TestSlug_3']))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('page_obj' in response.context)
        
        for post in response.context['page_obj']:
            self.assertEqual(post.slug, 'TestSlug_3')

    def test_add_post_view_authenticated_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('add_post'))
        self.assertEqual(response.status_code, 200)

    def test_delete_post_view_authenticated_user(self):
        test_post = Post.objects.create(
            title='Test Post',
            body='Test Body',
            author=self.test_user,
        )
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(reverse('delete_post', args=[test_post.pk]), {'delete_button': 'Delete'})

    def test_update_post_view_authenticated_user(self):
        test_post = Post.objects.create(
            title='Test Post',
            body='Test Body',
            author=self.test_user,
        )
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('update_post', args=[test_post.pk]))


    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)  

        response = self.client.post(reverse('register'), data=self.test_user_data)
        self.assertEqual(response.status_code, 200)  

        self.assertTrue(User.objects.filter(username=self.test_user_data['username']).exists())

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)  

        response = self.client.post(reverse('login'), data={'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302) 

    def test_logout_view(self):
        response = self.client.get(reverse('logout_view'))
        self.assertEqual(response.status_code, 302) 
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_not_found_view(self):
        response = self.client.get(reverse('Not_Found'))
        self.assertEqual(response.status_code, 200) 

    def test_page_faq_view_authenticated_user(self):
        # Log in the test user
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('page_faq'))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['profile_user'])

    def test_page_faq_view_unauthenticated_user(self):
        response = self.client.get(reverse('page_faq'))
        self.assertEqual(response.status_code, 200) 

        self.assertIsNone(response.context['profile_user']) 

    def test_contact_view_authenticated_user(self):
        # Log in the test user
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)  # Expect a 200 status code for authenticated user

        # You can also check if the 'profile_user' variable is passed to the template context
        self.assertIsNotNone(response.context['profile_user'])

    def test_contact_view_unauthenticated_user(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200) 
        self.assertIsNone(response.context['profile_user'])

    def test_user_profile_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('user_profile'))
        self.assertEqual(response.status_code, 200) 

    def test_user_room_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('user_room'))
        self.assertEqual(response.status_code, 200)  

    def test_user_profile_view_unauthenticated(self):
        response = self.client.get(reverse('user_profile'))
        self.assertEqual(response.status_code, 302)

    def test_user_room_view_unauthenticated(self):
        response = self.client.get(reverse('user_room'))
        self.assertEqual(response.status_code, 302) 
    
