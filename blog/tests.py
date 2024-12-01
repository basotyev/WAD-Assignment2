from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Post, Comment, Category


class PostAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.other_user = User.objects.create_user(username="otheruser", password="otherpassword")

        self.category1 = Category.objects.create(name="Tech")
        self.category2 = Category.objects.create(name="Health")

        self.post1 = Post.objects.create(
            title="First Post",
            description="Description of the first post",
            author=self.user,
            published=True
        )
        self.post1.category.add(self.category1)

        self.post2 = Post.objects.create(
            title="Second Post",
            description="Description of the second post",
            author=self.other_user,
            published=False
        )

        self.client = APIClient()

    def test_get_published_posts(self):
        response = self.client.get('/blog/api/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "First Post")

    def test_create_post_authenticated(self):
        self.client.login(username="testuser", password="testpassword")
        data = {
            "title": "New Post",
            "description": "New Post Description",
            "published": True,
            "category": [self.category1.id, self.category2.id]
        }
        response = self.client.post('/blog/api/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 3)
        self.assertEqual(Post.objects.last().title, "New Post")

    def test_create_post_unauthenticated(self):
        data = {
            "title": "Unauthorized Post",
            "description": "Should not be created",
            "published": True
        }
        response = self.client.post('/blog/api/posts/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_post(self):
        self.client.login(username="testuser", password="testpassword")
        data = {
            "title": "Updated First Post",
            "description": "Updated Description",
            "published": True
        }
        response = self.client.put(f'/blog/api/posts/{self.post1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post1.refresh_from_db()
        self.assertEqual(self.post1.title, "Updated First Post")

    def test_delete_post(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.delete(f'/blog/api/posts/{self.post1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 1)

    def test_unauthorized_delete_post(self):
        self.client.login(username="otheruser", password="otherpassword")
        response = self.client.delete(f'/blog/api/posts/{self.post1.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CommentAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="commenter", password="password")
        self.post = Post.objects.create(
            title="Post with Comments",
            description="Description",
            author=self.user,
            published=True
        )
        self.comment = Comment.objects.create(
            text="First Comment",
            author=self.user,
            post=self.post
        )
        self.client = APIClient()

    def test_get_comments(self):
        response = self.client.get('/blog/api/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['text'], "First Comment")

    def test_create_comment_authenticated(self):
        self.client.login(username="commenter", password="password")
        data = {
            "text": "New Comment",
            "post": self.post.id
        }
        response = self.client.post('/blog/api/comments/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(Comment.objects.last().text, "New Comment")

    def test_create_comment_unauthenticated(self):
        data = {
            "text": "Unauthorized Comment",
            "post": self.post.id
        }
        response = self.client.post('/blog/api/comments/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CategoryAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="categoryuser", password="password")
        self.category = Category.objects.create(name="Existing Category")
        self.client = APIClient()

    def test_get_categories(self):
        response = self.client.get('/blog/api/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Existing Category")

    def test_create_category_authenticated(self):
        self.client.login(username="categoryuser", password="password")
        data = {"name": "New Category"}
        response = self.client.post('/blog/api/categories/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(Category.objects.last().name, "New Category")

    def test_create_category_unauthenticated(self):
        data = {"name": "Unauthorized Category"}
        response = self.client.post('/blog/api/categories/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
