from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required,user_passes_test
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render


from .models import (
    Destinations,
    PlanningEnquiryPricing,
    Tours,
    FAQ,
    Review,
    PlanningEnquiry,
    SiteSettings,
    Proposal,
    PlanningEnquiryNote,
    PlanningEnquiryActivity,
)

from .forms import (
    PlanningEnquiryForm,
    PlanningEnquiryPricingForm,
    ReviewForm,
    SignupForm,
    SiteSettingsForm,
    DestinationForm,
    TourForm,
    FAQForm,
    ProposalForm,

)


# =========================================================
# REVIEWS
# =========================================================

# =========================================================
# REVIEWS
# =========================================================

def _get_reviews_for_viewer(request, limit=6):
    """
    Get homepage reviews.

    Rules:
    1. Only published reviews are shown publicly.
    2. Only one review is shown per customer.
    3. Each customer's highest-rated review is selected.
    4. If a customer has multiple reviews with the same
       highest rating, the newest review is selected.
    5. A maximum of `limit` reviews is returned.
    """

    published_reviews = (
        Review.objects
        .filter(is_published=True)
        .select_related('user', 'planning_enquiry')
        .order_by(
            '-rating',
            '-created_at',
            '-id'
        )
    )

    # ---------------------------------------------------------
    # ONE REVIEW PER CUSTOMER
    # ---------------------------------------------------------

    selected_reviews = []

    seen_users = set()

    for review in published_reviews:

        # Reviews without a linked user are handled separately.
        if review.user_id is not None:

            if review.user_id in seen_users:
                continue

            seen_users.add(review.user_id)

        else:
            # For legacy reviews that have no user attached,
            # treat each review as its own customer entry.
            pass

        selected_reviews.append(review)

        if len(selected_reviews) >= limit:
            break

    reviews = selected_reviews

    # ---------------------------------------------------------
    # REVIEW STATISTICS
    #
    # These statistics continue to represent ALL published
    # reviews, not just the six displayed on the homepage.
    # ---------------------------------------------------------

    review_agg = published_reviews.aggregate(
        average_rating=Avg('rating'),
        total=Count('id')
    )

    total_reviews = review_agg['total'] or 0

    recommend_count = published_reviews.filter(
        rating__gte=4
    ).count()

    review_stats = {
        'average_rating':
            review_agg['average_rating'],

        'total':
            total_reviews,

        'recommend_pct':
            round(
                (recommend_count / total_reviews) * 100
            )
            if total_reviews
            else None,
    }

    return reviews, review_stats



# =========================================================
# HOME
# =========================================================

def index(request):

    destinations = Destinations.objects.all()[:6]

    tours = Tours.objects.all()[:3]

    frequents = FAQ.objects.all()

    reviews, review_stats = \
        _get_reviews_for_viewer(request)


    return render(
        request,
        'index.html',
        {
            "destinations": destinations,
            "tours": tours,
            "frequents": frequents,
            "reviews": reviews,
            "review_stats": review_stats,
        }
    )



# =========================================================
# REVIEW JSON FEED
# =========================================================

def reviews_feed(request):

    reviews, review_stats = \
        _get_reviews_for_viewer(request)


    return JsonResponse({

        "reviews": [

            {
                "id": review.id,
                "name": review.name,
                "initials": review.initials,
                "trip": review.trip,
                "rating": review.rating,
                "quote": review.quote,
                "is_published": review.is_published,
            }

            for review in reviews

        ],

        "stats": review_stats,

    })



# =========================================================
# DESTINATIONS
# =========================================================

def destinations(request):

    destinations = Destinations.objects.all()

    return render(
        request,
        'destinations.html',
        {
            "destinations": destinations
        }
    )



# =========================================================
# TOURS
# =========================================================

def tours(request):

    tours = Tours.objects.all()

    return render(
        request,
        'tours.html',
        {
            "tours": tours
        }
    )



# =========================================================
# ABOUT
# =========================================================

def about(request):

    return render(
        request,
        'about.html'
    )



# =========================================================
# SIGN UP
# =========================================================

def signup(request):

    if request.method == 'POST':

        form = SignupForm(request.POST)


        if form.is_valid():

            user = form.save()

            auth_login(
                request,
                user
            )

            return redirect('index')


    else:

        form = SignupForm()


    return render(
        request,
        'signup.html',
        {
            "form": form
        }
    )



# =========================================================
# PROFILE
# =========================================================

@login_required(login_url='login')
def profile(request):

    # ---------------------------------------------------------
    # CUSTOMER REVIEWS
    # ---------------------------------------------------------

    reviews = (
        Review.objects
        .filter(user=request.user)
        .select_related('planning_enquiry')
        .order_by('-created_at')
    )

    # ---------------------------------------------------------
    # CUSTOMER PLANNING ENQUIRIES
    # ---------------------------------------------------------

    if request.user.email:

        planning_enquiries = (
            PlanningEnquiry.objects
            .filter(
                email__iexact=request.user.email
            )
            .order_by('-created_at')
        )

    else:

        planning_enquiries = (
            PlanningEnquiry.objects.none()
        )

    # ---------------------------------------------------------
    # COMPLETED TRIPS
    # ---------------------------------------------------------

    completed_enquiries = (
        planning_enquiries
        .filter(status='completed')
    )

    # ---------------------------------------------------------
    # ENQUIRIES STILL WAITING FOR A REVIEW
    # ---------------------------------------------------------

    reviewed_enquiry_ids = (
        reviews
        .filter(
            planning_enquiry__isnull=False
        )
        .values_list(
            'planning_enquiry_id',
            flat=True
        )
    )

    unreviewed_completed_enquiries = (
        completed_enquiries
        .exclude(
            id__in=reviewed_enquiry_ids
        )
    )

    # ---------------------------------------------------------
    # PROFILE
    # ---------------------------------------------------------

    return render(
        request,
        'profile.html',
        {
            'reviews': reviews,
            'planning_enquiries': planning_enquiries,
            'completed_enquiries': completed_enquiries,
            'unreviewed_completed_enquiries':
                unreviewed_completed_enquiries,
        }
    )


@login_required(login_url='login')
def planning_enquiry_detail(request, enquiry_id):
    enquiry = get_object_or_404(
        PlanningEnquiry,
        id=enquiry_id
    )

    if not request.user.email:
        return redirect('profile')

    if enquiry.email.lower() != request.user.email.lower():
        return redirect('profile')

    return render(
        request,
        'planning_enquiry_detail.html',
        {
            'enquiry': enquiry,
        }
    )



# =========================================================
# LEAVE REVIEW
# =========================================================

@login_required(login_url='login')
def leave_review(request):

    # A review must be connected to the customer's
    # account email so we can identify their trips.
    if not request.user.email:
        messages.error(
            request,
            'Please add an email address to your account before leaving a review.'
        )
        return redirect('profile')

    # Only completed trips can be reviewed.
    completed_enquiries = (
        PlanningEnquiry.objects
        .filter(
            email__iexact=request.user.email,
            status='completed'
        )
        .order_by('-created_at')
    )

    if request.method == 'POST':

        # Get the completed trip selected by the customer.
        enquiry_id = request.POST.get('planning_enquiry')

        if not enquiry_id:
            messages.error(
                request,
                'Please select the completed trip you want to review.'
            )
            return redirect('leave_review')

        # Make sure the selected enquiry:
        # 1. exists
        # 2. belongs to the logged-in customer
        # 3. is completed
        enquiry = get_object_or_404(
            PlanningEnquiry,
            id=enquiry_id,
            email__iexact=request.user.email,
            status='completed'
        )

        # Prevent the same customer from reviewing
        # the same completed trip more than once.
        existing_review = Review.objects.filter(
            user=request.user,
            planning_enquiry=enquiry
        ).first()

        if existing_review:

            messages.info(
                request,
                'You have already reviewed this trip.'
            )

            return redirect('profile')

        # The form now contains only:
        # - rating
        # - quote
        form = ReviewForm(request.POST)

        if form.is_valid():

            review = form.save(commit=False)

            # Automatically connect the review
            # to the logged-in customer.
            review.user = request.user

            # Automatically connect the review
            # to the selected completed trip.
            review.planning_enquiry = enquiry

            # Automatically use the customer's username.
            review.name = request.user.get_username()

            # Every new customer review must be
            # approved by the administrator first.
            review.is_published = False

            # Automatically generate the trip description.
            if enquiry.destination:
                review.trip = f"Trip to {enquiry.destination}"
            else:
                review.trip = "Bespoke trip"

            review.save()

            messages.success(
                request,
                'Thank you for sharing your experience. '
                'Your review is awaiting approval.'
            )

            return redirect('profile')

    else:

        form = ReviewForm()

    return render(
        request,
        'leave_review.html',
        {
            'form': form,
            'completed_enquiries': completed_enquiries,
        }
    )



# =========================================================
# PLANNING
# =========================================================

# =========================================================
# PLANNING
# =========================================================

def planning(request):

    submitted = False

    # =====================================================
    # FORM SUBMISSION
    # =====================================================

    if request.method == 'POST':

        form = PlanningEnquiryForm(
            request.POST
        )

        if form.is_valid():

            enquiry = form.save(
                commit=False
            )

            # ---------------------------------------------
            # LOGGED-IN USER
            # ---------------------------------------------

            if request.user.is_authenticated:

                enquiry.name = (
                    request.user.get_username()
                )

                if request.user.email:

                    enquiry.email = (
                        request.user.email
                    )

            # ---------------------------------------------
            # SAVE ENQUIRY
            # ---------------------------------------------

            enquiry.save()

            submitted = True

            # Clear the form after successful submission
            form = PlanningEnquiryForm()

    # =====================================================
    # DISPLAY FORM
    # =====================================================

    else:

        initial = {}

        # ---------------------------------------------
        # LOGGED-IN USER DETAILS
        # ---------------------------------------------

        if request.user.is_authenticated:

            initial['name'] = (
                request.user.get_username()
            )

            if request.user.email:

                initial['email'] = (
                    request.user.email
                )

        # ---------------------------------------------
        # TOUR SELECTED FROM TOUR CARD
        # ---------------------------------------------

        tour_id = request.GET.get(
            'tour'
        )

        if tour_id:

            try:

                tour = Tours.objects.get(
                    pk=tour_id
                )

                initial['destination'] = (
                    tour.headlights
                )

            except (
                Tours.DoesNotExist,
                ValueError,
                TypeError
            ):

                pass

        # ---------------------------------------------
        # CREATE FORM
        # ---------------------------------------------

        form = PlanningEnquiryForm(
            initial=initial
        )

    return render(
        request,
        'planning.html',
        {
            'form': form,
            'submitted': submitted,
        }
    )


def staff_required(view_func):
    return user_passes_test(
        lambda user: user.is_authenticated and user.is_staff,
        login_url='login'
    )(view_func)

@staff_required
def admin_dashboard(request):
    planning_count = PlanningEnquiry.objects.count()

    new_enquiries_count = PlanningEnquiry.objects.filter(
        status='new'
    ).count()

    contacted_enquiries_count = PlanningEnquiry.objects.filter(
        status='contacted'
    ).count()

    completed_enquiries_count = PlanningEnquiry.objects.filter(
        status='completed'
    ).count()

    total_reviews_count = Review.objects.count()

    pending_reviews_count = Review.objects.filter(
        is_published=False
    ).count()

    published_reviews_count = Review.objects.filter(
        is_published=True
    ).count()

    recent_enquiries = PlanningEnquiry.objects.order_by(
        '-created_at'
    )[:5]

    recent_reviews = Review.objects.order_by(
        '-created_at'
    )[:5]

    attention_enquiries = PlanningEnquiry.objects.filter(
        status='new'
    ).order_by('-created_at')[:5]

    attention_reviews = Review.objects.filter(
        is_published=False
    ).order_by('-created_at')[:5]

    return render(
        request,
        'admin_dashboard/dashboard.html',
        {
            'planning_count': planning_count,
            'new_enquiries_count': new_enquiries_count,
            'contacted_enquiries_count': contacted_enquiries_count,
            'completed_enquiries_count': completed_enquiries_count,

            'total_reviews_count': total_reviews_count,
            'pending_reviews_count': pending_reviews_count,
            'published_reviews_count': published_reviews_count,

            'recent_enquiries': recent_enquiries,
            'recent_reviews': recent_reviews,

            'attention_enquiries': attention_enquiries,
            'attention_reviews': attention_reviews,
        }
    )

@staff_required
def dashboard_reviews(request):

    reviews = Review.objects.select_related(
        'user',
        'planning_enquiry'
    ).all().order_by(
        '-created_at'
    )

    # ======================================================
    # STATISTICS
    # ======================================================

    total_reviews_count = (
        Review.objects.count()
    )

    pending_reviews_count = (
        Review.objects.filter(
            is_published=False
        ).count()
    )

    published_reviews_count = (
        Review.objects.filter(
            is_published=True
        ).count()
    )

    # ======================================================
    # SEARCH
    # ======================================================

    search = request.GET.get(
        'q',
        ''
    ).strip()

    if search:

        reviews = reviews.filter(

            Q(name__icontains=search) |

            Q(trip__icontains=search) |

            Q(quote__icontains=search) |

            Q(
                planning_enquiry__destination__icontains=search
            ) |

            Q(
                planning_enquiry__email__icontains=search
            )

        )

    # ======================================================
    # STATUS FILTER
    # ======================================================

    status = request.GET.get(
        'status',
        ''
    ).strip()

    if status == 'pending':

        reviews = reviews.filter(
            is_published=False
        )

    elif status == 'published':

        reviews = reviews.filter(
            is_published=True
        )

    return render(
        request,
        'admin_dashboard/reviews.html',
        {
            'reviews':
                reviews,

            'search':
                search,

            'status':
                status,

            'total_reviews_count':
                total_reviews_count,

            'pending_reviews_count':
                pending_reviews_count,

            'published_reviews_count':
                published_reviews_count,
        }
    )

@staff_required
def dashboard_review_approve(request, review_id):

    if request.method == 'POST':
        review = get_object_or_404(
            Review,
            id=review_id
        )

        review.is_published = True

        review.save(
            update_fields=['is_published']
        )

        messages.success(
            request,
            f'Review from {review.name} has been approved and published.'
        )

    return redirect('admin_reviews')

@staff_required
def dashboard_review_delete(request, review_id):

    if request.method == 'POST':
        review = get_object_or_404(
            Review,
            id=review_id
        )

        review_name = review.name

        review.delete()

        messages.success(
            request,
            f'Review from {review_name} has been deleted.'
        )

    return redirect('admin_reviews')


@staff_required
def dashboard_planning(request):
    enquiries = PlanningEnquiry.objects.all().order_by('-created_at')

    planning_count = PlanningEnquiry.objects.count()

    new_count = PlanningEnquiry.objects.filter(
        status='new'
    ).count()

    contacted_count = PlanningEnquiry.objects.filter(
        status='contacted'
    ).count()

    completed_count = PlanningEnquiry.objects.filter(
        status='completed'
    ).count()

    search = request.GET.get('q', '').strip()

    if search:
        enquiries = enquiries.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search) |
            Q(destination__icontains=search) |
            Q(travel_dates__icontains=search) |
            Q(message__icontains=search) |
            Q(travel_style__icontains=search) |
            Q(currency__icontains=search)
        )

    status = request.GET.get('status', '').strip()

    if status in ['new', 'contacted', 'completed']:
        enquiries = enquiries.filter(status=status)

    return render(
        request,
        'admin_dashboard/planning_enquiries.html',
        {
            'enquiries': enquiries,
            'search': search,
            'status': status,
            'planning_count': planning_count,
            'new_count': new_count,
            'contacted_count': contacted_count,
            'completed_count': completed_count,
        }
    )

@staff_required
def dashboard_planning_status(request, enquiry_id):
    if request.method == 'POST':
        enquiry = get_object_or_404(
            PlanningEnquiry,
            id=enquiry_id
        )

        new_status = request.POST.get('status', '').strip()

        valid_statuses = {
            'new',
            'contacted',
            'completed',
        }

        if new_status in valid_statuses:
            enquiry.status = new_status
            enquiry.save(update_fields=['status'])

            messages.success(
                request,
                f'Planning enquiry from {enquiry.name} updated to '
                f'{enquiry.get_status_display()}.'
            )

    return redirect('admin_planning')


# ==========================================================
# STAGE 5 - PLANNING ENQUIRY DETAIL
# ==========================================================

@staff_required
def dashboard_planning_detail(request, enquiry_id):

    enquiry = get_object_or_404(
        PlanningEnquiry,
        id=enquiry_id
    )

    notes = (
        PlanningEnquiryNote.objects
        .filter(enquiry=enquiry)
        .select_related('author')
    )

    activities = (
        PlanningEnquiryActivity.objects
        .filter(enquiry=enquiry)
        .select_related('actor')
    )

    return render(
        request,
        "admin_dashboard/planning_enquiry_detail.html",
        {
            "enquiry": enquiry,
            "notes": notes,
            "activities": activities,
        }
    )

@staff_required
def dashboard_planning_note_add(request, enquiry_id):

    enquiry = get_object_or_404(
        PlanningEnquiry,
        id=enquiry_id
    )

    if request.method == 'POST':

        note_text = request.POST.get(
            'note',
            ''
        ).strip()

        if not note_text:

            messages.error(
                request,
                'Please enter a note before saving.'
            )

            return redirect(
                'admin_planning_detail',
                enquiry_id=enquiry.id
            )

        PlanningEnquiryNote.objects.create(
            enquiry=enquiry,
            author=request.user,
            note=note_text
        )

        PlanningEnquiryActivity.objects.create(
    enquiry=enquiry,
    actor=request.user,
    activity_type='note_added',
    description='Internal note added'
)

        messages.success(
            request,
            'Internal note added successfully.'
        )

    return redirect(
        'admin_planning_detail',
        enquiry_id=enquiry.id
    )

@staff_required
def dashboard_planning_note_edit(request, note_id):

    note = get_object_or_404(
        PlanningEnquiryNote,
        id=note_id
    )

    if request.method == 'POST':

        note_text = request.POST.get(
            'note',
            ''
        ).strip()

        if not note_text:

            messages.error(
                request,
                'The note cannot be empty.'
            )

            return redirect(
                'admin_planning_detail',
                enquiry_id=note.enquiry_id
            )

        note.note = note_text
        note.save()

        messages.success(
            request,
            'Internal note updated successfully.'
        )

    return redirect(
        'admin_planning_detail',
        enquiry_id=note.enquiry_id
    )

@staff_required
def dashboard_planning_note_delete(request, note_id):

    note = get_object_or_404(
        PlanningEnquiryNote,
        id=note_id
    )

    enquiry_id = note.enquiry_id

    if request.method == 'POST':

        note.delete()

        messages.success(
            request,
            'Internal note deleted successfully.'
        )

    return redirect(
        'admin_planning_detail',
        enquiry_id=enquiry_id
    )

@staff_required
def dashboard_planning_pricing(request, enquiry_id):

    enquiry = get_object_or_404(
        PlanningEnquiry,
        id=enquiry_id
    )

    pricing, created = PlanningEnquiryPricing.objects.get_or_create(
        enquiry=enquiry
    )

    if request.method == 'POST':

        form = PlanningEnquiryPricingForm(
            request.POST,
            instance=pricing
        )

        if form.is_valid():

            form.save()

            PlanningEnquiryActivity.objects.create(
                enquiry=enquiry,
                actor=request.user,
                activity_type='pricing_updated',
                description='Trip pricing updated'
            )

            messages.success(
                request,
                'Trip pricing has been saved successfully.'
            )

            return redirect(
                'admin_planning_detail',
                enquiry_id=enquiry.id
            )

    else:

        form = PlanningEnquiryPricingForm(
            instance=pricing
        )

    return render(
        request,
        'admin_dashboard/planning_pricing.html',
        {
            'enquiry': enquiry,
            'pricing': pricing,
            'form': form,
        }
    )


@staff_required
def dashboard_analytics(request):
    total_enquiries = PlanningEnquiry.objects.count()

    new_enquiries = PlanningEnquiry.objects.filter(
        status='new'
    ).count()

    contacted_enquiries = PlanningEnquiry.objects.filter(
        status='contacted'
    ).count()

    completed_enquiries = PlanningEnquiry.objects.filter(
        status='completed'
    ).count()

    total_reviews = Review.objects.count()

    published_reviews = Review.objects.filter(
        is_published=True
    ).count()

    pending_reviews = Review.objects.filter(
        is_published=False
    ).count()

    travel_style_data = (
        PlanningEnquiry.objects
        .values('travel_style')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    currency_data = (
        PlanningEnquiry.objects
        .values('currency')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    destination_data = (
        PlanningEnquiry.objects
        .exclude(destination='')
        .values('destination')
        .annotate(total=Count('id'))
        .order_by('-total')[:10]
    )

    recent_enquiries = PlanningEnquiry.objects.order_by(
        '-created_at'
    )[:10]

    return render(
        request,
        'admin_dashboard/analytics.html',
        {
            'total_enquiries': total_enquiries,
            'new_enquiries': new_enquiries,
            'contacted_enquiries': contacted_enquiries,
            'completed_enquiries': completed_enquiries,
            'total_reviews': total_reviews,
            'published_reviews': published_reviews,
            'pending_reviews': pending_reviews,
            'travel_style_data': travel_style_data,
            'currency_data': currency_data,
            'destination_data': destination_data,
            'recent_enquiries': recent_enquiries,
        }
    )


@staff_required
def dashboard_settings(request):
    settings_obj, created = SiteSettings.objects.get_or_create(
        pk=1,
        defaults={
            'business_name': 'Wanderwell',
        }
    )

    if request.method == 'POST':
        form = SiteSettingsForm(
            request.POST,
            instance=settings_obj
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Website settings have been updated successfully.'
            )

            return redirect('dashboard_settings')

    else:
        form = SiteSettingsForm(
            instance=settings_obj
        )

    return render(
        request,
        'admin_dashboard/settings.html',
        {
            'form': form,
            'settings_obj': settings_obj,
        }
    )

# ==========================================================
# ADMIN — TOURS
# ==========================================================

@staff_required
def dashboard_tours(request):

    tours = Tours.objects.all().order_by('-id')

    return render(
        request,
        'admin_dashboard/tours.html',
        {
            'tours': tours,
        }
    )


@staff_required
def dashboard_tour_add(request):

    if request.method == 'POST':

        form = TourForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Tour added successfully.'
            )

            return redirect('admin_tours')

    else:

        form = TourForm()

    return render(
        request,
        'admin_dashboard/tour_form.html',
        {
            'form': form,
            'form_title': 'Add Tour',
            'submit_text': 'Add Tour',
        }
    )


@staff_required
def dashboard_tour_edit(request, tour_id):

    tour = get_object_or_404(
        Tours,
        id=tour_id
    )

    if request.method == 'POST':

        form = TourForm(
            request.POST,
            request.FILES,
            instance=tour
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Tour updated successfully.'
            )

            return redirect('admin_tours')

    else:

        form = TourForm(
            instance=tour
        )

    return render(
        request,
        'admin_dashboard/tour_form.html',
        {
            'form': form,
            'tour': tour,
            'form_title': 'Edit Tour',
            'submit_text': 'Save Changes',
        }
    )


@staff_required
def dashboard_tour_delete(request, tour_id):

    if request.method == 'POST':

        tour = get_object_or_404(
            Tours,
            id=tour_id
        )

        tour.delete()

        messages.success(
            request,
            'Tour deleted successfully.'
        )

    return redirect('admin_tours')

# ==========================================================
# ADMIN — DESTINATIONS
# ==========================================================

@staff_required
def dashboard_destinations(request):

    destinations = (
        Destinations.objects
        .all()
        .order_by('-id')
    )

    return render(
        request,
        'admin_dashboard/destinations.html',
        {
            'destinations': destinations,
        }
    )


@staff_required
def dashboard_destination_add(request):

    if request.method == 'POST':

        form = DestinationForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Destination added successfully.'
            )

            return redirect(
                'admin_destinations'
            )

    else:

        form = DestinationForm()

    return render(
        request,
        'admin_dashboard/destination_form.html',
        {
            'form': form,
            'form_title': 'Add Destination',
            'submit_text': 'Add Destination',
        }
    )


@staff_required
def dashboard_destination_edit(
    request,
    destination_id
):

    destination = get_object_or_404(
        Destinations,
        id=destination_id
    )

    if request.method == 'POST':

        form = DestinationForm(
            request.POST,
            request.FILES,
            instance=destination
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Destination updated successfully.'
            )

            return redirect(
                'admin_destinations'
            )

    else:

        form = DestinationForm(
            instance=destination
        )

    return render(
        request,
        'admin_dashboard/destination_form.html',
        {
            'form': form,
            'destination': destination,
            'form_title': 'Edit Destination',
            'submit_text': 'Save Changes',
        }
    )


@staff_required
def dashboard_destination_delete(
    request,
    destination_id
):

    if request.method == 'POST':

        destination = get_object_or_404(
            Destinations,
            id=destination_id
        )

        destination.delete()

        messages.success(
            request,
            'Destination deleted successfully.'
        )

    return redirect(
        'admin_destinations'
    )

# ==========================================================
# ADMIN — FAQ
# ==========================================================

@staff_required
def dashboard_faqs(request):

    faqs = FAQ.objects.all().order_by('id')

    return render(
        request,
        'admin_dashboard/faqs.html',
        {
            'faqs': faqs,
        }
    )


@staff_required
def dashboard_faq_add(request):

    if request.method == 'POST':

        form = FAQForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'FAQ added successfully.'
            )

            return redirect(
                'admin_faqs'
            )

    else:

        form = FAQForm()

    return render(
        request,
        'admin_dashboard/faq_form.html',
        {
            'form': form,
            'form_title': 'Add FAQ',
            'submit_text': 'Add FAQ',
        }
    )


@staff_required
def dashboard_faq_edit(request, faq_id):

    faq = get_object_or_404(
        FAQ,
        id=faq_id
    )

    if request.method == 'POST':

        form = FAQForm(
            request.POST,
            instance=faq
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'FAQ updated successfully.'
            )

            return redirect(
                'admin_faqs'
            )

    else:

        form = FAQForm(
            instance=faq
        )

    return render(
        request,
        'admin_dashboard/faq_form.html',
        {
            'form': form,
            'faq': faq,
            'form_title': 'Edit FAQ',
            'submit_text': 'Save Changes',
        }
    )


@staff_required
def dashboard_faq_delete(request, faq_id):

    if request.method == 'POST':

        faq = get_object_or_404(
            FAQ,
            id=faq_id
        )

        faq.delete()

        messages.success(
            request,
            'FAQ deleted successfully.'
        )

    return redirect(
        'admin_faqs'
    )


@login_required
def dashboard_proposal_create(request, enquiry_id):

    if not request.user.is_staff:
        return redirect('index')

    enquiry = get_object_or_404(
        PlanningEnquiry,
        id=enquiry_id
    )

    # ------------------------------------------------------
    # PREVENT DUPLICATE PROPOSALS
    # ------------------------------------------------------

    if hasattr(enquiry, 'proposal'):

        return redirect(
            'admin_proposal_edit',
            proposal_id=enquiry.proposal.id
        )

    # ------------------------------------------------------
    # GET SAVED PRICING
    # ------------------------------------------------------

    pricing = getattr(
        enquiry,
        'pricing',
        None
    )

    # ------------------------------------------------------
    # CREATE PROPOSAL
    # ------------------------------------------------------

    if request.method == 'POST':

        form = ProposalForm(
            request.POST
        )

        if form.is_valid():

            proposal = form.save(
                commit=False
            )

            proposal.enquiry = enquiry
            proposal.status = 'draft'

            proposal.save()

            messages.success(
                request,
                'Travel proposal created successfully.'
            )

            return redirect(
                'admin_proposal_edit',
                proposal_id=proposal.id
            )

    else:

        initial = {}

        # --------------------------------------------------
        # COPY SAVED PRICING INTO PROPOSAL
        # --------------------------------------------------

        if pricing:

            initial = {
                'accommodation_cost':
                    pricing.accommodation,

                'transport_cost':
                    (
                        pricing.transportation
                        + pricing.transfers
                    ),

                'activities_cost':
                    pricing.activities,

                'other_cost':
                    pricing.other_costs,

                'service_fee':
                    pricing.service_fee,
            }

        form = ProposalForm(
            initial=initial
        )

    return render(
        request,
        'admin_dashboard/proposal_form.html',
        {
            'form': form,
            'enquiry': enquiry,
            'proposal': None,
            'pricing': pricing,
            'page_title': 'Create Proposal',
        }
    )


@login_required
def dashboard_proposal_edit(request, proposal_id):
    if not request.user.is_staff:
        return redirect('index')

    proposal = get_object_or_404(
        Proposal,
        id=proposal_id
    )

    enquiry = proposal.enquiry

    # ------------------------------------------------------
    # BUDGET COMPARISON
    # ------------------------------------------------------

    customer_budget = enquiry.budget or 0

    proposal_total = proposal.total_cost or 0

    budget_difference = (
        customer_budget - proposal_total
    )

    within_budget = (
        proposal_total <= customer_budget
    )

    # ------------------------------------------------------
    # EDIT PROPOSAL
    # ------------------------------------------------------

    if request.method == 'POST':
        form = ProposalForm(
            request.POST,
            instance=proposal
        )

        if form.is_valid():
            proposal = form.save(commit=False)

            # If the customer requested changes,
            # editing the proposal returns it to draft.
            if proposal.status == 'changes_requested':
                proposal.status = 'draft'

            proposal.save()

            messages.success(
                request,
                'Proposal updated successfully.'
            )

            return redirect(
                'admin_proposal_edit',
                proposal_id=proposal.id
            )

    else:
        form = ProposalForm(
            instance=proposal
        )

    return render(
        request,
        'admin_dashboard/proposal_form.html',
        {
            'form': form,
            'enquiry': enquiry,
            'proposal': proposal,
            'page_title': 'Edit Proposal',

            # Budget comparison
            'customer_budget': customer_budget,
            'proposal_total': proposal_total,
            'budget_difference': budget_difference,
            'within_budget': within_budget,
        }
    )


@login_required
def dashboard_proposal_send(request, proposal_id):
    if not request.user.is_staff:
        return redirect('index')

    proposal = get_object_or_404(
        Proposal,
        id=proposal_id
    )

    if request.method != 'POST':
        return redirect(
            'admin_proposal_edit',
            proposal_id=proposal.id
        )

    # Only send proposals that have been saved as drafts.
    if proposal.status not in ['draft', 'changes_requested']:
        messages.warning(
            request,
            'This proposal cannot be sent in its current status.'
        )

        return redirect(
            'admin_proposal_edit',
            proposal_id=proposal.id
        )

    # Make sure there is actually a price.
    if proposal.total_cost <= 0:
        messages.error(
            request,
            'Please add the trip costs and service fee before sending the proposal.'
        )

        return redirect(
            'admin_proposal_edit',
            proposal_id=proposal.id
        )

    proposal.status = 'sent'
    proposal.save(update_fields=['status', 'updated_at'])

    messages.success(
        request,
        'Proposal has been sent to the customer.'
    )

    return redirect(
        'admin_proposal_edit',
        proposal_id=proposal.id
    )

@login_required
def customer_proposal_detail(request, proposal_id):
    proposal = get_object_or_404(
        Proposal,
        id=proposal_id,
        enquiry__user=request.user
    )

    # A sent proposal becomes viewed when the customer opens it.
    if proposal.status == 'sent':
        proposal.status = 'viewed'
        proposal.save(update_fields=['status', 'updated_at'])

    return render(
        request,
        'customer_proposal_detail.html',
        {
            'proposal': proposal,
            'enquiry': proposal.enquiry,
        }
    )







@login_required
def customer_proposal_request_changes(request, proposal_id):

    proposal = get_object_or_404(
        Proposal,
        id=proposal_id
    )

    if request.method != 'POST':
        return redirect(
            'customer_proposal',
            proposal_id=proposal.id
        )

    customer_message = request.POST.get(
        'customer_message',
        ''
    ).strip()

    if not customer_message:
        messages.error(
            request,
            'Please tell us what you would like changed.'
        )

        return redirect(
            'customer_proposal',
            proposal_id=proposal.id
        )

    if proposal.status not in [
        'sent',
        'viewed',
    ]:
        messages.warning(
            request,
            'This proposal is no longer available for changes.'
        )

        return redirect(
            'customer_proposal',
            proposal_id=proposal.id
        )

    proposal.status = 'changes_requested'
    proposal.customer_message = customer_message


    proposal.save(
        update_fields=[
            'status',
            'customer_message',
            'responded_at',
            'updated_at',
        ]
    )

    messages.success(
        request,
        'Your change request has been sent successfully.'
    )

    return redirect(
        'customer_proposal',
        proposal_id=proposal.id
    )





@login_required
def customer_proposal_detail(request, proposal_id):
    proposal = get_object_or_404(
        Proposal,
        id=proposal_id,
        enquiry__email=request.user.email
    )

    if proposal.status == 'sent':
        proposal.status = 'viewed'
        proposal.save(update_fields=['status', 'updated_at'])

    return render(
        request,
        'customer_proposal_detail.html',
        {
            'proposal': proposal,
            'enquiry': proposal.enquiry,
        }
    )



@login_required
def customer_proposal_view(request, proposal_id):

    proposal = get_object_or_404(
        Proposal.objects.select_related('enquiry'),
        id=proposal_id,
    )

    enquiry = proposal.enquiry

    # ------------------------------------------------------
    # CUSTOMER ISOLATION
    # ------------------------------------------------------

    if request.user.email.lower() != enquiry.email.lower():
        return redirect('index')

    # ------------------------------------------------------
    # CUSTOMER PROPOSAL STATUS
    # ------------------------------------------------------

    if proposal.status == 'sent':
        proposal.status = 'viewed'

        proposal.save(
            update_fields=[
                'status',
                'updated_at',
            ]
        )

    # ------------------------------------------------------
    # CUSTOMER PROPOSAL
    # ------------------------------------------------------

    return render(
        request,
        'customer/proposal.html',
        {
            'proposal': proposal,
            'enquiry': enquiry,
        }
    )



@login_required
def customer_proposal_accept(request, proposal_id):

    proposal = get_object_or_404(
        Proposal,
        id=proposal_id
    )

    if request.method != 'POST':
        return redirect(
            'customer_proposal',
            proposal_id=proposal.id
        )

    # Only an active proposal can be accepted.
    if proposal.status not in ['sent', 'viewed']:
        messages.error(
            request,
            'This proposal cannot be accepted.'
        )

        return redirect(
            'customer_proposal',
            proposal_id=proposal.id
        )

    proposal.status = 'accepted'

    proposal.save(
    update_fields=[
        'status',
        'updated_at',
    ]
)

    messages.success(
        request,
        'Thank you. Your travel proposal has been accepted.'
    )

    return redirect(
        'customer_proposal',
        proposal_id=proposal.id
    )


@login_required
def customer_proposal_history(request):

    proposals = (
        Proposal.objects
        .filter(
            enquiry__email__iexact=request.user.email
        )
        .select_related(
            'enquiry'
        )
        .order_by(
            '-created_at'
        )
    )

    return render(
        request,
        'customer/proposal_history.html',
        {
            'proposals': proposals,
        }
    )
