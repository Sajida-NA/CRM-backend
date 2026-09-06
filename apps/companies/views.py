


from django.shortcuts import get_object_or_404 
from django.db.models import Q 
 
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
    # GET ALL COMPANIES + SEARCH + FILTER 
    # ----------------------------------------------------- 
 
    def get(self, request): 
 
        # Get all companies 
        companies = Company.objects.all().order_by("-id") 
 
        # ------------------------------------------------- 
        # SEARCH: Phone, Company Name, Email 
        # ------------------------------------------------- 
        search = request.query_params.get("search") 
 
        if search: 
            companies = companies.filter( 
                Q(phone_number__icontains=search) | 
                Q(company_name__icontains=search) | 
                Q(email__icontains=search) 
            ) 
 
        # ------------------------------------------------- 
        # FILTER: Industry 
        # ------------------------------------------------- 
        industry = request.query_params.get("industry") 
 
        if industry: 
            companies = companies.filter( 
                industry__iexact=industry 
            ) 
 
        # ------------------------------------------------- 
        # FILTER: City 
        # ------------------------------------------------- 
        city = request.query_params.get("city") 
 
        if city: 
            companies = companies.filter( 
                city__iexact=city 
            ) 
 
        # ------------------------------------------------- 
        # FILTER: Country / Region 
        # ------------------------------------------------- 
        country_region = request.query_params.get("country_region") 
 
        if country_region: 
            companies = companies.filter( 
                country_region__iexact=country_region 
            ) 
 
       
        created_date = request.query_params.get("created_date") 
 
        if created_date: 
            companies = companies.filter( 
                created_date__date=created_date 
            ) 
 
        # ------------------------------------------------- 
        # SERIALIZE RESULTS 
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
 
        serializer = CompanySerializer(data=request.data) 
 
        if serializer.is_valid(): 
 
            company = serializer.save() 
 
            # Return company owner name instead of only ID 
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