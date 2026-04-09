from django.shortcuts import render, redirect
from .forms import ServiceRequestForm, BusinessImageForm, ContactForm
from .models import ServiceRequest, BusinessImage, LandingPage
from notifications.models import Notification
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

# ------------------------------
# Pages
# ------------------------------

def about(request):
    return render(request, "services/about.html")


@login_required(login_url='/login/')
def home(request):
    images = BusinessImage.objects.all()
    return render(request, "services/home.html", {"images": images})


@login_required
def dashboard(request):
    requests = ServiceRequest.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "services/dashboard.html", {"requests": requests})


@login_required
def track_order(request):
    tracking_id = request.GET.get("tracking_id")
    order = None
    if tracking_id:
        order = ServiceRequest.objects.filter(tracking_id=tracking_id).first()
    return render(request, "services/track_order.html", {"order": order})


def landing(request):
    if request.user.is_authenticated:
        return redirect("home")

    landing = LandingPage.objects.filter(
        background_image__isnull=False
    ).first()

    return render(request, "services/landing.html", {"landing": landing})


# ------------------------------
# Contact
# ------------------------------

def contact_us(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            try:
                if getattr(settings, "ADMIN_EMAIL", None):
                    send_mail(
                        subject=f"New Contact Message: {contact_message.subject}",
                        message=f"From: {contact_message.name} <{contact_message.email}>\n\n{contact_message.message}",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[settings.ADMIN_EMAIL],
                        fail_silently=True
                    )
            except Exception as e:
                print("Contact email error:", e)

            return render(request, "services/contact_success.html", {"contact_message": contact_message})
    else:
        form = ContactForm()

    return render(request, "services/contact_us.html", {"form": form})


# ------------------------------
# Order creation
# ------------------------------

@login_required
def create_request(request, service_type):
    if request.method == "POST":
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.user = request.user
            service_request.service_type = service_type

            # Get weight
            weight = service_request.weight or 0

            # Get distance & price from frontend (fast)
            distance = request.POST.get("distance", 0)
            price = request.POST.get("price", 0)

            try:
                distance = float(distance)
            except (TypeError, ValueError):
                distance = 0

            try:
                price = float(price)
            except (TypeError, ValueError):
                price = 0

            service_request.distance_km = distance
            service_request.price = price

            # Save order
            service_request.save()

            # Admin notification (non-blocking)
            import threading
            def notify_admin():
                try:
                    admin_user = User.objects.filter(is_superuser=True).first()
                    if admin_user:
                        Notification.objects.create(
                            user=admin_user,
                            message=f"🚚 New {service_type} order from {request.user.username} ({service_request.tracking_id})"
                        )
                except Exception as e:
                    print("Notification error:", e)

            threading.Thread(target=notify_admin).start()

            # Success message
            messages.success(request, "Order submitted successfully!")

            return render(request, "services/order_success.html", {"service_request": service_request})
        else:
            print("Form errors:", form.errors)
    else:
        form = ServiceRequestForm()

    return render(request, "services/create_request.html", {"form": form, "service_type": service_type})


# ------------------------------
# Preview price (frontend calculates)
# ------------------------------

def preview_price(request):
    # Backend no longer calculates; return safe JSON
    return JsonResponse({
        "distance": 0,
        "price": 0
    })
