CREATE TABLE users (
    user_id serial PRIMARY KEY,
    email varchar(75) NOT NULL,
    password varchar(255) NOT NULL
);

