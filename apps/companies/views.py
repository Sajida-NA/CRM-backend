
# from django.shortcuts import get_object_or_404
# from django.db.models import Q

# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from .models import Company
# from apps.notifications.models import Notification

# from .serializers import (
#     CompanySerializer,
#     CompanyListSerializer,
#     UpdateCompanySerializer,
# )


# # =========================================================
# # HELPER
# # =========================================================

# def is_admin(user):
#     """
#     Admin users can access all companies.
#     """

#     return (
#         getattr(user, "role", "") == "Admin"
#         or user.is_staff
#     )


# # =========================================================
# # COMPANY LIST + CREATE
# # =========================================================

# class CompanyListCreateView(APIView):

#     permission_classes = [IsAuthenticated]

#     # -----------------------------------------------------
#     # GET COMPANIES
#     # -----------------------------------------------------

#     def get(self, request):

#         # -------------------------------------------------
#         # COMPANY ACCESS
#         # -------------------------------------------------

#         if is_admin(request.user):

#             # Admin -> all companies
#             companies = Company.objects.all().order_by("-id")

#         else:

#             # -------------------------------------------------
#             # NORMAL USERS
#             # -------------------------------------------------
#             # Show all companies.
#             #
#             # Company Owner can be any selected user
#             # such as Eshaan Muhammed, Saji jubi, etc.
#             # -------------------------------------------------

#             companies = Company.objects.all().order_by("-id")

#         # -------------------------------------------------
#         # SEARCH
#         # Phone, Company Name, Email
#         # -------------------------------------------------

#         search = request.query_params.get("search")

#         if search:
#             companies = companies.filter(
#                 Q(phone_number__icontains=search)
#                 | Q(company_name__icontains=search)
#                 | Q(email__icontains=search)
#             )

#         # -------------------------------------------------
#         # FILTER: INDUSTRY
#         # -------------------------------------------------

#         industry = request.query_params.get("industry")

#         if industry:
#             companies = companies.filter(
#                 industry__iexact=industry
#             )

#         # -------------------------------------------------
#         # FILTER: CITY
#         # -------------------------------------------------

#         city = request.query_params.get("city")

#         if city:
#             companies = companies.filter(
#                 city__iexact=city
#             )

#         # -------------------------------------------------
#         # FILTER: COUNTRY / REGION
#         # -------------------------------------------------

#         country_region = request.query_params.get(
#             "country_region"
#         )

#         if country_region:
#             companies = companies.filter(
#                 country_region__iexact=country_region
#             )

#         # -------------------------------------------------
#         # FILTER: COMPANY TYPE
#         # -------------------------------------------------

#         # company_type = request.query_params.get("type")

#         # if company_type:
#         #     companies = companies.filter(
#         #         type__iexact=company_type
#         #     )

#         # -------------------------------------------------
#         # FILTER: CREATED DATE
#         # -------------------------------------------------

#         created_date = request.query_params.get(
#             "created_date"
#         )

#         if created_date:
#             companies = companies.filter(
#                 created_date__date=created_date
#             )

#         # -------------------------------------------------
#         # SERIALIZE
#         # -------------------------------------------------

#         serializer = CompanyListSerializer(
#             companies,
#             many=True
#         )

#         return Response(
#             serializer.data,
#             status=status.HTTP_200_OK
#         )

#     # -----------------------------------------------------
#     # CREATE COMPANY
#     # -----------------------------------------------------

#     def post(self, request):

#         serializer = CompanySerializer(
#             data=request.data
#         )

#         if serializer.is_valid():

#             # -------------------------------------------------
#             # IMPORTANT
#             # -------------------------------------------------
#             # Do NOT use:
#             #
#             # serializer.save(company_owner=request.user)
#             #
#             # because that would always make the logged-in
#             # user the company owner.
#             #
#             # The owner selected from the frontend is saved.
#             # -------------------------------------------------

#             company = serializer.save()

#             # -------------------------------------------------
#             # NOTIFICATION
#             # -------------------------------------------------

#             Notification.objects.create(
#                 user=request.user,
#                 title="New Company Added",
#                 message=(
#                     f"New company {company.company_name} "
#                     f"has been added."
#                 ),
#             )

#             # -------------------------------------------------
#             # RESPONSE
#             # -------------------------------------------------

#             response_serializer = CompanyListSerializer(
#                 company
#             )

#             return Response(
#                 {
#                     "message": "Company created successfully.",
#                     "data": response_serializer.data,
#                 },
#                 status=status.HTTP_201_CREATED,
#             )

#         return Response(
#             {
#                 "message": "Company creation failed.",
#                 "errors": serializer.errors,
#             },
#             status=status.HTTP_400_BAD_REQUEST,
#         )


# # =========================================================
# # COMPANY DETAIL + UPDATE + DELETE
# # =========================================================

# class CompanyDetailView(APIView):

#     permission_classes = [IsAuthenticated]

#     # -----------------------------------------------------
#     # GET SINGLE COMPANY
#     # -----------------------------------------------------

#     def get(self, request, pk):

#         if is_admin(request.user):

#             # Admin -> can access any company
#             company = get_object_or_404(
#                 Company,
#                 pk=pk
#             )

#         else:

#             # -------------------------------------------------
#             # NORMAL USER
#             # -------------------------------------------------
#             # Normal users can view any company.
#             # Company Owner can be another user.
#             # -------------------------------------------------

#             company = get_object_or_404(
#                 Company,
#                 pk=pk
#             )

#         serializer = CompanyListSerializer(
#             company
#         )

#         return Response(
#             serializer.data,
#             status=status.HTTP_200_OK
#         )

#     # -----------------------------------------------------
#     # UPDATE COMPANY
#     # -----------------------------------------------------

#     def put(self, request, pk):

#         if is_admin(request.user):

#             # Admin -> can update any company
#             company = get_object_or_404(
#                 Company,
#                 pk=pk
#             )

#         else:

#             # -------------------------------------------------
#             # NORMAL USER
#             # -------------------------------------------------
#             # Keep owner-based update permission.
#             # Only the current company owner can update it.
#             # -------------------------------------------------

#             company = get_object_or_404(
#                 Company,
#                 pk=pk,
#                 company_owner=request.user
#             )

#         serializer = UpdateCompanySerializer(
#             company,
#             data=request.data
#         )

#         if serializer.is_valid():

#             company = serializer.save()

#             Notification.objects.create(
#                 user=request.user,
#                 title="Company Updated",
#                 message=(
#                     f"Company {company.company_name} "
#                     f"has been updated."
#                 ),
#             )

#             return Response(
#                 {
#                     "message": "Company updated successfully.",
#                     "data": CompanyListSerializer(
#                         company
#                     ).data,
#                 },
#                 status=status.HTTP_200_OK,
#             )

#         return Response(
#             {
#                 "message": "Company update failed.",
#                 "errors": serializer.errors,
#             },
#             status=status.HTTP_400_BAD_REQUEST,
#         )

#     # -----------------------------------------------------
#     # DELETE COMPANY
#     # -----------------------------------------------------

#     def delete(self, request, pk):

#         if is_admin(request.user):

#             # Admin -> can delete any company
#             company = get_object_or_404(
#                 Company,
#                 pk=pk
#             )

#         else:

#             # -------------------------------------------------
#             # NORMAL USER
#             # -------------------------------------------------
#             # Only the current company owner can delete it.
#             # -------------------------------------------------

#             company = get_object_or_404(
#                 Company,
#                 pk=pk,
#                 company_owner=request.user
#             )

#         company_name = company.company_name

#         company.delete()

#         Notification.objects.create(
#             user=request.user,
#             title="Company Deleted",
#             message=(
#                 f"Company {company_name} "
#                 f"has been deleted."
#             ),
#         )

#         return Response(
#             {
#                 "message": "Company deleted successfully."
#             },
#             status=status.HTTP_200_OK,
#         )




# from django.shortcuts import get_object_or_404
# from django.db.models import Q

# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from .models import Company
# from apps.notifications.models import Notification

# from .serializers import (
#     CompanySerializer,
#     CompanyListSerializer,
#     UpdateCompanySerializer,
# )


# # =========================================================
# # HELPER
# # =========================================================

# def is_admin(user):
#     """
#     Only users whose role is Admin can access all companies.
#     """

#     return getattr(user, "role", "") == "Admin"


# # =========================================================
# # COMPANY LIST + CREATE
# # =========================================================

# class CompanyListCreateView(APIView):

#     permission_classes = [IsAuthenticated]

#     # -----------------------------------------------------
#     # GET COMPANIES
#     # -----------------------------------------------------

#     def get(self, request):

#         # -------------------------------------------------
#         # COMPANY ACCESS
#         # -------------------------------------------------

#         if is_admin(request.user):

#             # Admin -> see ALL companies
#             companies = Company.objects.all().order_by("-id")

#         else:

#             # Normal User -> see ONLY companies
#             # where logged-in user is the company owner
#             companies = Company.objects.filter(
#                 company_owner=request.user
#             ).order_by("-id")

#         # -------------------------------------------------
#         # SEARCH
#         # Phone, Company Name, Email
#         # -------------------------------------------------

#         search = request.query_params.get("search")

#         if search:
#             companies = companies.filter(
#                 Q(phone_number__icontains=search)
#                 | Q(company_name__icontains=search)
#                 | Q(email__icontains=search)
#             )

#         # -------------------------------------------------
#         # FILTER: INDUSTRY
#         # -------------------------------------------------

#         industry = request.query_params.get("industry")

#         if industry:
#             companies = companies.filter(
#                 industry__iexact=industry
#             )

#         # -------------------------------------------------
#         # FILTER: CITY
#         # -------------------------------------------------

#         city = request.query_params.get("city")

#         if city:
#             companies = companies.filter(
#                 city__iexact=city
#             )

#         # -------------------------------------------------
#         # FILTER: COUNTRY / REGION
#         # -------------------------------------------------

#         country_region = request.query_params.get(
#             "country_region"
#         )

#         if country_region:
#             companies = companies.filter(
#                 country_region__iexact=country_region
#             )

#         # -------------------------------------------------
#         # FILTER: COMPANY TYPE
#         # -------------------------------------------------

#         # company_type = request.query_params.get("type")

#         # if company_type:
#         #     companies = companies.filter(
#         #         type__iexact=company_type
#         #     )

#         # -------------------------------------------------
#         # FILTER: CREATED DATE
#         # -------------------------------------------------

#         created_date = request.query_params.get(
#             "created_date"
#         )

#         if created_date:
#             companies = companies.filter(
#                 created_date__date=created_date
#             )

#         # -------------------------------------------------
#         # SERIALIZE
#         # -------------------------------------------------

#         serializer = CompanyListSerializer(
#             companies,
#             many=True
#         )

#         return Response(
#             serializer.data,
#             status=status.HTTP_200_OK
#         )

#     # -----------------------------------------------------
#     # CREATE COMPANY
#     # -----------------------------------------------------

#     def post(self, request):

#         serializer = CompanySerializer(
#             data=request.data
#         )

#         if serializer.is_valid():

#             # -------------------------------------------------
#             # SAVE COMPANY
#             # -------------------------------------------------
#             # Company owner selected from frontend is saved.
#             # We are NOT forcing request.user as owner.
#             # -------------------------------------------------

#             company = serializer.save()

#             # -------------------------------------------------
#             # NOTIFICATION
#             # -------------------------------------------------

#             Notification.objects.create(
#                 user=request.user,
#                 title="New Company Added",
#                 message=(
#                     f"New company {company.company_name} "
#                     f"has been added."
#                 ),
#             )

#             # -------------------------------------------------
#             # RESPONSE
#             # -------------------------------------------------

#             response_serializer = CompanyListSerializer(
#                 company
#             )

#             return Response(
#                 {
#                     "message": "Company created successfully.",
#                     "data": response_serializer.data,
#                 },
#                 status=status.HTTP_201_CREATED,
#             )

#         return Response(
#             {
#                 "message": "Company creation failed.",
#                 "errors": serializer.errors,
#             },
#             status=status.HTTP_400_BAD_REQUEST,
#         )


# # =========================================================
# # COMPANY DETAIL + UPDATE + DELETE
# # =========================================================

# class CompanyDetailView(APIView):

#     permission_classes = [IsAuthenticated]

#     # -----------------------------------------------------
#     # GET SINGLE COMPANY
#     # -----------------------------------------------------

#     def get(self, request, pk):

#         if is_admin(request.user):

#             # Admin -> can view ANY company
#             company = get_object_or_404(
#                 Company,
#                 pk=pk
#             )

#         else:

#             # Normal User -> can view ONLY
#             # their own company
#             company = get_object_or_404(
#                 Company,
#                 pk=pk,
#                 company_owner=request.user
#             )

#         serializer = CompanyListSerializer(
#             company
#         )

#         return Response(
#             serializer.data,
#             status=status.HTTP_200_OK
#         )

#     # -----------------------------------------------------
#     # UPDATE COMPANY
#     # -----------------------------------------------------

#     def put(self, request, pk):

#         if is_admin(request.user):

#             # Admin -> can update ANY company
#             company = get_object_or_404(
#                 Company,
#                 pk=pk
#             )

#         else:

#             # Normal User -> can update ONLY
#             # their own company
#             company = get_object_or_404(
#                 Company,
#                 pk=pk,
#                 company_owner=request.user
#             )

#         serializer = UpdateCompanySerializer(
#             company,
#             data=request.data
#         )

#         if serializer.is_valid():

#             company = serializer.save()

#             # -------------------------------------------------
#             # NOTIFICATION
#             # -------------------------------------------------

#             Notification.objects.create(
#                 user=request.user,
#                 title="Company Updated",
#                 message=(
#                     f"Company {company.company_name} "
#                     f"has been updated."
#                 ),
#             )

#             return Response(
#                 {
#                     "message": "Company updated successfully.",
#                     "data": CompanyListSerializer(
#                         company
#                     ).data,
#                 },
#                 status=status.HTTP_200_OK,
#             )

#         return Response(
#             {
#                 "message": "Company update failed.",
#                 "errors": serializer.errors,
#             },
#             status=status.HTTP_400_BAD_REQUEST,
#         )

#     # -----------------------------------------------------
#     # DELETE COMPANY
#     # -----------------------------------------------------

#     def delete(self, request, pk):

#         if is_admin(request.user):

#             # Admin -> can delete ANY company
#             company = get_object_or_404(
#                 Company,
#                 pk=pk
#             )

#         else:

#             # Normal User -> can delete ONLY
#             # their own company
#             company = get_object_or_404(
#                 Company,
#                 pk=pk,
#                 company_owner=request.user
#             )

#         company_name = company.company_name

#         company.delete()

#         # -------------------------------------------------
#         # NOTIFICATION
#         # -------------------------------------------------

#         Notification.objects.create(
#             user=request.user,
#             title="Company Deleted",
#             message=(
#                 f"Company {company_name} "
#                 f"has been deleted."
#             ),
#         )

#         return Response(
#             {
#                 "message": "Company deleted successfully."
#             },
#             status=status.HTTP_200_OK,
#         )



from django.shortcuts import get_object_or_404
from django.db.models import Q

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


# =========================================================
# HELPER
# =========================================================

def is_admin(user):
    """
    Admin users can access all companies.

    Supports:
    - role = Admin
    - staff users
    - superusers
    """

    return (
        getattr(user, "role", "").strip().lower() == "admin"
        or getattr(user, "is_staff", False)
        or getattr(user, "is_superuser", False)
    )


# =========================================================
# COMPANY LIST + CREATE
# =========================================================

class CompanyListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    # -----------------------------------------------------
    # GET COMPANIES
    # -----------------------------------------------------

    def get(self, request):

        # -------------------------------------------------
        # COMPANY ACCESS
        # -------------------------------------------------

        if is_admin(request.user):

            # Admin -> see ALL companies
            companies = Company.objects.all().order_by("-id")

        else:

            # Normal User -> see ONLY companies
            # where logged-in user is the company owner
            companies = Company.objects.filter(
                company_owner=request.user
            ).order_by("-id")

        # -------------------------------------------------
        # SEARCH
        # Phone, Company Name, Email
        # -------------------------------------------------

        search = request.query_params.get("search")

        if search:
            companies = companies.filter(
                Q(phone_number__icontains=search)
                | Q(company_name__icontains=search)
                | Q(email__icontains=search)
            )

        # -------------------------------------------------
        # FILTER: INDUSTRY
        # -------------------------------------------------

        industry = request.query_params.get("industry")

        if industry:
            companies = companies.filter(
                industry__iexact=industry
            )

        # -------------------------------------------------
        # FILTER: CITY
        # -------------------------------------------------

        city = request.query_params.get("city")

        if city:
            companies = companies.filter(
                city__iexact=city
            )

        # -------------------------------------------------
        # FILTER: COUNTRY / REGION
        # -------------------------------------------------

        country_region = request.query_params.get(
            "country_region"
        )

        if country_region:
            companies = companies.filter(
                country_region__iexact=country_region
            )

        # -------------------------------------------------
        # FILTER: COMPANY TYPE
        # -------------------------------------------------

        # company_type = request.query_params.get("type")

        # if company_type:
        #     companies = companies.filter(
        #         type__iexact=company_type
        #     )

        # -------------------------------------------------
        # FILTER: CREATED DATE
        # -------------------------------------------------

        created_date = request.query_params.get(
            "created_date"
        )

        if created_date:
            companies = companies.filter(
                created_date__date=created_date
            )

        # -------------------------------------------------
        # SERIALIZE
        # -------------------------------------------------

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

        serializer = CompanySerializer(
            data=request.data
        )

        if serializer.is_valid():

            # -------------------------------------------------
            # SAVE COMPANY
            # -------------------------------------------------
            # Company owner selected from frontend is saved.
            # We are NOT forcing request.user as owner.
            # -------------------------------------------------

            company = serializer.save()

            # -------------------------------------------------
            # NOTIFICATION
            # -------------------------------------------------

            Notification.objects.create(
                user=request.user,
                title="New Company Added",
                message=(
                    f"New company {company.company_name} "
                    f"has been added."
                ),
            )

            # -------------------------------------------------
            # RESPONSE
            # -------------------------------------------------

            response_serializer = CompanyListSerializer(
                company
            )

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

        if is_admin(request.user):

            # Admin -> can view ANY company
            company = get_object_or_404(
                Company,
                pk=pk
            )

        else:

            # Normal User -> can view ONLY
            # their own company
            company = get_object_or_404(
                Company,
                pk=pk,
                company_owner=request.user
            )

        serializer = CompanyListSerializer(
            company
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # -----------------------------------------------------
    # UPDATE COMPANY
    # -----------------------------------------------------

    def put(self, request, pk):

        if is_admin(request.user):

            # Admin -> can update ANY company
            company = get_object_or_404(
                Company,
                pk=pk
            )

        else:

            # Normal User -> can update ONLY
            # their own company
            company = get_object_or_404(
                Company,
                pk=pk,
                company_owner=request.user
            )

        serializer = UpdateCompanySerializer(
            company,
            data=request.data
        )

        if serializer.is_valid():

            company = serializer.save()

            # -------------------------------------------------
            # NOTIFICATION
            # -------------------------------------------------

            Notification.objects.create(
                user=request.user,
                title="Company Updated",
                message=(
                    f"Company {company.company_name} "
                    f"has been updated."
                ),
            )

            return Response(
                {
                    "message": "Company updated successfully.",
                    "data": CompanyListSerializer(
                        company
                    ).data,
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

        if is_admin(request.user):

            # Admin -> can delete ANY company
            company = get_object_or_404(
                Company,
                pk=pk
            )

        else:

            # Normal User -> can delete ONLY
            # their own company
            company = get_object_or_404(
                Company,
                pk=pk,
                company_owner=request.user
            )

        company_name = company.company_name

        company.delete()

        # -------------------------------------------------
        # NOTIFICATION
        # -------------------------------------------------

        Notification.objects.create(
            user=request.user,
            title="Company Deleted",
            message=(
                f"Company {company_name} "
                f"has been deleted."
            ),
        )

        return Response(
            {
                "message": "Company deleted successfully."
            },
            status=status.HTTP_200_OK,
        )