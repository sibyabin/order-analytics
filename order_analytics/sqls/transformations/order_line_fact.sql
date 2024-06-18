-- DELETE DATA for an existing batch (rerun scenario)

DELETE FROM order_line_fact WHERE created_id='{CREATED_BATCH_ID}';

INSERT INTO order_line_fact(order_id,order_line_id,order_date,customer_id,currency_id,product_id,quantity,price,total_amount,created_ts,created_id)
SELECT DISTINCT
    substr(order_number,1,9) AS order_id,
    CAST(substr(order_number,11,4) AS INTEGER) AS order_line_id,
    date(substr(payment_billing_code,11,4) || '-' || substr(payment_billing_code,15,2) || '-' || substr(payment_billing_code,17,2)) AS order_date,
    cust.id AS customer_id,
    curr.id AS currency_id,
    prod.id AS product_id,
    CAST(TRIM(stg.product_quantity) AS INTEGER) AS quantity,
    CAST(TRIM(stg.unit_price) AS DECIMAL(17,2)) AS price,
    CAST(TRIM(stg.total_price) AS DECIMAL(17,2)) AS total_amount,
    CURRENT_TIMESTAMP,
    '{CREATED_BATCH_ID}'
from stg_orders stg
LEFT JOIN customer_dim cust ON cust.customer_name = UPPER(TRIM(stg.client_name))
LEFT JOIN product_dim prod ON prod.product_name = TRIM(stg.product_name) AND prod.product_type = TRIM(stg.product_type)
LEFT JOIN currency_dim curr ON curr.currency_code = UPPER(TRIM(stg.currency))
WHERE stg.created_id = '{CREATED_BATCH_ID}'
