from django.db import models
from django.utils.text import slugify


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(
        max_length=100, help_text="Icon class (e.g., 'fas fa-code')"
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.title


class ProjectCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Project Category"
        verbose_name_plural = "Project Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Project(models.Model):
    category = models.ForeignKey(
        ProjectCategory,
        on_delete=models.SET_NULL,
        related_name="projects",
        blank=True,
        null=True,
    )
    title = models.CharField(max_length=200)
    client_name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    technologies = models.CharField(
        max_length=500, help_text="Comma-separated technologies"
    )
    live_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    @property
    def technologies_list(self):
        return [item.strip() for item in self.technologies.split(",") if item.strip()]

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    company = models.CharField(max_length=200, blank=True)
    photo = models.ImageField(upload_to="testimonials/", blank=True, null=True)
    message = models.TextField()
    rating = models.PositiveIntegerField(
        default=5, choices=[(i, i) for i in range(1, 6)]
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return f"{self.name} - {self.company}"


class PricingPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    features = models.TextField(help_text="One feature per line")
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Pricing Plan"
        verbose_name_plural = "Pricing Plans"

    def get_features_list(self):
        return [item.strip() for item in self.features.splitlines() if item.strip()]

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=300, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.name} - {self.email}"


class TeamMember(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    photo = models.ImageField(upload_to="team/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"

    def __str__(self):
        return f"{self.name} - {self.role}"


class CompanyHighlight(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=250)
    icon = models.CharField(
        max_length=100, help_text="Icon class (e.g., 'fas fa-rocket')"
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Company Highlight"
        verbose_name_plural = "Company Highlights"

    def __str__(self):
        return self.title


class SiteSettings(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    description = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Legacy Site Setting"
        verbose_name_plural = "Legacy Site Settings"

    def __str__(self):
        return self.key


class SiteConfiguration(SingletonModel):
    site_name = models.CharField(max_length=100, default="TechNova")
    site_tagline = models.CharField(
        max_length=200, default="Digital Solutions for Modern Business"
    )
    logo = models.ImageField(upload_to="branding/", blank=True, null=True)
    meta_description = models.TextField(
        default=(
            "Building scalable digital solutions for modern businesses. "
            "Web development, mobile apps, AI solutions, and cloud services."
        )
    )
    meta_keywords = models.CharField(
        max_length=300,
        default=(
            "web development, mobile apps, AI solutions, cloud computing, "
            "UI UX design, startup, technology"
        ),
    )
    author_name = models.CharField(max_length=100, default="TechNova")
    navbar_cta_text = models.CharField(max_length=50, default="Get Started")
    footer_description = models.TextField(
        default=(
            "Building scalable digital solutions for modern businesses. "
            "We transform ideas into powerful technology that drives growth."
        )
    )
    contact_email = models.EmailField(default="hello@technova.com")
    contact_phone = models.CharField(max_length=50, default="+1 (555) 123-4567")
    contact_address = models.TextField(
        default="123 Tech Street, Suite 100, San Francisco, CA 94105"
    )
    working_hours = models.CharField(
        max_length=100, default="Mon - Fri: 9:00 AM - 6:00 PM"
    )
    map_embed_url = models.CharField(
        max_length=100,
        blank=True,
        help_text="Enter coordinates as 'latitude,longitude' e.g. '24.8607,67.0011'",
    )
    map_placeholder_text = models.CharField(
        max_length=150, default="Set map coordinates in admin panel."
    )
    footer_copyright = models.CharField(
        max_length=200, default="TechNova. All rights reserved."
    )
    privacy_policy_url = models.URLField(blank=True)
    terms_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"

    def __str__(self):
        return "Site Configuration"


class HomePageContent(SingletonModel):
    hero_badge = models.CharField(
        max_length=100, default="Transforming Ideas Into Reality"
    )
    hero_title_line_one = models.CharField(max_length=100, default="We Build Scalable")
    hero_title_line_two = models.CharField(max_length=100, default="Digital Solutions")
    hero_description = models.TextField(
        default=(
            "From web development to AI solutions, we help startups and "
            "enterprises transform their vision into powerful, scalable technology."
        )
    )
    hero_primary_cta_text = models.CharField(max_length=50, default="Get Started")
    hero_secondary_cta_text = models.CharField(max_length=50, default="View Our Work")
    hero_stat_1_value = models.CharField(max_length=50, default="500+")
    hero_stat_1_label = models.CharField(max_length=100, default="Projects Completed")
    hero_stat_2_value = models.CharField(max_length=50, default="150+")
    hero_stat_2_label = models.CharField(max_length=100, default="Happy Clients")
    hero_stat_3_value = models.CharField(max_length=50, default="8+")
    hero_stat_3_label = models.CharField(max_length=100, default="Years Experience")
    services_eyebrow = models.CharField(max_length=50, default="Our Services")
    services_title = models.CharField(
        max_length=120, default="Comprehensive Tech Solutions"
    )
    services_description = models.TextField(
        default=(
            "We offer end-to-end technology services tailored to your business "
            "needs, from concept to deployment and beyond."
        )
    )
    about_eyebrow = models.CharField(max_length=50, default="About Us")
    about_title = models.CharField(
        max_length=120, default="Driving Innovation Since 2018"
    )
    about_description_one = models.TextField(
        default=(
            "TechNova is a forward-thinking technology startup dedicated to helping "
            "businesses navigate the digital landscape."
        )
    )
    about_description_two = models.TextField(
        default=(
            "Our mission is to empower businesses with scalable, innovative "
            "technology solutions that transform their operations and accelerate growth."
        )
    )
    about_stat_1_value = models.CharField(max_length=50, default="500+")
    about_stat_1_label = models.CharField(max_length=100, default="Projects")
    about_stat_2_value = models.CharField(max_length=50, default="150+")
    about_stat_2_label = models.CharField(max_length=100, default="Clients")
    about_stat_3_value = models.CharField(max_length=50, default="8+")
    about_stat_3_label = models.CharField(max_length=100, default="Years")
    about_link_text = models.CharField(max_length=50, default="Learn More")
    mission_title = models.CharField(max_length=100, default="Our Mission")
    mission_text = models.TextField(
        default=(
            "To deliver innovative technology solutions that empower businesses "
            "to succeed in the digital age."
        )
    )
    vision_title = models.CharField(max_length=100, default="Our Vision")
    vision_text = models.TextField(
        default=(
            "To be the leading technology partner for businesses seeking digital transformation."
        )
    )
    metric_1_value = models.CharField(max_length=50, default="98%")
    metric_1_label = models.CharField(max_length=100, default="Client Satisfaction")
    metric_2_value = models.CharField(max_length=50, default="24/7")
    metric_2_label = models.CharField(max_length=100, default="Support Available")
    portfolio_eyebrow = models.CharField(max_length=50, default="Our Work")
    portfolio_title = models.CharField(max_length=120, default="Featured Projects")
    portfolio_description = models.TextField(
        default=(
            "A showcase of our recent work spanning web development, mobile apps, "
            "and innovative technology solutions."
        )
    )
    portfolio_button_text = models.CharField(max_length=50, default="View All Projects")
    testimonials_eyebrow = models.CharField(max_length=50, default="Testimonials")
    testimonials_title = models.CharField(
        max_length=120, default="What Our Clients Say"
    )
    testimonials_description = models.TextField(
        default=(
            "Do not just take our word for it. Here is what our clients have to say "
            "about working with us."
        )
    )
    pricing_eyebrow = models.CharField(max_length=50, default="Pricing")
    pricing_title = models.CharField(
        max_length=120, default="Simple, Transparent Pricing"
    )
    pricing_description = models.TextField(
        default=(
            "Choose the plan that fits your needs. All plans include dedicated support "
            "and flexible options."
        )
    )
    pricing_featured_badge_text = models.CharField(
        max_length=50, default="Most Popular"
    )
    contact_eyebrow = models.CharField(max_length=50, default="Contact Us")
    contact_title = models.CharField(
        max_length=120, default="Let Us Build Something Amazing"
    )
    contact_description = models.TextField(
        default=(
            "Have a project in mind? Send us a message and we will get back to you soon."
        )
    )
    contact_form_title = models.CharField(max_length=100, default="Send Us a Message")
    contact_info_title = models.CharField(max_length=100, default="Get In Touch")
    office_title = models.CharField(max_length=100, default="Our Office")

    class Meta:
        verbose_name = "Home Page Content"
        verbose_name_plural = "Home Page Content"

    def __str__(self):
        return "Home Page Content"


class ServicesPageContent(SingletonModel):
    hero_title = models.CharField(max_length=120, default="Our Services")
    hero_description = models.TextField(
        default="We deliver cutting-edge technology solutions tailored to your business needs."
    )
    cta_title = models.CharField(
        max_length=120, default="Ready to Transform Your Business?"
    )
    cta_description = models.TextField(
        default="Let us discuss your project and find the perfect solution for your needs."
    )
    cta_primary_text = models.CharField(max_length=50, default="Get Started")
    cta_secondary_text = models.CharField(max_length=50, default="View Our Work")

    class Meta:
        verbose_name = "Services Page Content"
        verbose_name_plural = "Services Page Content"

    def __str__(self):
        return "Services Page Content"


class AboutPageContent(SingletonModel):
    hero_title = models.CharField(max_length=120, default="About TechNova")
    hero_description = models.TextField(
        default="Empowering businesses with innovative technology solutions since 2020."
    )
    intro_title = models.CharField(
        max_length=150, default="Transforming Ideas Into Digital Reality"
    )
    intro_description_one = models.TextField(
        default=(
            "TechNova is a leading IT startup dedicated to delivering cutting-edge "
            "digital solutions."
        )
    )
    intro_description_two = models.TextField(
        default=(
            "Our team of expert developers and designers works collaboratively to "
            "transform ideas into powerful, scalable, and user-friendly applications."
        )
    )
    stat_1_value = models.CharField(max_length=50, default="500+")
    stat_1_label = models.CharField(max_length=100, default="Projects Completed")
    stat_2_value = models.CharField(max_length=50, default="150+")
    stat_2_label = models.CharField(max_length=100, default="Happy Clients")
    mission_title = models.CharField(max_length=100, default="Our Mission")
    mission_text = models.TextField(
        default=(
            "To empower businesses with innovative technology solutions that drive "
            "growth, efficiency, and competitive advantage."
        )
    )
    vision_title = models.CharField(max_length=100, default="Our Vision")
    vision_text = models.TextField(
        default=(
            "To be the most trusted technology partner for businesses seeking "
            "digital transformation."
        )
    )
    team_title = models.CharField(max_length=100, default="Meet Our Team")
    team_description = models.TextField(
        default="Our talented team of experts is passionate about creating innovative solutions."
    )
    cta_title = models.CharField(max_length=120, default="Want to Work With Us?")
    cta_description = models.TextField(
        default="We are always ready to discuss exciting ideas and ambitious projects."
    )
    cta_button_text = models.CharField(max_length=50, default="Get in Touch")

    class Meta:
        verbose_name = "About Page Content"
        verbose_name_plural = "About Page Content"

    def __str__(self):
        return "About Page Content"


class PortfolioPageContent(SingletonModel):
    hero_title = models.CharField(max_length=120, default="Our Portfolio")
    hero_description = models.TextField(
        default="Showcasing our latest projects and success stories."
    )
    filter_all_label = models.CharField(max_length=50, default="All")
    cta_title = models.CharField(max_length=120, default="Have a Project in Mind?")
    cta_description = models.TextField(
        default="Let us create something amazing together."
    )
    cta_primary_text = models.CharField(max_length=50, default="Start a Project")
    cta_secondary_text = models.CharField(max_length=50, default="Contact Us")

    class Meta:
        verbose_name = "Portfolio Page Content"
        verbose_name_plural = "Portfolio Page Content"

    def __str__(self):
        return "Portfolio Page Content"


class PortfolioProfile(SingletonModel):
    is_visible = models.BooleanField(default=False)
    section_badge = models.CharField(max_length=50, default="Personal Profile")
    name = models.CharField(max_length=120, blank=True)
    role = models.CharField(max_length=150, blank=True)
    photo = models.ImageField(upload_to="portfolio/profile/", blank=True, null=True)
    introduction = models.TextField(
        blank=True,
        help_text="Short intro shown near your portfolio profile.",
    )
    experience_summary = models.TextField(
        blank=True,
        help_text="Write about your experience, strengths, and work style.",
    )
    years_experience = models.PositiveIntegerField(default=0)
    projects_completed = models.PositiveIntegerField(default=0)
    happy_clients = models.PositiveIntegerField(default=0)
    location = models.CharField(max_length=120, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    skills = models.CharField(
        max_length=300,
        blank=True,
        help_text="Comma-separated skills or specialties.",
    )
    primary_button_text = models.CharField(max_length=50, default="Contact Me")
    secondary_button_text = models.CharField(max_length=50, default="View Services")

    class Meta:
        verbose_name = "Portfolio Profile"
        verbose_name_plural = "Portfolio Profile"

    @property
    def skills_list(self):
        return [item.strip() for item in self.skills.split(",") if item.strip()]

    def __str__(self):
        return "Portfolio Profile"


class ContactPageContent(SingletonModel):
    hero_title = models.CharField(max_length=120, default="Contact Us")
    hero_description = models.TextField(
        default="Get in touch with us for your next project."
    )
    form_title = models.CharField(max_length=100, default="Send Us a Message")
    info_title = models.CharField(max_length=100, default="Contact Information")
    social_title = models.CharField(max_length=100, default="Follow Us")
    map_title = models.CharField(max_length=100, default="Find Us on Map")
    submit_button_text = models.CharField(max_length=50, default="Send Message")
    success_message = models.CharField(
        max_length=200,
        default="Thank you for your message! We will get back to you soon.",
    )

    class Meta:
        verbose_name = "Contact Page Content"
        verbose_name_plural = "Contact Page Content"

    def __str__(self):
        return "Contact Page Content"
