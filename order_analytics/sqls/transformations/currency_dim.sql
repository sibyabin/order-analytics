-- DELETE DATA for an existing batch (rerun scenario)

DELETE FROM currency_dim WHERE created_id='{CREATED_BATCH_ID}';

-- INSERT any new records that is not present in the dim table
INSERT INTO currency_dim (currency_code, conversion_rate,created_ts,created_id)
SELECT DISTINCT
UPPER(TRIM(currency)),
NULL as conversion_rate, --later implementation
CURRENT_TIMESTAMP,
'{CREATED_BATCH_ID}'
FROM stg_orders src
WHERE NOT EXISTS (
    SELECT 1
    FROM currency_dim tgt
    WHERE tgt.currency_code = UPPER(TRIM(src.currency))
) AND src.created_id = '{CREATED_BATCH_ID}';

-- Update mart table
-- TODO: Not needed at this moment for this table as there is no attribute that can get updated
