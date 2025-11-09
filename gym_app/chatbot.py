"""
Intelligent Chatbot for Gym Management System
Handles database queries and user interactions
"""

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from django.utils import timezone
from django.db import models
from datetime import timedelta
import re
from decimal import Decimal

from .models import (
    User, MembershipPlan, FlexibleAccess, UserMembership,
    Payment, WalkInPayment, Analytics
)


class GymChatBot:
    """
    Intelligent chatbot with database query capabilities
    """

    def __init__(self):
        """Initialize the chatbot"""
        self.bot = ChatBot(
            'GymAssistant',
            storage_adapter='chatterbot.storage.SQLStorageAdapter',
            database_uri='sqlite:///chatbot_db.sqlite3',
            logic_adapters=[
                {
                    'import_path': 'chatterbot.logic.BestMatch',
                    'default_response': 'I am not sure I understand. Could you rephrase that?',
                    'maximum_similarity_threshold': 0.90
                }
            ]
        )
        self.trained = False

    def train_chatbot(self):
        """Train the chatbot with gym-specific conversations"""
        if self.trained:
            return

        # Train with English corpus
        corpus_trainer = ChatterBotCorpusTrainer(self.bot)
        corpus_trainer.train("chatterbot.corpus.english.greetings")

        # Train with custom gym-specific conversations
        list_trainer = ListTrainer(self.bot)

        gym_conversations = [
            # Greetings
            "Hi",
            "Hello! Welcome to our Gym Management System. How can I help you today?",
            "Hello",
            "Hi there! I'm here to assist you with memberships, plans, and general inquiries.",
            "Hey",
            "Hey! What can I do for you?",

            # Membership Plans
            "What membership plans do you offer?",
            "We offer various membership plans including monthly and yearly subscriptions. Would you like to know the prices?",
            "Tell me about membership plans",
            "Our membership plans vary in duration and price. You can check available plans on the Membership Plans page.",
            "How much is a monthly membership?",
            "Membership prices vary by plan. Please check our Membership Plans page for current pricing.",

            # Walk-in Passes
            "Do you have day passes?",
            "Yes! We offer flexible access passes including 1-day, 3-day, and weekly passes for walk-in customers.",
            "Can I come without membership?",
            "Absolutely! We offer walk-in passes for those who prefer not to commit to a full membership.",
            "How much is a day pass?",
            "Day pass prices vary. Please visit our Walk-in page or ask staff for current pricing.",

            # Payment Methods
            "What payment methods do you accept?",
            "We accept Cash, GCash, and Card payments for all memberships and walk-in passes.",
            "Can I pay with GCash?",
            "Yes! GCash is accepted. We'll provide a QR code for easy payment.",
            "Do you accept credit cards?",
            "Yes, we accept card payments through our payment terminal.",

            # Operating Hours
            "What are your hours?",
            "Our gym is open 24/7 for members. Walk-in hours may vary, please contact staff for details.",
            "Are you open on weekends?",
            "Yes! We're open 24/7, including weekends for members.",

            # Membership Status
            "How do I check my membership status?",
            "You can view your membership status on your dashboard after logging in.",
            "When does my membership expire?",
            "Your membership expiration date is displayed on your dashboard. You'll also receive notifications before expiry.",
            "How do I renew my membership?",
            "You can renew your membership by subscribing to a new plan from the Membership Plans page.",

            # Registration
            "How do I sign up?",
            "Click the 'Register' button on the homepage and fill in your details to create an account.",
            "Do I need to register?",
            "Registration is required for membership plans. Walk-in customers don't need to register.",

            # Contact & Support
            "How do I contact support?",
            "You can contact our staff through the contact information on the About page.",
            "I have a problem",
            "I'm sorry to hear that. Please contact our staff or admin for assistance with your issue.",

            # General Info
            "What facilities do you have?",
            "We offer state-of-the-art gym equipment, training areas, and fitness facilities. Check our About page for more details.",
            "Do you have trainers?",
            "Please contact our staff for information about personal training and coaching services.",

            # Goodbye
            "Thanks",
            "You're welcome! Feel free to ask if you need anything else.",
            "Thank you",
            "Happy to help! Have a great workout!",
            "Bye",
            "Goodbye! Stay healthy and strong!",
        ]

        list_trainer.train(gym_conversations)
        self.trained = True

    def get_response(self, message, user=None):
        """
        Get chatbot response with database query capabilities

        Args:
            message: User's message
            user: Django User object (if authenticated)

        Returns:
            str: Chatbot response
        """
        message_lower = message.lower().strip()

        # Check for database queries first
        db_response = self._handle_database_query(message_lower, user)
        if db_response:
            return db_response

        # Get chatbot response
        try:
            response = self.bot.get_response(message)
            return str(response)
        except Exception as e:
            return "I'm sorry, I couldn't process that. Could you try asking differently?"

    def _handle_database_query(self, message, user):
        """
        Handle database queries based on user message

        Args:
            message: Lowercase user message
            user: Django User object

        Returns:
            str or None: Response if query handled, None otherwise
        """

        # Check membership status
        if any(word in message for word in ['my membership', 'membership status', 'my plan', 'subscription status']):
            if not user or not user.is_authenticated:
                return "Please login to check your membership status."

            try:
                membership = UserMembership.objects.filter(
                    user=user,
                    status='active'
                ).order_by('-start_date').first()

                if membership:
                    days_left = (membership.end_date - timezone.now().date()).days
                    return f"Your {membership.plan.name} is active until {membership.end_date.strftime('%B %d, %Y')}. You have {days_left} days remaining."
                else:
                    return "You don't have an active membership. Would you like to subscribe to a plan?"
            except Exception:
                return "Unable to retrieve your membership information at the moment."

        # Check available plans
        if any(word in message for word in ['available plans', 'show plans', 'list plans', 'plan prices', 'membership prices']):
            try:
                plans = MembershipPlan.objects.filter(is_active=True)
                if plans.exists():
                    response = "Here are our available membership plans:\n\n"
                    for plan in plans:
                        response += f"• {plan.name}: ₱{plan.price} for {plan.duration_days} days\n"
                    response += "\nYou can subscribe from the Membership Plans page!"
                    return response
                else:
                    return "No membership plans are currently available. Please contact staff."
            except Exception:
                return "Unable to retrieve plans at the moment."

        # Check walk-in passes
        if any(word in message for word in ['walk-in', 'day pass', 'daily pass', 'flexible pass', 'passes available']):
            try:
                passes = FlexibleAccess.objects.filter(is_active=True)
                if passes.exists():
                    response = "Here are our available walk-in passes:\n\n"
                    for pass_item in passes:
                        response += f"• {pass_item.name}: ₱{pass_item.price} for {pass_item.duration_days} days\n"
                    response += "\nVisit our Walk-in page to purchase!"
                    return response
                else:
                    return "No walk-in passes are currently available. Please contact staff."
            except Exception:
                return "Unable to retrieve walk-in passes at the moment."

        # Payment history
        if any(word in message for word in ['payment history', 'my payments', 'transaction history', 'my transactions']):
            if not user or not user.is_authenticated:
                return "Please login to view your payment history."

            try:
                payments = Payment.objects.filter(user=user).order_by('-payment_date')[:5]
                if payments.exists():
                    response = "Your recent payments:\n\n"
                    for payment in payments:
                        response += f"• ₱{payment.amount} on {payment.payment_date.strftime('%B %d, %Y')} via {payment.method}\n"
                    return response
                else:
                    return "You don't have any payment history yet."
            except Exception:
                return "Unable to retrieve payment history at the moment."

        # Total members (admin/staff only)
        if any(word in message for word in ['total members', 'how many members', 'member count']):
            if user and user.is_staff_or_admin():
                try:
                    total = User.objects.filter(role='member').count()
                    active_memberships = UserMembership.objects.filter(status='active').count()
                    return f"Total registered members: {total}\nActive memberships: {active_memberships}"
                except Exception:
                    return "Unable to retrieve member statistics."
            else:
                return "This information is only available to staff and administrators."

        # Today's revenue (admin/staff only)
        if any(word in message for word in ['today revenue', "today's revenue", 'daily revenue', 'revenue today']):
            if user and user.is_staff_or_admin():
                try:
                    today = timezone.now().date()
                    member_payments = Payment.objects.filter(
                        payment_date__date=today
                    ).aggregate(total=models.Sum('amount'))['total'] or Decimal('0')

                    walkin_payments = WalkInPayment.objects.filter(
                        payment_date__date=today
                    ).aggregate(total=models.Sum('amount'))['total'] or Decimal('0')

                    total = member_payments + walkin_payments
                    return f"Today's revenue: ₱{total}\n(Member payments: ₱{member_payments}, Walk-in: ₱{walkin_payments})"
                except Exception:
                    return "Unable to retrieve revenue information."
            else:
                return "This information is only available to staff and administrators."

        # Expiring memberships (admin/staff only)
        if any(word in message for word in ['expiring memberships', 'memberships expiring', 'expiring soon']):
            if user and user.is_staff_or_admin():
                try:
                    seven_days = timezone.now().date() + timedelta(days=7)
                    expiring = UserMembership.objects.filter(
                        status='active',
                        end_date__lte=seven_days,
                        end_date__gte=timezone.now().date()
                    ).count()
                    return f"{expiring} membership(s) expiring in the next 7 days."
                except Exception:
                    return "Unable to retrieve expiring memberships."
            else:
                return "This information is only available to staff and administrators."

        # Help
        if message in ['help', 'what can you do', 'commands', 'options']:
            help_text = """I can help you with:

📊 General Queries:
• Ask about membership plans and prices
• Ask about walk-in passes
• Ask about payment methods
• Ask about gym hours and facilities

👤 Personal Info (Login Required):
• "my membership status"
• "my payment history"
• "when does my membership expire"

🔐 Staff/Admin Only:
• "total members"
• "today's revenue"
• "expiring memberships"

Just ask me anything!"""
            return help_text

        return None


# Global chatbot instance
_chatbot_instance = None

def get_chatbot():
    """Get or create the global chatbot instance"""
    global _chatbot_instance
    if _chatbot_instance is None:
        _chatbot_instance = GymChatBot()
        _chatbot_instance.train_chatbot()
    return _chatbot_instance
