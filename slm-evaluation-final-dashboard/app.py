"""Read-only SLM evaluation dashboard. No model inference or GPU required."""
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title="SLM Evaluation | Qwen2.5 0.5B", page_icon="📊", layout="wide")

@st.cache_data
def load_data():
    raw = pd.read_csv(ROOT / "data" / "raw_generation_results.csv")
    review = pd.read_csv(ROOT / "reports" / "human_review_provisional.csv")
    checks = pd.read_csv(ROOT / "data" / "format_check_details.csv")
    required = {"test_id", "category", "condition", "repeat_index", "prompt", "response", "latency_sec", "generated_tokens", "token_limit_hit"}
    missing = required - set(raw.columns)
    if missing:
        raise ValueError(f"Missing generation columns: {sorted(missing)}")
    return raw, review, checks

try:
    raw, review, checks = load_data()
except (OSError, ValueError, pd.errors.ParserError) as exc:
    st.error(f"Could not load evaluation results: {exc}")
    st.stop()

primary = raw[raw["repeat_index"] == 1].copy()
conditions = ["A_baseline", "B_system"]
labels = {"A_baseline": "A · Baseline", "B_system": "B · System prompt"}

st.title("Small Language Model Evaluation")
st.caption("Qwen/Qwen2.5-0.5B-Instruct · Saved results only · No live model inference")
st.info("Exploratory comparison: 10 prompts per condition and 6 extra repeat generations. This is not a comprehensive benchmark. Human scores are provisional, single-reviewer assessments.")

st.subheader("Primary comparison")
summary = primary.groupby("condition", as_index=False).agg(
    prompts=("test_id", "count"), mean_latency_sec=("latency_sec", "mean"),
    mean_generated_tokens=("generated_tokens", "mean"),
    token_limit_hits=("token_limit_hit", "sum"),
)
scores = review.groupby("condition", as_index=False)["total_quality_0_8"].mean()
summary = summary.merge(scores, on="condition", how="left")
summary["condition"] = summary["condition"].map(labels)
summary = summary.rename(columns={"condition":"Condition", "prompts":"Primary outputs", "mean_latency_sec":"Mean latency (s)", "mean_generated_tokens":"Mean output tokens", "token_limit_hits":"Token cap hits", "total_quality_0_8":"Mean reviewed quality (/8)"})
st.dataframe(summary.round(2), use_container_width=True, hide_index=True)
st.caption("Latency reflects the recorded Colab run and is not a portable deployment benchmark. A token cap hit signals possible truncation, not proof of an incomplete answer.")

left, right = st.columns(2)
with left:
    st.markdown("**Mean latency (seconds)**")
    st.bar_chart(primary.groupby("condition")["latency_sec"].mean(), horizontal=True)
with right:
    st.markdown("**Mean reviewed quality (/8)**")
    st.bar_chart(review.groupby("condition")["total_quality_0_8"].mean(), horizontal=True)

st.subheader("Explore individual responses")
category_options = sorted(primary["category"].dropna().unique().tolist())
selected_categories = st.multiselect("Prompt categories", category_options, default=category_options)
filtered = primary[primary["category"].isin(selected_categories)]
ids = sorted(filtered["test_id"].unique().tolist())
if not ids:
    st.warning("No prompts match the selected categories.")
else:
    chosen = st.selectbox("Test case", ids, format_func=lambda i: f"#{i} · {primary.loc[primary.test_id == i, 'category'].iloc[0]}")
    subset = primary[primary.test_id == chosen]
    st.markdown("**Prompt**")
    st.write(subset["prompt"].iloc[0])
    st.caption("Expected answer notes: " + str(subset["expected_answer_notes"].iloc[0]))
    a, b = st.columns(2)
    for col, cond in [(a, "A_baseline"), (b, "B_system")]:
        with col:
            st.markdown(f"**{labels[cond]}**")
            item = subset[subset.condition == cond]
            if item.empty:
                st.warning("No recorded response")
                continue
            r = item.iloc[0]
            st.text_area("Recorded response", value=str(r.response), height=300, key=f"response_{cond}_{chosen}")
            st.caption(f"{r.latency_sec:.2f}s · {int(r.generated_tokens)} generated tokens · Token cap hit: {bool(r.token_limit_hit)}")
            reviewed = review[(review.test_id == chosen) & (review.condition == cond)]
            if not reviewed.empty:
                v = reviewed.iloc[0]
                st.metric("Provisional reviewed score", f"{v.total_quality_0_8:g}/8")
                st.write("**Reviewer notes:**", v.reviewer_notes)

st.subheader("Review dimensions")
review_cols = ["factual_correctness_0_2", "relevance_completeness_0_2", "instruction_following_0_2", "clarity_0_2"]
st.dataframe(review.groupby("condition")[review_cols].mean().round(2), use_container_width=True)
st.caption("Each dimension was manually scored from 0 to 2. Scores are not independent external validation.")

st.subheader("Repeatability and format checks")
repeats = raw[raw.repeat_index > 1]
st.write(f"{len(repeats)} additional generations for {repeats.test_id.nunique()} test cases. Repeated outputs are not part of the primary 10-prompt score averages.")
if not checks.empty:
    visible = [c for c in ["test_id", "condition", "repeat_index", "two_sentence_check", "three_numbered_items_check"] if c in checks]
    st.dataframe(checks[visible], use_container_width=True, hide_index=True)
    st.caption("Blank checks mean the rule was not applicable; zero means the specific automated check did not pass. These are narrow formatting checks, not factual accuracy scores.")

st.subheader("Known failure cases and limitations")
st.markdown("""- **Data leakage:** Responses confused machine learning leakage with exposure of private information.
- **Exact formatting:** The two-sentence database instruction was not consistently followed.
- **Output truncation:** Many responses reached the configured 160-token cap.
- **Generalization:** Ten prompts and one small model cannot establish broad model reliability or prompt superiority.
- **Review:** The manual rubric has one provisional reviewer; scores should not be presented as objective ground truth.""")
st.caption("Source: saved generation logs, automated checks, and provisional review included in this repository. See reports/final_evaluation_report.md for details.")
