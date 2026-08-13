## Table Users
Saves the user information from Telegram and Web app 



```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE  NULL,
    username VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
```


## Table Trackings
Saves the tracking information about active and inactive trackings about prices of routes and flights

```sql
CREATE TABLE trackings (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    origin VARCHAR(255) NOT NULL,
    destination VARCHAR(255) NOT NULL,
    departure_date DATE NOT NULL,
    target_price DECIMAL(10, 2) NOT NULL,
    transport_type VARCHAR(50) NOT NULL,
    route VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);


-- INDEX FOR DEDUPLICATION IN Celery 
CREATE UNIQUE INDEX idx_unique_tracking ON trackings(user_id, origin, destination, departure_date, transport_type)
WHERE is_active = TRUE;
```


## Table PriceHistory
Saves the price history of the tracked routes and flights and will be used for create graphs and charts for the users to see the price history of the tracked routes and flights

```sql
CREATE TABLE price_history (
    time TIMESTAMPTZ NOT NULL, -- will be used for creating hypertable in TimescaleDB for better performance and scalability --
    tracking_id INT REFERENCES trackings(id) ON DELETE CASCADE,
    price DECIMAL(10, 2) NOT NULL,
    carrier VARCHAR(255) NOT NULL,
    recorded_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    details JSONB,
    PRIMARY KEY (time, tracking_id) --no duplicates for the same tracking_id at the same time --
);

COMMON TABLE -> HYPERTABLE
```sql
SELECT create_hypertable('price_history', 'time', chunk_time_interval => INTERVAL '3 days');
```

INDEX USAGE
```sql
CREATE INDEX idx_price_history_tracking_id ON price_history(tracking_id, time DESC);
```
