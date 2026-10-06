from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


from .models import (
    PlanningEnquiry,
    Review,
    SiteSettings,
    Destinations,
    Tours,
    FAQ,
    Proposal,
    PlanningEnquiryPricing,
)


# =========================================================
# SIGN UP
# =========================================================

class SignupForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'you@example.com',
            }
        )
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]

        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Choose a username',
                }
            ),
        }


# =========================================================
# PLANNING ENQUIRY
# =========================================================








class PlanningEnquiryForm(forms.ModelForm):

    destination = forms.ModelChoiceField(
        queryset=Tours.objects.all().order_by('headlights'),
        empty_label='Select a destination',
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-select',
            }
        )
    )

    class Meta:
        model = PlanningEnquiry

        fields = [
            'name',
            'email',
            'phone',
            'destination',
            'travel_dates',
            'travellers',
            'budget',
            'currency',
            'travel_style',
            'message',
        ]

        widgets = {

            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Your full name',
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Your email address',
                }
            ),

            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Your phone number',
                }
            ),

            'travel_dates': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'e.g. December 2026 or Flexible',
                }
            ),

            'travellers': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '1',
                    'placeholder': 'Number of travellers',
                }
            ),

            'budget': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '0',
                    'step': '0.01',
                    'placeholder': 'Approximate trip budget',
                }
            ),

            'currency': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),

            'travel_style': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),

            'message': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'placeholder': (
                        'Tell us anything else about your trip...'
                    ),
                }
            ),
        }

    def save(self, commit=True):
        enquiry = super().save(commit=False)

        destination = self.cleaned_data.get('destination')

        if destination:
            enquiry.destination = destination.headlights

        if commit:
            enquiry.save()

        return enquiry





class PlanningEnquiryPricingForm(forms.ModelForm):

    class Meta:
        model = PlanningEnquiryPricing

        fields = [
            'accommodation',
            'transportation',
            'activities',
            'transfers',
            'other_costs',
            'service_fee',
        ]

        widgets = {

            'accommodation': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '0',
                    'step': '0.01',
                    'placeholder': '0.00',
                }
            ),

            'transportation': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '0',
                    'step': '0.01',
                    'placeholder': '0.00',
                }
            ),

            'activities': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '0',
                    'step': '0.01',
                    'placeholder': '0.00',
                }
            ),

            'transfers': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '0',
                    'step': '0.01',
                    'placeholder': '0.00',
                }
            ),

            'other_costs': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '0',
                    'step': '0.01',
                    'placeholder': '0.00',
                }
            ),

            'service_fee': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '0',
                    'step': '0.01',
                    'placeholder': '0.00',
                }
            ),
        }


# =========================================================
# REVIEW
# =========================================================

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review

        # IMPORTANT:
        # The customer does NOT enter their name or trip.
        # Both are supplied automatically by the backend.
        fields = [
            'rating',
            'quote',
        ]

        widgets = {
            'rating': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),

            'quote': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': (
                        'Tell us about your experience...'
                    ),
                    'rows': 5,
                }
            ),
        }


# =========================================================
# SITE SETTINGS
# =========================================================

class SiteSettingsForm(forms.ModelForm):

    class Meta:
        model = SiteSettings

        fields = [
            'business_name',
            'email',
            'phone',
            'whatsapp',
            'address',
            'website_description',
            'instagram',
            'facebook',
            'planning_message',
        ]

        widgets = {

            'business_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Wanderwell',
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'hello@example.com',
                }
            ),

            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '+234...',
                }
            ),

            'whatsapp': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '+234...',
                }
            ),

            'address': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Business address',
                }
            ),

            'website_description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': (
                        'Describe your travel business...'
                    ),
                }
            ),

            'instagram': forms.URLInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'https://instagram.com/...',
                }
            ),

            'facebook': forms.URLInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'https://facebook.com/...',
                }
            ),

            'planning_message': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': (
                        'Tell customers how Wanderwell can help '
                        'them plan their trip...'
                    ),
                }
            ),
        }

# ==========================================================
# DESTINATION ADMIN FORM
# ==========================================================

class DestinationForm(forms.ModelForm):

    class Meta:
        model = Destinations
        fields = [
            'image',
            'city',
            'country',
        ]

        widgets = {
            'city': forms.TextInput(
                attrs={
                    'placeholder': 'e.g. Marrakech',
                    'class': 'admin-content-input',
                }
            ),

            'country': forms.TextInput(
                attrs={
                    'placeholder': 'e.g. Morocco',
                    'class': 'admin-content-input',
                }
            ),
        }


# ==========================================================
# TOUR ADMIN FORM
# ==========================================================

class TourForm(forms.ModelForm):

    class Meta:
        model = Tours
        fields = [
            'image',
            'headlights',
            'description',
        ]

        widgets = {
            'headlights': forms.TextInput(
                attrs={
                    'placeholder': 'e.g. Desert Escape',
                    'class': 'admin-content-input',
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Describe this tour...',
                    'class': 'admin-content-input',
                    'rows': 6,
                }
            ),
        }


class FAQForm(forms.ModelForm):

    class Meta:
        model = FAQ
        fields = [
            'questions',
            'answers',
        ]

        widgets = {
            'questions': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter the frequently asked question',
                }
            ),

            'answers': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 6,
                    'placeholder': 'Enter the answer',
                }
            ),
        }



class ProposalForm(forms.ModelForm):

    class Meta:
        model = Proposal

        fields = [
            'title',
            'description',
            'itinerary',
            'flight_cost',
            'accommodation_cost',
            'transport_cost',
            'activities_cost',
            'other_cost',
            'service_fee',
        ]

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'e.g. Dubai Luxury Escape',
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': (
                        'Briefly describe the proposed trip...'
                    ),
                }
            ),

            'itinerary': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 10,
                    'placeholder': (
                        'Day 1 — Arrival\n'
                        'Day 2 — City tour\n'
                        'Day 3 — Desert experience'
                    ),
                }
            ),

            'flight_cost': forms.NumberInput(
                attrs={
                    'class': 'form-control proposal-cost',
                    'step': '0.01',
                    'min': '0',
                }
            ),

            'accommodation_cost': forms.NumberInput(
                attrs={
                    'class': 'form-control proposal-cost',
                    'step': '0.01',
                    'min': '0',
                }
            ),

            'transport_cost': forms.NumberInput(
                attrs={
                    'class': 'form-control proposal-cost',
                    'step': '0.01',
                    'min': '0',
                }
            ),

            'activities_cost': forms.NumberInput(
                attrs={
                    'class': 'form-control proposal-cost',
                    'step': '0.01',
                    'min': '0',
                }
            ),

            'other_cost': forms.NumberInput(
                attrs={
                    'class': 'form-control proposal-cost',
                    'step': '0.01',
                    'min': '0',
                }
            ),

            'service_fee': forms.NumberInput(
                attrs={
                    'class': 'form-control proposal-cost',
                    'step': '0.01',
                    'min': '0',
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        cost_fields = [
            'flight_cost',
            'accommodation_cost',
            'transport_cost',
            'activities_cost',
            'other_cost',
            'service_fee',
        ]

        for field_name in cost_fields:
            value = cleaned_data.get(field_name)

            if value is not None and value < 0:
                self.add_error(
                    field_name,
                    'Cost cannot be negative.'
                )

        return cleaned_data
