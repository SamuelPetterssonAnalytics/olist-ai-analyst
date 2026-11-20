CREATE OR REPLACE VIEW olist.ai_orders AS

SELECT
    o.order_id,
    o.order_status,
    (o.order_status = 'delivered') AS is_delivered,

    o.order_purchase_timestamp,
    o.order_approved_at,
    o.order_delivered_carrier_date,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,

    c.customer_unique_id,
    c.customer_city,
    c.customer_state,

    COUNT(oi.order_item_id) AS item_count,
    COUNT(DISTINCT oi.product_id) AS distinct_product_count,

    COALESCE(SUM(oi.price), 0) AS product_value,
    COALESCE(SUM(oi.freight_value), 0) AS freight_value,
    COALESCE(SUM(oi.price + oi.freight_value), 0) AS total_order_value,

    EXTRACT(
        EPOCH FROM (
            o.order_delivered_customer_date
            - o.order_purchase_timestamp
        )
    ) / 86400.0 AS delivery_days,

    CASE
        WHEN o.order_delivered_customer_date IS NULL
          OR o.order_estimated_delivery_date IS NULL
        THEN NULL
        ELSE o.order_delivered_customer_date
             > o.order_estimated_delivery_date
    END AS late_delivery

FROM olist.olist_orders_dataset o

LEFT JOIN olist.olist_customers_dataset c
    ON o.customer_id = c.customer_id

LEFT JOIN olist.olist_order_items_dataset oi
    ON o.order_id = oi.order_id

GROUP BY
    o.order_id,
    o.order_status,
    o.order_purchase_timestamp,
    o.order_approved_at,
    o.order_delivered_carrier_date,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,
    c.customer_unique_id,
    c.customer_city,
    c.customer_state;


CREATE OR REPLACE VIEW olist.ai_order_items AS

SELECT
    oi.order_id,
    oi.order_item_id,

    o.order_status,
    (o.order_status = 'delivered') AS is_delivered,
    o.order_purchase_timestamp,

    c.customer_unique_id,
    c.customer_city,
    c.customer_state,

    oi.product_id,
    oi.seller_id,

    p.product_category_name,

    COALESCE(
        t.product_category_name_english,
        p.product_category_name
    ) AS product_category,

    oi.price AS item_price,
    oi.freight_value AS item_freight_value,
    oi.price + oi.freight_value AS total_item_value,

    oi.shipping_limit_date

FROM olist.olist_order_items_dataset oi

JOIN olist.olist_orders_dataset o
    ON oi.order_id = o.order_id

LEFT JOIN olist.olist_customers_dataset c
    ON o.customer_id = c.customer_id

LEFT JOIN olist.olist_products_dataset p
    ON oi.product_id = p.product_id

LEFT JOIN olist.product_category_name_translation t
    ON p.product_category_name = t.product_category_name;

CREATE OR REPLACE VIEW olist.ai_reviews AS

SELECT
    r.review_id,
    r.order_id,

    r.review_score,
    r.review_comment_title,
    r.review_comment_message,
    r.review_creation_date,
    r.review_answer_timestamp,

    o.order_status,
    o.order_purchase_timestamp,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,

    c.customer_unique_id,
    c.customer_city,
    c.customer_state,

    COUNT(oi.order_item_id) AS item_count,
    COUNT(DISTINCT oi.product_id) AS distinct_product_count,

    CASE
        WHEN COUNT(DISTINCT oi.product_id) = 1
        THEN MIN(oi.product_id)
        ELSE NULL
    END AS single_product_id

FROM olist.olist_order_reviews_dataset r

JOIN olist.olist_orders_dataset o
    ON r.order_id = o.order_id

LEFT JOIN olist.olist_customers_dataset c
    ON o.customer_id = c.customer_id

LEFT JOIN olist.olist_order_items_dataset oi
    ON r.order_id = oi.order_id

GROUP BY
    r.review_id,
    r.order_id,
    r.review_score,
    r.review_comment_title,
    r.review_comment_message,
    r.review_creation_date,
    r.review_answer_timestamp,
    o.order_status,
    o.order_purchase_timestamp,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,
    c.customer_unique_id,
    c.customer_city,
    c.customer_state;