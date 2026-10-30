"""Coursera Scraper: Coursera scraper for Python and the command line: course search by keyword with partner, rating, exact review count, level, duration, skills and product type (course, specialization, certificate, degree), as JSON or CSV. Free and open source; sign in with your QuanticData account, no proxies or headless browser to run.

    from quanticdata_coursera_scraper import CourseraScraper

    scraper = CourseraScraper()   # saved login (`coursera-scraper login`) or QUANTICDATA_API_KEY
    run = scraper.search(...)   # Coursera search results for a topic
"""

from typing import Any, Dict, Optional, Sequence, Union

from ._qd.client import Client, Run
from ._qd.errors import (APIError, AuthError, InsufficientCredit, InvalidInput, JobFailed, JobTimeout,
                         QuanticDataError, RateLimited)
from ._qd.output import write

__version__ = "0.1.0"
__all__ = ["CourseraScraper", "Run", "write", "APIError", "AuthError", "InsufficientCredit", "InvalidInput",
           "JobFailed", "JobTimeout", "QuanticDataError", "RateLimited", "__version__"]


def _as_list(value: Any) -> Any:
    if value is None or isinstance(value, (list, tuple)):
        return list(value) if value is not None else None
    return [value]


class CourseraScraper:
    """Coursera Scraper on the QuanticData Data API.

    Every method runs one collector and returns a :class:`Run`: iterate it for the
    rows (plain dicts, typed in ``types``), or save it with ``to_csv()``,
    ``to_json()``, ``to_jsonl()`` or ``to_dataframe()``.
    """

    def __init__(self, api_key: Optional[str] = None, *, timeout: float = 180.0) -> None:
        self.client = Client(api_key, user_agent="coursera-scraper/0.1.0 (+https://github.com/quantumproxies/coursera-scraper)", timeout=timeout)

    def search(
        self, query: str,
        *,
        level: Optional[str] = None,
        product_type: Optional[str] = None,
        country: Optional[str] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Search Coursera by keyword — partner, rating, review count, level and duration per course.

        Args:
            query: What to search Coursera for — a topic, technology or skill.
            level: Restrict to one difficulty level. Coursera's own filter values. One of: Beginner, Intermediate, Advanced, Mixed.
            product_type: Restrict to one kind of product. Coursera's own filter values — use "Courses" to exclude degrees and certificates. One of: Courses, Specializations, Guided Projects, Professional Certificates, Projects, Degrees.
            country: Country to search from, as an ISO 3166-1 alpha-2 code (default us).
            max_results: How many results to deliver at most (1–60). You pay only for delivered results.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 60 rows, one per result: see ``types.CourseraCoursesRow``.
        """
        payload = {
            "query": query,
            "level": level,
            "product_type": product_type,
            "country": country,
            "max_results": max_results,
        }
        return self.client.run_collector("coursera_courses", payload, wait=wait, timeout=timeout)
