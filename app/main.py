import pandas as pd
import streamlit as st

from analyst import answer_question


st.set_page_config(
    page_title="Olist AI Data Analyst",
    page_icon="📊",
    layout="wide"
)

st.title("Olist AI Data Analyst")

st.write(
    "Ask business questions about the Olist Brazilian e-commerce dataset. "
    "The analyst generates read-only SQL against approved analytical views."
)

question = st.text_input(
    "Ask a business question",
    placeholder="Which five product categories generated the most revenue?"
)

if st.button("Analyze"):
    if not question.strip():
        st.warning("Enter a question first.")

    else:
        with st.spinner("Analyzing..."):
            try:
                result = answer_question(question)

                st.subheader("Analyst answer")
                st.write(result["answer"])

                if result["rows"] is not None:
                    st.subheader("Query result")

                    dataframe = pd.DataFrame(
                        result["rows"],
                        columns=result["columns"]
                    )

                    st.dataframe(
                        dataframe,
                        use_container_width=True
                    )

                if result["sql"]:
                    with st.expander("View generated SQL"):
                        st.code(
                            result["sql"],
                            language="sql"
                        )

            except Exception as error:
                st.error(f"Analysis failed: {error}")