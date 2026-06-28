💬 ChatApp

A real-time chat application that covers the full backend architecture — WebSockets, message queuing, push notifications, end-to-end encryption design, and scalable database schema — paired with a React Native mobile client for Android.


🧠 Project Purpose

This project was built to learn system design by implementing it — not just studying it. Every architectural decision (WebSocket gateway, message delivery tracking, presence service, offline sync) was designed on paper first, then built step by step. The goal is a production-grade chat system understood from the ground up.

Features


Real-time 1:1 messaging via WebSockets (Django Channels)
Group chats with member roles (admin / member)
Message history persisted in PostgreSQL
Typing indicators & read receipts — sent → delivered → read status tracking
Offline support — undelivered messages synced on reconnect
Push notifications via Firebase Cloud Messaging (FCM) for offline users
Presence service — online/offline/typing status tracked in Redis
End-to-end encryption design (encrypted blobs, keys never stored server-side)
JWT authentication for all REST API and WebSocket connections

