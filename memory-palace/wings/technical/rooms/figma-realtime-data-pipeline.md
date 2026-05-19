# Figma Real-Time Data Pipeline Upgrade

Source: ByteByteGo email, `How Figma Upgraded Data Pipeline from Multi-Day Latency to Real-Time`, received 2026-05-12.

## Core Problem

Figma's original analytics sync used daily full-table copies from Amazon RDS PostgreSQL into Snowflake through S3. This was simple when tables were small, but product and user growth made it expensive and slow. By 2023, daily syncs took around six hours, the largest tables took several days, and dedicated export replicas cost millions of dollars per year.

## Architecture Shift

Figma moved from full synchronization to incremental synchronization using Change Data Capture.

Key components:
- Amazon RDS snapshot exports to S3 for initial table bootstrap.
- Kafka topics, one per table, for CDC events.
- Snowflake stored procedures to merge inserts, updates, and deletes into warehouse tables.
- Default merge cadence of three hours, with team-specific overrides such as 30 minutes for billing.

## Important Design Detail

CDC streams only capture changes after listening starts, so Figma overlaps the CDC start offset with the snapshot timestamp. This may create duplicate events, but merge logic can handle duplicates. Missing events between snapshot start and CDC start would be much worse.

## Build-vs-Buy Reasons

Figma built in-house because vendors could not use RDS-specific snapshot APIs, pricing was reportedly 5x to 10x higher at Figma's scale, and tested tools could not reliably handle projected data growth.

## Validation Strategy

Figma built an independent validation workflow:
- Clone the live base table.
- Run the bootstrap process into a temporary schema.
- Align both copies to the same time point using CDC data.
- Compare cell by cell.
- Run weekly for every table.

This independent path avoids false confidence from checks that reuse the same flawed pipeline code.

## Re-Bootstrap Strategy

Figma supports zero-downtime re-bootstrap by versioning bootstrap artifacts while keeping the final user-facing view stable. A new version builds in parallel and is promoted atomically through a view update.

## Automation Model

Two levels:
- First-level automation executes bootstrap or validation for a given table and alerts on failure.
- Second-level automation decides when to onboard new tables or dispatch weekly validation.

## Results

Reported impact:
- Data freshness improved from over 30 hours to under 3 hours, with some paths configurable down to minutes.
- Pipeline handles tables over 10x larger than the previous system.
- Dedicated export replicas were removed, saving millions annually.
- No major incidents during and after launch.
- CDC history became queryable for incident response and debugging.

## Reusable Lessons

- Full syncs are fine until table size and data freshness needs cross a threshold.
- CDC pipelines need careful snapshot offset handling to avoid invisible data loss.
- Correctness checks should be independent from the main data path.
- Atomic view promotion is a practical pattern for zero-downtime re-bootstrap.
- Per-table or per-team freshness lets teams pay only for the compute they need.
