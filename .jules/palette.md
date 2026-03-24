## 2026-03-24 - [Improve Bot Responsiveness with Typing Indicators]
**Learning:** In conversational interfaces, long-running operations like AI inference can make the bot feel unresponsive or broken. Providing immediate visual feedback via chat actions (like "typing...") significantly improves perceived performance and user confidence.
**Action:** Always include a typing indicator or relevant chat action (e.g., `ChatAction.TYPING`) before starting any operation that takes more than a few hundred milliseconds, especially AI generation or external API calls.
