# Project Brief: Simple Scraper

## Project Overview

A Python-based web scraper to collect data from the **Vitrine Sebrae Startups** website (https://vitrine.sebraestartups.com.br). The scraper extracts startup information and exports it to a structured CSV file.

## Core Requirements

1. **Data Extraction**: Collect startup data including:
   - `type`
   - `name`
   - `local`
   - `segment_pt`
   - `maturity_pt`
   - `siteUrl`
   - `email`
   - `phone`
   - `description_pt`
   - `imageUrl`

2. **Pagination Support**: Handle paginated data to collect all startups

3. **Error Handling**: Implement retry logic and proper error handling

4. **Output**: Generate CSV files with dynamic naming: `vitrine_startups_YYYY-MM-DD_HH-MM.csv`

## Goals

- Create a reliable, automated scraper for the Vitrine Sebrae Startups
- Generate structured data for analysis and dashboards
- Ensure the script runs without manual intervention
