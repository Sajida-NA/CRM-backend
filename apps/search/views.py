from django.shortcuts import render

from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.leads.models import Lead, Product
from apps.companies.models import Company
from apps.deals.models import Deal

# Create your views here.

class GlobalSearchView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        query = request.query_params.get("q", "").strip()

        if not query:
            return Response({
                "leads": [],
                "companies": [],
                "deals": [],
                "products": [],
            })

        # -------------------------
        # LEADS
        # -------------------------

        leads = Lead.objects.filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(email__icontains=query)
            | Q(phone_number__icontains=query)
            | Q(job_title__icontains=query)
            | Q(city__icontains=query)
            | Q(company__company_name__icontains=query)
        ).distinct()[:10]

        # -------------------------
        # COMPANIES
        # -------------------------

        companies = Company.objects.filter(
            Q(company_name__icontains=query)
            | Q(domain_name__icontains=query)
            | Q(industry__icontains=query)
            | Q(type__icontains=query)
            | Q(city__icontains=query)
            | Q(country_region__icontains=query)
            | Q(phone_number__icontains=query)
            | Q(email__icontains=query)
        ).distinct()[:10]

        # -------------------------
        # DEALS
        # -------------------------

        deals = Deal.objects.filter(
            Q(deal_name__icontains=query)
            | Q(deal_stage__icontains=query)
            | Q(priority__icontains=query)
            | Q(associated_lead__first_name__icontains=query)
            | Q(associated_lead__last_name__icontains=query)
            | Q(associated_lead__email__icontains=query)
            | Q(associated_lead__company__company_name__icontains=query)
        ).distinct()[:10]

        # -------------------------
        # PRODUCTS
        # -------------------------

        products = Product.objects.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
        ).distinct()[:10]

        # -------------------------
        # RESPONSE
        # -------------------------

        return Response({
            "leads": [
                {
                    "id": lead.id,
                    "name": f"{lead.first_name} {lead.last_name}",
                    "email": lead.email,
                    "type": "lead",
                }
                for lead in leads
            ],

            "companies": [
                {
                    "id": company.id,
                    "name": company.company_name,
                    "email": company.email,
                    "type": "company",
                }
                for company in companies
            ],

            "deals": [
                {
                    "id": deal.id,
                    "name": deal.deal_name,
                    "stage": deal.deal_stage,
                    "type": "deal",
                }
                for deal in deals
            ],

            "products": [
                {
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "type": "product",
                }
                for product in products
            ],
        })