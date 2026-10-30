"""Which universities and companies lead a topic on Coursera.

    python partner_share.py "data science"
    python partner_share.py cybersecurity --product-type "Professional Certificates"

Searches the topic and counts the results per partner (every listed partner
of a co-branded programme counts), with the average rating and the total
number of ratings of their results. Writes partner_share.csv, biggest first.
"""

import argparse
from collections import defaultdict

from quanticdata_coursera_scraper import CourseraScraper, write

TYPES = ["Courses", "Specializations", "Guided Projects", "Professional Certificates", "Projects", "Degrees"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("topic")
    parser.add_argument("--product-type", choices=TYPES)
    parser.add_argument("--max-results", type=int, default=60, help="results to read (max 60)")
    parser.add_argument("--out", default="partner_share.csv")
    args = parser.parse_args()

    coursera = CourseraScraper()
    run = coursera.search(args.topic, product_type=args.product_type, max_results=args.max_results)
    groups = defaultdict(list)
    for c in run:
        for partner in c.get("partners") or [c.get("partner") or "unknown"]:
            groups[partner].append(c)

    summary = []
    for partner, results in groups.items():
        rated = [c["rating"] for c in results if c.get("rating") is not None]
        summary.append({
            "partner": partner,
            "results": len(results),
            "share": round(len(results) / len(run), 3) if len(run) else None,
            "avg_rating": round(sum(rated) / len(rated), 2) if rated else None,
            "total_ratings": sum(c.get("reviews") or 0 for c in results),
            "top_title": max(results, key=lambda c: c.get("reviews") or 0).get("title"),
        })
    summary.sort(key=lambda s: (s["results"], s["total_ratings"]), reverse=True)

    for s in summary[:15]:
        print(f"{s['results']:>3}  {s['avg_rating']}  {s['total_ratings']:>9,}  {s['partner']}")
    write(summary, args.out)
    print(f"{len(summary)} partners from {len(run)} results written to {args.out}")


if __name__ == "__main__":
    main()
