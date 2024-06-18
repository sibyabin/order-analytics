-- @author Siby Abin
-- 17/Jun/2024
-- order_line fact table
-- since the data at order line , this table grain kept at order_line level
-- if needed aggregate table at order_id level can be built for reporting requirements at aggregated levels



CREATE TABLE IF NOT EXISTS order_line_fact (
  order_key INTEGER PRIMARY KEY AUTOINCREMENT,
  order_id varchar(15),
  order_line_id bigint,
  order_date date,
  customer_id bigint,
  currency_id bigint,
  product_id bigint,
  quantity bigint,
  price decimal(17,2),
  total_amount decimal(17,2),
  created_ts timestamp,
  created_id varchar(15),
  FOREIGN KEY (currency_id) REFERENCES currency_dim(id)
);

-- ALTER TABLE order_line_fact ADD FOREIGN KEY (currency_id) REFERENCES currency_dim(id);
-- ALTER TABLE order_line_fact ADD FOREIGN KEY (product_id) REFERENCES product_dim(id);
-- ALTER TABLE order_line_fact ADD FOREIGN KEY (customer_id) REFERENCES customer_dim(id);
-- ALTER TABLE order_line_fact ADD FOREIGN KEY (order_date) REFERENCES date_dim(full_date);

DROP INDEX IF EXISTS idx_order_line_fact;
CREATE UNIQUE INDEX IF NOT EXISTS idx_order_line_fact ON order_line_fact(order_id,order_line_id,order_date);
