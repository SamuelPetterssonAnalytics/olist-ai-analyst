# AI Data Model

The AI analyst may query only the approved analytical views listed in this document.

Raw Olist source tables must not be queried directly.

Do not reference columns that are not explicitly listed in this data model.

## `olist.ai_orders`

### Grain

One row represents one order.

### Use for

- Order counts
- Order-level revenue
- Average order value
- Customer analysis
- Geographic analysis
- Delivery-time analysis
- Late-delivery analysis
- Repeat-customer analysis

### Available fields

`order_id`

Unique order identifier.

`order_status`

Status of the order.

`is_delivered`

True when `order_status = 'delivered'`.

`order_purchase_timestamp`

Purchase timestamp. Use this as the default date for sales and order analysis.

`order_approved_at`

Timestamp when the order was approved.

`order_delivered_carrier_date`

Timestamp when the order was delivered to the carrier.

`order_delivered_customer_date`

Timestamp when the order was delivered to the customer.

`order_estimated_delivery_date`

Estimated customer delivery date.

`customer_unique_id`

Persistent customer identifier. Use this for unique-customer and repeat-customer analysis.

`customer_city`

Customer city.

`customer_state`

Customer state.

`item_count`

Number of order-item rows associated with the order.

`distinct_product_count`

Number of distinct products contained in the order.

`product_value`

Total value of products in the order, excluding freight.

Use this field for order-level product revenue.

`freight_value`

Total recorded freight value associated with the order.

`total_order_value`

Product value plus freight value.

Do not use this as product revenue unless freight is explicitly requested.

`delivery_days`

Number of days between order purchase and actual customer delivery.

This may be null when an actual delivery date is unavailable.

`late_delivery`

True when actual customer delivery occurred after the estimated delivery date.

This may be null when the required delivery dates are unavailable.

### Important rules

Use `product_value` for order-level revenue analysis.

Unless explicitly requested otherwise, revenue analysis should include only rows where `is_delivered = true`.

Use `COUNT(DISTINCT order_id)` when counting orders.

Use `customer_unique_id` for unique-customer and repeat-customer analysis.

Do not calculate product-category or seller-level revenue using this view. Use `olist.ai_order_items` instead.


## `olist.ai_order_items`

### Grain

One row represents one item within an order.

### Use for

- Product analysis
- Product-category analysis
- Seller analysis
- Item counts
- Revenue by product
- Revenue by product category
- Revenue by seller
- Item-level freight analysis

### Available fields

`order_id`

Unique identifier of the associated order.

`order_item_id`

Item number within the order.

`order_status`

Status of the associated order.

`is_delivered`

True when the associated order is delivered.

`order_purchase_timestamp`

Purchase timestamp of the associated order.

`customer_unique_id`

Persistent customer identifier.

`customer_city`

Customer city.

`customer_state`

Customer state.

`product_id`

Product identifier.

`seller_id`

Seller identifier.

`product_category_name`

Original product category name from the source data.

`product_category`

Preferred product-category field for analysis.

This field uses the English category name when available and otherwise falls back to the original category name.

`item_price`

Product price for this individual order item.

Use this field for item-level product revenue.

`item_freight_value`

Freight value associated with this individual order item.

`total_item_value`

Item price plus freight value.

`shipping_limit_date`

Shipping-limit timestamp for the item.

### Important rules

Use `product_category` for product-category analysis.

Do not attempt to recreate category-translation logic.

Use `item_price` as product revenue at item level.

Unless explicitly requested otherwise, revenue analysis should include only rows where `is_delivered = true`.

Count rows in this view when calculating items sold.

Do not count rows in this view as orders.

When an order count is required, use `COUNT(DISTINCT order_id)`.

Do not reference `product_category_name_english`. That column is not available in this analytical view.

Do not reference columns that are not listed above.


## `olist.ai_reviews`

### Grain

One row represents one review associated with an order.

### Use for

- Review-score analysis
- Review text analysis
- Customer-feedback analysis
- Delivery and review-score relationships
- Geographic review analysis
- Order-level review analysis

### Available fields

`review_id`

Unique review identifier.

`order_id`

Identifier of the order associated with the review.

`review_score`

Numeric review score.

`review_comment_title`

Optional review title supplied by the customer.

`review_comment_message`

Optional review message supplied by the customer.

`review_creation_date`

Date when the review was created.

`review_answer_timestamp`

Timestamp associated with the review response process.

`order_status`

Status of the associated order.

`order_purchase_timestamp`

Purchase timestamp of the associated order.

`order_delivered_customer_date`

Timestamp when the associated order was delivered to the customer.

`order_estimated_delivery_date`

Estimated delivery date of the associated order.

`customer_unique_id`

Persistent customer identifier.

`customer_city`

Customer city.

`customer_state`

Customer state.

`item_count`

Number of order-item rows contained in the associated order.

`distinct_product_count`

Number of distinct products contained in the associated order.

`single_product_id`

Contains a product ID only when the associated order contains exactly one distinct product.

If the order contains multiple distinct products, this field is null.

### Important rules

Reviews exist at the order level.

Do not automatically attribute a review to an individual product.

Use `single_product_id` only when making product-specific conclusions from a review.

If `single_product_id` is null, do not make product-specific conclusions from that review.

A missing review title or message does not mean the customer had no opinion.

Review text may be translated into English for interpretation, but the meaning of the original text must be preserved.

Do not infer customer motivations or causal explanations from review text unless directly supported by the available data.


## General query rules

Use only:

- `olist.ai_orders`
- `olist.ai_order_items`
- `olist.ai_reviews`

Do not query raw Olist source tables.

Do not reference columns that are not explicitly listed in this document.

Generate read-only queries only.

Do not use:

- `INSERT`
- `UPDATE`
- `DELETE`
- `DROP`
- `ALTER`
- `CREATE`
- `TRUNCATE`

If the available views cannot answer the user's question, do not invent an answer.