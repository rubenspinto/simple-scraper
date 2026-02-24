# Product Context

## Why This Project Exists

The **Vitrine Sebrae Startups** website displays a curated list of Brazilian startups, but doesn't provide an easy way to export this data for analysis. This project solves that problem by creating an automated scraper that collects startup information and structures it for use in dashboards and analysis tools.

## Problem Solved

- Manual data collection from the website is time-consuming
- Need for structured data to feed dashboards and reports
- Requirement for periodic data collection (the scraper can be scheduled)

## Target Users

- Data analysts needing startup data for research
- Business teams requiring startup lists for outreach
- Developers building dashboards and applications

## How It Should Work

1. The script runs autonomously without user intervention
2. It navigates through paginated listings
3. Extracts key startup information from each listing
4. Handles errors gracefully with retry logic
5. Outputs a timestamped CSV file for easy tracking and versioning
