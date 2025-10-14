from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal


class User(AbstractUser):
    """Custom User model with role-based access and demographics"""
    
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('member', 'Member'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    mobile_no = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def save(self, *args, **kwargs):
        """Auto-calculate age from birthdate before saving"""
        if self.birthdate:
            today = date.today()
            self.age = today.year - self.birthdate.year - (
                (today.month, today.day) < (self.birthdate.month, self.birthdate.day)
            )
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_staff_or_admin(self):
        return self.role in ['admin', 'staff']


class MembershipPlan(models.Model):
    """Permanent membership plans (monthly, yearly, etc.)"""
    
    name = models.CharField(max_length=100)
    duration_days = models.IntegerField(help_text="Duration in days")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'membership_plans'
        verbose_name = 'Membership Plan'
        verbose_name_plural = 'Membership Plans'
        ordering = ['price']
    
    def __str__(self):
        return f"{self.name} - ₱{self.price} ({self.duration_days} days)"


class FlexibleAccess(models.Model):
    """Walk-in passes (1-day, 3-day, weekly, etc.)"""
    
    name = models.CharField(max_length=100)
    duration_days = models.IntegerField(help_text="Validity in days")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'flexible_access'
        verbose_name = 'Flexible Access Pass'
        verbose_name_plural = 'Flexible Access Passes'
        ordering = ['duration_days']
    
    def __str__(self):
        return f"{self.name} - ₱{self.price} ({self.duration_days} days)"


class UserMembership(models.Model):
    """Tracks member subscriptions to plans"""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships')
    plan = models.ForeignKey(MembershipPlan, on_delete=models.PROTECT, related_name='subscriptions')
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_memberships'
        verbose_name = 'User Membership'
        verbose_name_plural = 'User Memberships'
        ordering = ['-start_date']
    
    def save(self, *args, **kwargs):
        """Auto-calculate end_date based on plan duration"""
        if not self.end_date and self.start_date and self.plan:
            self.end_date = self.start_date + timedelta(days=self.plan.duration_days)
        
        # Auto-update status based on dates
        if self.end_date < date.today():
            self.status = 'expired'
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.plan.name} ({self.status})"
    
    def is_active(self):
        """Check if membership is currently active"""
        return self.status == 'active' and self.end_date >= date.today()
    
    def days_remaining(self):
        """Calculate days remaining in membership"""
        if self.end_date >= date.today():
            return (self.end_date - date.today()).days
        return 0


class Payment(models.Model):
    """Payment records for registered members"""
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('gcash', 'GCash'),
        ('card', 'Card'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    membership = models.ForeignKey(UserMembership, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    payment_date = models.DateTimeField(default=timezone.now)
    reference_no = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'payments'
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - ₱{self.amount} ({self.payment_date.strftime('%Y-%m-%d')})"


class WalkInPayment(models.Model):
    """Payment records for walk-in clients (no account required)"""
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('gcash', 'GCash'),
        ('card', 'Card'),
    ]
    
    pass_type = models.ForeignKey(FlexibleAccess, on_delete=models.PROTECT, related_name='walk_in_sales')
    customer_name = models.CharField(max_length=100, blank=True, null=True)
    mobile_no = models.CharField(max_length=20, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    payment_date = models.DateTimeField(default=timezone.now)
    reference_no = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'walk_in_payments'
        verbose_name = 'Walk-in Payment'
        verbose_name_plural = 'Walk-in Payments'
        ordering = ['-payment_date']
    
    def __str__(self):
        customer = self.customer_name if self.customer_name else "Anonymous"
        return f"{customer} - {self.pass_type.name} - ₱{self.amount}"


class Analytics(models.Model):
    """Daily/weekly aggregated data for dashboard"""
    
    date = models.DateField(unique=True)
    total_members = models.IntegerField(default=0)
    total_passes = models.IntegerField(default=0)
    total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    age_group = models.CharField(max_length=20, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'analytics'
        verbose_name = 'Analytics'
        verbose_name_plural = 'Analytics'
        ordering = ['-date']
    
    def __str__(self):
        return f"Analytics for {self.date}"
    
    @classmethod
    def generate_daily_report(cls, target_date=None):
        """Generate analytics for a specific date"""
        if target_date is None:
            target_date = date.today()
        
        # Count active memberships
        active_members = UserMembership.objects.filter(
            status='active',
            start_date__lte=target_date,
            end_date__gte=target_date
        ).count()
        
        # Count walk-in passes sold on this date
        passes_sold = WalkInPayment.objects.filter(
            payment_date__date=target_date
        ).count()
        
        # Calculate total sales
        member_sales = Payment.objects.filter(
            payment_date__date=target_date
        ).aggregate(total=models.Sum('amount'))['total'] or Decimal('0.00')
        
        walkin_sales = WalkInPayment.objects.filter(
            payment_date__date=target_date
        ).aggregate(total=models.Sum('amount'))['total'] or Decimal('0.00')
        
        total_sales = member_sales + walkin_sales
        
        # Create or update analytics record
        analytics, created = cls.objects.update_or_create(
            date=target_date,
            defaults={
                'total_members': active_members,
                'total_passes': passes_sold,
                'total_sales': total_sales,
            }
        )
        
        return analytics

