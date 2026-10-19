Scratchpad for information regarding dashboard goals and repo-wide expectations. Use this to generate a design plan and tech needs document, at resources/dashboard-design.md. Build a file here that tracks: 
    - client's needs and goals
    - functionality expectations for the dashboard
    - space for proposed methods for implementing the requested features and design -- do not propose first, just make space for where those implementation plans will go. we will do research on implementation methods and present options to user before writing anything here in a future step.
    - create space for creative design choices -- layouts, color schemes, organization of elements, etc. 
    - create space for brainstorming design goals / overarching themes of the website

Rules to add to .agents/rules/, check existing rule coverage first and improve folder until all values here are well covered.
    - build in reusable components, like cards/widgets/boxes/tables, and section-based structure.
    - design mobile-first
        - start from the smallest screen
        - adapt with Tailwind breakpoints (sm:, md:. lg:)
        - ensure the same components work on tablet and desktop
        - avoid pixel-based sizes
        - use Tailwind spacing and sizing utilities
    - use semantic HTML  with appropriate tags to create a clear document outline
    - use Tailwind CSS v4 and HTML only
        - Preflight is okay
        - do not mix in other CSS frameworks or custom CSS except for Chart CSS if needed
    - for KPIs oir drivers, you can use Chart CSS (https://chartscss.org/). Data can be simple data, focus on clear hierarchy and readability
    - use consistent patterns for similar elements (eg, all KPI cards share the same structure and style)


Design Request:
{
What makes a dashboard "good"?

Organize the dashboard into broad blocks:

1️⃣ Top block: Main outcome indicators (KPI):

    Volume: sales, sign-ups, active users, impressions
    Revenue: revenue (commissions, sales), MRR (monthly recurring revenue in subscriptions), average selling price
    Engagement: engagement rate, total interactions, conversion rate
    Retention: churn (churn rate), persistence, completion rate of the sales or subscription process
    Performance: total conversions, click-through rate (CTR), conversion rate
    Satisfaction: loyalty score (NPS), satisfaction score (CSAT)
    Efficiency: cost per outcome, margin, lead times

2️⃣ Middle block: "Drivers" (factors that explain the outcome):

    Conversion by stage (sales funnel)
    Performance by platform (Instagram, TikTok, YouTube, etc.)
    Quality (qualified lead ratio, attendance rate, pass rate)
    Performance by product (which product generates more commissions and better conversion)
    Activity (posts published, stories, reels, videos by platform)
    Engagement (likes, comments, shares, saves by platform)

3️⃣ Bottom block: Operational details (tables/lists, alerts):

    Products table: price, commissions generated, conversions, ROI per product
    Platforms table: reach, engagement, conversions, best platform by metric
    Campaigns table: dates, products promoted, results, performance
    Alerts: sharp drops in conversion, conversion spikes, performance anomalies
    Lists with filters: "top products", "top platforms", "top campaigns", "improvement opportunities"
}