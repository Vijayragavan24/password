# Email Configuration Guide for PassChecker Pro

The contact form now supports automatic email notifications! This guide explains how to configure email sending.

## Current Status
- ✅ Contact messages are **automatically saved** to the database
- ⚠️ Email sending is **optional** - the form works without it
- If email credentials are not configured, messages are stored safely in the database

## How to Enable Email Notifications

### Option 1: Gmail (Recommended for Testing)

1. **Enable 2-Factor Authentication** on your Gmail account
   - Go to: https://myaccount.google.com/security

2. **Create an App Password**
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer"
   - Google will generate a 16-character password

3. **Update your `.env` file**
   ```env
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=xxxx xxxx xxxx xxxx
   MAIL_DEFAULT_SENDER=noreply@passcheckerpro.com
   ADMIN_EMAIL=your-email@gmail.com
   ```

4. **Restart the Flask server**
   ```bash
   python app.py
   ```

### Option 2: Other SMTP Servers

Update the `.env` file with your provider's details:

**Outlook/Hotmail:**
```env
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@outlook.com
MAIL_PASSWORD=your-password
```

**Custom SMTP:**
```env
MAIL_SERVER=your-smtp-server.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-username
MAIL_PASSWORD=your-password
```

## Email Notifications

When email is configured, the system sends:

### 1. **Admin Notification Email**
- **Recipient:** ADMIN_EMAIL (set in .env)
- **Content:** Complete contact message with user details
- **Purpose:** Alerts admin about new feedback/inquiries

### 2. **User Confirmation Email**
- **Recipient:** User's email address (from form)
- **Content:** Confirmation message with their submission
- **Purpose:** Assures users their message was received

## Testing Email Configuration

1. Open your browser to: http://localhost:5000
2. Navigate to the footer area and find the "Get in Touch" contact form
3. Fill in the form and submit
4. Check:
   - ✅ Database: Contact message saved to `contact_messages` table
   - ✅ Inbox: Confirmation email received (if configured)
   - ✅ Admin Email: Admin notification received (if configured)

## Troubleshooting

**Issue:** Emails not sending
- Check .env file has MAIL_USERNAME and MAIL_PASSWORD filled
- Verify MAIL_SERVER and MAIL_PORT are correct
- Messages are still saved to database even if email fails

**Issue:** "App password incorrect" (Gmail)
- Ensure you're using the 16-character App Password (with spaces)
- NOT your regular Gmail password
- Remove spaces from the app password if issues persist

**Issue:** "Connection refused"
- Verify MAIL_PORT is correct (usually 587 for TLS)
- Check firewall isn't blocking SMTP port
- Restart Flask server after changing .env

## Database Storage

Contact messages are **always** saved to the database regardless of email status.

View all messages:
```sql
SELECT * FROM contact_messages;
```

## Security Notes

- 🔒 Never commit `.env` file with credentials to git
- Never use your personal Gmail password - always use App Password
- Consider using environment variables in production
- For production, use trusted SMTP service (AWS SES, SendGrid, etc.)

## Production Setup

For production deployment:
1. Use managed email service (SendGrid, AWS SES, Mailgun)
2. Store credentials in environment variables
3. Set up email templates
4. Monitor bounce rates
5. Implement email verification for users

For questions or issues, refer to Flask-Mail documentation:
https://flask-mail.readthedocs.io/
