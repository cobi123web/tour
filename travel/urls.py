from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    # =========================================================
    # PUBLIC WEBSITE
    # =========================================================

    path(
        "",
        views.index,
        name="index"
    ),

    path(
        "destinations/",
        views.destinations,
        name="destinations"
    ),

    path(
        "tours/",
        views.tours,
        name="tours"
    ),

    path(
        "about/",
        views.about,
        name="about"
    ),

    path(
        "planning/",
        views.planning,
        name="planning"
    ),


    # =========================================================
    # REVIEWS
    # =========================================================

    path(
        "leave-a-review/",
        views.leave_review,
        name="leave_review"
    ),

    path(
        "api/reviews/",
        views.reviews_feed,
        name="reviews_feed"
    ),


    # =========================================================
    # CUSTOMER ACCOUNT
    # =========================================================

    path(
        "profile/",
        views.profile,
        name="profile"
    ),

    path(
        "signup/",
        views.signup,
        name="signup"
    ),

    path(
    "login/",
    auth_views.LoginView.as_view(
        template_name="login.html"
    ),
    name="login"
),

    path(
        "logout/",
        auth_views.LogoutView.as_view(
            next_page="index"
        ),
        name="logout"
    ),


    # =========================================================
    # CUSTOMER PLANNING ENQUIRY DETAILS
    # =========================================================

    path(
        "planning-enquiry/<int:enquiry_id>/",
        views.planning_enquiry_detail,
        name="planning_enquiry_detail"
    ),


    # =========================================================
    # ADMIN DASHBOARD
    # =========================================================

    path(
        "dashboard/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),

    path(
        "dashboard/reviews/",
        views.dashboard_reviews,
        name="admin_reviews"
    ),

    path(
        "dashboard/reviews/approve/<int:review_id>/",
        views.dashboard_review_approve,
        name="admin_review_approve"
    ),

    path(
        "dashboard/reviews/delete/<int:review_id>/",
        views.dashboard_review_delete,
        name="admin_review_delete"
    ),

    path(
        "dashboard/planning/",
        views.dashboard_planning,
        name="admin_planning"
    ),

    path(
        "dashboard/planning/status/<int:enquiry_id>/",
        views.dashboard_planning_status,
        name="admin_planning_status"
    ),

    path(
        "dashboard/planning/<int:enquiry_id>/",
        views.dashboard_planning_detail,
        name="admin_planning_detail"
    ),

    path(
        "dashboard/analytics/",
        views.dashboard_analytics,
        name="admin_analytics"
    ),

    path(
        "dashboard/settings/",
        views.dashboard_settings,
        name="dashboard_settings"
    ),

    # ==========================================================
# TOURS
# ==========================================================

path(
    'dashboard/tours/',
    views.dashboard_tours,
    name='admin_tours'
),

path(
    'dashboard/tours/add/',
    views.dashboard_tour_add,
    name='admin_tour_add'
),

path(
    'dashboard/tours/<int:tour_id>/edit/',
    views.dashboard_tour_edit,
    name='admin_tour_edit'
),

path(
    'dashboard/tours/<int:tour_id>/delete/',
    views.dashboard_tour_delete,
    name='admin_tour_delete'
),


# ==========================================================
# DESTINATIONS
# ==========================================================

path(
    'dashboard/destinations/',
    views.dashboard_destinations,
    name='admin_destinations'
),

path(
    'dashboard/destinations/add/',
    views.dashboard_destination_add,
    name='admin_destination_add'
),

path(
    'dashboard/destinations/<int:destination_id>/edit/',
    views.dashboard_destination_edit,
    name='admin_destination_edit'
),

path(
    'dashboard/destinations/<int:destination_id>/delete/',
    views.dashboard_destination_delete,
    name='admin_destination_delete'
),

# ==========================================================
# FAQ MANAGEMENT
# ==========================================================

path(
    'dashboard/faqs/',
    views.dashboard_faqs,
    name='admin_faqs'
),

path(
    'dashboard/faqs/add/',
    views.dashboard_faq_add,
    name='admin_faq_add'
),

path(
    'dashboard/faqs/<int:faq_id>/edit/',
    views.dashboard_faq_edit,
    name='admin_faq_edit'
),

path(
    'dashboard/faqs/<int:faq_id>/delete/',
    views.dashboard_faq_delete,
    name='admin_faq_delete'
),

path(
    'dashboard/proposal/create/<int:enquiry_id>/',
    views.dashboard_proposal_create,
    name='admin_proposal_create'
),

path(
    'dashboard/proposal/<int:proposal_id>/edit/',
    views.dashboard_proposal_edit,
    name='admin_proposal_edit'
),


path(
    'dashboard/proposal/<int:proposal_id>/send/',
    views.dashboard_proposal_send,
    name='admin_proposal_send'
),

path(
    'proposal/<int:proposal_id>/',
    views.customer_proposal_detail,
    name='customer_proposal_detail'
),


path(
    'proposal/<int:proposal_id>/accept/',
    views.customer_proposal_accept,
    name='customer_proposal_accept'
),



path(
    'customer/proposal/<int:proposal_id>/',
    views.customer_proposal_view,
    name='customer_proposal'
),

path(
    'customer/proposal/<int:proposal_id>/accept/',
    views.customer_proposal_accept,
    name='customer_proposal_accept'
),

path(
    'dashboard/planning/<int:enquiry_id>/notes/add/',
    views.dashboard_planning_note_add,
    name='admin_planning_note_add'
),

path(
    'dashboard/planning/notes/<int:note_id>/edit/',
    views.dashboard_planning_note_edit,
    name='admin_planning_note_edit'
),

path(
    'dashboard/planning/notes/<int:note_id>/delete/',
    views.dashboard_planning_note_delete,
    name='admin_planning_note_delete'
),

path(
    'dashboard/planning/<int:enquiry_id>/pricing/',
    views.dashboard_planning_pricing,
    name='admin_planning_pricing'
),

path(
    'customer/proposal/<int:proposal_id>/changes/',
    views.customer_proposal_request_changes,
    name='customer_proposal_request_changes'
),


path(
    'customer/proposals/',
    views.customer_proposal_history,
    name='customer_proposal_history'
),


]


# =========================================================
# MEDIA FILES - DEVELOPMENT ONLY
# =========================================================

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )