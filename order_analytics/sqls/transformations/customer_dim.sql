-- DELETE DATA for an existing batch (rerun scenario)

DELETE FROM customer_dim WHERE created_id='{CREATED_BATCH_ID}';

-- INSERT any new records that is not present in the dim table
INSERT INTO customer_dim (customer_name, customer_code,address_line_1,post_code,city,country,contact_number,from_date,to_date,enabled_yn,created_ts,created_id)
SELECT DISTINCT
	UPPER(TRIM(client_name)) AS customer_name,
	NULL AS customer_code, -- TODO: for later implementations
	TRIM(delivery_address) AS address_line_1,
	TRIM(delivery_postcode) AS post_code,
	UPPER(TRIM(delivery_city)) AS city,
	CASE
		WHEN UPPER(TRIM(delivery_country)) in ('UK','UNITED KINGDOM') THEN 'UNITED KINGDOM'
		ELSE UPPER(TRIM(delivery_country))
	END AS country,
	TRIM(delivery_contact_number) AS contact_number,
	CURRENT_DATE AS from_date,
	date('9999-12-31') AS to_date,
	'Y' as enabled_yn,
	CURRENT_TIMESTAMP,
	'{CREATED_BATCH_ID}'
FROM stg_orders src
WHERE NOT EXISTS (
    SELECT 1
    FROM customer_dim tgt
    WHERE tgt.customer_name = UPPER(TRIM(src.client_name))
) AND src.created_id = '{CREATED_BATCH_ID}';

-- Update mart table - SCD Disable records

UPDATE customer_dim
SET enabled_yn = (SELECT 'N' FROM stg_orders WHERE customer_dim.customer_name = UPPER(TRIM(stg_orders.client_name))),
updated_id = (SELECT '{CREATED_BATCH_ID}' FROM stg_orders WHERE customer_dim.customer_name = UPPER(TRIM(stg_orders.client_name))),
to_date = (SELECT CURRENT_DATE FROM stg_orders WHERE customer_dim.customer_name = UPPER(TRIM(stg_orders.client_name)))
WHERE EXISTS (SELECT 1 FROM stg_orders WHERE customer_dim.customer_name = UPPER(TRIM(stg_orders.client_name)));

-- SCD new inserts
-- TODO : if address or post_code or city changes
