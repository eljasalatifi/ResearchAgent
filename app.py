import os
import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import markdown as md_lib
from fpdf import FPDF

st.set_page_config(page_title="ResearchAgent", layout="wide")

st.session_state.setdefault("report", None)
st.session_state.setdefault("running", False)

api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    st.error("GROQ_API_KEY environment variable is not set.")
    st.stop()

client = Groq(api_key=api_key)

st.title("ResearchAgent")

topic = st.text_input("Research Topic", placeholder="Enter any topic to research...")
depth = st.selectbox("Depth", ["Quick (3 searches)", "Standard (5 searches)", "Deep (8 searches)"])

depth_map = {
    "Quick (3 searches)": 3,
    "Standard (5 searches)": 5,
    "Deep (8 searches)": 8,
}
iterations = depth_map[depth]

run = st.button("Run Agent", disabled=st.session_state.running)

if run and topic:
    st.session_state.running = True
    st.session_state.report = None

    all_facts = []
    all_sources = []

    with st.status("Agent working...", expanded=True) as status:
        for i in range(iterations):
            st.write(f"**Iteration {i + 1}/{iterations}** — deciding what to search for...")

            context_str = "\n".join(all_facts) if all_facts else "No facts gathered yet."

            try:
                query_response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a research assistant. Given a topic and already gathered facts, decide the single most useful search query to find new and relevant information. Respond with ONLY the search query, nothing else.",
                        },
                        {
                            "role": "user",
                            "content": f"Topic: {topic}\n\nAlready gathered:\n{context_str}\n\nWhat should I search for next?",
                        },
                    ],
                )
            except Exception as e:
                st.error(f"Groq API error: {e}")
                st.stop()

            query = query_response.choices[0].message.content.strip()
            st.write(f"**Searching:** `{query}`")

            results = []
            try:
                with DDGS() as ddgs:
                    results = list(ddgs.text(query, max_results=3))
            except Exception:
                pass

            if not results:
                st.write("No search results returned — continuing to next iteration.")
                continue

            for r in results:
                if r.get("href"):
                    all_sources.append(r["href"])

            results_text = "\n\n".join(
                f"Title: {r.get('title', '')}\nURL: {r.get('href', '')}\nSnippet: {r.get('body', '')}"
                for r in results
            )

            st.write(f"**Extracting facts** from {len(results)} result(s)...")

            try:
                facts_response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a research assistant. Extract the key facts from the search results that are directly relevant to the topic. List each distinct fact on its own line starting with a dash.",
                        },
                        {
                            "role": "user",
                            "content": f"Topic: {topic}\n\nSearch Results:\n{results_text}\n\nExtract key facts:",
                        },
                    ],
                )
            except Exception as e:
                st.error(f"Groq API error: {e}")
                st.stop()

            facts = facts_response.choices[0].message.content.strip()
            all_facts.append(f"[Search {i + 1}: {query}]\n{facts}")
            st.write(f"**Facts captured** for iteration {i + 1}.")

        status.update(label="Synthesising final report...", state="running")
        st.write("**Synthesising** all gathered facts into the final report...")

        full_context = "\n\n".join(all_facts)
        sources_list = "\n".join(list(dict.fromkeys(all_sources)))

        try:
            synthesis_response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a research analyst. Write a comprehensive, well-structured markdown report "
                            "based solely on the gathered facts provided. The report must contain: "
                            "a title using a # heading, an Executive Summary section, clearly labelled ## sections "
                            "for each major finding or theme, a Conclusions section, and a Sources section that "
                            "lists every URL. Use proper markdown formatting throughout."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Topic: {topic}\n\n"
                            f"Gathered Facts:\n{full_context}\n\n"
                            f"Sources visited:\n{sources_list}\n\n"
                            "Write the complete markdown report:"
                        ),
                    },
                ],
            )
        except Exception as e:
            st.error(f"Groq API error: {e}")
            st.stop()

        st.session_state.report = synthesis_response.choices[0].message.content.strip()
        status.update(label="Research complete!", state="complete")

    st.session_state.running = False

if st.session_state.report:
    st.markdown(st.session_state.report)

    safe_name = "".join(c if c.isalnum() or c in " _-" else "" for c in topic).strip().replace(" ", "_")
    base_name = f"research_{safe_name[:60]}" if safe_name else "research_report"

    html_content = md_lib.markdown(st.session_state.report)
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.write_html(html_content)
    pdf_bytes = bytes(pdf.output())

    st.download_button(
        label="Download Report as PDF",
        data=pdf_bytes,
        file_name=f"{base_name}.pdf",
        mime="application/pdf",
    )
