from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from rest_framework import status
from rest_framework.test import APIClient
from .models import Candidate

class CandidateAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.version = settings.REST_FRAMEWORK['DEFAULT_VERSION']
        self.candidates_data = [
            {
                "name": "test user",
                "age": 28,
                "gender": "M",
                "email": "test.user@example.com",
                "phone_number": "9876543210"
            },
            {
                "name": "test user1",
                "age": 32,
                "gender": "M",
                "email": "testuser1@example.com",
                "phone_number": "9876543211"
            }
        ]
        self.candidates = Candidate.objects.bulk_create([
            Candidate(**data) for data in self.candidates_data
        ])

    def test_create_candidate(self):
        candidate_data = {
            "name": "New Candidate",
            "age": 25,
            "gender": "F",
            "email": "new.candidate@example.com",
            "phone_number": "9999999999"
        }
        response = self.client.post(
            reverse('candidate-list', kwargs={"version": self.version}), 
            candidate_data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Candidate.objects.count(), 3)

    def test_update_candidate(self):
        candidate = self.candidates[0]
        update_data = {"name": "Updated Name"}
        response = self.client.patch(
            reverse('candidate-detail', kwargs={
                'version': self.version, 
                'pk': candidate.id
            }), 
            update_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        candidate.refresh_from_db()
        self.assertEqual(candidate.name, "Updated Name")

    def test_delete_candidate(self):
        candidate = self.candidates[0]
        response = self.client.delete(
            reverse('candidate-detail', kwargs={
                'version': self.version, 
                'pk': candidate.id
            })
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Candidate.objects.filter(pk=candidate.id).exists())

    def test_search_candidates(self):
        response = self.client.get(
            reverse('candidate-search', kwargs={"version": self.version}), 
            {'q': 'test user'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data
        self.assertTrue(len(results) > 0)
        names = [result['name'] for result in results]
        self.assertIn("test user", names)
        self.assertIn("test user1", names)

    def test_search_empty_query(self):
        response = self.client.get(
            reverse('candidate-search', kwargs={"version": self.version}), 
            {'q': ''}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_search_relevancy(self):
        test_candidates = [
            Candidate.objects.create(name="Ajay Kumar Yadav", age=28, gender="M", email="ajay.yadav1@example.com", phone_number="1111111111"),
            Candidate.objects.create(name="Ajay Kumar", age=32, gender="M", email="ajay.kumar1@example.com", phone_number="2222222222"),
            Candidate.objects.create(name="Ajay Yadav", age=35, gender="M", email="ajay.yadav2@example.com", phone_number="3333333333"),
            Candidate.objects.create(name="Kumar Yadav", age=30, gender="M", email="kumar.yadav@example.com", phone_number="4444444444"),
            Candidate.objects.create(name="Ramesh Yadav", age=40, gender="M", email="ramesh.yadav@example.com", phone_number="5555555555"),
            Candidate.objects.create(name="Ajay Singh", age=33, gender="M", email="ajay.singh@example.com", phone_number="6666666666")
        ]
        search_query = "Ajay Kumar Yadav"
        response = self.client.get(
            reverse('candidate-search', kwargs={"version": self.version}), 
            {'q': search_query}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result_names = [result['name'] for result in response.data]
        expected_order = [
            "Ajay Kumar Yadav",
            "Ajay Kumar",
            "Ajay Yadav",
            "Kumar Yadav",
            "Ramesh Yadav",
            "Ajay Singh"
        ]
        self.assertEqual(result_names, expected_order)
        self.assertEqual(len(result_names), 6)
