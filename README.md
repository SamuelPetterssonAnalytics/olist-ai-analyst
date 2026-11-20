# Olist AI Data Analyst

Python | PostgreSQL | LLM | OpenAI API | Streamlit | Text-to-SQL | SQL Validation

A small AI data analyst prototype that connects an LLM to a PostgreSQL database containing the Olist Brazilian e-commerce dataset.

The goal was not to build or train an AI model from scratch. Instead, the goal was to understand how an existing LLM can be connected to structured business data, given business context, restricted to approved data, and used to answer natural-language analytical questions.

The application allows a user to ask questions in plain English. The LLM then generates PostgreSQL SQL, the query is validated and executed using a read-only database account, and the result is sent back to the LLM to provide an explanation.

# Architecture

```text
User question
    ↓
Streamlit interface
    ↓
Analyst workflow
    ↓
LLM generates SQL
    ↓
SQL validation
    ↓
Read-only PostgreSQL
    ↓
Query result
    ↓
LLM interpretation
    ↓
Business-friendly answer
```

# Main design decisions

## Curated analytical views

The LLM does not query the raw Olist tables directly.

Three analytical views provide a simpler and more controlled data layer:

- `olist.ai_orders` — one row per order
- `olist.ai_order_items` — one row per order item
- `olist.ai_reviews` — one row per review

The views handle some common joins and calculations before the data reaches the LLM.

## Business definitions

`config/business_definitions.md` defines how important business concepts should be interpreted.

Examples:

- Revenue is based on delivered orders unless otherwise requested.
- Product revenue excludes freight.
- Repeat customers are identified using `customer_unique_id`.
- A repeat customer has more than one distinct delivered order.

## Data model

`config/data_model.md` tells the LLM which analytical views and columns are available and when they should be used.

This reduces the risk of the model inventing columns or selecting an inappropriate data source.

## Read-only database access

The application connects to PostgreSQL through a separate read-only database user.

The account has access only to approved analytical views and cannot directly query the raw Olist tables.

This provides an additional layer of protection alongside the SQL validator.

## SQL validation

Generated SQL is parsed before execution using `sqlglot`.

The validator:

- Allows only a single read-only query.
- Restricts access to approved analytical views.
- Blocks raw source tables.
- Blocks modifying SQL such as `DELETE`, `UPDATE`, or `DROP`.
- Supports CTEs while still validating their underlying data sources.

# Project structure

```text
olist-ai-analyst/
│
├── app/
│   ├── analyst.py
│   ├── db.py
│   ├── llm.py
│   ├── main.py
│   ├── query_executor.py
│   ├── sql_generator.py
│   └── sql_validator.py
│
├── config/
│   ├── business_definitions.md
│   └── data_model.md
│
├── sql/
│   └── views.sql
│
├── tests/
│   └── evaluation_questions.md
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

# Application

`main.py` provides the Streamlit interface.

`analyst.py` coordinates the complete analysis workflow.

`sql_generator.py` combines the user question, business definitions, and data model into a prompt and asks the LLM to generate PostgreSQL SQL.

`sql_validator.py` checks generated SQL before it is allowed to reach the database.

`query_executor.py` executes validated SQL against PostgreSQL.

`db.py` creates the PostgreSQL connection using stored credentials.

`llm.py` handles communication with the LLM API.

# Evaluation

The prototype was manually evaluated using questions covering different areas:

- Revenue / products
- Orders / customers
- Delivery
- Reviews
- Unsupported or ambiguous questions

Where possible, results were compared against previous independent SQL analysis of the same Olist dataset.

The evaluation also exposed issues that were then corrected.

The complete evaluation notes are available in `tests/evaluation_questions.md`.

# Setup

## Requirements

- Python
- PostgreSQL
- Olist data loaded into PostgreSQL
- Access to an LLM API

Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Environment variables

Copy `.env.example` to `.env` and provide your own credentials:

```text
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database
DB_USER=your_readonly_user
DB_PASSWORD=your_password

OPENAI_API_KEY=your_openai_api_key
LLM_MODEL=your_model_name
```

The real `.env` file is excluded from Git and should never be committed.

## Database views

Run:

```text
sql/views.sql
```

against the PostgreSQL database after the underlying Olist tables have been loaded.

The SQL creates:

```text
olist.ai_orders
olist.ai_order_items
olist.ai_reviews
```

## Read-only user

The application should use a dedicated PostgreSQL account with access only to the analytical views.

Example:

```sql
CREATE USER olist_ai_readonly
WITH PASSWORD 'your_password';

GRANT CONNECT
ON DATABASE your_database
TO olist_ai_readonly;

GRANT USAGE
ON SCHEMA olist
TO olist_ai_readonly;

GRANT SELECT
ON olist.ai_orders,
   olist.ai_order_items,
   olist.ai_reviews
TO olist_ai_readonly;
```

## Running the application

Activate the Python environment and run:

```bash
streamlit run app/main.py
```

Streamlit will launch the application locally in the browser.

# Limitations

This is a portfolio prototype rather than a production system.

- Only three curated analytical views are available.
- Product names are not available, so some product-level answers use product IDs.
- Evaluation is currently manual rather than automated.
- Generated SQL can still vary between model calls.

# Development notes

The project was built with AI-assisted development.

I used AI to help with implementation, debugging, and learning.

The main objective was to understand and learn how this type of AI-enabled data tool works.