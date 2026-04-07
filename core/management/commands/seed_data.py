from django.core.management.base import BaseCommand

from core.models import (
    AboutPageContent,
    CompanyHighlight,
    ContactPageContent,
    HomePageContent,
    PortfolioPageContent,
    PricingPlan,
    Project,
    ProjectCategory,
    Service,
    ServicesPageContent,
    SiteConfiguration,
    TeamMember,
    Testimonial,
)


class Command(BaseCommand):
    help = "Seed the database with starter content for the landing page"

    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")

        Service.objects.all().delete()
        Project.objects.all().delete()
        ProjectCategory.objects.all().delete()
        Testimonial.objects.all().delete()
        PricingPlan.objects.all().delete()
        TeamMember.objects.all().delete()
        CompanyHighlight.objects.all().delete()

        SiteConfiguration.load()
        HomePageContent.load()
        ServicesPageContent.load()
        AboutPageContent.load()
        PortfolioPageContent.load()
        ContactPageContent.load()

        services = [
            {
                "title": "Web Development",
                "description": "Custom web applications built with modern frameworks like Django, React, and Node.js.",
                "icon": "fas fa-code",
                "order": 1,
            },
            {
                "title": "Mobile App Development",
                "description": "Native and cross-platform mobile apps for iOS and Android with smooth user experiences.",
                "icon": "fas fa-mobile-alt",
                "order": 2,
            },
            {
                "title": "UI and UX Design",
                "description": "Beautiful, intuitive interfaces that improve user adoption and engagement.",
                "icon": "fas fa-paint-brush",
                "order": 3,
            },
            {
                "title": "Cloud Solutions",
                "description": "Cloud architecture, migration, and scaling support for modern businesses.",
                "icon": "fas fa-cloud",
                "order": 4,
            },
            {
                "title": "AI Solutions",
                "description": "Machine learning and automation workflows that turn data into action.",
                "icon": "fas fa-brain",
                "order": 5,
            },
            {
                "title": "Maintenance and Support",
                "description": "Reliable support, monitoring, and updates to keep your systems healthy.",
                "icon": "fas fa-tools",
                "order": 6,
            },
        ]
        for payload in services:
            Service.objects.create(**payload)

        web = ProjectCategory.objects.create(name="Web Development", slug="web", order=1)
        mobile = ProjectCategory.objects.create(name="Mobile Apps", slug="mobile", order=2)
        ai = ProjectCategory.objects.create(name="AI Solutions", slug="ai", order=3)

        projects = [
            {
                "title": "E-Commerce Platform",
                "client_name": "Retail Nova",
                "description": "A full-featured online commerce platform with secure checkout and an admin dashboard.",
                "technologies": "Django, React, Stripe",
                "category": web,
                "order": 1,
            },
            {
                "title": "Food Delivery App",
                "client_name": "QuickBite",
                "description": "A delivery app with live order tracking, restaurant onboarding, and customer notifications.",
                "technologies": "Flutter, Firebase, Python",
                "category": mobile,
                "order": 2,
            },
            {
                "title": "AI Analytics Dashboard",
                "client_name": "Insight Labs",
                "description": "A business intelligence platform powered by predictive analytics and reporting automation.",
                "technologies": "Python, TensorFlow, Django",
                "category": ai,
                "order": 3,
            },
        ]
        for payload in projects:
            Project.objects.create(**payload)

        testimonials = [
            {
                "name": "John Smith",
                "position": "CEO",
                "company": "TechStart Inc.",
                "message": "TechNova transformed our business with a polished product and a dependable delivery process.",
                "rating": 5,
            },
            {
                "name": "Emily Martinez",
                "position": "Founder",
                "company": "DataViz Labs",
                "message": "Their AI and cloud expertise helped us scale faster without losing product quality.",
                "rating": 5,
            },
            {
                "name": "Raj Kumar",
                "position": "Director",
                "company": "FoodieApp",
                "message": "The team was responsive, creative, and deeply invested in getting the details right.",
                "rating": 5,
            },
        ]
        for payload in testimonials:
            Testimonial.objects.create(**payload)

        pricing = [
            {
                "name": "Starter",
                "price": "$2,999",
                "description": "Perfect for small businesses and startups",
                "features": "Landing page or small site\nMobile responsive design\nBasic SEO setup\n30 days support",
                "order": 1,
            },
            {
                "name": "Professional",
                "price": "$7,999",
                "description": "Ideal for growing businesses",
                "features": "Full web application\nUser authentication\nDatabase integration\n90 days support\nAPI development",
                "order": 2,
                "is_featured": True,
            },
            {
                "name": "Enterprise",
                "price": "Custom",
                "description": "For large-scale and advanced systems",
                "features": "Complex web applications\nAI and ML integration\nCloud architecture\nDedicated support\nCustom integrations",
                "order": 3,
            },
        ]
        for payload in pricing:
            PricingPlan.objects.create(**payload)

        highlights = [
            {
                "title": "Fast Delivery",
                "description": "Clear milestones and quick feedback loops.",
                "icon": "fas fa-rocket",
                "order": 1,
            },
            {
                "title": "Secure Systems",
                "description": "Built with reliability and security in mind.",
                "icon": "fas fa-shield-alt",
                "order": 2,
            },
            {
                "title": "Scalable Thinking",
                "description": "Architecture that grows with your business.",
                "icon": "fas fa-chart-line",
                "order": 3,
            },
            {
                "title": "Reliable Support",
                "description": "A long-term partner, not just a launch team.",
                "icon": "fas fa-heart",
                "order": 4,
            },
        ]
        for payload in highlights:
            CompanyHighlight.objects.create(**payload)

        team_members = [
            {"name": "John Smith", "role": "CEO and Founder", "order": 1},
            {"name": "Sarah Johnson", "role": "CTO", "order": 2},
            {"name": "Michael Chen", "role": "Lead Developer", "order": 3},
            {"name": "Emily Davis", "role": "UI and UX Designer", "order": 4},
        ]
        for payload in team_members:
            TeamMember.objects.create(**payload)

        self.stdout.write(self.style.SUCCESS("Database seeded successfully."))
