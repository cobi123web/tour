from .models import SiteSettings,Proposal


def site_settings(request):
    settings_obj = SiteSettings.objects.filter(
        pk=1
    ).first()

    return {
        'site_settings': settings_obj,
    }




def customer_notifications(request):

    if not request.user.is_authenticated:
        return {
            'customer_proposal_count': 0,
        }

    if not request.user.email:
        return {
            'customer_proposal_count': 0,
        }

    unread_count = Proposal.objects.filter(
        enquiry__email__iexact=request.user.email,
        status='sent',
    ).count()

    return {
        'customer_proposal_count': unread_count,
    }
