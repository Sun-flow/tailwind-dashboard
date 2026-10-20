#!/usr/bin/env python3
"""
Mock data generator for the Tailwind influencer dashboard.

Writes a single static `data.js` module that exposes `window.DATA` — the global
object renderers consume (no build step; the committed file is what the page
serves). Deterministic and seeded: same seed -> byte-identical output. The
script enforces internal invariants (rollups == sums of rows, commission ==
revenue x 0.15, referential integrity) and exits non-zero on any failure so we
never commit bad data.

Schema v1.0 contract lives in resources/mock-data-plan.md (§4).
Decisions (2026-10-20, user-approved): global window.DATA · Python generator ·
precomputed derived rollups · 10 campaigns · product categories · 10 months.

Usage:
    python3 scripts/generate-data.py                # writes ../data.js (seed 20261020)
    python3 scripts/generate-data.py --seed 42      # optional alternate dataset
    python3 scripts/generate-data.py --out /tmp/data.js
"""

from __future__ import annotations

import argparse
import json
import math
import os
import random
import string
import sys

COMMISSION_RATE = 0.15
SEED_DEFAULT = 20261020

PRODUCTS = [
    {"id": "prod-a", "name": "Product A", "price": 50, "category": "lifestyle"},
    {"id": "prod-b", "name": "Product B", "price": 120, "category": "premium"},
    {"id": "prod-c", "name": "Product C", "price": 80, "category": "starter"},
]
PRODUCT_BY_ID = {p["id"]: p for p in PRODUCTS}

# Common + platform-specific config. `actions` are engagement action buckets.
# `window_days` echoes real attribution windows (Safari ITP caps at 24h/1 day,
# typical programs run 7-30 days).
PLATFORM_CONFIG = [
    {"id": "instagram", "name": "Instagram", "type": "photo",
     "actions": [("likes", 0.62), ("comments", 0.05), ("shares", 0.18), ("saves", 0.15)],
     "tag": "reels", "window_days": 30,
     "impressions_per_f": (8, 20), "reach_rate": (0.55, 0.75), "er_range": (2.0, 9.0)},
    {"id": "youtube", "name": "YouTube", "type": "video",
     "actions": [("likes", 0.74), ("comments", 0.13), ("shares", 0.13)],
     "tag": "shorts", "window_days": 30,
     "impressions_per_f": (8, 20), "reach_rate": (0.5, 0.7), "er_range": (2.0, 8.0)},
    {"id": "tiktok", "name": "TikTok", "type": "short-video",
     "actions": [("likes", 0.66), ("comments", 0.04), ("shares", 0.20), ("saves", 0.10)],
     "tag": "shop", "window_days": 7,
     "impressions_per_f": (18, 25), "reach_rate": (0.60, 0.85), "er_range": (3.0, 10.0)},
    {"id": "x", "name": "X / Twitter", "type": "micro-blog",
     "actions": [("likes", 0.50), ("reposts", 0.12), ("replies", 0.08), ("bookmarks", 0.18), ("mentions", 0.12)],
     "tag": "thread", "window_days": 7,
     "impressions_per_f": (8, 18), "reach_rate": (0.50, 0.70), "er_range": (1.5, 7.0)},
    {"id": "twitch", "name": "Twitch", "type": "live",
     "actions": [],  # engagement modelled via chatMessages
     "tag": "live", "window_days": 30,
     "impressions_per_f": (1.2, 3.5), "reach_rate": (0.60, 0.80), "er_range": (1.0, 4.5)},
]
PLATFORM_BY_ID = {c["id"]: c for c in PLATFORM_CONFIG}

MONTHS = [f"2026-{m:02d}" for m in range(1, 11)]  # 2026-01 .. 2026-10


# --------------------------------------------------------------------------
# JS rendering helpers (tidy output, no float noise)
# --------------------------------------------------------------------------

def js_number(x) -> str:
    if isinstance(x, bool):
        return "true" if x else "false"
    if isinstance(x, int):
        return str(x)
    if isinstance(x, float) and math.isfinite(x):
        if x.is_integer() and abs(x) < 1e15:
            return str(int(x))
        return f"{x:.4f}".rstrip("0").rstrip(".")
    raise ValueError(f"cannot render number: {x!r}")


def render_value(value, level: int) -> str:
    pad = "  " * level
    if isinstance(value, dict):
        if not value:
            return "{}"
        parts = ["{"]
        for k, v in value.items():
            parts.append(f"{pad}  {json.dumps(k, ensure_ascii=False)}: {render_value(v, level + 1)},")
        parts.append(pad + "}")
        return "\n".join(parts)
    if isinstance(value, list):
        if not value:
            return "[]"
        if all(isinstance(x, (int, float, str)) and not isinstance(x, bool) for x in value):
            return "[" + ", ".join(render_value(x, level) for x in value) + "]"
        parts = ["["]
        for v in value:
            parts.append(f"{pad}  {render_value(v, level + 1)},")
        parts.append(pad + "]")
        return "\n".join(parts)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return js_number(value)
    if value is None:
        return "null"
    raise ValueError(f"cannot render: {value!r}")


def render_data(data: dict) -> str:
    header = (
        "/*\n"
        " * data.js - Mock data module for the influencer dashboard.\n"
        " * GENERATED FILE - do not hand-edit. Regenerate with:\n"
        " *   python3 scripts/generate-data.py\n"
        " * Schema v1.0 - see resources/mock-data-plan.md\n"
        " */\n"
    )
    return header + "\nwindow.DATA = " + render_value(data, 0) + ";\n"


# --------------------------------------------------------------------------
# Build steps
# --------------------------------------------------------------------------

def audience_metrics(cfg: dict, rng: random.Random) -> dict:
    """Funnel top half: followers, reach, impressions, engagement, clicks, conversions."""
    if cfg["id"] == "twitch":
        start_f = rng.randint(6000, 22000)
    else:
        start_f = rng.randint(15000, 80000)
    growth = rng.uniform(8.0, 45.0)                      # total period growth %
    end_f = int(start_f * (1 + growth / 100))

    avg_f = (start_f + end_f) / 2
    impressions = int(avg_f * rng.uniform(*cfg["impressions_per_f"]))
    reach = int(impressions * rng.uniform(*cfg["reach_rate"]))
    er = rng.uniform(*cfg["er_range"])

    # engagement action split (per-platform buckets; twitch = chatMessages)
    if cfg["id"] == "twitch":
        engagement = {"chatMessages": int(reach * er / 100)}
    else:
        totals = int(reach * er / 100)
        weights = [w * rng.uniform(0.7, 1.3) for _, w in cfg["actions"]]
        wsum = sum(weights)
        values = [int(totals * x / wsum) for x in weights]
        values[0] += totals - sum(values)                # absorb rounding diff
        engagement = {name: values[i] for i, (name, _) in enumerate(cfg["actions"])}

    # funnel bottom: impressions -> clicks -> conversions (1 unit per order)
    link_clicks = max(1, int(impressions * rng.uniform(0.7, 3.5) / 100))
    conversions = max(1, int(link_clicks * rng.uniform(1.0, 6.0) / 100))
    ctr = link_clicks / impressions * 100
    conv_rate = conversions / link_clicks * 100

    return {
        "start_f": start_f, "end_f": end_f, "growth": growth,
        "impressions": impressions, "reach": reach, "er": er,
        "engagement": engagement, "link_clicks": link_clicks, "conversions": conversions,
        "ctr": ctr, "conv_rate": conv_rate,
    }


def monthly_followers(meta_aud: dict) -> list:
    """Interpolate start->end follower counts across the 10 months."""
    start, end = meta_aud["start_f"], meta_aud["end_f"]
    ratio = (end / start) ** (1 / (len(MONTHS) - 1)) if start else 1.0
    return [round(start * (ratio ** m)) for m in range(len(MONTHS))]


def build(rng: random.Random, seed: int) -> dict:
    data = {
        "meta": {
            "schemaVersion": "1.0",
            "generatedAt": "2026-10-20",
            "period": {"start": MONTHS[0], "end": MONTHS[-1]},
            "persona": "mid-tier multi-platform creator",
            "currency": "USD",
            "seed": seed,
            "generator": "scripts/generate-data.py",
        },
        "products": [],
        "platforms": [],
        "campaigns": [],
        "monthlySeries": [],
        "alerts": [],
        "derived": {},
    }

    # ---- 1. platform audience + funnel totals -----------------------------
    aud = {c["id"]: audience_metrics(c, rng) for c in PLATFORM_CONFIG}

    # ---- 2. distribute each platform's conversions across products --------
    # units[p][pl] = conversions attributed to (product, platform); price-weighted
    # split uses per-platform product affinity noise so mixes vary by channel.
    units: dict = {p["id"]: {c["id"]: 0 for c in PLATFORM_CONFIG} for p in PRODUCTS}
    unit_share = {c["id"]: {} for c in PLATFORM_CONFIG}     # product share per platform

    for cfg in PLATFORM_CONFIG:
        pl_id = cfg["id"]
        conversions = aud[pl_id]["conversions"]
        # base affinity: cheaper products convert more on social
        raw = {p["id"]: (50 / p["price"]) * rng.uniform(0.6, 1.5) for p in PRODUCTS}
        s = sum(raw.values())
        frac = {pid: raw[pid] / s for pid in raw}
        # deterministic-ish assignment of exact integer units
        allotted = [int(conversions * frac[pid]) for pid in raw]
        allotted[-1] += conversions - sum(allotted)          # fix rounding
        for i, p in enumerate(PRODUCTS):
            units[p["id"]][pl_id] = allotted[i]
            unit_share[pl_id][p["id"]] = allotted[i] / conversions if conversions else 0

    # ---- 3. products (inputs + precomputed derived field) ------------------
    for p in PRODUCTS:
        units_sold = sum(units[p["id"]].values())
        revenue = units_sold * p["price"]
        prod_clicks = 0
        for cfg in PLATFORM_CONFIG:
            prod_clicks += int(aud[cfg["id"]]["link_clicks"] * unit_share[cfg["id"]].get(p["id"], 0))
        conv_rate = (units_sold / prod_clicks * 100) if prod_clicks else 0.0
        share = {c["id"]: round(units[p["id"]][c["id"]] / units_sold * 100, 1) if units_sold else 0
                 for c in PLATFORM_CONFIG}
        data["products"].append({
            "id": p["id"], "name": p["name"], "price": p["price"],
            "commissionRate": COMMISSION_RATE, "category": p["category"],
            "unitsSold": units_sold,
            "revenue": revenue,
            "commission": round(revenue * COMMISSION_RATE, 2),
            "conversionRate": round(conv_rate, 2),
            "platformShare": share,
        })

    # ---- 4. platforms (audience + funnel + revenue + roi + trend) ----------
    platform_revenue = {}
    platform_commission = {}
    platform_cost = {}

    # platform cost derived from a plausible ROI so roi stats are realistic
    for cfg in PLATFORM_CONFIG:
        pl_id = cfg["id"]
        rev = sum(units[p["id"]][pl_id] * PRODUCT_BY_ID[p["id"]]["price"] for p in PRODUCTS)
        platform_revenue[pl_id] = rev
        platform_commission[pl_id] = round(rev * COMMISSION_RATE, 2)
        roi_target = rng.uniform(1.5, 8.0)
        if pl_id == "x":
            roi_target = rng.uniform(0.8, 3.5)
        cost = rev / (roi_target + 1)
        platform_cost[pl_id] = round(cost, 2)
        roi = round((rev - cost) / cost, 2) if cost else 0.0

        a = aud[pl_id]
        monthly_f = monthly_followers(a)
        # X dips in the final month (follower-churn alert story)
        if pl_id == "x":
            monthly_f[-1] = int(monthly_f[-2] * 0.985)
            monthly_f[-2] = int(monthly_f[-2] * 0.99)

        # extension fields (research-driven per-platform metrics)
        ext = {}
        er_last = round(a["er"], 2)
        er_prev = round(a["er"] * rng.uniform(0.85, 1.02), 2)
        rev_last = None  # set below from monthly series

        data["platforms"].append({
            "id": pl_id, "name": cfg["name"], "type": cfg["type"],
            "followers": monthly_f[-1],
            "followersGrowthPct": round((monthly_f[-1] / a["start_f"] - 1) * 100, 1),
            "reach": a["reach"], "impressions": a["impressions"],
            "engagement": a["engagement"],
            "engagementRate": er_last,
            "linkClicks": a["link_clicks"], "ctr": round(a["ctr"], 2),
            "conversions": a["conversions"], "conversionRate": round(a["conv_rate"], 2),
            "revenue": rev, "commission": round(rev * COMMISSION_RATE, 2),
            "roi": roi,
            "trend": {
                "followers": f"{round((monthly_f[-1] / a['start_f'] - 1) * 100, 1):+.1f}%",
                "engagementRate": f"{round(er_last - er_prev, 1):+.1f}pt",
                "revenue": "+0.0%",  # filled after monthly series
            },
            # platform-specific extensions ---------------------------------
            "_ext": ext, "_aud": a, "_mth_f": monthly_f,
        })

    # ---- 5. campaigns (10 = 2 per platform, tied to a product) -------------
    campaigns = []
    low_roi_campaign = None
    for cfg in PLATFORM_CONFIG:
        pl_id = cfg["id"]
        cost = platform_cost[pl_id]
        # split platform cost between its two campaigns
        splits = [rng.uniform(0.42, 0.58), rng.uniform(0.42, 0.58)]
        ss = sum(splits)
        spends = [round(cost * x / ss, 2) for x in splits]
        spends[-1] += round(cost - sum(spends), 2)
        for idx in range(2):
            product = rng.choice(PRODUCTS)
            period = rng.choice(MONTHS[2:])
            spend = spends[idx]
            roi_c = rng.uniform(cfg and pl_id and (platform_revenue[pl_id] / cost - 1) * 0.8,
                                (platform_revenue[pl_id] / cost - 1) * 1.15)
            # one guaranteed under-delivering campaign (drives roi-alert)
            if low_roi_campaign is None and rng.random() < 0.5:
                roi_c = rng.uniform(0.8, 1.4)
            if len(campaigns) == 0 and low_roi_campaign is None:
                roi_c = rng.uniform(0.8, 1.4)       # deterministic: first campaign
            revenue_c = round(spend * (roi_c + 1), 2)

            name = f"{cfg['name']} {cfg['tag'].title()} - {product['name']}"
            if idx == 0:
                name = f"{period} {cfg['tag'].title()} Push - {product['name']}"
            campaign = {
                "id": f"cmp-{len(campaigns) + 1:02d}",
                "name": name,
                "productId": product["id"],
                "platformId": pl_id,
                "period": period,
                "budget": round(spend * rng.uniform(1.05, 1.3), 2),
                "spend": spend,
                "attributionWindowDays": cfg["window_days"],
                "discountCode": "".join(rng.choice(string.ascii_uppercase) for _ in range(3)) + str(rng.randint(10, 30)),
                "utm": f"{pl_id}-{product['id']}-{period[-2:]}-{rng.randint(1, 99)}",
                "labels": [cfg["tag"], "affiliate"],
                "_rev": revenue_c, "_roi": roi_c,
            }
            campaigns.append(campaign)
            if low_roi_campaign is None and roi_c < 1.5:
                low_roi_campaign = campaign

    # campaign funnel must stay consistent with spend/roi and within platform totals
    for cfg in PLATFORM_CONFIG:
        pl_id = cfg["id"]
        plat_campaigns = [c for c in campaigns if c["platformId"] == pl_id]
        # scale campaign revenues down if they exceed the platform's revenue
        total_rev = sum(c["_rev"] for c in plat_campaigns)
        if total_rev > platform_revenue[pl_id] > 0:
            factor = platform_revenue[pl_id] / total_rev
            for c in plat_campaigns:
                c["_rev"] = round(c["_rev"] * factor, 2)
                c["_roi"] = round(c["_rev"] / c["spend"] - 1, 2) if c["spend"] else 0.0
        for c in plat_campaigns:
            price = PRODUCT_BY_ID[c["productId"]]["price"]
            conversions_c = max(1, int(c["_rev"] / price))
            conversions_c = min(conversions_c, aud[pl_id]["conversions"])
            rev_c = conversions_c * price                      # keep int-multiple of price
            rev_c = min(rev_c, platform_revenue[pl_id])
            conv_rate_c = rng.uniform(1.0, 6.0)
            clicks_c = max(1, int(conversions_c / (conv_rate_c / 100)))
            ctr_c = rng.uniform(0.8, 3.2)
            impressions_c = max(1, int(clicks_c / (ctr_c / 100)))
            reach_c = int(impressions_c * rng.uniform(0.55, 0.8))
            c.update({
                "impressions": impressions_c,
                "reach": reach_c,
                "linkClicks": clicks_c,
                "ctr": round(clicks_c / impressions_c * 100, 2),
                "conversions": conversions_c,
                "conversionRate": round(conversions_c / clicks_c * 100, 2),
                "revenue": rev_c,
                "commission": round(rev_c * COMMISSION_RATE, 2),
                "roi": round((rev_c - c["spend"]) / c["spend"], 2) if c["spend"] else 0.0,
            })

    data["campaigns"] = [{k: v for k, v in c.items() if not k.startswith("_")} for c in campaigns]

    # ---- 6. monthly series (sums to platform/period totals) ----------------
    weights_by_platform = {}
    for cfg in PLATFORM_CONFIG:
        pl_id = cfg["id"]
        w = [0.72 * (1 + 0.06 * m) * rng.uniform(0.85, 1.15) for m in range(len(MONTHS))]
        w[-1] *= rng.uniform(1.05, 1.3)                      # growth month
        ws = sum(w)
        weights_by_platform[pl_id] = [x / ws for x in w]

    monthly = [{k: 0.0 for k in ("revenue", "commission", "conversions", "followersTotal")}
               for _ in MONTHS]
    for m in range(len(MONTHS)):
        monthly[m]["perPlatform"] = {}
        for cfg in PLATFORM_CONFIG:
            pl_id = cfg["id"]
            w = weights_by_platform[pl_id][m]
            monthly[m]["revenue"] += platform_revenue[pl_id] * w
            monthly[m]["commission"] += platform_commission[pl_id] * w
            monthly[m]["conversions"] += aud[pl_id]["conversions"] * w
    # blended engagement rate (reach-weighted) + follower totals
    for m in range(len(MONTHS)):
        rev = monthly[m]["revenue"]
        monthly[m]["revenue"] = round(rev, 2)
        monthly[m]["commission"] = round(monthly[m]["commission"], 2)
        monthly[m]["conversions"] = round(monthly[m]["conversions"], 0)
        er_num = 0.0
        er_den = 0
        f_tot = 0
        for cfg in PLATFORM_CONFIG:
            pl_id = cfg["id"]
            mf = [p["_mth_f"] for p in data["platforms"] if p["id"] == pl_id][0]
            followers_at = mf[m]
            f_tot += followers_at
            er_adj = aud[pl_id]["er"] * (0.9 + 0.02 * m) * rng.uniform(0.9, 1.1)
            er_num += er_adj * aud[pl_id]["reach"]
            er_den += aud[pl_id]["reach"]
            monthly[m]["perPlatform"][pl_id] = followers_at
        monthly[m]["followersTotal"] = int(f_tot)
        monthly[m]["engagementRate"] = round(er_num / er_den, 2) if er_den else 0.0
        monthly[m]["month"] = MONTHS[m]

    data["monthlySeries"] = monthly

    # fill per-platform revenue trend strings from the monthly series
    for p in data["platforms"]:
        pl_id = p["id"]
        last = [m for m in monthly if m["month"] == MONTHS[-1]][0]
        prev = [m for m in monthly if m["month"] == MONTHS[-2]][0]
        delta = (last["perPlatform"][pl_id] / prev["perPlatform"][pl_id] - 1) * 100 if prev["perPlatform"][pl_id] else 0
        p["trend"]["revenue"] = f"{delta:+.1f}%"

    # ---- 7. derived rollups (precomputed — renderers stay dumb) ------------
    total_revenue = sum(platform_revenue.values())
    total_commission = round(total_revenue * COMMISSION_RATE, 2)
    total_units = sum(p["unitsSold"] for p in data["products"])
    total_cost = sum(platform_cost.values())
    er_num = sum(aud[c["id"]]["er"] * aud[c["id"]]["reach"] for c in PLATFORM_CONFIG)
    er_den = sum(aud[c["id"]]["reach"] for c in PLATFORM_CONFIG)
    overall_roi = round((total_revenue - total_cost) / total_cost, 2) if total_cost else 0.0

    total_impressions = sum(p["impressions"] for p in data["platforms"])
    total_clicks = sum(p["linkClicks"] for p in data["platforms"])
    total_conversions = sum(p["conversions"] for p in data["platforms"])

    last = monthly[-1]
    prev = monthly[-2]
    def mom(cur, prev_) -> float:
        if prev_ == 0:
            return 0.0
        return (cur - prev_) / prev_ * 100

    data["derived"] = {
        "totalCommission": total_commission,
        "totalCommissionDeltaPct": round(mom(last["commission"], prev["commission"]), 1),
        "totalRevenue": round(total_revenue, 2),
        "totalRevenueDeltaPct": round(mom(last["revenue"], prev["revenue"]), 1),
        "topProduct": max(data["products"], key=lambda x: x["revenue"])["id"],
        "topPlatform": max(data["platforms"], key=lambda x: x["commission"])["id"],
        "avgEngagementRate": round(er_num / er_den, 2),
        "avgEngagementDeltaPct": round(last["engagementRate"] - prev["engagementRate"], 1),
        "totalConversions": int(sum(aud[c["id"]]["conversions"] for c in PLATFORM_CONFIG)),
        "overallRoi": overall_roi,
        "unitsSold": total_units,
        "unitsSoldDeltaPct": round(mom(last["conversions"], prev["conversions"]), 1),
        "totalImpressions": total_impressions,
        "totalLinkClicks": total_clicks,
        "overallCtr": round(total_clicks / total_impressions * 100, 2) if total_impressions else 0.0,
        "overallConversionRate": round(total_conversions / total_clicks * 100, 2) if total_clicks else 0.0,
        "platformRevenueShare": {pl_id: round(platform_revenue[pl_id] / total_revenue * 100, 1)
                                 for pl_id in platform_revenue},
        "productRevenueShare": {p["id"]: round(p["revenue"] / total_revenue * 100, 1)
                                for p in data["products"]},
    }

    # ---- 8. alerts (explicit data; >=1 guaranteed, referential integrity) ---
    data["alerts"] = [
        {
            "id": "al-01", "type": "conversion-drop", "severity": "high",
            "message": f"Product C conversions dropped 31% month-over-month on TikTok",
            "productId": "prod-c", "platformId": "tiktok", "month": "2026-10",
            "actual": 2.1, "threshold": 3.0,
        },
        {
            "id": "al-02", "type": "engagement-spike", "severity": "medium",
            "message": f"TikTok engagement spiked +140% (viral Reel) - verify shop link promoted",
            "platformId": "tiktok", "month": "2026-10",
            "actual": 9.8, "threshold": 6.0,
        },
        {
            "id": "al-03", "type": "follower-churn", "severity": "medium",
            "message": f"X followers dipped {round((1 - 0.985) * 100, 1):.0f}% this month - possible audit purge",
            "platformId": "x", "month": "2026-10",
            "actual": -1.5, "threshold": 0.0,
        },
    ]
    if low_roi_campaign is not None:
        data["alerts"].append({
            "id": "al-04", "type": "roi-alert", "severity": "low",
            "message": f"{low_roi_campaign['name']} under-delivered (ROI {low_roi_campaign['_roi']:.1f}x) - review offer",
            "campaignId": low_roi_campaign["id"], "month": low_roi_campaign["period"],
            "actual": round(low_roi_campaign["_roi"], 1), "threshold": 1.5,
        })
    data["alerts"] = data["alerts"]

    # strip private keys and rebuild clean public records
    for p in data["platforms"]:
        p.update({k: v for k, v in _platform_extensions(p, aud, rng).items()})
        for k in list(p.keys()):
            if k.startswith("_"):
                del p[k]

    return data


def _platform_extensions(platform: dict, aud: dict, rng: random.Random) -> dict:
    """Per-platform metric extensions (schema §4.4)."""
    pl_id = platform["id"]
    a = aud[pl_id]
    f = platform["followers"]
    if pl_id == "instagram":
        return {
            "reelsCount": rng.randint(20, 60),
            "storiesCount": rng.randint(120, 300),
            "avgLikesPerReel": rng.randint(600, 3000),
            "profileVisits": int(a["reach"] * rng.uniform(0.06, 0.12)),
        }
    if pl_id == "youtube":
        return {
            "subscribers": f,
            "videosCount": rng.randint(40, 120),
            "views": a["impressions"],
            "watchHours": int(a["impressions"] * rng.uniform(0.25, 0.5) * rng.uniform(0.2, 0.4)),
            "avgViewDurationSec": rng.randint(180, 480),
            "completionRatePct": round(rng.uniform(30, 60), 1),
            "shortsCount": rng.randint(30, 80),
            "ctr": round(a["ctr"], 2),
        }
    if pl_id == "tiktok":
        return {
            "postsCount": rng.randint(60, 150),
            "views": a["impressions"],
            "avgWatchTimeSec": rng.randint(12, 30),
            "completionRatePct": round(rng.uniform(20, 50), 1),
            "shareRatePct": round(rng.uniform(0.5, 3.5), 2),
            "shopListings": rng.randint(5, 15),
            "inAppPurchases": int(a["conversions"] * rng.uniform(0.5, 0.8)),
        }
    if pl_id == "x":
        return {
            "impressions": a["impressions"],
            "linkClicks": a["link_clicks"],
            "mentions": rng.randint(400, 2000),
            "reposts": rng.randint(1500, 8000),
            "replies": rng.randint(1200, 6000),
            "quotePosts": rng.randint(200, 900),
            "bookmarks": rng.randint(3000, 15000),
        }
    if pl_id == "twitch":
        stream_count = rng.randint(30, 80)
        avg_viewers = rng.randint(40, 220)
        return {
            "streamCount": stream_count,
            "avgViewers": avg_viewers,
            "peakViewers": int(avg_viewers * rng.uniform(3, 6)),
            "hoursWatched": int(avg_viewers * stream_count * rng.uniform(2, 4)),
            "subs": int(f * rng.uniform(0.005, 0.015)),
            "bits": int(f * rng.uniform(0.04, 0.09)),
            "chatMessages": a["engagement"].get("chatMessages", 0),
            "activeChatPct": round(rng.uniform(20, 40), 1),
            "followers": f,
            "donations": int(f * rng.uniform(0.5, 0.9)),
        }
    return {}


# --------------------------------------------------------------------------
# Invariants (fail loudly -> never commit bad data)
# --------------------------------------------------------------------------

def run_invariants(data: dict) -> bool:
    ok = True
    problems = []

    def check(cond, label):
        nonlocal ok
        status = "PASS" if cond else "FAIL"
        if not cond:
            ok = False
            problems.append(label)
        print(f"  [{status}] {label}")

    eps = 0.02
    pl_by_id = {p["id"]: p for p in data["platforms"]}
    prod_by_id = {p["id"]: p for p in data["products"]}

    print("\nInvariant checks:")
    # 1. commission == revenue * 0.15, per product and platform
    for p in data["products"]:
        check(abs(p["commission"] - round(p["revenue"] * COMMISSION_RATE, 2)) <= eps,
              f"product {p['id']} commission = revenue x {COMMISSION_RATE}")
        check(p["unitsSold"] > 0 and p["revenue"] == p["unitsSold"] * p["price"],
              f"product {p['id']} revenue = units x price")
        check(abs(sum(p["platformShare"].values()) - 100) < 1.0,
              f"product {p['id']} platformShare sums to 100")
    for p in data["platforms"]:
        check(abs(p["commission"] - round(p["revenue"] * COMMISSION_RATE, 2)) <= eps,
              f"platform {p['id']} commission = revenue x {COMMISSION_RATE}")
    # 2. rollups == rows
    prod_rev = sum(p["revenue"] for p in data["products"])
    plat_rev = sum(p["revenue"] for p in data["platforms"])
    check(abs(prod_rev - plat_rev) <= eps, "total revenue: products == platforms")
    check(abs(data["derived"]["totalRevenue"] - prod_rev) <= eps, "derived.totalRevenue == rows")
    check(abs(data["derived"]["totalCommission"] - sum(p["commission"] for p in data["products"])) <= eps,
          "derived.totalCommission == rows")
    check(abs(data["derived"]["unitsSold"] - sum(p["unitsSold"] for p in data["products"])) <= eps,
          "derived.unitsSold == rows")
    check(abs(data["derived"]["totalConversions"] - sum(p["conversions"] for p in data["platforms"])) <= eps,
          "derived.totalConversions == platform conversions")
    # 3. monthly series sums to period totals
    m_rev = sum(m["revenue"] for m in data["monthlySeries"])
    m_comm = sum(m["commission"] for m in data["monthlySeries"])
    m_conv = sum(m["conversions"] for m in data["monthlySeries"])
    check(abs(m_rev - prod_rev) <= max(eps, prod_rev * 0.01), "monthly revenue sums to total")
    check(abs(m_comm - data["derived"]["totalCommission"]) <= max(eps, prod_rev * 0.01),
          "monthly commission sums to total")
    check(abs(m_conv - data["derived"]["totalConversions"]) <= max(1, data["derived"]["totalConversions"] * 0.01),
          "monthly conversions sum to total")
    # 4. referential integrity
    for c in data["campaigns"]:
        check(c["productId"] in prod_by_id, f"campaign {c['id']} product ref ok")
        check(c["platformId"] in pl_by_id, f"campaign {c['id']} platform ref ok")
        check(c["revenue"] <= pl_by_id[c["platformId"]]["revenue"] + eps,
              f"campaign {c['id']} revenue <= platform revenue")
        check(c["conversions"] <= pl_by_id[c["platformId"]]["conversions"],
              f"campaign {c['id']} conversions <= platform conversions")
    for m in data["monthlySeries"]:
        check(set(m["perPlatform"].keys()) == set(pl_by_id.keys()), "monthly perPlatform keys valid")
    for al in data["alerts"]:
        if "productId" in al:
            check(al["productId"] in prod_by_id, f"alert {al['id']} product ref ok")
        if "platformId" in al:
            check(al["platformId"] in pl_by_id, f"alert {al['id']} platform ref ok")
        if "campaignId" in al:
            check(any(c["id"] == al["campaignId"] for c in data["campaigns"]), f"alert {al['id']} campaign ref ok")
    check(len(data["alerts"]) >= 1, "at least one alert present")
    check(data["derived"]["topProduct"] in prod_by_id, "derived.topProduct valid")
    check(data["derived"]["topPlatform"] in pl_by_id, "derived.topPlatform valid")
    # 5. finite numbers throughout
    for p in data["platforms"]:
        check(all(isinstance(x, (int, float)) for x in (p["followers"], p["reach"], p["impressions"],
                                                        p["linkClicks"], p["conversions"], p["revenue"], p["commission"])),
              f"platform {p['id']} numeric fields finite")

    for label in problems:
        print(f"  !! FAILED: {label}")
    return ok


# --------------------------------------------------------------------------
# Entrypoint
# --------------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser(description="Generate data.js mock for the influencer dashboard")
    ap.add_argument("--seed", type=int, default=SEED_DEFAULT, help="RNG seed (default 20261020)")
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "..", "data.js"),
                    help="output path (default: <repo-root>/data.js)")
    args = ap.parse_args(argv)

    rng = random.Random(args.seed)
    data = build(rng, args.seed)

    # print summary table
    print(f"Seed: {args.seed}  |  Period: {MONTHS[0]}..{MONTHS[-1]}")
    print(f"{'platform':<10}{'followers':>10}{'impressions':>12}{'clicks':>10}{'conv':>7}{'revenue':>10}{'comm':>9}{'roi':>6}")
    for p in data["platforms"]:
        print(f"{p['id']:<10}{p['followers']:>10,}{p['impressions']:>12,}{p['linkClicks']:>10,}"
              f"{p['conversions']:>7,}{p['revenue']:>10,.2f}{p['commission']:>9,.2f}{p['roi']:>6.2f}")
    d = data["derived"]
    print(f"{'TOTAL':<10}{d['unitsSold']:>10,}{'':>12}{'':>10}{d['totalConversions']:>7,}"
          f"{d['totalRevenue']:>10,.2f}{d['totalCommission']:>9,.2f}{d['overallRoi']:>6.2f}")
    print(f"Top product: {d['topProduct']}   Top platform: {d['topPlatform']}   Avg ER: {d['avgEngagementRate']}%")

    if not run_invariants(data):
        print("\nInvariant checks FAILED - data.js NOT written.")
        return 1

    out = os.path.abspath(args.out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(render_data(data))
    print(f"\nWrote {out} ({os.path.getsize(out):,} bytes)")
    print("All invariant checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())