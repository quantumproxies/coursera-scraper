"""Best-rated Coursera courses for a list of topics, in one CSV.

    python top_courses.py python "machine learning" "project management" --min-reviews 1000 --top 5

Searches each topic, drops results with fewer ratings than --min-reviews
(and sponsored rows unless --keep-sponsored), sorts what is left by rating
and keeps the best --top per topic. Writes top_courses.csv.
"""

import argparse

from quanticdata_coursera_scraper import CourseraScraper, write

LEVELS = ["Beginner", "Intermediate", "Advanced", "Mixed"]
TYPES = ["Courses", "Specializations", "Guided Projects", "Professional Certificates", "Projects", "Degrees"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("topics", nargs="+")
    parser.add_argument("--level", choices=LEVELS)
    parser.add_argument("--product-type", choices=TYPES)
    parser.add_argument("--min-reviews", type=int, default=500, help="fewest ratings a result needs")
    parser.add_argument("--top", type=int, default=5, help="results kept per topic")
    parser.add_argument("--keep-sponsored", action="store_true")
    parser.add_argument("--out", default="top_courses.csv")
    args = parser.parse_args()

    coursera = CourseraScraper()
    rows = []
    for topic in args.topics:
        run = coursera.search(topic, level=args.level, product_type=args.product_type, max_results=60)
        rated = [c for c in run if c.get("rating") is not None and (c.get("reviews") or 0) >= args.min_reviews
                 and (args.keep_sponsored or not c.get("sponsored"))]
        rated.sort(key=lambda c: (c["rating"], c["reviews"]), reverse=True)
        for c in rated[:args.top]:
            rows.append({"topic": topic, **c})
            print(f"[{topic}] {c['rating']:.2f} ({c['reviews']:,})  {c.get('partner')}  {c.get('title')}")

    write(rows, args.out)
    print(f"{len(rows)} courses written to {args.out}")


if __name__ == "__main__":
    main()
