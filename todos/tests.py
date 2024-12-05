from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Todo

class TodoTests(TestCase):
    def setUp(self):
        """Set up test data"""
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        # Create another user for testing isolation
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        
        # Create token for authentication
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        # Create test todo
        self.todo = Todo.objects.create(
            title='Test Todo',
            description='Test Description',
            user=self.user,
            created_by=self.user,
            updated_by=self.user
        )

    def test_create_todo(self):
        """Test creating a new todo"""
        data = {
            'title': 'New Todo',
            'description': 'New Description',
            'completed': False
        }
        response = self.client.post('/api/todos/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Todo.objects.count(), 2)
        
        # Check if created_by and updated_by are set correctly
        new_todo = Todo.objects.get(title='New Todo')
        self.assertEqual(new_todo.created_by, self.user)
        self.assertEqual(new_todo.updated_by, self.user)

    def test_get_todos(self):
        """Test retrieving todos list"""
        # Create todo for other user
        Todo.objects.create(
            title='Other Todo',
            description='Other Description',
            user=self.other_user,
            created_by=self.other_user,
            updated_by=self.other_user
        )
        
        response = self.client.get('/api/todos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should only see own todos

    def test_update_todo(self):
        """Test updating a todo"""
        data = {
            'completed': True,
            'description': 'Updated Description'
        }
        response = self.client.patch(f'/api/todos/{self.todo.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh from database
        self.todo.refresh_from_db()
        self.assertTrue(self.todo.completed)
        self.assertEqual(self.todo.description, 'Updated Description')
        self.assertEqual(self.todo.updated_by, self.user)

    def test_delete_todo(self):
        """Test deleting a todo"""
        response = self.client.delete(f'/api/todos/{self.todo.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.count(), 0)

    def test_unauthorized_access(self):
        """Test unauthorized access to API"""
        # Remove authentication
        self.client.credentials()
        response = self.client.get('/api/todos/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_other_user_todo_access(self):
        """Test accessing another user's todo"""
        other_todo = Todo.objects.create(
            title='Other Todo',
            description='Other Description',
            user=self.other_user,
            created_by=self.other_user,
            updated_by=self.other_user
        )
        
        # Try to access other user's todo
        response = self.client.get(f'/api/todos/{other_todo.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # Try to update other user's todo
        response = self.client.patch(f'/api/todos/{other_todo.id}/', {'completed': True})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # Try to delete other user's todo
        response = self.client.delete(f'/api/todos/{other_todo.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_token_authentication(self):
        """Test token authentication"""
        # Test valid token
        response = self.client.get('/api/todos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test invalid token
        self.client.credentials(HTTP_AUTHORIZATION='Token invalid_token')
        response = self.client.get('/api/todos/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_todo_creation_validation(self):
        """Test todo creation validation"""
        # Test missing required field
        data = {'description': 'Test Description'}
        response = self.client.post('/api/todos/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test empty title
        data = {'title': '', 'description': 'Test Description'}
        response = self.client.post('/api/todos/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
