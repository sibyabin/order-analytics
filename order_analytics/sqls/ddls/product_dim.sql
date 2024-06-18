-- @author Siby Abin
-- 17/Jun/2024
-- product dimension table

CREATE TABLE IF NOT EXISTS product_dim (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  product_name varchar(40) NOT NULL,
  product_type varchar(30) NOT NULL,
  unit_price decimal(17,2) NOT NULL,
  created_ts timestamp NOT NULL ,
  updated_ts timestamp,
  created_id varchar(15) NOT NULL,
  updated_id varchar(15)
);

DROP INDEX IF EXISTS idx_product_dim;
CREATE UNIQUE INDEX IF NOT EXISTS idx_product_dim ON product_dim(product_name,product_type);
