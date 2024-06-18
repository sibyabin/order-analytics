-- @Author Siby Abin
-- 17/Jun/2024
-- batch_information audit table


CREATE TABLE IF NOT EXISTS batch_information
(
    id integer PRIMARY KEY AUTOINCREMENT,
    batch_id varchar(20) NOT NULL,
    batch_date date NOT NULL,
    batch_number integer NOT NULL,
    batch_status varchar(20) NOT NULL,
    batch_starttime timestamp NOT NULL,
    batch_endtime timestamp,
    batch_created_ts timestamp NOT NULL,
    batch_updated_ts timestamp,
    batch_created_id varchar(15) NOT NULL,
    batch_updated_id varchar(15)
);

DROP INDEX IF EXISTS idx_batch_information;
CREATE UNIQUE INDEX IF NOT EXISTS idx_batch_information ON batch_information(batch_id);
