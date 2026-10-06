
from django.db import models
from django.contrib.auth.models import User


# ==========================================================
# DESTINATIONS
# ==========================================================

class Destinations(models.Model):

    image = models.ImageField(
        upload_to='destination/'
    )

    city = models.CharField(
        max_length=50
    )

    country = models.CharField(
        max_length=50
    )

    def __str__(self):
        return f"{self.city}, {self.country}"


# ==========================================================
# TOURS
# ==========================================================

class Tours(models.Model):

    image = models.ImageField(
        upload_to='tours/'
    )

    headlights = models.CharField(
        max_length=50
    )

    description = models.TextField(
        max_length=200
    )

    def __str__(self):
        return self.headlights

# ==========================================================
# FAQ
# ==========================================================

class FAQ(models.Model):

    questions = models.CharField(
        max_length=100
    )

    answers = models.TextField(
        max_length=1000
    )

    def __str__(self):
        return self.questions


# ==========================================================
# REVIEWS
# ==========================================================

class Review(models.Model):

    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    # ------------------------------------------------------
    # CUSTOMER
    # ------------------------------------------------------

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='reviews',
        help_text='Customer who submitted the review.'
    )

    # ------------------------------------------------------
    # LINK REVIEW TO SPECIFIC PLANNING ENQUIRY
    # ------------------------------------------------------

    planning_enquiry = models.ForeignKey(
        'PlanningEnquiry',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviews',
        help_text='The planning enquiry this review is associated with.'
    )

    # ------------------------------------------------------
    # REVIEW DETAILS
    # ------------------------------------------------------

    name = models.CharField(
        max_length=100
    )

    trip = models.CharField(
        max_length=150,
        blank=True,
        help_text='e.g. "Trip to Kyoto, Japan"'
    )

    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        default=5
    )

    quote = models.TextField(
        max_length=500
    )

    # ------------------------------------------------------
    # PUBLICATION
    # ------------------------------------------------------

    is_published = models.BooleanField(
        default=True,
        help_text='Uncheck to hide this review from the site without deleting it.'
    )

    # ------------------------------------------------------
    # TIMESTAMP
    # ------------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} — {self.rating}★"

    @property
    def initials(self):

        parts = self.name.split()

        return ''.join(
            part[0].upper()
            for part in parts[:2]
        ) if parts else ''

    @property
    def stars_filled(self):

        return range(
            self.rating
        )

    @property
    def stars_empty(self):

        return range(
            5 - self.rating
        )


# ==========================================================
# PLANNING ENQUIRY
# ==========================================================

class PlanningEnquiry(models.Model):

    # ------------------------------------------------------
    # TRAVEL STYLE
    # ------------------------------------------------------

    TRAVEL_STYLE_CHOICES = [

        (
            'budget',
            'Budget-conscious'
        ),

        (
            'comfortable',
            'Comfortable'
        ),

        (
            'premium',
            'Premium'
        ),

        (
            'luxury',
            'Luxury'
        ),

    ]

    # ------------------------------------------------------
    # CURRENCY
    # ------------------------------------------------------

    CURRENCY_CHOICES = [

        (
            'NGN',
            'Nigerian Naira (₦)'
        ),

        (
            'USD',
            'US Dollar ($)'
        ),

        (
            'GBP',
            'British Pound (£)'
        ),

        (
            'EUR',
            'Euro (€)'
        ),

    ]

    # ------------------------------------------------------
    # STATUS
    # ------------------------------------------------------

    STATUS_CHOICES = [

        (
            'new',
            'New'
        ),

        (
            'contacted',
            'Contacted'
        ),

        (
            'completed',
            'Completed'
        ),

    ]

    # ------------------------------------------------------
    # CUSTOMER
    # ------------------------------------------------------

    name = models.CharField(
        max_length=100
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=30,
        blank=True
    )

    # ------------------------------------------------------
    # TRIP
    # ------------------------------------------------------

    destination = models.CharField(
        max_length=100,
        blank=True,
        help_text='Where are you dreaming of going?'
    )

    travel_dates = models.CharField(
        max_length=100,
        blank=True,
        help_text='Rough dates, or "flexible"'
    )

    travellers = models.PositiveIntegerField(
        default=1,
        help_text='Number of people travelling.'
    )

    # ------------------------------------------------------
    # BUDGET
    # ------------------------------------------------------

    budget = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Approximate total trip budget.'
    )

    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='NGN'
    )

    travel_style = models.CharField(
        max_length=20,
        choices=TRAVEL_STYLE_CHOICES,
        default='comfortable'
    )

    # ------------------------------------------------------
    # ENQUIRY STATUS
    # ------------------------------------------------------

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )

    # ------------------------------------------------------
    # MESSAGE
    # ------------------------------------------------------

    message = models.TextField(
        max_length=1000,
        blank=True
    )

    # ------------------------------------------------------
    # CREATED
    # ------------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-created_at']

        verbose_name_plural = 'Planning enquiries'

    def __str__(self):

        return f"{self.name} ({self.email})"

    @property
    def whatsapp_number(self):

        digits = ''.join(
            character
            for character in self.phone
            if character.isdigit()
        )

        if digits.startswith('0'):

            return '234' + digits[1:]

        if digits.startswith('234'):

            return digits

        return digits

class PlanningEnquiryPricing(models.Model):

    enquiry = models.OneToOneField(
        PlanningEnquiry,
        on_delete=models.CASCADE,
        related_name='pricing'
    )

    accommodation = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    transportation = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    activities = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    transfers = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    other_costs = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    service_fee = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    @property
    def total(self):

        return (
            self.accommodation
            + self.transportation
            + self.activities
            + self.transfers
            + self.other_costs
            + self.service_fee
        )

    def __str__(self):

        return f"Pricing for {self.enquiry.name}"

@property
def customer_budget(self):
    return self.enquiry.budget or 0


@property
def budget_difference(self):
    return self.customer_budget - self.total


@property
def within_budget(self):
    return self.total <= self.customer_budget


# ==========================================================
# TRAVEL PROPOSALS
# ==========================================================

class Proposal(models.Model):

    # ------------------------------------------------------
    # STATUS
    # ------------------------------------------------------

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('viewed', 'Viewed'),
        ('changes_requested', 'Changes Requested'),
        ('accepted', 'Accepted'),
    ]

    # ------------------------------------------------------
    # LINK TO PLANNING ENQUIRY
    # ------------------------------------------------------

    enquiry = models.OneToOneField(
        'PlanningEnquiry',
        on_delete=models.CASCADE,
        related_name='proposal',
        help_text='Planning enquiry this proposal belongs to.'
    )

    # ------------------------------------------------------
    # PROPOSAL INFORMATION
    # ------------------------------------------------------

    title = models.CharField(
        max_length=200,
        default='Your Wanderwell Travel Proposal'
    )

    description = models.TextField(
        max_length=3000,
        blank=True,
        help_text='Introduction or summary of the proposed trip.'
    )

    itinerary = models.TextField(
        max_length=10000,
        blank=True,
        help_text='Day-by-day or general trip itinerary.'
    )

    # ------------------------------------------------------
    # COSTS
    # ------------------------------------------------------

    flight_cost = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    accommodation_cost = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    transport_cost = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    activities_cost = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    other_cost = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    service_fee = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        help_text='Wanderwell planning/service fee.'
    )

    # ------------------------------------------------------
    # STATUS
    # ------------------------------------------------------

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='draft'
    )

    sent_at = models.DateTimeField(
    null=True,
    blank=True
    )

    viewed_at = models.DateTimeField(
    null=True,
    blank=True
    )

    # ------------------------------------------------------
    # EXPIRATION
    # ------------------------------------------------------

    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Optional date and time when this proposal expires.'
    )

    # ------------------------------------------------------
    # CUSTOMER RESPONSE
    # ------------------------------------------------------

    customer_message = models.TextField(
        max_length=3000,
        blank=True,
        help_text='Message from the customer when requesting changes.'
    )

    responded_at = models.DateTimeField(
        null=True,
        blank=True
    )

    # ------------------------------------------------------
    # TIMESTAMPS
    # ------------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # ------------------------------------------------------
    # META
    # ------------------------------------------------------

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Travel Proposal'
        verbose_name_plural = 'Travel Proposals'

    # ------------------------------------------------------
    # DISPLAY
    # ------------------------------------------------------

    def __str__(self):
        return f"{self.title} — {self.enquiry.name}"

    # ------------------------------------------------------
    # CURRENCY
    # ------------------------------------------------------

    @property
    def currency(self):
        return self.enquiry.currency

    
    # ------------------------------------------------------
    # TRIP COST
    # ------------------------------------------------------

    @property
    def trip_cost(self):
        return (
            self.flight_cost
            + self.accommodation_cost
            + self.transport_cost
            + self.activities_cost
            + self.other_cost
        )

    # ------------------------------------------------------
    # TOTAL
    # ------------------------------------------------------

    @property
    def total_cost(self):
        return self.trip_cost + self.service_fee



# ==========================================================
# SITE SETTINGS
# ==========================================================

class SiteSettings(models.Model):

    business_name = models.CharField(
        max_length=150,
        default='Wanderwell'
    )

    email = models.EmailField(
        blank=True
    )

    phone = models.CharField(
        max_length=30,
        blank=True
    )

    whatsapp = models.CharField(
        max_length=30,
        blank=True
    )

    address = models.CharField(
        max_length=255,
        blank=True
    )

    website_description = models.TextField(
        max_length=1000,
        blank=True
    )

    instagram = models.URLField(
        blank=True
    )

    facebook = models.URLField(
        blank=True
    )

    planning_message = models.TextField(
        max_length=1000,
        blank=True,
        help_text='Message shown to customers when encouraging them to plan a trip.'
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        verbose_name = 'Site Settings'

        verbose_name_plural = 'Site Settings'

    def __str__(self):

        return self.business_name

    def save(self, *args, **kwargs):

        # Keep one shared website settings record.
        self.pk = 1

        super().save(
            *args,
            **kwargs
        )

    @property
    def whatsapp_number(self):

        digits = ''.join(
            character
            for character in self.whatsapp
            if character.isdigit()
        )

        if digits.startswith('0'):

            return '234' + digits[1:]

        if digits.startswith('234'):

            return digits

        return digits

class PlanningEnquiryNote(models.Model):

    enquiry = models.ForeignKey(
        PlanningEnquiry,
        on_delete=models.CASCADE,
        related_name='internal_notes'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='planning_enquiry_notes'
    )

    note = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Note for {self.enquiry.name}"

class PlanningEnquiryActivity(models.Model):

    enquiry = models.ForeignKey(
        PlanningEnquiry,
        on_delete=models.CASCADE,
        related_name='activities'
    )

    actor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='planning_enquiry_activities'
    )

    activity_type = models.CharField(
        max_length=50
    )

    description = models.CharField(
        max_length=255
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.enquiry.name} - {self.description}"

