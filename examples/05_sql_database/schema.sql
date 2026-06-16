DROP TABLE IF EXISTS paid_report;
DROP TABLE IF EXISTS authentication_request;
DROP TABLE IF EXISTS artwork;
DROP TABLE IF EXISTS artist;
DROP TABLE IF EXISTS client;

CREATE TABLE client (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  tier TEXT NOT NULL CHECK (tier IN ('basic', 'collector', 'gallery'))
);

CREATE TABLE artist (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  birth_year INTEGER,
  style TEXT NOT NULL
);

CREATE TABLE artwork (
  id INTEGER PRIMARY KEY,
  artist_id INTEGER NOT NULL,
  title TEXT NOT NULL,
  produced_year INTEGER,
  medium TEXT NOT NULL,
  owner_note TEXT,
  FOREIGN KEY (artist_id) REFERENCES artist(id)
);

CREATE TABLE authentication_request (
  id INTEGER PRIMARY KEY,
  client_id INTEGER NOT NULL,
  artwork_id INTEGER NOT NULL,
  submitted_at TEXT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('submitted', 'analyzing', 'reviewed', 'paid_report_issued', 'rejected')),
  risk_score INTEGER NOT NULL CHECK (risk_score BETWEEN 0 AND 100),
  fee INTEGER NOT NULL CHECK (fee >= 0),
  FOREIGN KEY (client_id) REFERENCES client(id),
  FOREIGN KEY (artwork_id) REFERENCES artwork(id)
);

CREATE TABLE paid_report (
  id INTEGER PRIMARY KEY,
  request_id INTEGER NOT NULL UNIQUE,
  issued_at TEXT NOT NULL,
  verdict TEXT NOT NULL CHECK (verdict IN ('likely_authentic', 'needs_review', 'high_risk_fake')),
  price INTEGER NOT NULL CHECK (price > 0),
  report_url TEXT NOT NULL,
  FOREIGN KEY (request_id) REFERENCES authentication_request(id)
);

CREATE INDEX idx_artwork_artist ON artwork(artist_id);
CREATE INDEX idx_request_client ON authentication_request(client_id);
CREATE INDEX idx_request_artwork ON authentication_request(artwork_id);
CREATE INDEX idx_request_status ON authentication_request(status);
