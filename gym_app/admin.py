from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, MembershipPlan, FlexibleAccess, UserMembership, Payment, WalkInPayment, Analytics


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User admin with additional fields"""
    
    list_display = ['username', 'email', 'get_full_name', 'role', 'is_superuser', 'is_staff', 'age', 'mobile_no', 'is_active']
    list_filter = ['role', 'is_superuser', 'is_staff', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'mobile_no']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role & Permissions', {
            'fields': ('role',),
            'description': 'Note: Superusers are automatically assigned admin role'
        }),
        ('Additional Info', {
            'fields': ('mobile_no', 'address', 'birthdate', 'age')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Role Assignment', {
            'fields': ('role',),
        }),
        ('Additional Info', {
            'fields': ('mobile_no', 'address', 'birthdate', 'email', 'first_name', 'last_name')
        }),
    )
    
    readonly_fields = ['age', 'date_joined', 'last_login']
    
    def save_model(self, request, obj, form, change):
        """Override save to sync role with Django permissions"""
        # If making someone a superuser, make them admin
        if obj.is_superuser:
            obj.role = 'admin'
        # If making someone staff (but not superuser), make them staff role
        elif obj.is_staff and obj.role == 'member':
            obj.role = 'staff'
        
        super().save_model(request, obj, form, change)


@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    """Admin interface for Membership Plans"""
    
    list_display = ['name', 'duration_days', 'price', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    ordering = ['price']
    
    fieldsets = (
        ('Plan Details', {
            'fields': ('name', 'duration_days', 'price', 'description')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(FlexibleAccess)
class FlexibleAccessAdmin(admin.ModelAdmin):
    """Admin interface for Walk-in Passes"""
    
    list_display = ['name', 'duration_days', 'price', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    ordering = ['duration_days']
    
    fieldsets = (
        ('Pass Details', {
            'fields': ('name', 'duration_days', 'price', 'description')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(UserMembership)
class UserMembershipAdmin(admin.ModelAdmin):
    """Admin interface for User Memberships"""
    
    list_display = ['user', 'plan', 'start_date', 'end_date', 'status', 'days_remaining']
    list_filter = ['status', 'start_date', 'end_date']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Membership Details', {
            'fields': ('user', 'plan', 'start_date', 'end_date', 'status')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def days_remaining(self, obj):
        """Display days remaining in membership"""
        days = obj.days_remaining()
        if days > 0:
            return f"{days} days"
        return "Expired"
    days_remaining.short_description = 'Days Left'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Admin interface for Member Payments"""
    
    list_display = ['user', 'amount', 'method', 'payment_date', 'reference_no', 'membership']
    list_filter = ['method', 'payment_date']
    search_fields = ['user__username', 'user__email', 'reference_no', 'user__first_name', 'user__last_name']
    date_hierarchy = 'payment_date'
    
    fieldsets = (
        ('Payment Details', {
            'fields': ('user', 'membership', 'amount', 'method', 'payment_date')
        }),
        ('Additional Info', {
            'fields': ('reference_no', 'notes')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(WalkInPayment)
class WalkInPaymentAdmin(admin.ModelAdmin):
    """Admin interface for Walk-in Payments"""
    
    list_display = ['customer_name', 'pass_type', 'amount', 'method', 'payment_date', 'mobile_no']
    list_filter = ['method', 'payment_date', 'pass_type']
    search_fields = ['customer_name', 'mobile_no', 'reference_no']
    date_hierarchy = 'payment_date'
    
    fieldsets = (
        ('Customer Info', {
            'fields': ('customer_name', 'mobile_no')
        }),
        ('Payment Details', {
            'fields': ('pass_type', 'amount', 'method', 'payment_date')
        }),
        ('Additional Info', {
            'fields': ('reference_no', 'notes')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Analytics)
class AnalyticsAdmin(admin.ModelAdmin):
    """Admin interface for Analytics"""
    
    list_display = ['date', 'total_members', 'total_passes', 'total_sales', 'age_group']
    list_filter = ['date']
    date_hierarchy = 'date'
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Report Date', {
            'fields': ('date',)
        }),
        ('Metrics', {
            'fields': ('total_members', 'total_passes', 'total_sales', 'age_group')
        }),
    )
    
    def has_add_permission(self, request):
        """Prevent manual addition - analytics should be auto-generated"""
        return False


# Customize admin site headers
admin.site.site_header = "Gym Management System"
admin.site.site_title = "Gym Admin"
admin.site.index_title = "Welcome to Gym Management System"