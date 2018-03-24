DROP TABLE IF EXISTS entries;
CREATE TABLE entries (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  water_level REAL NOT NULL,
  entry_time  TEXT NOT NULL
);