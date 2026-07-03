"""Public-facing review forms."""

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Review


class ReviewForm(forms.ModelForm):
    """Submit or update a review for a restaurant."""

    class Meta:
        model = Review
        fields = ("rating", "comment")
        widgets = {
            "rating": forms.HiddenInput(attrs={"id": "review-rating-input"}),
            "comment": forms.Textarea(
                attrs={
                    "class": "rp-review-textarea",
                    "rows": 4,
                    "placeholder": _("Share your dining experience…"),
                },
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["rating"].required = True
        self.fields["comment"].required = True
        self.fields["rating"].widget.attrs.setdefault("value", "0")

    def clean_rating(self):
        rating = self.cleaned_data.get("rating")
        if not rating or int(rating) < 1:
            raise forms.ValidationError(_("Please select a star rating."))
        return int(rating)

    def clean_comment(self):
        comment = (self.cleaned_data.get("comment") or "").strip()
        if len(comment) < 10:
            raise forms.ValidationError(
                _("Please write at least 10 characters."),
            )
        return comment
