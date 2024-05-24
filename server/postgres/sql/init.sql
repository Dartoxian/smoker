CREATE TABLE temp_records (
    id serial primary key,
    created_at timestamp not null,
    source text not null,
    value float not null
);