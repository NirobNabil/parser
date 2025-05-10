import requests
from django.conf import settings
from django_q.tasks import async_task

from core.choices import ProjectPageType
from core.models import Competitor, Project, ProjectPage
from seo_blog_bot.utils import get_seo_blog_bot_logger

logger = get_seo_blog_bot_logger(__name__)


def add_email_to_buttondown(email, tag):
    data = {
        "email_address": str(email),
        "metadata": {"source": tag},
        "tags": [tag],
        "referrer_url": "https://seo_blog_bot.app",
        "subscriber_type": "regular",
    }

    r = requests.post(
        "https://api.buttondown.email/v1/subscribers",
        headers={"Authorization": f"Token {settings.BUTTONDOWN_API_KEY}"},
        json=data,
    )

    return r.json()


def analyze_project_page(project_id: int, link: str):
    project = Project.objects.get(id=project_id)
    project_page, created = ProjectPage.objects.get_or_create(project=project, url=link)
    page_analyzed = False

    if created:
        project_page.get_page_content()
        page_analyzed = project_page.analyze_content()

    if project_page.type == ProjectPageType.PRICING and page_analyzed:
        async_task(project_page.create_new_pricing_strategy)

    return f"Analyzed {link} for {project.name}"


def schedule_project_page_analysis(project_id):
    project = Project.objects.get(id=project_id)
    project_links = project.get_a_list_of_links()

    count = 0
    for link in project_links:
        async_task(
            analyze_project_page,
            project_id,
            link,
        )
        count += 1

    return f"Scheduled analysis for {count} links"


def schedule_project_competitor_analysis(project_id):
    project = Project.objects.get(id=project_id)
    competitors = project.find_competitors()
    if competitors:
        competitors = project.get_and_save_list_of_competitors()
        for competitor in competitors:
            async_task(analyze_project_competitor, competitor.id)

    return f"Saved Competitors for {project.name}"


def analyze_project_competitor(competitor_id):
    competitor = Competitor.objects.get(id=competitor_id)
    got_content = competitor.get_page_content()

    if got_content:
        competitor.analyze_competitor()

    return f"Analyzed Competitor for {competitor.name}"
