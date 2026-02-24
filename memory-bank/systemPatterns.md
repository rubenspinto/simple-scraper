# System Patterns

## Architecture

```
simple-scraper/
├── main.py              # Playwright-based scraper (preferred)
├── scraper.py           # Selenium-based scraper (alternative)
├── startups_completo.csv    # Output data file
├── page.html            # Test HTML file
├── memory-bank/         # Project documentation
│   ├── projectbrief.md
│   ├── productContext.md
│   ├── activeContext.md
│   ├── systemPatterns.md
│   ├── techContext.md
│   └── progress.md
└── plans/               # Original planning documents
    ├── problema_plans.md
    └── scrapi_plans.md
```

## Key Technical Decisions

1. **Browser Automation**: The Vitrine Sebrae website uses dynamic JavaScript rendering, requiring browser automation instead of simple HTTP requests
   
2. **Two Implementation Approaches**:
   - **Playwright (main.py)**: Preferred - Modern, faster, better async support
   - **Selenium (scraper.py)**: Alternative - Uses clipboard interception for email/phone

3. **Email/Phone Extraction**:
   - Click-to-reveal pattern - buttons with mail/phone icons
   - Playwright: Regex difference before/after click
   - Selenium: Clipboard interception via execute_script

4. **Pagination Strategy**: 
   - URL pattern: `https://vitrine.sebraestartups.com.br/?hasTag=true&page=X`
   - Detect end by waiting for cards selector timeout

5. **Error Handling Pattern**:
   - Try/except blocks for each card extraction
   - Timeout handling for page loads and element waits
   - Graceful degradation when elements not found

6. **Output Pattern**:
   - CSV with UTF-8-sig encoding (Excel compatible)
   - Dynamic naming: `vitrine_startups_YYYYMMDD_HHMMSS.csv` or `startups_completo.csv`

## Design Patterns

- **Modular Functions**: Separate concerns within each scraper
- **BeautifulSoup Integration**: Parse card HTML after browser rendering
- **Progress Logging**: Print statements for visibility

## Component Relationships

- `main.py`: Playwright orchestrator with `scrape_sebrae_vitrine()` function
- `scraper.py`: Selenium orchestrator with direct execution
- Both output to CSV with pandas DataFrame
- Output: CSV files in project root directory
