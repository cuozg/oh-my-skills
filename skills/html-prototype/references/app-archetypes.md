# App Archetypes: Common Screen Maps & Navigation Flows

This reference guide outlines the screen inventories, navigation structures, and data models for common application types. Use this to quickly scaffold interactive prototypes.

## Table of Contents
1. [E-Reader / Book App](#1-e-reader--book-app)
2. [E-Commerce / Shopping](#2-e-commerce--shopping)
3. [Social Media](#3-social-media)
4. [Fitness / Health Tracker](#4-fitness--health-tracker)
5. [Food / Recipe App](#5-food--recipe-app)
6. [Finance / Banking](#6-finance--banking)
7. [Task / Project Management](#7-task--project-management)
8. [Messaging / Chat](#8-messaging--chat)
9. [Music / Podcast](#9-music--podcast)
10. [Travel / Booking](#10-travel--booking)

---

## 1. E-Reader / Book App
- **Screens**: `splash`, `login`, `library` (grid), `discover`, `book-detail`, `reader-view`, `bookmarks`, `progress`, `settings`.
- **Navigation**: Bottom Tabs (Library, Discover, Bookmarks, Profile). Stack nav for Book Detail → Reader.
- **Data Model**: `Book { id, title, author, coverColor, totalPages, currentPage, progressPercent, genre }`.
- **Transitions**: `library` → `book-detail` (slide-left), `book-detail` → `reader` (zoom-in), Tabs (fade).

## 2. E-Commerce / Shopping
- **Screens**: `splash`, `login`, `home`, `product-list`, `product-detail`, `cart`, `checkout`, `order-success`, `order-history`, `profile`.
- **Navigation**: Bottom Tabs (Home, Search, Cart, Orders, Profile). Sequential flow for Checkout.
- **Data Model**: `Product { id, name, price, rating, reviewCount, imageUrl, description, category }`.
- **Transitions**: List → Detail (slide-left), `cart` → `checkout` (slide-up), Tabs (instant/fade).

## 3. Social Media
- **Screens**: `splash`, `login`, `feed`, `post-detail`, `create-post`, `profile-me`, `profile-user`, `notifications`, `inbox`, `chat-thread`, `search`.
- **Navigation**: Bottom Tabs (Feed, Search, Create, Notifications, Profile). Modal for `create-post`.
- **Data Model**: `Post { id, userId, username, userAvatar, content, images[], likes, commentsCount, timestamp }`.
- **Transitions**: `feed` → `post-detail` (slide-left), `create-post` (slide-up), Tabs (fade).

## 4. Fitness / Health Tracker
- **Screens**: `splash`, `onboarding-1..3`, `login`, `dashboard`, `workout-list`, `workout-detail`, `active-workout`, `history`, `charts`, `profile`.
- **Navigation**: Bottom Tabs (Today, Workouts, History, Profile). Dashboard uses cards for stats.
- **Data Model**: `Stat { steps, calories, heartRate, activeMinutes }`, `Workout { id, title, duration, intensity, exercises[] }`.
- **Transitions**: `workout-detail` → `active-workout` (fade-overlay), Onboarding (horizontal-swipe).

## 5. Food / Recipe App
- **Screens**: `splash`, `login`, `home`, `recipe-list`, `recipe-detail`, `meal-planner`, `shopping-list`, `favorites`, `profile`, `settings`.
- **Navigation**: Bottom Tabs (Home, Search, Plan, Groceries, Profile). Detail uses tabs for Ingredients/Steps.
- **Data Model**: `Recipe { id, name, time, servings, calories, ingredients[{name, qty}], steps[] }`.
- **Transitions**: `recipe-list` → `recipe-detail` (slide-left), Grocery check (strikethrough animation).

## 6. Finance / Banking
- **Screens**: `splash`, `login-pin`, `dashboard`, `transactions`, `tx-detail`, `transfer`, `pay-bills`, `cards`, `notifications`, `settings`.
- **Navigation**: Bottom Tabs (Home, Payments, Cards, More). High-security feel, clean typography.
- **Data Model**: `Account { id, type, balance, lastDigits }`, `Transaction { id, amount, merchant, date, category, status }`.
- **Transitions**: `dashboard` → `transactions` (slide-left), `transfer` (slide-up), PIN entry (shake on error).

## 7. Task / Project Management
- **Screens**: `splash`, `login`, `dashboard`, `project-list`, `kanban-board`, `task-detail`, `create-task`, `calendar`, `team`, `notifications`.
- **Navigation**: Mobile: Bottom Tabs (Tasks, Projects, Calendar, Profile). Desktop: Persistent Sidebar.
- **Data Model**: `Task { id, projectId, title, status, assigneeId, dueDate, priority, description }`.
- **Transitions**: `project` → `board` (slide-left), `task-detail` (slide-right/drawer), Priority change (color-fade).

## 8. Messaging / Chat
- **Screens**: `splash`, `login`, `chat-list`, `chat-thread`, `group-info`, `new-chat`, `contacts`, `profile`, `settings`.
- **Navigation**: Bottom Tabs (Chats, Calls, Contacts, Settings). Header shows user status.
- **Data Model**: `Message { id, chatId, senderId, text, timestamp, isRead, type: 'text'|'image' }`.
- **Transitions**: `chat-list` → `chat-thread` (slide-left), Swipe message (reply-action).

## 9. Music / Podcast
- **Screens**: `splash`, `login`, `home`, `browse`, `playlist-detail`, `player-full`, `mini-player`, `library`, `queue`, `settings`.
- **Navigation**: Bottom Tabs (Home, Search, Library). Persistent Mini Player above tabs.
- **Data Model**: `Track { id, title, artist, album, duration, coverArt, url }`.
- **Transitions**: `mini-player` → `player-full` (slide-up), List → Detail (slide-left), Play/Pause (scale-pop).

## 10. Travel / Booking
- **Screens**: `splash`, `login`, `explore`, `search-results`, `listing-detail`, `booking-flow`, `my-bookings`, `booking-detail`, `reviews`, `profile`.
- **Navigation**: Bottom Tabs (Explore, Favorites, Bookings, Profile). Floating "Book Now" button on Detail.
- **Data Model**: `Listing { id, name, location, pricePerNight, rating, amenities[], images[] }`.
- **Transitions**: `explore` → `results` (slide-left), `listing-detail` (hero-expand), Booking steps (horizontal-slide).
