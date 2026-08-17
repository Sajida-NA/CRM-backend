from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class TicketAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="owner@example.com",
            password="StrongPassword123",
            phone_number="1234567890",
            company_name="Acme",
            industry_type="IT",
            country="US",
        )
        self.client.force_authenticate(user=self.user)

    def test_create_ticket(self):
        url = reverse("ticket-list")
        payload = {
            "name": "Payment failure issue",
            "description": "Customer cannot complete payment.",
            "status": "NEW",
            "source": "EMAIL",
            "priority": "HIGH",
            "owner": self.user.id,
            "associated_deal": "DEAL-001",
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["data"]["name"], payload["name"])

    def test_list_tickets(self):
        self.client.post(
            reverse("ticket-list"),
            {
                "name": "Test ticket",
                "description": "Need work.",
                "status": "NEW",
                "source": "PHONE",
                "priority": "MEDIUM",
                "owner": self.user.id,
                "associated_deal": "DEAL-002",
            },
            format="json",
        )

        response = self.client.get(reverse("ticket-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_update_ticket(self):
        create_response = self.client.post(
            reverse("ticket-list"),
            {
                "name": "Old ticket",
                "description": "Old description.",
                "status": "NEW",
                "source": "EMAIL",
                "priority": "LOW",
                "owner": self.user.id,
                "associated_deal": "DEAL-003",
            },
            format="json",
        )
        ticket_id = create_response.data["data"]["id"]

        response = self.client.patch(
            reverse("ticket-detail", kwargs={"pk": ticket_id}),
            {"status": "IN_PROGRESS"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["status"], "IN_PROGRESS")

    def test_delete_ticket(self):
        create_response = self.client.post(
            reverse("ticket-list"),
            {
                "name": "Delete me",
                "description": "Will delete.",
                "status": "NEW",
                "source": "WEB",
                "priority": "HIGH",
                "owner": self.user.id,
                "associated_deal": "DEAL-004",
            },
            format="json",
        )
        ticket_id = create_response.data["data"]["id"]

        response = self.client.delete(reverse("ticket-detail", kwargs={"pk": ticket_id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("deleted successfully", response.data["message"].lower())
