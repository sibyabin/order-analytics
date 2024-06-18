-- @author Siby Abin
-- 17/Jun/2024
-- date dimension table
-- TODO: can be extended further if required

CREATE TABLE IF NOT EXISTS date_dim (
  full_date date PRIMARY KEY,
  week_day int,
  weekday_name varchar(10),
  day int,
  month int,
  quarter varchar(2),
  year int
);
