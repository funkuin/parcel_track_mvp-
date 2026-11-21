import re
import secrets
import unicodedata
from sqlalchemy.orm import Session

from app.models.parcel import Parcel

# Normalized 3-letter city codes for major transport hubs in Cameroon
KNOWN_CITY_CODES = {
    "bamenda": "BAM",
    "douala": "DLA",
    "yaounde": "YDE",
    "yaoundé": "YDE",
    "bafoussam": "BAF",
    "buea": "BUE",
    "limbe": "LMB",
    "kumba": "KBA",
    "garoua": "GAR",
    "maroua": "MRA",
    "ngaoundere": "NGA",
    "ngaoundéré": "NGA",
    "bertoua": "BTA",
    "ebolowa": "EBW",
    "kribi": "KRI",
}


def normalize_city_code(city_name: str) -> str:
    """Normalize a destination city name into a 3-character uppercase code.

    Handles accents, whitespace, punctuation, and unmapped cities safely.
    """
    if not city_name:
        return "XXX"

    cleaned = city_name.strip().lower()
    if cleaned in KNOWN_CITY_CODES:
        return KNOWN_CITY_CODES[cleaned]

    # Decompose unicode characters to strip accents (e.g., 'é' -> 'e')
    normalized = (
        unicodedata.normalize("NFKD", cleaned)
        .encode("ASCII", "ignore")
        .decode("utf-8")
    )
    # Retain alphanumeric characters only
    alphanumeric = re.sub(r"[^A-Za-z0-9]", "", normalized).upper()

    if len(alphanumeric) >= 3:
        return alphanumeric[:3]
    elif len(alphanumeric) > 0:
        return alphanumeric.ljust(3, "X")
    else:
        return "XXX"


def generate_tracking_id(destination: str) -> str:
    """Generate a tracking ID string in the format PT-{CITY}-{HEX6}."""
    city_code = normalize_city_code(destination)
    suffix = secrets.token_hex(3).upper()  # 3 bytes produces exactly 6 uppercase hex characters
    return f"PT-{city_code}-{suffix}"


def generate_unique_tracking_id(
    db: Session, destination: str, max_retries: int = 10
) -> str:
    """Generate a globally unique tracking ID by checking database collisions.

    Retries up to max_retries times before raising a RuntimeError.
    """
    for _ in range(max_retries):
        candidate_id = generate_tracking_id(destination)
        exists = (
            db.query(Parcel.id)
            .filter(Parcel.tracking_id == candidate_id)
            .first()
            is not None
        )
        if not exists:
            return candidate_id

    raise RuntimeError(
        "Failed to generate a unique tracking ID after multiple attempts."
    )
