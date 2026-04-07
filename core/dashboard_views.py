from functools import wraps

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import redirect_to_login
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import DashboardLoginForm, TestimonialDashboardForm, build_styled_modelform
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
    SiteConfiguration,
    TeamMember,
    Testimonial,
)


SINGLETON_CONFIGS = {
    "site-configuration": {
        "label": "Site Configuration",
        "description": "Branding, SEO, footer, contact details, and social links.",
        "model": SiteConfiguration,
        "form": build_styled_modelform(SiteConfiguration),
        "icon": "fas fa-swatchbook",
    },
    "home-page": {
        "label": "Home Page Content",
        "description": "Hero, section headings, pricing labels, and homepage contact copy.",
        "model": HomePageContent,
        "form": build_styled_modelform(HomePageContent),
        "icon": "fas fa-house",
    },
    "services-page": {
        "label": "Services Page Content",
        "description": "Header and CTA content for the services page.",
        "model": ServicesPageContent,
        "form": build_styled_modelform(ServicesPageContent),
        "icon": "fas fa-laptop-code",
    },
    "about-page": {
        "label": "About Page Content",
        "description": "Intro, mission, vision, team section, and about-page CTA.",
        "model": AboutPageContent,
        "form": build_styled_modelform(AboutPageContent),
        "icon": "fas fa-circle-info",
    },
    "portfolio-page": {
        "label": "Portfolio Page Content",
        "description": "Portfolio header, filter labels, and CTA content.",
        "model": PortfolioPageContent,
        "form": build_styled_modelform(PortfolioPageContent),
        "icon": "fas fa-briefcase",
    },
    "portfolio-profile": {
        "label": "Portfolio Profile",
        "description": "Your photo, experience, intro, and personal stats for the portfolio page.",
        "model": PortfolioProfile,
        "form": build_styled_modelform(PortfolioProfile),
        "icon": "fas fa-id-badge",
    },
    "contact-page": {
        "label": "Contact Page Content",
        "description": "Contact page section titles and success message.",
        "model": ContactPageContent,
        "form": build_styled_modelform(ContactPageContent),
        "icon": "fas fa-envelope-open-text",
    },
}


COLLECTION_CONFIGS = {
    "services": {
        "label": "Services",
        "singular_label": "Service",
        "description": "The actual services shown across the site.",
        "model": Service,
        "form": build_styled_modelform(Service),
        "icon": "fas fa-layer-group",
        "columns": [
            {"field": "title", "label": "Title"},
            {"field": "icon", "label": "Icon"},
            {"field": "order", "label": "Order"},
            {"field": "is_active", "label": "Active"},
        ],
    },
    "project-categories": {
        "label": "Project Categories",
        "singular_label": "Project Category",
        "description": "Filter groups used in the portfolio section.",
        "model": ProjectCategory,
        "form": build_styled_modelform(ProjectCategory),
        "icon": "fas fa-tags",
        "columns": [
            {"field": "name", "label": "Name"},
            {"field": "slug", "label": "Slug"},
            {"field": "order", "label": "Order"},
            {"field": "is_active", "label": "Active"},
        ],
    },
    "projects": {
        "label": "Projects",
        "singular_label": "Project",
        "description": "Portfolio items and featured work cards.",
        "model": Project,
        "form": build_styled_modelform(Project),
        "icon": "fas fa-diagram-project",
        "columns": [
            {"field": "title", "label": "Title"},
            {"field": "client_name", "label": "Client"},
            {"field": "category", "label": "Category"},
            {"field": "order", "label": "Order"},
            {"field": "is_active", "label": "Active"},
        ],
    },
    "team-members": {
        "label": "Team Members",
        "singular_label": "Team Member",
        "description": "People shown on the about page.",
        "model": TeamMember,
        "form": build_styled_modelform(TeamMember),
        "icon": "fas fa-people-group",
        "columns": [
            {"field": "name", "label": "Name"},
            {"field": "role", "label": "Role"},
            {"field": "order", "label": "Order"},
            {"field": "is_active", "label": "Active"},
        ],
    },
    "highlights": {
        "label": "Company Highlights",
        "singular_label": "Company Highlight",
        "description": "Strength cards shown on the about page.",
        "model": CompanyHighlight,
        "form": build_styled_modelform(CompanyHighlight),
        "icon": "fas fa-bolt",
        "columns": [
            {"field": "title", "label": "Title"},
            {"field": "icon", "label": "Icon"},
            {"field": "order", "label": "Order"},
            {"field": "is_active", "label": "Active"},
        ],
    },
    "testimonials": {
        "label": "Testimonials",
        "singular_label": "Testimonial",
        "description": "Client reviews submitted from the website. Use Active to show or hide them anytime.",
        "model": Testimonial,
        "form": TestimonialDashboardForm,
        "icon": "fas fa-quote-left",
        "columns": [
            {"field": "name", "label": "Name"},
            {"field": "position", "label": "Position"},
            {"field": "company", "label": "Company"},
            {"field": "rating", "label": "Rating"},
            {"field": "is_active", "label": "Active"},
        ],
        "allow_create": False,
    },
    "pricing-plans": {
        "label": "Pricing Plans",
        "singular_label": "Pricing Plan",
        "description": "Pricing cards used on the homepage.",
        "model": PricingPlan,
        "form": build_styled_modelform(PricingPlan),
        "icon": "fas fa-money-check-dollar",
        "columns": [
            {"field": "name", "label": "Name"},
            {"field": "price", "label": "Price"},
            {"field": "is_featured", "label": "Featured"},
            {"field": "order", "label": "Order"},
            {"field": "is_active", "label": "Active"},
        ],
    },
    "contact-messages": {
        "label": "Contact Messages",
        "singular_label": "Contact Message",
        "description": "Messages submitted from the public contact forms.",
        "model": ContactMessage,
        "form": build_styled_modelform(ContactMessage),
        "icon": "fas fa-inbox",
        "columns": [
            {"field": "name", "label": "Name"},
            {"field": "email", "label": "Email"},
            {"field": "subject", "label": "Subject"},
            {"field": "is_read", "label": "Read"},
            {"field": "created_at", "label": "Received"},
        ],
        "allow_create": False,
    },
}


def dashboard_required(view_func):
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path(), reverse("dashboard_login"))
        if not request.user.is_staff:
            logout(request)
            messages.error(request, "This account does not have dashboard access.")
            return redirect("dashboard_login")
        return view_func(request, *args, **kwargs)

    return wrapped


def dashboard_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("dashboard_home")

    if request.user.is_authenticated and not request.user.is_staff:
        logout(request)

    form = DashboardLoginForm(request, data=request.POST or None)
    next_url = request.GET.get("next") or request.POST.get("next") or ""

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        if not user.is_staff:
            form.add_error(None, "This account does not have dashboard access.")
        else:
            login(request, user)
            if next_url and url_has_allowed_host_and_scheme(
                next_url, allowed_hosts={request.get_host()}
            ):
                return redirect(next_url)
            return redirect("dashboard_home")

    return render(
        request,
        "dashboard/login.html",
        {"form": form, "next_url": next_url},
    )


@dashboard_required
def dashboard_logout(request):
    logout(request)
    return redirect("dashboard_login")


@dashboard_required
def dashboard_home(request):
    singleton_sections = _singleton_sections(active_key=None)
    collection_sections = _collection_sections(active_key=None)

    stats = [
        {"label": section["label"], "count": section["count"], "icon": section["icon"]}
        for section in collection_sections
    ]

    context = _dashboard_context("dashboard", "Dashboard Overview")
    context.update(
        {
            "singleton_sections": singleton_sections,
            "collection_sections": collection_sections,
            "stats": stats,
        }
    )
    return render(request, "dashboard/home.html", context)


@dashboard_required
def singleton_edit(request, key):
    config = SINGLETON_CONFIGS.get(key)
    if not config:
        raise Http404("Unknown dashboard section.")

    obj = config["model"].load()
    form = config["form"](request.POST or None, request.FILES or None, instance=obj)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"{config['label']} updated successfully.")
        return redirect("dashboard_singleton_edit", key=key)

    context = _dashboard_context(key, f"Edit {config['label']}")
    context.update(
        {
            "section_label": config["label"],
            "section_description": config["description"],
            "form": form,
            "back_url": reverse("dashboard_home"),
            "submit_label": "Save Changes",
        }
    )
    return render(request, "dashboard/form.html", context)


@dashboard_required
def collection_list(request, key):
    config = _get_collection_config(key)
    items = config["model"].objects.all()

    context = _dashboard_context(key, config["label"])
    context.update(
        {
            "section_label": config["label"],
            "section_description": config["description"],
            "columns": config["columns"],
            "items": items,
            "key": key,
            "allow_create": config.get("allow_create", True),
            "allow_delete": config.get("allow_delete", True),
        }
    )
    return render(request, "dashboard/list.html", context)


@dashboard_required
def collection_create(request, key):
    config = _get_collection_config(key)
    if not config.get("allow_create", True):
        messages.error(request, f"You cannot create new {config['label'].lower()} here.")
        return redirect("dashboard_collection_list", key=key)

    form = config["form"](request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"{config['singular_label']} created successfully.")
        return redirect("dashboard_collection_list", key=key)

    context = _dashboard_context(key, f"Add {config['label']}")
    context.update(
        {
            "section_label": config["label"],
            "section_description": config["description"],
            "form": form,
            "back_url": reverse("dashboard_collection_list", kwargs={"key": key}),
            "submit_label": "Create",
        }
    )
    return render(request, "dashboard/form.html", context)


@dashboard_required
def collection_edit(request, key, pk):
    config = _get_collection_config(key)
    item = get_object_or_404(config["model"], pk=pk)
    form = config["form"](request.POST or None, request.FILES or None, instance=item)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"{config['singular_label']} updated successfully.")
        return redirect("dashboard_collection_list", key=key)

    context = _dashboard_context(key, f"Edit {config['label']}")
    context.update(
        {
            "section_label": config["label"],
            "section_description": config["description"],
            "form": form,
            "object_name": str(item),
            "back_url": reverse("dashboard_collection_list", kwargs={"key": key}),
            "submit_label": "Save Changes",
        }
    )
    return render(request, "dashboard/form.html", context)


@dashboard_required
def collection_delete(request, key, pk):
    config = _get_collection_config(key)
    if not config.get("allow_delete", True):
        messages.error(request, f"You cannot delete {config['label'].lower()} here.")
        return redirect("dashboard_collection_list", key=key)

    item = get_object_or_404(config["model"], pk=pk)
    if request.method == "POST":
        item.delete()
        messages.success(request, f"{config['singular_label']} deleted successfully.")
        return redirect("dashboard_collection_list", key=key)

    context = _dashboard_context(key, f"Delete {config['label']}")
    context.update(
        {
            "section_label": config["label"],
            "object_name": str(item),
            "back_url": reverse("dashboard_collection_list", kwargs={"key": key}),
        }
    )
    return render(request, "dashboard/confirm_delete.html", context)


def _dashboard_context(active_key, page_title):
    return {
        "page_title": page_title,
        "dashboard_singletons": _singleton_sections(active_key),
        "dashboard_collections": _collection_sections(active_key),
        "active_key": active_key,
    }


def _singleton_sections(active_key):
    sections = []
    for key, config in SINGLETON_CONFIGS.items():
        sections.append(
            {
                "key": key,
                "label": config["label"],
                "description": config["description"],
                "icon": config["icon"],
                "url": reverse("dashboard_singleton_edit", kwargs={"key": key}),
                "active": active_key == key,
            }
        )
    return sections


def _collection_sections(active_key):
    sections = []
    for key, config in COLLECTION_CONFIGS.items():
        sections.append(
            {
                "key": key,
                "label": config["label"],
                "description": config["description"],
                "icon": config["icon"],
                "url": reverse("dashboard_collection_list", kwargs={"key": key}),
                "count": config["model"].objects.count(),
                "active": active_key == key,
            }
        )
    return sections


def _get_collection_config(key):
    config = COLLECTION_CONFIGS.get(key)
    if not config:
        raise Http404("Unknown dashboard section.")
    return config
