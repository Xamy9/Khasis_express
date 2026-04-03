from django.shortcuts import render, redirect, get_object_or_404
from .forms import ServiceRequestForm,BusinessImageForm
from .models import ServiceRequest,BusinessImage
from .utils import calculate_price, calculate_distance
from notifications.models import Notification
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from .forms import ContactForm
from .models import LandingPage





def about(request):
    return render(request, "services/about.html")


@login_required(login_url='/login/')
def home(request):
    images = BusinessImage.objects.all()
    return render(request, "services/home.html", {"images": images})


@login_required
def create_request(request, service_type):
    if request.method == "POST":
        form = ServiceRequestForm(request.POST)

        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.user = request.user
            service_request.service_type = service_type

            # GET WEIGHT
            weight = service_request.weight or 0

            # CALCULATE DISTANCE
            try:
                distance = calculate_distance(
                    service_request.pickup_location,
                    service_request.destination
                )
                if distance is None:
                    distance = 0
            except Exception as e:
                print("Distance calculation error:", e)
                distance = 0

            service_request.distance_km = distance

            # 🔥 CALCULATE PRICE WITH WEIGHT
            service_request.price = calculate_price(
                service_type,
                distance,
                weight
            )

            service_request.save()

            # SEND EMAIL
            send_mail(
                subject="New Delivery Request - KHASIS EXPRESS",
                message=f"""
A new {service_type} request has been placed.

Customer: {request.user.username}
Sender Phone: {service_request.sender_phone_number}
Receiver: {service_request.receiver_name}
Receiver Phone: {service_request.receiver_phone_number}

Package: {service_request.package_description}
Weight: {service_request.weight} kg

Distance: {service_request.distance_km} km
Price: {service_request.price}

Tracking ID: {service_request.tracking_id}
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )

            # ADMIN NOTIFICATION
            admin_user = User.objects.filter(is_superuser=True).first()
            if admin_user:
                Notification.objects.create(
                    user=admin_user,
                    message=f"{service_type} request from {request.user.username} ({service_request.tracking_id})"
                )

            return redirect("home")
    else:
        form = ServiceRequestForm()

    return render(
        request,
        "services/create_request.html",
        {"form": form, "service_type": service_type}
    )



@login_required
def dashboard(request):
    # SHOW ONLY ORDERS PLACED BY LOGGED-IN USER
    requests = ServiceRequest.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "services/dashboard.html", {"requests": requests})

@login_required
def track_order(request):
    tracking_id = request.GET.get("tracking_id")
    # USE get_object_or_404 TO HANDLE INVALID TRACKING ID
    order = None
    if tracking_id:
        order = ServiceRequest.objects.filter(tracking_id=tracking_id).first()
    return render(request, "services/track_order.html", {"order": order})



def preview_price(request):
    pickup = request.GET.get("pickup")
    destination = request.GET.get("destination")
    service_type = request.GET.get("service_type")
    weight = request.GET.get("weight", 0)

    if not pickup or not destination or not service_type:
        return JsonResponse({"error": "Missing data"})

    service_type = service_type.strip().lower()

    try:
        weight = float(weight)
    except (ValueError, TypeError):
        weight = 0

    # Calculate distance
    try:
        distance = calculate_distance(pickup, destination)
        if distance is None:
            distance = 0
    except Exception as e:
        print("Preview distance error:", e)
        distance = 0

    # Calculate price including weight
    price = calculate_price(service_type, distance, weight)

    return JsonResponse({
        "distance": round(distance, 2),
        "price": round(price, 2)
    })
    
    
    
    
    
    
def contact_us(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()

            # Optional: send an email notification
            send_mail(
                subject=f"New Contact Message: {contact_message.subject}",
                message=f"From: {contact_message.name} <{contact_message.email}>\n\n{contact_message.message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=True
            )

            return render(request, "services/contact_success.html", {"contact_message": contact_message})
    else:
        form = ContactForm()

    return render(request, "services/contact_us.html", {"form": form})






#from .models import LandingPage

def landing(request):
    # 🔐 Skip landing if already logged in
    if request.user.is_authenticated:
        return redirect("home")  # or "dashboard"

    # 🖼 Get landing content from admin
    landing = LandingPage.objects.first()

    return render(request, "services/landing.html", {
        "landing": landing
    })