# Mock Data Plan — Influencer Dashboard

> **Date**: 2026-10-20
> **Status**: Proposed — awaiting approval before generating `data.js`
> **Companion docs**: `resources/profile.md` (persona/products), `resources/design-spec.md` (layout and section content); planning history in `archive/`

---

## 1. Purpose

This document defines **what data we generate**, **why each metric exists**, and **how we generate it deterministically** so that Phase 2 renderers can consume one `data.js` module and produce the three dashboard blocks. It closes rollout task **1.1** ("Define the mock data schema") and satisfies rule **B5**:

> *Mock data lives in exactly one `data.js` module. Renderers consume the module only; a future API swap changes one file. Define the schema (products, platforms, campaigns, KPI rollups) before writing renderers.*

---

## 2. Research Summary — What Influencers Actually Track

Sources fetched this session (sources that 403'd/404'd are recorded in `archive/memory-bank/changelog.md`; not blocking):

### 2.1 Core KPI categories (Influencer Marketing Hub — influencer marketing KPIs)
Influencer performance is tracked across six funnel categories, **top to bottom**:

| Funnel Stage | Metrics | Feeds Our Block |
|---|---|---|
| **Reach / Awareness** | Impressions, reach | Drivers (bars), Details (tables) |
| **Audience growth** | Followers, follower growth %, fake-follower risk | Drivers, Details |
| **Engagement** | Likes, comments, shares, saves; engagement rate = interactions ÷ reach | TOP KPI (engagement), Drivers |
| **Traffic / CTR** | Link clicks, CTR, UTM attribution | Drivers, Details (campaigns) |
| **Conversion** | Conversion rate, affiliate sales, referral links, discount codes | TOP KPI (volume), Drivers (funnel) |
| **ROI / Revenue** | ROI = (attributed revenue − cost) ÷ cost × 100; EMV; CLV; commissions | TOP KPI (revenue), Drivers (platform ROI) |

**Video/livestream KPIs** (YouTube, TikTok, Twitch): views, watch time, comments, shares, video completion rate (video platforms); average viewers, peak viewers, chat messages, stream count (live platforms).

**Benchmark**: the most commonly tracked metrics across the industry are **views, reach, impressions**.

### 2.2 Affiliate mechanics (Shopify — affiliate marketing)
- Attribution flow: **unique link → cookie/attribution window → conversion attributed → commission paid**. Windows vary (24h Safari ITP up to 30+ days).
- Payment models: **PPS/CPS**, **CPA**, PPI, PPC, recurring, hybrid.
- **Social commerce native affiliate**: TikTok Shop (in-app purchase), YouTube Shopping (click-through), Instagram affiliate tagging (relaunched late March 2026, Reels), Pinterest link.
- Realistic commission rates: Amazon 1–20% by category; Manduka 10%; EcoFlow 5%. Photoshop of cases: Moonboon ~10% of net sales, 6.5× ROI; Immi 432 ambassadors / $200K sales / 4,400 orders; Duradry 250 creators / $50K in 7 months, −29% CAC.
- Creator income mix: **ads 45%, social selling 32%, subscriptions 31%, affiliate 29%** (impact/Shopify 2025 survey).

### 2.3 Twitch-specific (IMH — Twitch stats)
- Platform scale: ~240M MAU, ~35M DAU, ~2.3M avg concurrent.
- Streamer monetization tiers: **Affiliate → Partner** (subs, Bits, ads, donations).
- Streamer dashboard-friendly metrics: followers, hours watched, avg viewers, peak viewers, **active-chat %** (top channels ~36%), stream count.
- Campaign example (Chobani): **7M impressions, 101.3K engagements, 80K stream views, 6.7K unique chat messages** — a realistic ballpark for a mid-size campaign.

### 2.4 X / Twitter (not yet fetched — optional)
X-specific metrics (impressions, link clicks, mentions, reposts, replies) are industry-standard but the fetch 403'd/redirected this session. They are represented in the schema below; a benchmark refetch is optional and **not blocking**.

---

## 3. Brainstorm — Many Ways an Influencer Could Have "Information to Track"

This is the exhaustive candidate list we generated before narrowing to the schema. The persona is a **mid-tier multi-platform creator** (tens of thousands of followers per platform) selling 3 affiliate products at **15% commission**, so we include the metrics a dashboard for *this* persona plausibly shows — not everything an enterprise brand tool would.

**Audience**
- Followers per platform (and total), follower growth % (period + trend)
- Demographics (age, gender, geo, device) — mostly a future per-platform detail page, **not shown in 3-block dashboard**
- Audience quality: fake-follower risk, verified %

**Reach & Attention**
- Impressions, reach, views (video), watch time, avg % watched, video completion rate
- Peak/average viewers (live), hours watched

**Engagement**
- Likes, comments, shares, saves, reposts, replies, mentions
- Chat messages / active-chat % (Twitch)
- Engagement rate = interactions ÷ reach (or ÷ impressions — we standardize on **reach**)

**Traffic & Attribution**
- Link clicks, CTR, UTM source/medium, referral breakdown, discount codes used

**Conversion**
- Conversions (orders), conversion rate (conversions ÷ clicks and/or ÷ reach), funnel steps, returns/refunds, cart/discount-driven uplift

**Revenue & ROI**
- Product revenue = units × price; commission = revenue × 15%
- Per-platform revenue/commission, ROI = (revenue − cost) ÷ cost, EMV, CLV (EMV/CLV → future, not first slice)

**Content cadence & Publishing**
- Posts/reels/videos/streams count, publishing frequency, best-performing post

**Campaigns & Promotions**
- Campaign budget, spend, impressions, clicks, CTR, conversions, revenue, ROI, attribution window
- Discount codes, UTM tags, promo partners

**Trust, Sentiment & Compliance**
- Sentiment score, brand mentions (future), FTC disclosure flag (boolean per post — nice to include, cheap)

**Alerts / Anomalies**
- Conversion drop, engagement spike, follower churn, refund-rate spike, campaign under-delivery

**Time-series**
- Monthly trends of revenue, commissions, engagement, followers per platform (feeds trend arrows + sparklines)

**What we deliberately leave OUT of the first slice** (noted so we can add later without redesign): demographics, sentiment, CLV/EMV, multi-touch attribution, refunds detail (keep a simple `refundRate` aggregate), paid ad spend split by platform. These would inflate the schema and blur the 10-second-orientation goal.

---

## 4. Recommended Schema for `data.js`

### 4.1 Load pattern (make an explicit decision)
The project-overview diagram shows `<script src="data.js">` — no build step. Two options:

| Option | How it loads |
|---|---|
| **A. Global object** | `data.js` defines `const DATA = {...}` → loaded with plain `<script src="data.js"></script>` **before** `app.js`. Renderers read `window.DATA`. Works file:// and http://. Oldest, most compatible. |
| **B. ES module** | `data.js` is `export const DATA = {...}` → loaded with `<script type="module" src="app.js"></script>` which imports it. Modern, file:// has CORS friction. |

**Recommendation: Option A (global `window.DATA`)** — matches the no-build, low-friction TANSTAAFL constraint; works when opened directly and behind any static host; one-file swap later means replacing `data.js` contents and keeping the same global name. If we later add a real API, `app.js` adapts a small `fetch` against the same `DATA` contract.

### 4.2 Top-level shape
```js
// data.js (generated output — do not hand-edit)
const DATA = {
  meta: {
    schemaVersion: "1.0",
    generatedAt: "2026-10-20",
    period: { start: "2026-01", end: "2026-10" },   // 10 months
    persona: "mid-tier multi-platform creator",
    currency: "USD",
    seed: 20261020,                                   // deterministic RNG seed
    generator: "scripts/generate-data.py"
  },
  products: [ ... ],      // 3 products (A $50, B $120, C $80)
  platforms: [ ... ],     // instagram, youtube, tiktok, x, twitch
  campaigns: [ ... ],     // 8–10 campaigns tying platform × product
  monthlySeries: [ ... ], // 10 months of rollups
  alerts: [ ... ],        // derived + hand-flagged anomalies
  derived: { ... }        // precomputed KPI rollups (see 4.6)
};
```

### 4.3 Products
**Ground truth from `resources/profile.md`** (never drift): A $50 · B $120 · C $80, commission **15%**.

```js
products: [
  { id: "prod-a", name: "Product A", price: 50,  commissionRate: 0.15, category: "lifestyle" },
  { id: "prod-b", name: "Product B", price: 120, commissionRate: 0.15, category: "premium"   },
  { id: "prod-c", name: "Product C", price: 80,  commissionRate: 0.15, category: "starter"   },
]
```
> `id`, `price`, `commissionRate` are **inputs**. Units sold, revenue, commission, conversion rate are **derived** and live in `derived` (4.6) or are computed by the generator and stored on the record (we'll store derived values on the product record too, precomputed, so renderers stay dumb).

**Product record (generator fills derived fields):**
```js
{
  id: "prod-a", name: "Product A", price: 50, commissionRate: 0.15,
  unitsSold: 3240,            // period total
  revenue: 162000,            // unitsSold × price
  commission: 24300,          // revenue × 0.15
  conversionRate: 2.8,        // conversions ÷ clicks (percent)
  platformShare: { instagram: 42, youtube: 31, tiktok: 18, x: 6, twitch: 3 } // % of units
}
```

### 4.4 Platforms
Five platforms with a **common core** and **platform-specific extensions** (each platform has its own tailored metrics — this is where research realism shows).

**Common core** (all platforms):
```js
{
  id: "instagram", name: "Instagram", type: "photo|video|short-video|micro-blog|live",
  followers: 42500, followersGrowthPct: 3.2,        // period growth
  reach: 620000, impressions: 910000,
  engagement: { likes: 31000, comments: 2400, shares: 6100, saves: 2900 },
  engagementRate: 6.8,        // (likes+comments+shares+saves) ÷ reach × 100
  linkClicks: 12400, ctr: 2.0, // clicks ÷ impressions × 100
  conversions: 320, conversionRate: 2.6,  // conversions ÷ clicks
  revenue: 24000, commission: 3600,
  roi: 4.1,                                   // (revenue − cost) ÷ cost
  trend: { followers: "+3.2%", engagementRate: "+0.4pt", revenue: "+12%" }
}
```

**Platform-specific extensions**:

| Platform | Extra fields (real from research) |
|---|---|
| **instagram** | `reelsCount`, `storiesCount`, `avgLikesPerReel`, `profileVisits` |
| **youtube** | `subscribers`, `videosCount`, `views`, `watchHours`, `avgViewDurationSec`, `completionRatePct`, `shortsCount`, `ctr` (as % of thumbnail shown) |
| **tiktok** | `postsCount`, `views`, `avgWatchTimeSec`, `completionRatePct`, `shareRatePct` (native social commerce: `shopListings`, `inAppPurchases`) |
| **x** | `impressions`, `linkClicks`, `mentions`, `reposts`, `replies`, `quotePosts`, `bookmarks` |
| **twitch** | `streamCount`, `avgViewers`, `peakViewers`, `hoursWatched`, `subs`, `bits`, `chatMessages`, `activeChatPct` (e.g. ~0.36), `followers` (channel), `donations` |

> **Note on `ctr`**: X/YouTube use link clicks ÷ impressions; Instagram uses profile visits ÷ reach. We record the *meaning* with the field. Renderers just display the stored number.

### 4.5 Campaigns
8–10 campaigns, each tying a platform to a product with full-funnel numbers + attribution window (realistic: 7D/30D; note Safari 24h caps).

```js
{
  id: "cmp-01", name: "Summer Reel Series — Product A",
  productId: "prod-a", platformId: "instagram",
  period: "2026-07",
  budget: 2000, spend: 1850,
  impressions: 420000, reach: 287000,
  linkClicks: 8400, ctr: 2.0,
  conversions: 231, conversionRate: 2.75,
  revenue: 11550, commission: 1732.5,
  roi: 5.2,                          // (revenue − spend) ÷ spend
  attributionWindowDays: 30,
  discountCode: "SUMMER50",
  utm: "ig-summer-a",
  labels: ["reels", "affiliate"]
}
```

### 4.6 Derived KPI rollups
`derived` holds the **four TOP KPI cards** and their deltas, precomputed so renderers never compute:

```js
derived: {
  totalCommission: 81900,      // Σ product commission (period)
  totalCommissionDeltaPct: 14.2, // vs previous period
  totalRevenue: 546000,
  totalRevenueDeltaPct: 11.0,
  topProduct: "prod-b",         // by revenue
  topPlatform: "youtube",       // by commission
  avgEngagementRate: 5.4,       // weighted by reach
  avgEngagementDeltaPct: 0.6,
  totalConversions: 13200,
  overallRoi: 4.8,
  unitsSold: 8100,
  // per-percent helper for bar charts
  platformRevenueShare: { instagram: 24, youtube: 38, tiktok: 26, x: 8, twitch: 4 },
  productRevenueShare:  { "prod-a": 30, "prod-b": 44, "prod-c": 26 }
}
```

### 4.7 MonthlySeries (feeds trend arrows + sparklines)
10 rows (2026-01 … 2026-10):
```js
{ month: "2026-07", revenue: 58400, commission: 8760, conversions: 1410,
  engagementRate: 5.1, followersTotal: 182400,
  perPlatform: { instagram: 42500, youtube: 61800, tiktok: 38500, x: 22400, twitch: 17200 } }
```

### 4.8 Alerts
Alerts are **explicit data**, not render-time surprises. Mix of anomalies the generator inserts (guaranteed ≥1 to demo the pattern) and realistic follow-ons:
```js
{
  id: "al-01",
  type: "conversion-drop",        // conversion-drop | engagement-spike | follower-churn | roi-alert | refund-spike
  severity: "high|medium|low",
  message: "Product C conversions dropped 31% MoM on TikTok",
  productId: "prod-c", platformId: "tiktok", month: "2026-10",
  actual: 2.1, threshold: 3.0     // percent
}
```

---

## 5. Generation Method

### 5.1 Recommendation: deterministic generator script

| Option | Pros | Cons | Verdict |
|---|---|---|---|
| **A. Hand-written static `data.js`** | Zero tooling; TANSTAAFL-simple | Hard to keep 10-month series + 5 platforms × 3 products self-consistent; error-prone arithmetic; not reproducible | ✗ too error-prone for the volume |
| **B. Generator script (recommended)** | Self-consistent by construction (rollups = sums of rows); seeded → reproducible; easy to regenerate bigger/smaller datasets; single source of truth for *shape* | One more dev tool (does not touch runtime) | **✓ Choose this** |

**Key point about "no build step"**: The `index.html` served by `server.py` loads the **committed static `data.js`** — we never run a build to serve the page. `scripts/generate-data.py` is a *dev-time* tool you run when you want to regenerate the mock; the committed output is plain JS. This does **not** conflict with the no-build rule.

### 5.2 Why Python + `random.Random(seed)`
- Deterministic: `random.Random(20261020)` gives identical output every run on the same Python version/machine — reproducible commits.
- Invariant checks built in: after generating, the script **asserts** rollup consistency (Σ platform revenue ≈ total revenue; Σ campaign revenue ≤ per-platform totals within rounding; commission = revenue × 0.15 for every product/row). If an invariant fails, the script exits non-zero — we never commit bad data.
- Reuses none of the runtime stack, so it can't affect page load.

> Alternative if we want to stay pure-JS: `scripts/generate-data.mjs` with a small `mulberry32` PRNG. Decision: **Python** — the repo already has a Python toolchain (`server.py`, `init.sh`), so a `scripts/` helper is natural. If the user prefers JS-only, swap is trivial (identical outputs modulo tiny float differences).

### 5.3 Anchor numbers / realism bounds
The generator clamps randomly-drawn values into realistic mid-tier influencer ranges (drawn from research):

| Input | Bound (per platform, period) | Research basis |
|---|---|---|
| Followers | 15K–80K | mid-tier creator; Sephora nano example 3.6K, ODEON 4K→100K growth |
| Follower growth / month | 1–8% | ~10% MoM seen as strong (Euroleague TikTok) |
| Engagement rate | 2–9% | industry 1–10%; micro-influencers higher |
| Impressions per follower | 8–25× | reach/impressions > followers for creators |
| CTR (link clicks ÷ impressions) | 0.5–4% | standard ecommerce CTR band |
| Conversion rate (conv ÷ clicks) | 0.5–5% | standard full-funnel conversion band |
| ROAS/ROI | 1.5–10× | Moonboon 6.5×, campaign examples |
| Commission | always revenue × 0.15 | persona ground truth |
| Campaign budget | $500–$5,000 | realistic mid-tier campaign spend |

### 5.4 Regeneration
```bash
# from repo root
python3 scripts/generate-data.py            # writes data.js (uses embedded seed; optional --seed override)
python3 scripts/generate-data.py --seed 42  # optional: regenerate a new dataset
```
The script prints the seed used and the invariant-check result. Committed `data.js` is reviewed like any other file.

---

## 6. Verification Tie-In (DoD)

Generated `data.js` must satisfy the verification gate (B4.5) and feed the Phase 2 smoke checks:

- [ ] `data.js` exists at repo root and **resolves** (HTTP 200 for `/data.js` in the smoke check / browser network tab)
- [ ] Renderers consume **only** `window.DATA` — no inline magic numbers (rule C-section DoD: *"Mock data consumed from the single data source (no inline magic numbers)"*)
- [ ] Schema matches `meta.schemaVersion`; generator's asserts pass before commit
- [ ] Numbers render sanely at 375 / 768 / 1024 (the Phase 2 screenshot loop) — no overflowing KPI cards, charts with data
- [ ] Every `platform.id` / `product.id` referenced in `campaigns`, `monthlySeries`, `alerts` exists in the source arrays (referential integrity — checked by generator)
- [ ] At least one alert is present so the Alerts block is never empty in the MVP

---

## 7. Open Questions for Approval

> **Status: ALL RESOLVED — Approved 2026-10-20** (client answered inline below).

1. **Load pattern**: go with **Option A (global `window.DATA`)** as recommended? (Alternative: ES module.)
- **option A** ✅
2. **Generator language**: **Python** (`scripts/generate-data.py`) as recommended, or JS (`generate-data.mjs`)?
- **python** ✅
3. **Derived-storage**: precompute derived rollups on records (recommended, keeps renderers dumb) vs. compute in `app.js`? (Recommend: **precompute** — matches "renderers consume only".)
- **precompute** ✅
4. **Campaign count**: generate **8–10 campaigns** by default (I propose 10). Good?
- **seems fine → 10** ✅
5. **Category**: should products carry a `category` label (lifestyle/premium/starter) or stay generic Product A/B/C? (Nice cosmetic touch, cheap.)
- **give them categories** ✅
6. **Time span**: 10 months (2026-01 → 10) OK for trend arrows + sparklines?
- **sounds good** ✅

**Delivery summary (2026-10-20)**: (a) `scripts/generate-data.py` added ✅, (b) `data.js` generated (19 KB→16.7 KB after cleanup) ✅, (c) generator's invariant checks all **PASS** ✅, (d) handed off to Phase 2 tooling tasks ✅. Determined deterministic: same seed → byte-identical `data.js`.