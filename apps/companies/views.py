from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Company

from apps.notifications.models import Notification

from .serializers import (
    CompanySerializer,
    CompanyListSerializer,
    UpdateCompanySerializer,
)


class CompanyListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        companies = Company.objects.all().order_by("-id")

        serializer = CompanyListSerializer(companies, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CompanySerializer(data=request.data)

        if serializer.is_valid():
            company = serializer.save()

            Notification.objects.create(
               user=request.user,
               title="New Company Added",
               message=f"New company {company.company_name} has been added.",
            )

            return Response(
                {
                    "message": "Company created successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class CompanyDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        company = get_object_or_404(Company, pk=pk)

        serializer = CompanyListSerializer(company)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def put(self, request, pk):
        company = get_object_or_404(Company, pk=pk)

        serializer = UpdateCompanySerializer(
            company,
            data=request.data,
        )

        if serializer.is_valid():
            company = serializer.save()

            Notification.objects.create(
               user=request.user,
               title="Company Updated",
               message=f"Company {company.company_name} has been updated.",
            )

            return Response(
                {
                    "message": "Company updated successfully.",
                    "data": CompanyListSerializer(company).data,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk):
        company = get_object_or_404(Company, pk=pk)

        company_name = company.company_name

        company.delete()

        Notification.objects.create(
           user=request.user,
           title="Company Deleted",
           message=f"Company {company_name} has been deleted.",
        )

        return Response(
            {
                "message": "Company deleted successfully."
            },
            status=status.HTTP_200_OK,
        )