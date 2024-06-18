-- DELETE DATA for an existing batch (rerun scenario)

DELETE FROM product_dim WHERE created_id='{CREATED_BATCH_ID}';

-- INSERT any new records that is not present in the dim table
INSERT INTO product_dim (product_name, product_type,unit_price,created_ts,created_id)
SELECT DISTINCT
TRIM(product_name),
TRIM(product_type),
CAST(COALESCE(TRIM(unit_price),0.00) AS DECIMAL(17,2)),
CURRENT_TIMESTAMP,
'{CREATED_BATCH_ID}'
FROM stg_orders src
WHERE NOT EXISTS (
    SELECT 1
    FROM product_dim tgt
    WHERE tgt.product_name = TRIM(src.product_name) AND tgt.product_type = TRIM(src.product_type)
) AND src.created_id = '{CREATED_BATCH_ID}';

-- Update mart table  (only unit_price can get updated)

UPDATE product_dim
SET unit_price = (SELECT CAST(COALESCE(TRIM(unit_price),0.00) AS DECIMAL(17,2)) FROM stg_orders WHERE product_dim.product_name = TRIM(stg_orders.product_name) AND product_dim.product_type = TRIM(stg_orders.product_type))
WHERE EXISTS (SELECT 1 FROM stg_orders WHERE product_dim.product_name = TRIM(stg_orders.product_name) AND product_dim.product_type = TRIM(stg_orders.product_type));
