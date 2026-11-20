# Evaluation questions

Where possible, results were compared against previous independent analysis of the same dataset.

## Revenue / products

1. Which five product categories generated the most revenue?
Expected:
- Uses ai_order_items
- Uses item_price
- Filters delivered orders
- Returns five categories

Result: PASS

Note: 
- NULL product categories were excluded, so unclassified items are not represented in the ranking.
- Results matched the previous analysis.

2. Which product category sold the most items?
Expected:
- Uses ai_order_items
- Counts item rows
- Filters delivered orders

Result: PASS

## Orders / customers

3. Which five customer states had the most delivered orders?
Expected:
- Uses ai_orders
- Counts orders correctly
- Filters delivered orders

Result: PASS

4. How many repeat customers were there and what was the repeat customer percentage?
Expected:
- Uses customer_unique_id

Result: PASS after fixes

Notes:
- Added a repeat-customer definition specifying more than one distinct delivered order.
- Updated `sql_validator.py` to allow CTE aliases needed for the percentage calculation.
- Result matched previous analysis: 2,801 repeat customers.

## Delivery

5. Which five states had the longest average delivery time?
Expected:
- Uses ai_orders
- Uses delivery_days

Result: PASS

Note:
- State ranking matched the previous analysis.
- Average delivery times were about 0.3–0.5 days higher because the AI view uses exact elapsed time including partial days.

6. What percentage of delivered orders arrived late?
Expected:
- Uses late_delivery
- Uses delivered orders

Result: PASS

Note:
- Result matched previous analysis: 8.11%.

## Reviews

7. Which states had the lowest average review scores?
Expected:
- Uses ai_reviews
- Uses review_score

Result: PASS with minor issue

Notes:
- Correct ranking and useful inclusion of review counts.
- Generated SQL returned all states instead of using LIMIT 5.
- Final answer still reported the correct five lowest-scoring states.

8. Are longer delivery times associated with lower review scores?
Expected:
- Uses review/order delivery data
- Describes an association
- Does not automatically claim causation

Result: PASS

## Unsupported

9. Why did customers stop buying from Olist?
Expected:
- CANNOT_ANSWER
- Does not invent customer motivations

Result: PASS

10. What were the best products?
Expected:
- Ideally recognizes that "best" is ambiguous or clearly states what interpretation it uses

Result: PASS with a caveat

Notes:
- Analyzer interpreted "best" as highest delivered product revenue and stated this assumption.
- Returned items sold.
- Results are shown by product ID because product names are not available in the current analytical views.