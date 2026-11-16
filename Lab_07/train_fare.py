"""Train journey input parsing with explicit validation."""
import re

BERTHS = ["SU", "LB", "MB", "UB", "LB", "MB", "UB", "SL"]


def parse_pnr(pnr):
    """Return the zone digit and remaining number of a 10-digit ASCII PNR."""
    if not isinstance(pnr, str) or not re.fullmatch(r"[0-9]{10}", pnr):
        raise ValueError("PNR must contain exactly 10 digits")
    return int(pnr[0]), int(pnr[1:])


def journey_distance(distances_csv):
    """Calculate distance from two or more nondecreasing station distances."""
    if not isinstance(distances_csv, str):
        raise ValueError("Station distances must be a CSV string")
    parts = [part.strip() for part in distances_csv.split(',')]
    if len(parts) < 2 or any(not re.fullmatch(r"[0-9]+", part) for part in parts):
        raise ValueError("Enter at least two nonnegative integer distances")
    try:
        distances = [int(part) for part in parts]
    except ValueError as exc:
        raise ValueError("Station distance is too large") from exc
    if any(a > b for a, b in zip(distances, distances[1:])):
        raise ValueError("Station distances must be nondecreasing")
    return distances[-1] - distances[0]


def berth_type(seat):
    """Return coach and berth for a seat numbered 1 to 72 in this lab model."""
    if not isinstance(seat, str):
        raise ValueError("Seat must be a string like S3-45")
    match = re.fullmatch(r"([A-Za-z]+[1-9][0-9]?)-([0-9]{1,2})", seat)
    if not match or not 1 <= int(match.group(2)) <= 72:
        raise ValueError("Enter a coach and seat from 1 to 72, e.g. S3-45")
    return match.group(1).upper(), BERTHS[int(match.group(2)) % 8]


def main():
    try:
        print("==== Running parse_pnr ====")
        result = parse_pnr(input("Enter a 10 digit PNR (e.g. 4521367890): "))
        print("Zone and Number:", result)
        print("\n==== Running journey_distance ====")
        result = journey_distance(input("Enter station distances as CSV (e.g. 0,120,340): "))
        print("Total Distance:", result)
        print("\n==== Running berth_type ====")
        result = berth_type(input("Enter coach and seat (e.g. S3-45): "))
        print("Coach and Berth:", result)
    except (ValueError, EOFError) as exc:
        print("Invalid input:", str(exc) or "input ended unexpectedly")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
