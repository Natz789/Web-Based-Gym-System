"""
Utility functions for Gym Management System
"""

import qrcode
from io import BytesIO
import base64
from decimal import Decimal
from django.conf import settings


def generate_gcash_qr(amount, reference_no=None, account_name="Rhose Gym", account_number="09XX-XXX-XXXX"):
    """
    Generate GCash QR code for payment

    Args:
        amount (Decimal): Payment amount
        reference_no (str): Payment reference number
        account_name (str): GCash account name
        account_number (str): GCash mobile number

    Returns:
        str: Base64 encoded QR code image
    """
    try:
        # Format payment data (simplified GCash format)
        # In production, use actual GCash API format
        payment_data = {
            'account': account_number,
            'name': account_name,
            'amount': str(amount),
            'reference': reference_no or 'N/A',
            'currency': 'PHP'
        }

        # Create payment string
        payment_string = f"GCash Payment\nAccount: {payment_data['account']}\nName: {payment_data['name']}\nAmount: ₱{payment_data['amount']}\nRef: {payment_data['reference']}"

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        qr.add_data(payment_string)
        qr.make(fit=True)

        # Create image
        img = qr.make_image(fill_color="black", back_color="white")

        # Convert to base64
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()

        return f"data:image/png;base64,{img_str}"

    except Exception as e:
        print(f"Error generating QR code: {e}")
        return None


def generate_payment_qr(payment_type, amount, reference_no=None, customer_info=None):
    """
    Generate payment QR code based on payment type

    Args:
        payment_type (str): Payment method (gcash, paymaya, etc.)
        amount (Decimal): Payment amount
        reference_no (str): Payment reference number
        customer_info (dict): Customer information

    Returns:
        str: Base64 encoded QR code image or None
    """
    if payment_type.lower() == 'gcash':
        return generate_gcash_qr(amount, reference_no)

    # Add other payment methods here
    # elif payment_type.lower() == 'paymaya':
    #     return generate_paymaya_qr(amount, reference_no)

    return None


def format_currency(amount):
    """
    Format amount as Philippine Peso

    Args:
        amount (Decimal/float): Amount to format

    Returns:
        str: Formatted currency string
    """
    try:
        if isinstance(amount, str):
            amount = Decimal(amount)
        return f"₱{amount:,.2f}"
    except:
        return f"₱{amount}"


def calculate_membership_end_date(start_date, duration_days):
    """
    Calculate membership end date

    Args:
        start_date (date): Start date
        duration_days (int): Duration in days

    Returns:
        date: End date
    """
    from datetime import timedelta
    return start_date + timedelta(days=duration_days)


def validate_mobile_number(mobile):
    """
    Validate Philippine mobile number format

    Args:
        mobile (str): Mobile number

    Returns:
        bool: True if valid, False otherwise
    """
    import re

    # Philippine mobile number format: 09XX-XXX-XXXX or 09XXXXXXXXX
    patterns = [
        r'^09\d{9}$',  # 09XXXXXXXXX
        r'^09\d{2}-\d{3}-\d{4}$',  # 09XX-XXX-XXXX
        r'^\+639\d{9}$',  # +639XXXXXXXXX
    ]

    for pattern in patterns:
        if re.match(pattern, mobile):
            return True

    return False


def generate_reference_number(prefix='GYM'):
    """
    Generate unique reference number

    Args:
        prefix (str): Reference prefix

    Returns:
        str: Reference number (e.g., GYM-20241109-123456)
    """
    from datetime import datetime
    import random

    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    random_suffix = random.randint(1000, 9999)

    return f"{prefix}-{timestamp}-{random_suffix}"


def get_age_group(age):
    """
    Get age group category

    Args:
        age (int): Age

    Returns:
        str: Age group (e.g., '18-25')
    """
    if age < 18:
        return 'Under 18'
    elif age <= 25:
        return '18-25'
    elif age <= 35:
        return '26-35'
    elif age <= 45:
        return '36-45'
    elif age <= 55:
        return '46-55'
    else:
        return '56+'


def calculate_days_between(start_date, end_date):
    """
    Calculate days between two dates

    Args:
        start_date (date): Start date
        end_date (date): End date

    Returns:
        int: Number of days
    """
    delta = end_date - start_date
    return delta.days


def send_email_notification(to_email, subject, message, html_message=None):
    """
    Send email notification

    Args:
        to_email (str/list): Recipient email(s)
        subject (str): Email subject
        message (str): Plain text message
        html_message (str): HTML message (optional)

    Returns:
        bool: True if sent successfully
    """
    from django.core.mail import send_mail
    from django.conf import settings

    try:
        if isinstance(to_email, str):
            to_email = [to_email]

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=to_email,
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def sanitize_filename(filename):
    """
    Sanitize filename for safe storage

    Args:
        filename (str): Original filename

    Returns:
        str: Sanitized filename
    """
    import re

    # Remove unsafe characters
    filename = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)

    # Limit length
    name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
    name = name[:50]  # Limit to 50 characters

    return f"{name}.{ext}" if ext else name


def get_client_ip(request):
    """
    Get client IP address from request

    Args:
        request: Django request object

    Returns:
        str: IP address
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def format_duration(seconds):
    """
    Format duration in seconds to human-readable format

    Args:
        seconds (int): Duration in seconds

    Returns:
        str: Formatted duration (e.g., "2h 30m")
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60

    if hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"
