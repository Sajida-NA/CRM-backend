from django.db.models import Count, Q, Sum, Value, DecimalField
from django.db.models.functions import TruncMonth,Coalesce
from django.utils import timezone

from django.contrib.auth import get_user_model

from apps.leads.models import Lead
from apps.deals.models import Deal

User = get_user_model()


CLOSED_STAGES = [
    "Closed Won",
    "Closed Lost",
]

ACTIVE_STAGES = [
    "Contract Sent",
    "Appointment Scheduled",
    "Presentation Scheduled",
    "Qualified to Buy",
    "Decision Maker Bought In",
]


def get_dashboard_summary():

    # Total number of leads
    total_leads = Lead.objects.count()

    # Active deals
    active_deals = Deal.objects.filter(
        deal_stage__in=ACTIVE_STAGES
    ).count()

    # Closed deals
    closed_deals = Deal.objects.filter(
        deal_stage__in=CLOSED_STAGES
    ).count()

    # Current date
    today = timezone.localdate()

    # Current month revenue
    monthly_revenue = Deal.objects.filter(
        deal_stage="Closed Won",
        close_date__year=today.year,
        close_date__month=today.month,
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0

    return {
        "total_leads": total_leads,
        "active_deals": active_deals,
        "closed_deals": closed_deals,
        "monthly_revenue": monthly_revenue,
    }


def get_conversion_data():

    total_leads = Lead.objects.count()

    if total_leads == 0:
        return {
            "contact": {
                "count": 0,
                "percentage": 0,
            },
            "qualified_lead": {
                "count": 0,
                "percentage": 0,
            },
            "proposal_sent": {
                "count": 0,
                "percentage": 0,
            },
            "negotiation": {
                "count": 0,
                "percentage": 0,
            },
            "closed_won": {
                "count": 0,
                "percentage": 0,
            },
            "closed_lost": {
                "count": 0,
                "percentage": 0,
            },
        }

    contact_count = Lead.objects.filter(
        lead_status__in=[
            "New",
            "Open",
            "In Progress",
            "Appointment Scheduled",
        ]
    ).count()

    qualified_lead_count = Lead.objects.filter(
        lead_status="Qualified to Buy"
    ).count()

    proposal_sent_count = Lead.objects.filter(
        lead_status="Contract Sent"
    ).count()

    negotiation_count = Lead.objects.filter(
        lead_status="Decision Maker Bought In"
    ).count()

    closed_won_count = Lead.objects.filter(
        lead_status="Closed Won"
    ).count()

    closed_lost_count = Lead.objects.filter(
        lead_status="Closed Lost"
    ).count()

    return {
        "contact": {
            "count": contact_count,
            "percentage": round(
                (contact_count / total_leads) * 100
            ),
        },

        "qualified_lead": {
            "count": qualified_lead_count,
            "percentage": round(
                (qualified_lead_count / total_leads) * 100
            ),
        },

        "proposal_sent": {
            "count": proposal_sent_count,
            "percentage": round(
                (proposal_sent_count / total_leads) * 100
            ),
        },

        "negotiation": {
            "count": negotiation_count,
            "percentage": round(
                (negotiation_count / total_leads) * 100
            ),
        },

        "closed_won": {
            "count": closed_won_count,
            "percentage": round(
                (closed_won_count / total_leads) * 100
            ),
        },

        "closed_lost": {
            "count": closed_lost_count,
            "percentage": round(
                (closed_lost_count / total_leads) * 100
            ),
        },
    }


def get_sales_report():

    today = timezone.localdate()

    monthly_sales = (
        Deal.objects
        .filter(
            deal_stage="Closed Won",
            close_date__year=today.year,
        )
        .annotate(
            month=TruncMonth("close_date")
        )
        .values("month")
        .annotate(
            revenue=Sum("amount")
        )
        .order_by("month")
    )

    sales_by_month = {
        item["month"].month: item["revenue"]
        for item in monthly_sales
    }

    months = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]

    report = []

    for month_number, month_name in enumerate(months, start=1):

        revenue = sales_by_month.get(month_number, 0)

        report.append({
            "month": month_name,
            "revenue": revenue,
        })

    return report


def get_team_performance():

    team_performance = (
        User.objects
        .filter(
            owned_deals__isnull=False
        )
        .annotate(
            active_deals=Count(
                "owned_deals",
                filter=Q(
                    owned_deals__deal_stage__in=ACTIVE_STAGES
                ),
                distinct=True
            ),

            closed_deals=Count(
                "owned_deals",
                filter=Q(
                    owned_deals__deal_stage__in=CLOSED_STAGES
                ),
                distinct=True
            ),

            revenue=Coalesce(
                Sum(
                    "owned_deals__amount",
                    filter=Q(
                        owned_deals__deal_stage="Closed Won"
                    )
                ),
                Value(0),
                output_field=DecimalField(
                    max_digits=12,
                    decimal_places=2
                )
            )
        )
        .order_by("-revenue")
    )

    for employee in team_performance:
        employee.revenue_change = "0%"

    return team_performance