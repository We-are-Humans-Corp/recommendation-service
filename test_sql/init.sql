-- Create Schema
CREATE SCHEMA IF NOT EXISTS recommendation_service;

-- Create Table
CREATE TABLE recommendation_service.recommendation (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    item_id BIGINT NOT NULL,
    rating FLOAT NOT NULL
);


