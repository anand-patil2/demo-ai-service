def create_schema() -> str:
    return """
    CREATE TABLE customer_profiles (
        id TEXT PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT,
        birth_date TEXT,
        address TEXT,
        demographic_segment TEXT,
        preferred_language TEXT,
        status TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        archived_at TEXT,
        deleted_at TEXT
    );

    CREATE TABLE profile_events (
        id TEXT PRIMARY KEY,
        profile_id TEXT NOT NULL,
        event_type TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        changed_by TEXT NOT NULL,
        notes TEXT,
        FOREIGN KEY(profile_id) REFERENCES customer_profiles(id)
    );
    """
