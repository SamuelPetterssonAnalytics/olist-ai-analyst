# Business definitions

## Scope

This AI analyst answers business questions using the Olist Brazilian e-commerce dataset.

It should only make claims that can be supported by the available database data.

## Core

### Order

A unique order identified by `order_id`.

### Customer

`customer_unique_id` represents a persistent customer across multiple orders.

Use `customer_unique_id` when counting unique customers or analysing repeat-customer behaviour.

Do not use an order-specific customer record as evidence that two orders belong to different people.

### Repeat customer

A repeat customer is a `customer_unique_id` associated with more than one distinct delivered order.

Unless explicitly requested otherwise, repeat-customer analysis should include only orders where `order_status = 'delivered'`.
### Revenue

Product revenue represents the value of products sold, excluding freight.

Unless explicitly requested otherwise, revenue calculations include only delivered orders.

Freight is not included in product revenue unless specifically requested.

Do not use payment value as product revenue.

If a revenue analysis uses a different order status or includes multiple statuses, state the inclusion criteria clearly.

### Order count

Count unique `order_id` values.

Do not count order-item rows as orders.

If the question asks for total orders, include all order statuses unless otherwise specified.

If the question refers to completed sales or completed orders, use only orders where `order_status = 'delivered'`.

### Freight

Freight represents the freight amount recorded for an order or order item.

Do not interpret freight as the seller's actual logistics cost unless the data explicitly supports that interpretation.

### Items sold

Count order-item records associated with delivered orders unless another order status or quantity definition is explicitly requested.

Do not count cancelled or unavailable orders as completed item sales.

### Dates

Use `order_purchase_timestamp` for sales analysis and order timing.

Use the actual delivered timestamp when measuring delivery completion.

Use estimated delivery date only when comparing promised versus actual delivery.

### Product category

Use the English product category where available.

If no English category is available, retain the original category value rather than inventing a translation.

### Delivered orders

An order whose `order_status` is `delivered`.

### Reviews

Reviews are recorded at the order level.

Use `review_score`, `review_comment_title`, and `review_comment_message`
when analysing customer feedback.

If review text is written in Portuguese or another language, it may be translated to English for interpretation.

Preserve the meaning of the original review and do not add information that is not present in the text.

Reviews are connected to orders using `order_id`.

An order may contain more than one product. Therefore, a review linked to an order cannot automatically be attributed to a specific product when the order contains multiple products.

Product-level review conclusions should only be made when the relationship between the review and product is unambiguous.

### Delivery time

Delivery time is measured from `order_purchase_timestamp` to `order_delivered_customer_date`.

Use only orders with a valid actual delivery date when calculating actual delivery duration.

### Delivery delay

An order is considered late when `order_delivered_customer_date` is later than `order_estimated_delivery_date`.

Do not treat a missing actual delivery date as a late delivery automatically.

## Behaviour rules

- Do not invent values that are not represented in the data.
- Perform calculations using the database rather than estimating them.
- Clearly state the time period used in analysis.
- Distinguish calculated facts from interpretation.
- If available data cannot be found to answer a question, say so.
- Do not infer customer motivations or causes that are not observable in the dataset.
- Database access must be read-only.
- Use only the approved analytical views described in `data_model.md`.
- Do not query raw Olist source tables directly.

## Missing values

Missing values should not automatically be interpreted as zero.

A missing review comment does not mean the customer had no opinion.

A missing delivery date should not automatically be interpreted as a failed delivery.

Report relevant missing-data limitations when they materially affect the analysis.

## Interpretation rules

Calculated relationships may be described as associations or patterns.

Do not claim causation unless the available data directly supports it.

For example, if orders with longer delivery times have lower review scores, the analyst may report the association but should not automatically state that longer delivery caused the lower scores.

Do not infer customer motivations, intentions, satisfaction drivers, or business causes unless they are directly supported by available data.