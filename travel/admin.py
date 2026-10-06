from django.contrib import admin
from .models import Destinations, Tours, FAQ, PlanningEnquiry, Review


@admin.register(Destinations)
class DestinationsAdmin(admin.ModelAdmin):
    list_display = ('city', 'country')
    search_fields = ('city', 'country')


@admin.register(Tours)
class ToursAdmin(admin.ModelAdmin):
    list_display = ('headlights',)
    search_fields = ('headlights', 'description')


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('questions',)
    search_fields = ('questions',)


@admin.register(PlanningEnquiry)
class PlanningEnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'destination', 'travel_dates', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'destination', 'message')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'rating', 'is_published', 'created_at')
    list_filter = ('is_published', 'rating', 'created_at')
    search_fields = ('name', 'quote', 'trip', 'user__username', 'user__email')
    readonly_fields = ('user', 'created_at')
    ordering = ('-created_at',)
    actions = ['approve_reviews', 'unpublish_reviews']

    @admin.action(description="Approve selected reviews (publish to the site)")
    def approve_reviews(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f"{updated} review(s) approved and published.")

    @admin.action(description="Unpublish selected reviews")
    def unpublish_reviews(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f"{updated} review(s) unpublished.")