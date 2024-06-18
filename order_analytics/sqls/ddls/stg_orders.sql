-- @author Siby Abin
-- 17/Jun/2024
-- orders stage table
-- all columns are string since the data will be dumped from csv file
-- no constaints to avoid load performance
-- batch columns are added to select incremental data


CREATE TABLE IF NOT EXISTS stg_orders (
  order_number varchar(15),
  client_name varchar(200),
  product_name varchar(40),
  product_type varchar(30),
  unit_price varchar(20),
  product_quantity varchar(5),
  total_price varchar(20),
  currency varchar(3),
  delivery_address varchar(300),
  delivery_city varchar(40),
  delivery_postcode varchar(7),
  delivery_country varchar(30),
  delivery_contact_number varchar(20),
  payment_type varchar(6),
  payment_billing_code varchar(15),
  payment_date varchar(10),
  created_ts timestamp,
  created_id varchar(15)
);
