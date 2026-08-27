# from django.shortcuts import get_object_or_404

# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from .models import Company
# from .serializers import (
#     CompanySerializer,
#     CompanyListSerializer,
#     UpdateCompanySerializer,
# )


# class CompanyListCreateView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         companies = Company.objects.all().order_by("-id")

#         serializer = CompanyListSerializer(companies, many=True)

#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         serializer = CompanySerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()

#             return Response(
#                 {
#                     "message": "Company created successfully.",
#                     "data": serializer.data,
#                 },
#                 status=status.HTTP_201_CREATED,
#             )

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST,
#         )


# class CompanyDetailView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, pk):
#         company = get_object_or_404(Company, pk=pk)

#         serializer = CompanyListSerializer(company)

#         return Response(
#             serializer.data,
#             status=status.HTTP_200_OK,
#         )

#     def put(self, request, pk):
#         company = get_object_or_404(Company, pk=pk)

#         serializer = UpdateCompanySerializer(
#             company,
#             data=request.data,
#         )

#         if serializer.is_valid():
#             serializer.save()

#             return Response(
#                 {
#                     "message": "Company updated successfully.",
#                     "data": CompanyListSerializer(company).data,
#                 },
#                 status=status.HTTP_200_OK,
#             )

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST,
#         )

#     def delete(self, request, pk):
#         company = get_object_or_404(Company, pk=pk)

#         company.delete()

#         return Response(
#             {
#                 "message": "Company deleted successfully."
#             },
#             status=status.HTTP_200_OK,
#         )

from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Company
from .serializers import (
    CompanySerializer,
    CompanyListSerializer,
    UpdateCompanySerializer,
)


# =========================================================
# COMPANY LIST + CREATE
# =========================================================

class CompanyListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    # -----------------------------------------------------
    # GET ALL COMPANIES
    # -----------------------------------------------------

    def get(self, request):

        companies = Company.objects.all().order_by("-id")

        serializer = CompanyListSerializer(
            companies,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # -----------------------------------------------------
    # CREATE COMPANY
    # -----------------------------------------------------

    def post(self, request):

        serializer = CompanySerializer(data=request.data)

        if serializer.is_valid():

            company = serializer.save()

            # Use list serializer so owner ID is returned as owner name
            response_serializer = CompanyListSerializer(company)

            return Response(
                {
                    "message": "Company created successfully.",
                    "data": response_serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {
                "message": "Company creation failed.",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


# =========================================================
# COMPANY DETAIL + UPDATE + DELETE
# =========================================================

class CompanyDetailView(APIView):

    permission_classes = [IsAuthenticated]

    # -----------------------------------------------------
    # GET SINGLE COMPANY
    # -----------------------------------------------------

    def get(self, request, pk):

        company = get_object_or_404(
            Company,
            pk=pk
        )

        serializer = CompanyListSerializer(company)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # -----------------------------------------------------
    # UPDATE COMPANY
    # -----------------------------------------------------

    def put(self, request, pk):

        company = get_object_or_404(
            Company,
            pk=pk
        )

        serializer = UpdateCompanySerializer(
            company,
            data=request.data
        )

        if serializer.is_valid():

            company = serializer.save()

            return Response(
                {
                    "message": "Company updated successfully.",
                    "data": CompanyListSerializer(company).data,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {
                "message": "Company update failed.",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # -----------------------------------------------------
    # DELETE COMPANY
    # -----------------------------------------------------

    def delete(self, request, pk):

        company = get_object_or_404(
            Company,
            pk=pk
        )

        company.delete()

        return Response(
            {
                "message": "Company deleted successfully."
            },
            status=status.HTTP_200_OK,
        )