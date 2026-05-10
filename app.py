import os
import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import markdown as md_lib
from fpdf import FPDF
import ui

st.set_page_config(
    page_title="ResearchAgent",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.session_state.setdefault("report", None)
st.session_state.setdefault("running", False)
st.session_state.setdefault("stats", {})
st.session_state.setdefault("last_topic", "")

ui.inject_styles()

api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    st.error("GROQ_API_KEY environment variable is not set.")
    st.stop()

client = Groq(api_key=api_key)

ui.header()

ui.card_open()

topic = st.text_input(
    "Research Topic",
    placeholder="e.g. The geopolitical impact of artificial intelligence on global trade…",
)

depth = st.radio(
    "Research Depth",
    ["⚡  Quick · 3 searches", "🔬  Standard · 5 searches", "🧪  Deep · 8 searches"],
    horizontal=True,
)

depth_map = {
    "⚡  Quick · 3 searches": 3,
    "🔬  Standard · 5 searches": 5,
    "🧪  Deep · 8 searches": 8,
}
iterations = depth_map[depth]

ui.spacer(0.5)
run = st.button("Run Agent →", disabled=st.session_state.running, use_container_width=True)

ui.card_close()

if run and topic:
    st.session_state.running = True
    st.session_state.report = None
    st.session_state.last_topic = topic

    all_facts = []
    all_sources = []
    total_facts = 0

    progress_bar = st.progress(0)

    with st.status("Initialising agent…", expanded=True) as status:

        for i in range(iterations):
            status.update(label=f"Iteration {i + 1} / {iterations}…", state="running")

            ui.log("🧠", f"<b>Iteration {i + 1} / {iterations}</b> — analysing context and planning next query…")

            context_str = "\n".join(all_facts) if all_facts else "No prior research yet."

            try:
                qr = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a research assistant. Given a topic and already gathered facts, decide the single most useful web search query to discover new, relevant information. Respond with ONLY the search query — no explanation, no quotes.",
                        },
                        {
                            "role": "user",
                            "content": f"Topic: {topic}\n\nAlready gathered:\n{context_str}\n\nNext search query:",
                        },
                    ],
                )
            except Exception as e:
                st.error(f"Groq API error: {e}")
                st.stop()

            query = qr.choices[0].message.content.strip()
            ui.log("🔍", f"Searching &nbsp;<code>{query}</code>")

            results = []
            try:
                with DDGS() as ddgs:
                    results = list(ddgs.text(query, max_results=3))
            except Exception:
                pass

            if not results:
                ui.log("⚠️", '<span class="ra-warn">No results returned</span> — skipping iteration.')
                progress_bar.progress((i + 1) / iterations)
                continue

            for r in results:
                if r.get("href"):
                    all_sources.append(r["href"])

            ui.log("📄", f"Reading <b>{len(results)}</b> source(s) and extracting key facts…")

            results_text = "\n\n".join(
                f"Title: {r.get('title', '')}\nURL: {r.get('href', '')}\nSnippet: {r.get('body', '')}"
                for r in results
            )

            try:
                fr = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a research assistant. Extract every distinct, factual piece of information from these search results that is relevant to the topic. Write each fact on its own line starting with a dash (-). Be thorough.",
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

            facts = fr.choices[0].message.content.strip()
            fact_count = max(1, facts.count("\n-") + 1)
            total_facts += fact_count
            all_facts.append(f"[Search {i + 1}: {query}]\n{facts}")

            ui.log("✅", f'<span class="ra-ok">+{fact_count} facts captured</span> &nbsp;·&nbsp; iteration {i + 1} complete.')
            progress_bar.progress((i + 1) / iterations)

        status.update(label="Writing final report…", state="running")
        ui.log("✍️", "<b>Synthesising</b> all gathered research into a structured report…")

        full_context = "\n\n".join(all_facts)
        sources_list = "\n".join(list(dict.fromkeys(all_sources)))

        try:
            sr = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert research analyst. Produce a comprehensive, well-structured markdown report from the gathered facts. "
                            "Use this structure exactly: # Title, ## Executive Summary, ## [2-4 themed sections for major findings], "
                            "## Conclusions, ## Sources (a bullet list of URLs). "
                            "Write in a clear, authoritative tone. Use markdown tables, bullet lists, and bold text where they add clarity."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Topic: {topic}\n\n"
                            f"Gathered Research:\n{full_context}\n\n"
                            f"All sources visited:\n{sources_list}\n\n"
                            "Write the complete report:"
                        ),
                    },
                ],
            )
        except Exception as e:
            st.error(f"Groq API error: {e}")
            st.stop()

        st.session_state.report = sr.choices[0].message.content.strip()
        st.session_state.stats = {
            "iterations": iterations,
            "sources": len(set(all_sources)),
            "facts": total_facts,
        }

        ui.log("🎉", '<span class="ra-ok">Report complete.</span> Scroll down to read.')
        status.update(label="✅ Research complete", state="complete")

    st.session_state.running = False

if st.session_state.report:
    s = st.session_state.stats
    ui.section("Research Report")
    ui.stats(s.get("iterations", 0), s.get("sources", 0), s.get("facts", 0))

    report_html = md_lib.markdown(st.session_state.report, extensions=["extra"])
    ui.report(report_html)

    ui.spacer(1.5)

    safe_name = "".join(c if c.isalnum() or c in " _-" else "" for c in st.session_state.last_topic).strip().replace(" ", "_")
    base_name = f"research_{safe_name[:60]}" if safe_name else "research_report"

    html_content = md_lib.markdown(st.session_state.report)
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.write_html(html_content)
    pdf_bytes = bytes(pdf.output())

    st.download_button(
        label="⬇  Download Report as PDF",
        data=pdf_bytes,
        file_name=f"{base_name}.pdf",
        mime="application/pdf",
        use_container_width=True,
    )
