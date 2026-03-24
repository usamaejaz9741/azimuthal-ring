# Sentinel's Journal 🛡️

## 2025-05-14 - Unauthorized Access to Personal Data
**Vulnerability:** The bot lacked any user authorization, allowing any Telegram user who discovered the bot to read and modify private notes, tasks, and personal "memories" stored in the local SQLite database.
**Learning:** For "personal" bots, the default assumption should be "deny all" rather than "allow all," as discovery on Telegram is relatively easy.
**Prevention:** Implement a mandatory `AUTHORIZED_USER_ID` check on all handlers that interact with personal data or the LLM.

## 2025-05-15 - LLM Prompt Injection via ChatML Tokens
**Vulnerability:** The LLM prompt construction used raw user input and search results within ChatML tags (`<|im_start|>`, `<|im_end|>`). An attacker could include these tokens in their message or a searched webpage to "break out" of the user role and inject system instructions.
**Learning:** Raw string concatenation for LLM prompts is inherently risky when using models with specific control tokens.
**Prevention:** Always sanitize user-controlled strings by stripping or escaping model-specific control tokens before insertion into the prompt template.

## 2025-05-15 - Information Leakage in Async Handlers
**Vulnerability:** Exceptions in LLM inference and web search were returned directly to the user, potentially exposing internal paths, library names, and logic details.
**Learning:** For a production-ready bot, internal errors must be logged for debugging but masked with generic messages for the user.
**Prevention:** Wrap all external service calls (LLM, Search, DB) in try-except blocks that log the full error and return a safe, generic response.
