# Active Context

## Current Work Focus

**Active Development** - The scraper is fully implemented and working. Two scraping implementations exist: Playwright-based (main.py) and Selenium-based (scraper.py).

## Recent Changes

- Implemented Playwright-based scraper in `main.py` with click-to-reveal email handling
- Implemented Selenium-based scraper in `scraper.py` with clipboard interception for email/phone
- Both scrapers successfully collect startup data including emails and phone numbers
- Generated output CSV file: `startups_completo.csv`

## Next Steps

1. Run full scraping to collect all pages
2. Validate data quality in the CSV output
3. Consider merging or optimizing the two implementations

## Active Decisions

- **Technology Stack**: Playwright (preferred) + Selenium (alternative)
- **Output Format**: CSV with UTF-8 encoding (utf-8-sig for Excel compatibility)
- **Email Collection**: Click-to-reveal pattern using regex difference or clipboard interception

## Important Patterns

- Website uses dynamic rendering - requires browser automation (Playwright/Selenium)
- Email/phone are hidden behind click-to-reveal buttons
- Pagination uses `?hasTag=true&page=X` URL parameters
- Need to handle cookie consent banner

## Project Insights

- The Vitrine Sebrae website loads content dynamically with JavaScript
- Email extraction requires clicking buttons and capturing revealed content
- Cards use Tailwind CSS classes for styling
- Both implementations successfully extract: type, name, local, segment, maturity, siteUrl, email, phone, description, imageUrl
