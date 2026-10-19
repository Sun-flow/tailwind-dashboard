# Client Profile: Influencer Dashboard

> **Date**: 2026-10-19  
> **Purpose**: User persona for the Tailwind CSS dashboard — defines who we're building for and what they need.

---

## Background

Our client is a **multi-platform influencer** who promotes products across several social media accounts. They currently lack a unified view of their earnings, ad performance, and audience engagement — data is scattered across platform analytics dashboards, spreadsheets, and manual notes.

They need a **single reporting dashboard** that consolidates income, revenue, and engagement metrics so they can make data-driven decisions about content, ad spend, and product promotion.

---

## Platforms

| Platform | Type | Notes |
|---|---|
| Instagram | Photos / Stories / Reels | Likely a primary engagement driver |
| YouTube | Long-form & Shorts video | Revenue from ad sense + promoted links |
| TikTok | Short-form video | High viral potential, growing audience |
| Twitter / X | Micro-blogging | Community engagement, link sharing |
| Twitch.tv | Live streaming | Real-time interaction, subscriptions |

---

## Products Promoted

The client promotes **3 products** with a **15% commission** on sales generated through their affiliate links.

| Product | Price | Commission (15%) |
|---|---|---|
| Product A | $50.00 | $7.50 |
| Product B | $120.00 | $18.00 |
| Product C | $80.00 | $12.00 |

---

## Goals & Key Questions

The dashboard must answer these questions at a glance:

| Goal | Metric / KPI |
|---|---|
| 💰 **How much commission am I earning?** | Total commissions = units sold × price × 15%, broken out by product and platform |
| 📦 **Which products are generating the most revenue?** | Product-level revenue ranking (units sold × price) |
| 📈 **How well are my ads converting?** | Conversion rate = conversions ÷ reach, per platform and per product |
| 🏆 **Which platforms generate the best return?** | Return = (revenue generated − costs) per platform; ROI ratio |
| ❤️ **What is the engagement rate by platform and by product?** | Engagement rate = (likes + comments + shares) ÷ impressions, split by platform and product post |

---

## Desired Deliverables

1. **Dashboard page** (`index.html`) — single-page responsive dashboard styled with Tailwind CSS v4
2. **KPI cards** — top-level summary of total commissions, top product, top platform, overall engagement rate
3. **Product breakdown** — per-product revenue, units sold, commission earned
4. **Platform breakdown** — per-platform metrics (followers, engagement, revenue, ROI)
5. **Conversion table** — ad conversion rates by product × platform
6. **Mock data** — embedded JSON or static JS data to drive the dashboard
7. **Charts / visual indicators** — lightweight, no heavy charting library (CSS bars, simple Canvas, or SVG)

---

## Constraints & Preferences

- **Budget**: Solo developer / bootstrap (no paid services)
- **Timeline**: Iterative — working prototype first, polish later
- **Tech**: Tailwind CSS v4 via CDN, vanilla JavaScript, Flask dev server
- **Data**: Mock/static initially; real API integration is a future goal
- **Design**: Clean, dashboard-style, responsive (mobile-first), dark or light mode optional

---

## Persona Snapshot

> *"I have numbers scattered across 5 platforms and 3 products. I need one place where I can see what's working, what's not, and where to focus my time."*