# Tech Context

## Technologies Used

- **Python 3.x**: Primary programming language
- **Playwright**: Browser automation (preferred) - modern, async-capable
- **Selenium**: Browser automation (alternative) - mature, widely used
- **BeautifulSoup**: HTML parsing for card content after rendering
- **pandas**: DataFrame manipulation and CSV export
- **re**: Regex for email pattern matching

## Development Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Chrome/Chromium browser installed

### Installation
```bash
pip install playwright beautifulsoup4 pandas selenium
playwright install chromium
```

## Technical Constraints

1. **Dynamic Content**: Website uses JavaScript rendering - requires browser automation
2. **Rate Limiting**: Implemented delays between page requests (1 second)
3. **Cookie Banner**: Need to handle OneTrust cookie consent popup
4. **Encoding**: UTF-8-sig for Excel compatibility with Brazilian Portuguese

## Tool Usage Patterns

- **playwright.sync_api**: Sync Playwright for browser automation
- **webdriver.Chrome**: Selenium Chrome driver
- **BeautifulSoup**: Parse card inner HTML after browser rendering
- **pandas.DataFrame**: Structure and export data to CSV
- **datetime.now().strftime()**: Generate timestamps for filenames

## Dependencies

```
playwright>=1.40.0
beautifulsoup4>=4.11.0
pandas>=2.0.0
selenium>=4.10.0
```
