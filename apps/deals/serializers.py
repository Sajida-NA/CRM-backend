

 
from rest_framework import serializers 
 
from .models import Deal 
 
 
# ============================================================ 
# CREATE / UPDATE DEAL SERIALIZER 
# ============================================================ 
 
class DealCreateSerializer(serializers.ModelSerializer): 
 
    # Lead display name 
    lead_name = serializers.SerializerMethodField() 
 
    # Lead phone number 
    lead_phone = serializers.SerializerMethodField() 
 
    class Meta: 
        model = Deal 
 
        fields = [ 
            "id", 
            "deal_name", 
            "deal_stage", 
            "associated_lead", 
            "lead_name", 
            "lead_phone", 
            "amount", 
            "deal_owner", 
            "close_date", 
            "priority", 
            "created_date", 
            "updated_at", 
        ] 
 
        read_only_fields = [ 
            "id", 
            "created_date", 
            "updated_at", 
            "lead_name", 
            "lead_phone", 
        ] 
 
    # ======================================================== 
    # LEAD NAME 
    # ======================================================== 
 
    def get_lead_name(self, obj): 
 
        if not obj.associated_lead: 
            return "" 
 
        return ( 
            f"{obj.associated_lead.first_name} " 
            f"{obj.associated_lead.last_name}" 
        ).strip() 
 
    # ======================================================== 
    # LEAD PHONE 
    # ======================================================== 
 
    def get_lead_phone(self, obj): 
 
        if not obj.associated_lead: 
            return "" 
 
        return obj.associated_lead.phone_number or "" 
 
    # ======================================================== 
    # CREATE 
    # ======================================================== 
 
    def create(self, validated_data): 
 
        # Get selected lead 
        lead = validated_data["associated_lead"] 
 
        # Create deal 
        deal = Deal.objects.create( 
            **validated_data 
        ) 
 
        # Update Lead status according to Deal stage 
        lead.lead_status = deal.deal_stage 
 
        lead.save( 
            update_fields=["lead_status"] 
        ) 
 
        return deal 
 
    # ======================================================== 
    # UPDATE 
    # ======================================================== 
 
    def update(self, instance, validated_data): 
 
        # Update deal 
        instance = super().update( 
            instance, 
            validated_data 
        ) 
 
        # Get associated lead 
        lead = instance.associated_lead 
 
        # Update Lead status 
        lead.lead_status = instance.deal_stage 
 
        lead.save( 
            update_fields=["lead_status"] 
        ) 
 
        return instance 
 
 
# ============================================================ 
# DEAL LIST SERIALIZER 
# ============================================================ 
 
class DealListSerializer(serializers.ModelSerializer): 
 
    # Lead display name 
    lead_name = serializers.SerializerMethodField() 
 
    # Lead phone number 
    lead_phone = serializers.SerializerMethodField() 
 
    # Owner display name 
    deal_owner = serializers.SerializerMethodField() 
 
    # Owner ID for Edit 
    deal_owner_id = serializers.IntegerField( 
        source="deal_owner.id", 
        read_only=True 
    ) 
 
    class Meta: 
        model = Deal 
 
        fields = [ 
            "id", 
            "deal_name", 
 
            # Lead ID 
            "associated_lead", 
 
            # Lead name 
            "lead_name", 
 
            # Lead phone 
            "lead_phone", 
 
            "deal_stage", 
            "close_date", 
 
            # Owner name 
            "deal_owner", 
 
            # Owner ID 
            "deal_owner_id", 
 
            "amount", 
            "priority", 
            "created_date", 
        ] 
 
    # ======================================================== 
    # LEAD NAME 
    # ======================================================== 
 
    def get_lead_name(self, obj): 
 
        if not obj.associated_lead: 
            return "" 
 
        return ( 
            f"{obj.associated_lead.first_name} " 
            f"{obj.associated_lead.last_name}" 
        ).strip() 
 
    # ======================================================== 
    # LEAD PHONE 
    # ======================================================== 
 
    def get_lead_phone(self, obj): 
 
        if not obj.associated_lead: 
            return "" 
 
        return obj.associated_lead.phone_number or "" 
 
    # ======================================================== 
    # OWNER NAME 
    # ======================================================== 
 
    def get_deal_owner(self, obj): 
 
        if not obj.deal_owner: 
            return "" 
 
        return ( 
            f"{obj.deal_owner.first_name} " 
            f"{obj.deal_owner.last_name}" 
        ).strip() 