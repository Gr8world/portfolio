from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import PublicTestimonialForm
from .models import (
    AboutPageContent,
    CompanyHighlight,
    ContactMessage,
    ContactPageContent,
    HomePageContent,
    PortfolioPageContent,
    PortfolioProfile,
    PricingPlan,
    Project,
    ProjectCategory,
    Service,
    ServicesPageContent,
    TeamMember,
    Testimonial,
)


def home(request):
    services = Service.objects.filter(is_active=True).order_by("order")
    projects = Project.objects.filter(is_active=True).select_related("category").order_by(
        "order"
    )[:6]
    testimonials = Testimonial.objects.filter(is_active=True)
    pricing_plans = PricingPlan.objects.filter(is_active=True).order_by("order")

    context = {
        "home_page": HomePageContent.load(),
        "services": services[:6],
        "hero_services": services[:4],
        "projects": projects,
        "testimonials": testimonials,
        "testimonial_form": PublicTestimonialForm(),
        "pricing_plans": pricing_plans,
    }
    return render(request, "core/home.html", context)


def services(request):
    context = {
        "services_page": ServicesPageContent.load(),
        "services": Service.objects.filter(is_active=True).order_by("order"),
    }
    return render(request, "core/services.html", context)


def about(request):
    context = {
        "about_page": AboutPageContent.load(),
        "highlights": CompanyHighlight.objects.filter(is_active=True).order_by("order")[:4],
        "team_members": TeamMember.objects.filter(is_active=True).order_by("order"),
        "testimonials": Testimonial.objects.filter(is_active=True)[:3],
    }
    return render(request, "core/about.html", context)


def portfolio(request):
    categories = (
        ProjectCategory.objects.filter(is_active=True, projects__is_active=True)
        .distinct()
        .order_by("order", "name")
    )
    context = {
        "portfolio_page": PortfolioPageContent.load(),
        "portfolio_profile": PortfolioProfile.load(),
        "projects": Project.objects.filter(is_active=True)
        .select_related("category")
        .order_by("order"),
        "categories": categories,
    }
    return render(request, "core/portfolio.html", context)


def contact(request):
    contact_page = ContactPageContent.load()

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        message_text = request.POST.get("message", "").strip()

        if not name or not email or not message_text:
            messages.error(
                request,
                "Name, email, and message are required.",
                extra_tags="contact",
            )
            return redirect("contact")

        ContactMessage.objects.create(
            name=name,
            email=email,
            phone=request.POST.get("phone", "").strip(),
            subject=request.POST.get("subject", "").strip(),
            message=message_text,
        )

        next_url = request.POST.get("next", "").strip()
        messages.success(request, contact_page.success_message, extra_tags="contact")

        if next_url.startswith("/"):
            return redirect(next_url)
        return redirect("contact")

    context = {"contact_page": contact_page}
    return render(request, "core/contact.html", context)


def handler404(request, exception):
    return render(request, "core/404.html", status=404)


def handler500(request):
    return render(request, "core/500.html", status=500)


def submit_testimonial(request):
    if request.method != "POST":
        return redirect("home")

    form = PublicTestimonialForm(request.POST, request.FILES)
    next_url = request.POST.get("next", "").strip()

    if form.is_valid():
        testimonial = form.save(commit=False)
        testimonial.is_active = True
        testimonial.save()
        messages.success(
            request,
            "Thanks for your review. It is now live on the website.",
            extra_tags="testimonial",
        )
    else:
        messages.error(
            request,
            "Please fill all required testimonial fields correctly.",
            extra_tags="testimonial",
        )

    if next_url.startswith("/"):
        return redirect(next_url)
    return redirect("home")
