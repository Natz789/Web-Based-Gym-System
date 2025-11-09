# 🤖 Intelligent Chatbot - Documentation

## Overview

The Gym Management System now features an **intelligent chatbot** powered by ChatterBot that can answer questions and query the database in real-time. The chatbot is accessible to all users (authenticated and anonymous) and provides personalized responses based on user roles and permissions.

---

## 🎯 Features

### General Capabilities
- ✅ Natural language processing
- ✅ Context-aware responses
- ✅ Database query integration
- ✅ Role-based access to information
- ✅ Chat history persistence (localStorage)
- ✅ Quick reply buttons
- ✅ Typing indicators
- ✅ Real-time responses
- ✅ Beautiful, responsive UI

### What the Chatbot Can Do

#### 📊 For All Users (Public)
- Answer questions about membership plans and pricing
- Provide information about walk-in passes
- Explain payment methods (Cash, GCash, Card)
- Share gym hours and operating information
- Provide general gym facility information
- Guide users on how to register and sign up

#### 👤 For Authenticated Members
- Check membership status and expiration date
- View remaining days on membership
- Display payment history
- Answer account-specific queries

#### 🔐 For Staff/Admin Only
- Total member count and statistics
- Active membership counts
- Today's revenue breakdown
- Expiring memberships in next 7 days
- Daily sales reports

---

## 📁 Files Created

### Backend Files
1. **`gym_app/chatbot.py`** - Core chatbot logic and database integration
2. **`gym_app/views.py`** - Added `chatbot_response` view
3. **`gym_app/urls.py`** - Added `/api/chatbot/` endpoint

### Frontend Files
4. **`gym_app/static/gym_app/js/chatbot.js`** - Chat widget JavaScript
5. **`gym_app/static/gym_app/css/chatbot.css`** - Chat widget styles
6. **`gym_app/templates/gym_app/base.html`** - Integrated chatbot widget

### Configuration
7. **`requirements.txt`** - Added ChatterBot and dependencies

---

## 🚀 Installation & Setup

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

**Key Dependencies:**
- `ChatterBot==1.0.8` - Core chatbot framework
- `chatterbot-corpus==1.2.0` - Pre-trained conversation data
- `sqlalchemy<2.0` - Database adapter for chatbot storage
- `nltk>=3.8.0` - Natural language processing

### Step 2: Download NLTK Data

```bash
python -m nltk.downloader punkt
python -m nltk.downloader averaged_perceptron_tagger
```

### Step 3: Initialize Chatbot Database

The chatbot automatically creates its own SQLite database (`chatbot_db.sqlite3`) on first run. No manual setup needed!

### Step 4: Run Migrations (if needed)

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Test the Chatbot

```bash
python manage.py runserver
```

Visit any page and you'll see the chatbot toggle button in the bottom-right corner!

---

## 💬 How to Use

### Opening the Chat

1. **Click the chat icon** in the bottom-right corner of any page
2. The chat window will slide up with a welcome message
3. Use the **quick reply buttons** or type your own message

### Quick Reply Buttons

- **💪 Plans** - View membership plans
- **💳 Payment** - Learn about payment methods
- **📊 Status** - Check your membership status (login required)
- **❓ Help** - Get list of available commands

### Example Queries

```
User: "What membership plans do you offer?"
Bot: Lists all available plans with prices

User: "My membership status"
Bot: Shows your active membership and expiration date

User: "How much is a day pass?"
Bot: Lists walk-in pass options

User: "Total members" (Staff/Admin only)
Bot: Shows total registered members and active memberships

User: "Today's revenue" (Staff/Admin only)
Bot: Shows today's revenue breakdown
```

### Closing the Chat

- Click the **minimize button** (−)
- Click the **close button** (×)
- Click the **chat toggle** button again

### Clearing Chat History

- Click the **trash icon** in the header
- Confirm deletion
- Chat history will be cleared from localStorage

---

## 🔧 Customization

### Adding New Conversation Patterns

Edit `gym_app/chatbot.py` and add to the `gym_conversations` list:

```python
gym_conversations = [
    # Your question
    "What are your opening hours?",
    # Bot response
    "We're open 24/7 for members. Walk-in hours are 6 AM - 10 PM daily.",

    # Add more Q&A pairs...
]
```

### Adding Database Queries

Add new query handlers in the `_handle_database_query` method:

```python
def _handle_database_query(self, message, user):
    # Check for your custom query
    if 'custom query' in message:
        # Your database logic
        result = YourModel.objects.filter(...)
        return f"Here's the result: {result}"
```

### Modifying UI Colors

Edit `gym_app/static/gym_app/css/chatbot.css`:

```css
.chatbot-toggle {
    background: linear-gradient(135deg, #YOUR_COLOR1, #YOUR_COLOR2);
}

.user-message .message-text {
    background: linear-gradient(135deg, #YOUR_COLOR1, #YOUR_COLOR2);
}
```

### Changing Quick Reply Buttons

Edit `gym_app/static/gym_app/js/chatbot.js`:

```javascript
<button class="quick-reply-btn" data-message="Your question">🎯 Label</button>
```

---

## 🎨 UI Components

### Chat Toggle Button
- **Position:** Fixed, bottom-right
- **Features:** Pulse animation, notification badge
- **Responsive:** Scales on mobile devices

### Chat Window
- **Size:** 400px × 600px (desktop)
- **Responsive:** Full-screen on mobile
- **Features:**
  - Gradient header with status indicator
  - Scrollable message area
  - Quick reply buttons
  - Input field with send button
  - Typing indicator

### Message Bubbles
- **Bot messages:** White background, left-aligned
- **User messages:** Blue gradient, right-aligned
- **Features:** Timestamps, smooth animations

---

## 🔒 Security & Privacy

### Data Protection
- Chat history stored locally in browser (localStorage)
- No server-side chat history storage
- User authentication checked for sensitive queries

### Access Control
- Public queries: Available to everyone
- Member queries: Require login
- Staff/Admin queries: Role-based access control

### API Endpoint
- **URL:** `/api/chatbot/`
- **Method:** POST only
- **CSRF:** Exempt (safe for public access)
- **Rate limiting:** Not implemented (consider adding)

---

## 📊 Database Schema

### Chatbot Storage
The chatbot uses a separate SQLite database (`chatbot_db.sqlite3`) for storing:
- Conversation training data
- Statement-response mappings
- Learning progress

**Note:** This is separate from your main Django database.

### Audit Logging
All chatbot queries from authenticated users are logged:

```python
AuditLog.log(
    action='chatbot_query',
    user=user,
    description='Chatbot query: {message}',
    severity='info'
)
```

---

## 🐛 Troubleshooting

### Issue: Chatbot doesn't appear

**Solution:**
1. Check browser console for JavaScript errors
2. Verify static files are loading: `python manage.py collectstatic`
3. Clear browser cache
4. Check that `{% load static %}` is in base.html

### Issue: "Module not found: ChatterBot"

**Solution:**
```bash
pip install ChatterBot==1.0.8
pip install chatterbot-corpus==1.2.0
```

### Issue: NLTK data not found

**Solution:**
```bash
python -m nltk.downloader punkt
python -m nltk.downloader averaged_perceptron_tagger
python -m nltk.downloader stopwords
```

### Issue: Chatbot gives incorrect responses

**Solution:**
1. Clear chatbot database: Delete `chatbot_db.sqlite3`
2. Retrain chatbot: Restart server (auto-trains on first request)
3. Add more training data in `gym_conversations`

### Issue: Database queries not working

**Check:**
1. User authentication status
2. User role/permissions
3. Database models are migrated
4. Check logs for errors

---

## 🎯 Testing

### Manual Testing Checklist

- [ ] Chatbot appears on all pages
- [ ] Toggle button works (open/close)
- [ ] Quick reply buttons work
- [ ] Text input and send button work
- [ ] Typing indicator appears
- [ ] Messages display correctly
- [ ] Timestamps show properly
- [ ] Clear chat works
- [ ] Chat history persists on page reload

### Test Queries

**General Queries:**
```
- "Hello"
- "What membership plans do you offer?"
- "Do you have day passes?"
- "What payment methods do you accept?"
- "help"
```

**Authenticated Member:**
```
- "My membership status"
- "My payment history"
- "When does my membership expire?"
```

**Staff/Admin:**
```
- "Total members"
- "Today's revenue"
- "Expiring memberships"
```

---

## 📈 Future Enhancements

### Planned Features
- [ ] Voice input/output support
- [ ] Multi-language support
- [ ] Integration with email notifications
- [ ] Appointment booking through chat
- [ ] Exercise recommendations
- [ ] Nutrition advice chatbot
- [ ] Integration with fitness tracking
- [ ] SMS notifications for chat messages
- [ ] Advanced NLP with spaCy
- [ ] Machine learning for better responses

### Advanced Features
- [ ] Sentiment analysis
- [ ] Intent classification
- [ ] Named entity recognition
- [ ] Context management across sessions
- [ ] Integration with external APIs (weather, nutrition)
- [ ] Chatbot analytics dashboard
- [ ] A/B testing for responses

---

## 💡 Best Practices

### For Users
1. **Be specific** - Clear questions get better answers
2. **Use keywords** - "membership", "payment", "status"
3. **Try quick replies** - Fastest way to get common info
4. **Ask for help** - Type "help" to see all commands

### For Developers
1. **Regular training** - Update conversation patterns
2. **Monitor logs** - Check audit trail for common queries
3. **Test responses** - Verify accuracy of database queries
4. **Update documentation** - Keep users informed
5. **Performance** - Monitor chatbot response times

---

## 🔗 API Reference

### Endpoint: `/api/chatbot/`

**Method:** POST

**Request Body:**
```json
{
    "message": "What membership plans do you offer?"
}
```

**Response (Success):**
```json
{
    "response": "Here are our available membership plans:\n\n• Monthly Plan: ₱1500 for 30 days\n• Yearly Plan: ₱15000 for 365 days",
    "timestamp": "2024-11-09T12:34:56.789Z"
}
```

**Response (Error):**
```json
{
    "error": "Message cannot be empty"
}
```

---

## 📞 Support

If you encounter issues:
1. Check this documentation
2. Review browser console logs
3. Check Django server logs
4. Verify all dependencies installed
5. Contact system administrator

---

## ✅ Summary

Your Gym Management System now has:
- ✅ Intelligent chatbot with NLP
- ✅ Database query capabilities
- ✅ Role-based information access
- ✅ Beautiful, responsive UI
- ✅ Real-time responses
- ✅ Chat history persistence
- ✅ Quick reply shortcuts
- ✅ Comprehensive audit logging

**The chatbot is ready to assist your users 24/7!** 🎉

---

*Last Updated: November 2024*
*Version: 1.0.0*
