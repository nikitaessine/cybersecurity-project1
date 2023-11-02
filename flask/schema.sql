CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    admin BOOLEAN
);

CREATE TABLE restaurants(
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,  
    restaurant_id INTEGER REFERENCES restaurants, 
    stars INTEGER, 
    comment TEXT
);

CREATE TABLE locations (
  id SERIAL PRIMARY KEY,
  restaurant_id INTEGER REFERENCES restaurants,
  address TEXT,
  city TEXT
);

CREATE TABLE categories (
  id SERIAL PRIMARY KEY,
  name TEXT,
  restaurant_id INTEGER REFERENCES restaurants
);