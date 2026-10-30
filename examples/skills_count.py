"""The skills Coursera lists across the results of a few topics.

    python skills_count.py "data analysis" "business intelligence" "sql" --top 25

Searches each topic, counts every skill tag on the results (once per
result) and how many topics it shows up in. Useful to see which skills a
curriculum or a job ad in that field should name. Writes skills_count.csv.
"""

import argparse
from collections import Counter, defaultdict

from quanticdata_coursera_scraper import CourseraScraper, write


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("topics", nargs="+")
    parser.add_argument("--max-results", type=int, default=60, help="results per topic (max 60)")
    parser.add_argument("--top", type=int, default=30, help="skills to print")
    parser.add_argument("--out", default="skills_count.csv")
    args = parser.parse_args()

    coursera = CourseraScraper()
    counts = Counter()
    topics_with = defaultdict(set)
    read = 0
    for topic in args.topics:
        run = coursera.search(topic, max_results=args.max_results)
        read += len(run)
        for c in run:
            for skill in set(c.get("skills") or []):
                counts[skill] += 1
                topics_with[skill].add(topic)

    rows = [{"skill": skill, "results": n, "share": round(n / read, 3), "topics": len(topics_with[skill])}
            for skill, n in counts.most_common()]
    for r in rows[:args.top]:
        print(f"{r['results']:>4}  {r['share']:>6.1%}  {r['skill']}")
    write(rows, args.out)
    print(f"{len(rows)} skills from {read} results written to {args.out}")


if __name__ == "__main__":
    main()
