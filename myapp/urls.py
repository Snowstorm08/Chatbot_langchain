from django.urls import path, re_path
from django.views.generic import TemplateView
from . import views

app_name = "core"

urlpatterns = [
    # API endpoint
    path("chat/", views.chat_view, name="chat"),

    # Root
    path("", TemplateView.as_view(template_name="index.html"), name="home"),

    # SPA fallback (must be last)
    re_path(r"^(?!admin|api|static|media).*", 
            TemplateView.as_view(template_name="index.html")),
]
