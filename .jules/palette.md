## 2026-03-24 - [Improve Task Feedback]
**Learning:** Users can get confused if they perform actions on non-existent items and receive either a generic success message or a silent failure.
**Action:** Always return the outcome of a database operation (e.g., via rowcount) to the handler so specific feedback can be provided (e.g., "Task not found").
