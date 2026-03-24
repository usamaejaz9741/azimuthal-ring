# Sentinel's Journal 🛡️

## 2025-05-14 - Unauthorized Access to Personal Data
**Vulnerability:** The bot lacked any user authorization, allowing any Telegram user who discovered the bot to read and modify private notes, tasks, and personal "memories" stored in the local SQLite database.
**Learning:** For "personal" bots, the default assumption should be "deny all" rather than "allow all," as discovery on Telegram is relatively easy.
**Prevention:** Implement a mandatory `AUTHORIZED_USER_ID` check on all handlers that interact with personal data or the LLM.
