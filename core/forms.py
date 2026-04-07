from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Testimonial


class DashboardLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Username", "autocomplete": "username"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "autocomplete": "current-password"}
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_form_styles(self)


class TestimonialDashboardForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        exclude = ("rating",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_form_styles(self)


class PublicTestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ["name", "position", "company", "photo", "message", "rating"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your full name"}),
            "position": forms.TextInput(
                attrs={"placeholder": "Your role or designation"}
            ),
            "company": forms.TextInput(attrs={"placeholder": "Company name"}),
            "message": forms.Textarea(
                attrs={
                    "placeholder": "Share your experience working with us",
                    "rows": 4,
                }
            ),
            "rating": forms.Select(
                attrs={
                    "class": "w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-slate-900 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
                },
                choices=[(i, f"{'★' * i} ({i}/5)") for i in range(1, 6)],
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["rating"].help_text = "Choose a rating from 1 to 5."
        self.fields["photo"].required = False
        _apply_form_styles(self)


def build_styled_modelform(model):
    class BaseStyledModelForm(forms.ModelForm):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            _apply_form_styles(self)

    meta = type("Meta", (), {"model": model, "fields": "__all__"})
    return type(
        f"{model.__name__}DashboardForm", (BaseStyledModelForm,), {"Meta": meta}
    )


def _apply_form_styles(form):
    for field in form.fields.values():
        widget = field.widget

        if "class" in widget.attrs:
            continue

        if isinstance(widget, forms.CheckboxInput):
            widget.attrs["class"] = (
                "h-4 w-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500"
            )
            continue

        if isinstance(widget, (forms.Select, forms.SelectMultiple)):
            widget.attrs["class"] = (
                "w-full rounded-xl border border-slate-200 bg-white px-4 py-3 "
                "text-slate-900 outline-none transition focus:border-blue-500 "
                "focus:ring-2 focus:ring-blue-100"
            )
            continue

        if isinstance(widget, forms.FileInput):
            widget.attrs["class"] = (
                "block w-full rounded-xl border border-dashed border-slate-300 "
                "bg-slate-50 px-4 py-3 text-sm text-slate-600"
            )
            if isinstance(field, forms.ImageField):
                widget.attrs["accept"] = "image/*"
            continue

        widget.attrs["class"] = (
            "w-full rounded-xl border border-slate-200 bg-white px-4 py-3 "
            "text-slate-900 outline-none transition focus:border-blue-500 "
            "focus:ring-2 focus:ring-blue-100"
        )

        if isinstance(widget, forms.Textarea):
            widget.attrs.setdefault("rows", 5)
