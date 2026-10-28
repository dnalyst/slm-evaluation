# Small Language Model Evaluation

**Does a concise system instruction improve the responses of a small language model?**

An exploratory, reproducible A/B evaluation of [`Qwen/Qwen2.5-0.5B-Instruct`](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct), comparing two prompting conditions across ten fixed prompts.

The project examines response quality, instruction following, generation behaviour, and repeatability. It combines recorded model outputs, operational metrics, and a provisional human evaluation.

## Key Findings

| Evaluation metric | Without system instruction | With system instruction |
|---|---:|---:|
| Mean human-review score | 5.4/8 | 5.4/8 |
| Factual correctness | 1.6/2 | 1.3/2 |
| Instruction following | 1.0/2 | 1.3/2 |

- **No improvement in overall mean score:** both conditions scored 5.4 out of 8.
- **Different strengths:** the system-instruction condition scored higher on instruction following but lower on factual correctness.
- **Generation limit:** 13 of the 20 primary responses reached the 160-token generation cap.

These results are exploratory and based on a small sample. They do not establish a general benefit or disadvantage of system prompting.

*Human-review scores are provisional, based on one reviewer's rubric assessment.*

## Project Structure

| Path | Description |
|---|---|
| `slm-evaluation-final-dashboard/notebooks/SLM_Evaluation_Final.ipynb` | Experiment, automated checks, charts, and exports |
| `slm-evaluation-final-dashboard/data/` | Recorded generations, test cases, runtime metadata, and metrics |
| `slm-evaluation-final-dashboard/reports/final_evaluation_report.md` | Findings, interpretation, and limitations |
| `slm-evaluation-final-dashboard/reports/human_review_provisional.csv` | Provisional human-review scores |
| `slm-evaluation-final-dashboard/reports/paired_score_comparison.csv` | Paired score comparison |
| `slm-evaluation-final-dashboard/figures/` | Operational evaluation charts |
| `slm-evaluation-final-dashboard/app.py` | Interactive evaluation dashboard |
| `slm-evaluation-final-dashboard/requirements.txt` | Dashboard dependencies |

## Methodology

- **Model:** Qwen2.5-0.5B-Instruct
- **Test set:** 10 fixed prompts
- **Conditions:** two prompting conditions
- **Primary evaluation:** 20 responses, one per prompt per condition
- **Repeatability check:** six additional system-condition generations across three prompts
- **Generation settings:** temperature 0.2, top-p 0.9, maximum 160 new tokens, paired primary seeds
- **Recorded hardware:** NVIDIA Tesla T4 GPU

The human-review rubric assessed four dimensions, each scored from 0 to 2:

1. Factual correctness
2. Relevance and completeness
3. Instruction following
4. Clarity

## Interactive Dashboard

The dashboard explores saved evaluation results, including response text, latency, token-limit hits, and provisional human-review scores.

It reads the bundled CSV files and does not load the language model or require a GPU.

### Run Locally

Clone the repository:

```bash
git clone https://github.com/dnalyst/slm-evaluation.git
cd slm-evaluation/slm-evaluation-final-dashboard
```

Install the dependencies and start the dashboard:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Reproducing the Experiment

1. Open `slm-evaluation-final-dashboard/notebooks/SLM_Evaluation_Final.ipynb` in Google Colab.
2. Select a GPU runtime if available; the original recorded run used a Tesla T4.
3. Run the notebook cells in order.
4. Review the generated outputs and exported results.

Generation is stochastic, and differences in hardware, package versions, or runtime environments may affect subsequent runs.

**Important:** The bundled CSV files and reports document the original recorded run. Running the notebook again produces new generations and does not automatically reproduce the separate provisional human review.

## Data Provenance and Limitations

- The raw CSV and JSONL files contain the same 26 recorded generations.
- The 20 primary response texts match the earlier reviewed package.
- Latency measurements differ between exports. The operational summary, report, and figures use latency values recalculated from the bundled raw CSV, filtered to `repeat_index == 1`.
- Human-review scores represent a provisional, single-reviewer assessment, not an automated or independently validated benchmark.
- The small prompt set and token-limit hits constrain the conclusions that can be drawn.

## Scope

This project is a small-scale evaluation exercise, not a comprehensive model benchmark. Its purpose is to document a controlled comparison, examine response-level trade-offs, and make the recorded results available for inspection.

## Author

**Jahanvi Mishra**

GitHub: [@dnalyst](https://github.com/dnalyst)
