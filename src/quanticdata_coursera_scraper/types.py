"""Row types of each command, for editors and type checkers (rows are plain dicts)."""

from typing import Any, Dict, List, Optional

try:  # Python 3.8+
    from typing import TypedDict
except ImportError:  # pragma: no cover
    from typing_extensions import TypedDict  # type: ignore


class CourseraCoursesRow(TypedDict, total=False):
    """One row of `coursera-scraper search` (coursera_courses v1.0.2)."""

    rank: int
    """1-based position in the delivered set, in Coursera's own result order."""
    id: Optional[str]
    """Coursera's typed product id, e.g. "course~ejOz7RDUEei99hK0xs-tsg" or "s12n~F-h1g0w7EeWeOApO_l5R1w" — the stable de-duplication key."""
    title: Optional[str]
    """Course, specialization or degree title."""
    partner: Optional[str]
    """First listed partner — the university or company offering it."""
    partners: List[str]
    """Every listed partner, in Coursera's order (co-branded programmes carry more than one)."""
    rating: Optional[float]
    """Average rating out of 5, to 2 decimals. Null on products Coursera has never rated, such as degrees."""
    reviews: Optional[int]
    """Exact number of ratings the average is based on — the site's cards round this to "44K"."""
    level: Optional[str]
    """Difficulty as the card states it: Beginner, Intermediate, Advanced or Mixed. Null on degrees, which state none."""
    duration: Optional[str]
    """Time commitment as the card states it, e.g. "1 - 3 Months", "Less Than 2 Hours", "1 - 4 Years"."""
    product_type: Optional[str]
    """What kind of product this is: Course, Specialization, Professional Certificate, Guided Project, Project or Degree."""
    url: Optional[str]
    """Absolute URL of the product page."""
    image: Optional[str]
    """Course artwork URL."""
    skills: List[str]
    """Skills Coursera lists for this product."""
    sponsored: bool
    """True when Coursera marks the row as a paid placement. These are mixed into the ranked list, so a sponsored row's rank is a bought slot, not a relevance position."""
    is_free: bool
    """True when Coursera marks the course itself as free."""
    in_coursera_plus: bool
    """True when the product is included in a Coursera Plus subscription."""
    is_new: bool
    """True when Coursera flags the product as new content."""
