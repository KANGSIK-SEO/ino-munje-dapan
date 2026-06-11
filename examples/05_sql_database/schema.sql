DROP TABLE IF EXISTS rental;
DROP TABLE IF EXISTS book;
DROP TABLE IF EXISTS member;
DROP TABLE IF EXISTS category;

CREATE TABLE member (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE
);

CREATE TABLE category (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE book (
  id INTEGER PRIMARY KEY,
  category_id INTEGER NOT NULL,
  title TEXT NOT NULL,
  author TEXT NOT NULL,
  stock INTEGER NOT NULL CHECK (stock >= 0),
  FOREIGN KEY (category_id) REFERENCES category(id)
);

CREATE TABLE rental (
  id INTEGER PRIMARY KEY,
  member_id INTEGER NOT NULL,
  book_id INTEGER NOT NULL,
  rented_at TEXT NOT NULL,
  returned_at TEXT,
  FOREIGN KEY (member_id) REFERENCES member(id),
  FOREIGN KEY (book_id) REFERENCES book(id)
);

CREATE INDEX idx_rental_member ON rental(member_id);
CREATE INDEX idx_rental_book ON rental(book_id);
