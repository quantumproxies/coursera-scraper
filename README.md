# Coursera Scraper

[![ci](https://github.com/quantumproxies/coursera-scraper/actions/workflows/ci.yml/badge.svg)](https://github.com/quantumproxies/coursera-scraper/actions/workflows/ci.yml) ![python](https://img.shields.io/badge/python-3.9%2B-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

Scrape Coursera search results from Python or the command line: the courses, specializations, professional certificates and degrees for any topic, with the university or company that offers them, average rating, exact number of ratings, level, duration, skills and the free, Coursera Plus, new and sponsored flags, as JSON or CSV. The code is free and open source (MIT). It runs on the QuanticData Data API, so there are no proxies to rotate and no headless browser to keep alive: sign in once and run a command.

```bash
pip install git+https://github.com/quantumproxies/coursera-scraper
coursera-scraper login
coursera-scraper search python --max-results 60 -o python_courses.csv
```

`login` opens the QuanticData sign-in page in your browser. New accounts get $2 of free usage every month, no card required: [create one](https://app.quanticdata.io/register?utm_source=github&utm_medium=readme&utm_campaign=coursera-scraper).

## What it scrapes

| Command | Input | Returns | Per run |
|---|---|---|---|
| `coursera-scraper search` | topic or skill | Partner, rating, review count, level and duration per course, 17 fields per row ([fields and price](https://quanticdata.io/collectors/coursera-scraper-api/?utm_source=github&utm_medium=readme&utm_campaign=coursera-scraper)) | up to 60 |

Narrow the search with `--level` (Beginner, Intermediate, Advanced, Mixed) and `--product-type` (Courses, Specializations, Guided Projects, Professional Certificates, Projects, Degrees). `reviews` is the exact number of ratings, where Coursera's cards round it ("44K"), and `id` is a stable key for de-duplicating results across searches.

## Sample output

A real row from `coursera-scraper search python --max-results 3` (2026-10-23):

```json
{
  "id": "s12n~F-h1g0w7EeWeOApO_l5R1w",
  "url": "https://www.coursera.org/specializations/python",
  "rank": 1,
  "image": "https://d2j5ihb19pt1hq.cloudfront.net/sdp_page/s12n_logos/python.jpg",
  "level": "Beginner",
  "title": "Python for Everybody",
  "is_new": false,
  "rating": 4.82,
  "skills": [
    "Database Design",
    "Data Processing",
    "Debugging",
    "Web Scraping",
    "File I/O",
    "Data Visualization",
    "Relational Databases",
    "Restful API"
  ],
  "is_free": false,
  "partner": "University of Michigan",
  "reviews": 280793,
  "duration": "3 - 6 Months",
  "partners": [
    "University of Michigan"
  ],
  "sponsored": false,
  "product_type": "Specialization",
  "in_coursera_plus": true
}
```

## Python

```python
from quanticdata_coursera_scraper import CourseraScraper

coursera = CourseraScraper()  # saved login, or QUANTICDATA_API_KEY

courses = coursera.search("python", max_results=60)
for c in courses:
    print(c["rank"], c["rating"], c["reviews"], c["partner"], c["title"])
courses.to_csv("python_courses.csv")

beginner = coursera.search("machine learning", level="Beginner", product_type="Courses", max_results=24)
top = max(beginner, key=lambda c: c["reviews"] or 0)
print(top["title"], top["partner"], top["skills"][:5])
```

Each call returns a `Run`: iterate it for the rows (plain dicts), take `len()`, or save it with `to_csv()`, `to_json()`, `to_jsonl()` or `to_dataframe()` (pandas). Errors are specific: `InsufficientCredit`, `RateLimited`, `InvalidInput`, `JobFailed`, `AuthError`.

## Examples

- **Best-rated courses by topic**: Run a list of topics and keep the best-rated courses that have at least a given number of ratings, in one CSV for all topics. See [`examples/top_courses.py`](examples/top_courses.py).
- **Who teaches a topic**: Count the results per university or company for a topic, with average rating and total ratings, to see which partners lead it. See [`examples/partner_share.py`](examples/partner_share.py).
- **Skills across a field**: Tally the skills Coursera lists across the results of a few topics, to see which skills a curriculum or a job ad should name. See [`examples/skills_count.py`](examples/skills_count.py).

## Command line

Results print as a table; `-o file.csv`, `-o file.json` or `-o file.jsonl` writes a file. List inputs take `a b c`, `a,b,c`, `@file.txt` (one per line) or `-` (stdin). `--no-wait` starts a long run in the background and prints its id; `coursera-scraper run <id> -o out.csv` collects it later.

### `coursera-scraper search`

Search Coursera by keyword — partner, rating, review count, level and duration per course.

```
coursera-scraper search QUERY [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `QUERY` | string |  | What to search Coursera for — a topic, technology or skill. |
| `--level` | Beginner / Intermediate / Advanced / Mixed |  | Restrict to one difficulty level. Coursera's own filter values. |
| `--product-type` | Courses / Specializations / Guided Projects / Professional Certificates / Projects / Degrees |  | Restrict to one kind of product. Coursera's own filter values — use "Courses" to exclude degrees and certificates. |
| `--country` | string |  | Country to search from, as an ISO 3166-1 alpha-2 code (default us). |
| `--max-results` | integer | `12` | How many results to deliver at most (1–60). You pay only for delivered results. |

## Output fields

<details><summary><code>coursera-scraper search</code>: 17 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based position in the delivered set, in Coursera's own result order. |
| `id` | string or null | Coursera's typed product id, e.g. "course~ejOz7RDUEei99hK0xs-tsg" or "s12n~F-h1g0w7EeWeOApO_l5R1w" — the stable de-duplication key. |
| `title` | string or null | Course, specialization or degree title. |
| `partner` | string or null | First listed partner — the university or company offering it. |
| `partners` | string[] | Every listed partner, in Coursera's order (co-branded programmes carry more than one). |
| `rating` | number or null | Average rating out of 5, to 2 decimals. Null on products Coursera has never rated, such as degrees. |
| `reviews` | integer or null | Exact number of ratings the average is based on — the site's cards round this to "44K". |
| `level` | string or null | Difficulty as the card states it: Beginner, Intermediate, Advanced or Mixed. Null on degrees, which state none. |
| `duration` | string or null | Time commitment as the card states it, e.g. "1 - 3 Months", "Less Than 2 Hours", "1 - 4 Years". |
| `product_type` | string or null | What kind of product this is: Course, Specialization, Professional Certificate, Guided Project, Project or Degree. |
| `url` | string or null | Absolute URL of the product page. |
| `image` | string or null | Course artwork URL. |
| `skills` | string[] | Skills Coursera lists for this product. |
| `sponsored` | boolean | True when Coursera marks the row as a paid placement. These are mixed into the ranked list, so a sponsored row's rank is a bought slot, not a relevance position. |
| `is_free` | boolean | True when Coursera marks the course itself as free. |
| `in_coursera_plus` | boolean | True when the product is included in a Coursera Plus subscription. |
| `is_new` | boolean | True when Coursera flags the product as new content. |

</details>

## Sign-in and API keys

- `coursera-scraper login` signs you in with OAuth 2.1 and PKCE in the browser. The token is stored in `~/.config/quanticdata/credentials.json` (readable only by you) and refreshed automatically. One login serves every QuanticData tool on the machine.
- No browser on the machine (SSH, Docker, Colab): run `coursera-scraper login --no-browser`, open the link anywhere, then paste back the address the browser ends on.
- Scripts and CI: set `QUANTICDATA_API_KEY` to a key from the dashboard, or store one with `coursera-scraper login --api-key`.
- `coursera-scraper logout` revokes the token. The connection is listed under API keys in the dashboard as "API · QuanticData CLI"; deleting that key disconnects every machine that uses it.

## Pricing

The code is free and MIT-licensed. Runs are billed to your QuanticData account per delivered row, at the price shown on each collector page linked above; $2 of usage is free every month and failed runs are never billed. Plans with higher limits: [pricing](https://quanticdata.io/pricing/?utm_source=github&utm_medium=readme&utm_campaign=coursera-scraper).

## Other ways to call it

The same data over plain HTTP:

```bash
curl -X POST https://api.quanticdata.io/v1/scraper/collectors/coursera_courses/run \
  -H "Authorization: Bearer $QUANTICDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {"query": "python", "max_results": 3}}'
```

- [API reference](https://quanticdata.io/docs/?utm_source=github&utm_medium=readme&utm_campaign=coursera-scraper) with Python, Node, PHP and curl examples.
- [MCP server](https://quanticdata.io/mcp-server/?utm_source=github&utm_medium=readme&utm_campaign=coursera-scraper) to give Claude, Cursor or any MCP client the same tools.
- [n8n node](https://github.com/quantumproxies/n8n-nodes-quanticdata) for no-code workflows.

## FAQ

**Is this Coursera scraper free?**

The code is free and MIT-licensed. Scraping runs on your QuanticData account: $2 of usage is free every month with no card, then you pay per delivered row at the price shown on each collector page. Failed runs are never billed.

**Do I need proxies or a headless browser?**

No. You send a topic and get rows back; the requests run on QuanticData's side. You do not need a Coursera account either.

**Does it flag free, Coursera Plus and sponsored results?**

Yes. Every row has is_free, in_coursera_plus, is_new and sponsored. Sponsored rows are paid placements mixed into Coursera's ranking, so their rank is a bought slot, not a relevance position.

**How many results can one run return?**

Up to 60 results per run; ask for fewer with --max-results and you pay only for what is delivered.

**Can I export to CSV or Excel?**

Add -o courses.csv (or .json, .jsonl). Lists such as skills and partners are joined with '; ', so the CSV opens cleanly in Excel or Google Sheets.

**Can I run it on a schedule?**

Yes. Set QUANTICDATA_API_KEY in the environment and call the CLI or examples/top_courses.py from cron, GitHub Actions or any scheduler.

## Related scrapers

- [Udemy Scraper](https://github.com/quantumproxies/udemy-scraper): Udemy course scraper for Python and the command line.
- [YouTube Scraper](https://github.com/quantumproxies/youtube-scraper): YouTube scraper for Python and the command line.
- [LinkedIn Scraper](https://github.com/quantumproxies/linkedin-scraper): LinkedIn scraper for Python and the command line.

## License

MIT. Built and maintained by [QuanticData](https://quanticdata.io/?utm_source=github&utm_medium=readme&utm_campaign=coursera-scraper).
