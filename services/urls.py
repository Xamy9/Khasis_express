from django.urls import path
from . import views

urlpatterns = [
    
    # Landing page
    path("", views.landing, name="landing"),

    # Home page
    path("home/", views.home, name="home"),

    # About page
    path("about/", views.about, name="about"),

    # Create delivery request
    path("request/<str:service_type>/", views.create_request, name="create_request"),

    # Preview distance and price (AJAX calculation)
    path("preview-price/", views.preview_price, name="preview_price"),

    # User dashboard (view orders)
    path("dashboard/", views.dashboard, name="dashboard"),

    # Track order
    path("track/", views.track_order, name="track_order"),
    
    # contact us
    path("contact/",views.contact_us, name="contact_us"),

]