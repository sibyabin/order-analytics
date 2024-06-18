-- @author Siby Abin
-- 17/Jun/2024
-- customer dimension table
-- columns are added for SCD-Type2 , implementation based on time availability

CREATE TABLE IF NOT EXISTS customer_dim (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  customer_name varchar(200),
  customer_code varchar(40),
  address_line_1 varchar(300),
  post_code varchar(7),
  city varchar(40),
  country varchar(30),
  contact_number varchar(20),
  from_date date,
  to_date date,
  enabled_yn char(1),
  created_ts timestamp,
  updated_ts timestamp,
  created_id varchar(15),
  updated_id varchar(15)
);

DROP INDEX IF EXISTS idx_customer_dim;
CREATE UNIQUE INDEX IF NOT EXISTS idx_customer_dim ON customer_dim(customer_code);
