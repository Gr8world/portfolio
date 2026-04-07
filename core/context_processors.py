from datetime import datetime

from .models import SiteConfiguration


def site_content(request):
    return {
        "site_config": SiteConfiguration.load(),
        "current_year": datetime.now().year,
    }
