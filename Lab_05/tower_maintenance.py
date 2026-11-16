
"""Track telecom tower maintenance and fault risks."""

import sqlite3

CONN = sqlite3.connect(":memory:")
CONN.execute(
    "CREATE TABLE towers (id INTEGER PRIMARY KEY, "
    "site TEXT, last_service INTEGER, faults INTEGER)"
)


def add_tower(site, last_service, faults=0):
    """Add a tower to the maintenance database."""
    CONN.execute(
        "INSERT INTO towers (site, last_service, faults) VALUES (?, ?, ?)",
        (site, last_service, faults),
    )
    CONN.commit()


def service_tower(tower_id, year):
    """Service a tower and return whether it was updated."""
    try:
        cursor = CONN.execute(
            "UPDATE towers SET last_service = ?, faults = 0 WHERE id = ?",
            (year, tower_id),
        )
        CONN.commit()
        return cursor.rowcount > 0
    except sqlite3.Error:
        print("service failed")
        return False


def overdue(year):
    """Return sites that have not been serviced for two years."""
    rows = CONN.execute(
        "SELECT site, last_service FROM towers"
    ).fetchall()
    return [site for site, last in rows if year - last >= 2]


def risk_level(tower_id):
    """Determine the risk level of a tower."""
    row = CONN.execute(
        "SELECT faults FROM towers WHERE id = ?", (tower_id,)
    ).fetchone()

    if row is None:
        return "unknown"
    if row[0] > 3:
        return "high"
    return "normal"


def snapshot():
    """Return a snapshot of all tower records."""
    return CONN.execute("SELECT * FROM towers").fetchall()


def main():
    """Demonstrate the tower maintenance tracker."""
    add_tower("Ridge-A", 2021, 5)
    add_tower("Coast-B", 2024)
    service_count = int(service_tower(2, 2025))
    total = len(snapshot())
    print(overdue(2025), risk_level(1), total, service_count)


if __name__ == "__main__":
    main()
