-- @author Siby Abin
-- 17/Jun/2024
-- currency dimension table

CREATE TABLE IF NOT EXISTS currency_dim (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  currency_code varchar(40) NOT NULL,
  conversion_rate decimal(5,2),
  created_ts timestamp NOT NULL,
  updated_ts timestamp,
  created_id varchar(15) NOT NULL,
  updated_id varchar(15)
);


DROP INDEX IF EXISTS idx_currency_dim;
CREATE UNIQUE INDEX IF NOT EXISTS idx_currency_dim ON currency_dim(currency_code);
