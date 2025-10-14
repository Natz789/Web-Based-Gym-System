
from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal

from .models import (
    User, MembershipPlan, FlexibleAccess, 
    UserMembership, Payment, WalkInPayment, Analytics
)


# ==================== Public Views ====================

def home(request):
    """Homepage - displays available plans and walk-in options"""
    context = {
        'membership_plans': MembershipPlan.objects.filter(is_active=True),
        'walk_in_passes': FlexibleAccess.objects.filter(is_active=True),
    }
    return render(request, 'gym_app/home.html', context)


def about(request):
    """About page"""
    return render(request, 'gym_app/about.html')


# ==================== Authentication Views ====================

def login_view(request):
    """Handle user login"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name()}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'gym_app/login.html')


@login_required
def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


def register_view(request):
    """Member registration"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile_no = request.POST.get('mobile_no')
        address = request.POST.get('address')
        birthdate = request.POST.get('birthdate')
        
        # Validation
        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'gym_app/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'gym_app/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'gym_app/register.html')
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            mobile_no=mobile_no,
            address=address,
            birthdate=birthdate if birthdate else None,
            role='member'
        )
        
        messages.success(request, 'Registration successful! Please log in.')
        return redirect('login')
    
    return render(request, 'gym_app/register.html')


# ==================== Dashboard Views ====================

@login_required
def dashboard(request):
    """Role-based dashboard"""
    user = request.user
    
    # Redirect based on role
    if user.is_admin():
        return admin_dashboard(request)
    elif user.role == 'staff':
        return staff_dashboard(request)
    else:
        return member_dashboard(request)


@login_required
def admin_dashboard(request):
    """Admin dashboard with full analytics"""
    if not request.user.is_admin():
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    # Get today's stats
    today = date.today()
    
    # Active memberships
    active_memberships = UserMembership.objects.filter(
        status='active',
        end_date__gte=today
    ).count()
    
    # Total members
    total_members = User.objects.filter(role='member').count()
    
    # Today's revenue
    today_member_sales = Payment.objects.filter(
        payment_date__date=today
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    
    today_walkin_sales = WalkInPayment.objects.filter(
        payment_date__date=today
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    
    today_revenue = today_member_sales + today_walkin_sales
    
    # This month's revenue
    month_start = today.replace(day=1)
    month_member_sales = Payment.objects.filter(
        payment_date__date__gte=month_start
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    
    month_walkin_sales = WalkInPayment.objects.filter(
        payment_date__date__gte=month_start
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    
    month_revenue = month_member_sales + month_walkin_sales
    
    # Recent payments
    recent_payments = Payment.objects.select_related('user', 'membership__plan')[:10]
    recent_walkins = WalkInPayment.objects.select_related('pass_type')[:10]
    
    # Expiring soon (next 7 days)
    expiring_soon = UserMembership.objects.filter(
        status='active',
        end_date__range=[today, today + timedelta(days=7)]
    ).select_related('user', 'plan')[:10]
    
    context = {
        'active_memberships': active_memberships,
        'total_members': total_members,
        'today_revenue': today_revenue,
        'month_revenue': month_revenue,
        'recent_payments': recent_payments,
        'recent_walkins': recent_walkins,
        'expiring_soon': expiring_soon,
    }
    
    return render(request, 'gym_app/dashboard_admin.html', context)


@login_required
def staff_dashboard(request):
    """Staff dashboard - similar to admin but limited"""
    if not request.user.is_staff_or_admin():
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    today = date.today()
    
    # Today's transactions
    today_payments = Payment.objects.filter(
        payment_date__date=today
    ).count()
    
    today_walkins = WalkInPayment.objects.filter(
        payment_date__date=today
    ).count()
    
    # Recent activity
    recent_payments = Payment.objects.select_related('user', 'membership__plan')[:10]
    recent_walkins = WalkInPayment.objects.select_related('pass_type')[:10]
    
    # Expiring soon
    expiring_soon = UserMembership.objects.filter(
        status='active',
        end_date__range=[today, today + timedelta(days=7)]
    ).select_related('user', 'plan')[:10]
    
    context = {
        'today_payments': today_payments,
        'today_walkins': today_walkins,
        'recent_payments': recent_payments,
        'recent_walkins': recent_walkins,
        'expiring_soon': expiring_soon,
    }
    
    return render(request, 'gym_app/dashboard_staff.html', context)


@login_required
def member_dashboard(request):
    """Member dashboard - view own membership status"""
    user = request.user
    
    # Get current membership
    current_membership = UserMembership.objects.filter(
        user=user,
        status='active'
    ).select_related('plan').first()
    
    # Payment history
    payment_history = Payment.objects.filter(
        user=user
    ).select_related('membership__plan').order_by('-payment_date')[:10]
    
    # All memberships (history)
    all_memberships = UserMembership.objects.filter(
        user=user
    ).select_related('plan').order_by('-start_date')
    
    context = {
        'current_membership': current_membership,
        'payment_history': payment_history,
        'all_memberships': all_memberships,
    }
    
    return render(request, 'gym_app/dashboard_member.html', context)


# ==================== Membership Management ====================

@login_required
def membership_plans_view(request):
    """View all available membership plans"""
    plans = MembershipPlan.objects.filter(is_active=True)
    
    # If member, show if they have active membership
    current_membership = None
    if request.user.role == 'member':
        current_membership = UserMembership.objects.filter(
            user=request.user,
            status='active'
        ).first()
    
    context = {
        'plans': plans,
        'current_membership': current_membership,
    }
    
    return render(request, 'gym_app/membership_plans.html', context)


@login_required
def subscribe_plan(request, plan_id):
    """Subscribe to a membership plan"""
    if request.user.role != 'member':
        messages.error(request, 'Only members can subscribe to plans.')
        return redirect('membership_plans')
    
    plan = get_object_or_404(MembershipPlan, id=plan_id, is_active=True)
    
    # Check if user already has active membership
    active_membership = UserMembership.objects.filter(
        user=request.user,
        status='active'
    ).first()
    
    if active_membership:
        messages.warning(request, 'You already have an active membership.')
        return redirect('member_dashboard')
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        reference_no = request.POST.get('reference_no', '')
        
        # Create membership
        membership = UserMembership.objects.create(
            user=request.user,
            plan=plan,
            start_date=date.today(),
            status='active'
        )
        
        # Create payment record
        Payment.objects.create(
            user=request.user,
            membership=membership,
            amount=plan.price,
            method=payment_method,
            reference_no=reference_no,
            payment_date=timezone.now()
        )
        
        messages.success(request, f'Successfully subscribed to {plan.name}!')
        return redirect('member_dashboard')
    
    context = {
        'plan': plan,
    }
    
    return render(request, 'gym_app/subscribe_plan.html', context)


# ==================== Walk-in Management ====================

@login_required
def walkin_purchase(request):
    """Process walk-in pass purchase (staff/admin only)"""
    if not request.user.is_staff_or_admin():
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        pass_id = request.POST.get('pass_id')
        customer_name = request.POST.get('customer_name', '')
        mobile_no = request.POST.get('mobile_no', '')
        payment_method = request.POST.get('payment_method')
        reference_no = request.POST.get('reference_no', '')
        
        pass_type = get_object_or_404(FlexibleAccess, id=pass_id, is_active=True)
        
        # Create walk-in payment
        walkin_payment = WalkInPayment.objects.create(
            pass_type=pass_type,
            customer_name=customer_name,
            mobile_no=mobile_no,
            amount=pass_type.price,
            method=payment_method,
            reference_no=reference_no,
            payment_date=timezone.now()
        )
        
        messages.success(request, f'Walk-in pass sold successfully! (₱{pass_type.price})')
        return redirect('walkin_purchase')
    
    passes = FlexibleAccess.objects.filter(is_active=True)
    recent_walkins = WalkInPayment.objects.select_related('pass_type')[:10]
    
    context = {
        'passes': passes,
        'recent_walkins': recent_walkins,
    }
    
    return render(request, 'gym_app/walkin_purchase.html', context)


# ==================== Reports & Analytics ====================

@login_required
def reports_view(request):
    """Analytics and reports (admin only)"""
    if not request.user.is_admin():
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    # Generate today's analytics if not exists
    Analytics.generate_daily_report()
    
    # Get recent analytics
    recent_analytics = Analytics.objects.all()[:30]
    
    # Summary stats
    total_revenue = Payment.objects.aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0.00')
    
    total_walkin_revenue = WalkInPayment.objects.aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0.00')
    
    grand_total = total_revenue + total_walkin_revenue
    
    context = {
        'recent_analytics': recent_analytics,
        'total_revenue': total_revenue,
        'total_walkin_revenue': total_walkin_revenue,
        'grand_total': grand_total,
    }
    
    return render(request, 'gym_app/reports.html', context)


# ==================== Member Management (Admin/Staff) ====================

@login_required
def members_list(request):
    """List all members (admin/staff only)"""
    if not request.user.is_staff_or_admin():
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    members = User.objects.filter(role='member').order_by('-date_joined')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        members = members.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(mobile_no__icontains=search_query)
        )
    
    context = {
        'members': members,
        'search_query': search_query,
    }
    
    return render(request, 'gym_app/members_list.html', context)


@login_required
def member_detail(request, user_id):
    """View member details (admin/staff only)"""
    if not request.user.is_staff_or_admin():
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    member = get_object_or_404(User, id=user_id, role='member')
    
    # Get memberships
    memberships = UserMembership.objects.filter(
        user=member
    ).select_related('plan').order_by('-start_date')
    
    # Get payments
    payments = Payment.objects.filter(
        user=member
    ).select_related('membership__plan').order_by('-payment_date')
    
    context = {
        'member': member,
        'memberships': memberships,
        'payments': payments,
    }
    
    return render(request, 'gym_app/member_detail.html', context)

