# Final evaluation report

## Research question
Does a concise system instruction improve output quality and instruction following compared with baseline prompting for `Qwen/Qwen2.5-0.5B-Instruct` on a fixed ten-prompt test set?

## Design
- One model; ten prompts covering explanations, arithmetic, formatting, code, and uncertainty.
- Two primary conditions: A_baseline and B_system, with paired prompt seeds and one recorded primary generation per condition per prompt (20 primary generations).
- Six additional B_system generations for three selected prompts, producing 26 generations overall. Repeats are not a full factorial comparison.
- Colab Tesla T4; sampling temperature 0.2, top_p 0.9, max_new_tokens 160. Latency excludes model loading.
- Automated operational and format checks; a separate **provisional single-reviewer** human audit of the 20 primary generations, four rubric dimensions each scored 0–2.

## Recorded operational results (primary generations only)

| Measure | A baseline | B system |
|---|---:|---:|
| Mean generation latency | 6.261 s | 5.025 s |
| Median generation latency | 5.269 s | 5.209 s |
| Mean generated tokens | 152.4 | 141.9 |
| Token cap reached | 7/10 | 6/10 |
| Nonempty responses | 10/10 | 10/10 |

The system condition had lower observed latency and token counts in this recorded run; this is descriptive and not a statistically supported performance gain. Latency is hardware/runtime dependent and should not be treated as a portable deployment benchmark. Thirteen of twenty primary generations reached the 160-token cap, limiting completeness comparisons.

## Provisional human audit

| Mean score per prompt | A baseline | B system |
|---|---:|---:|
| Factual correctness (0–2) | 1.6 | 1.3 |
| Relevance/completeness (0–2) | 1.4 | 1.5 |
| Instruction following (0–2) | 1.0 | 1.3 |
| Clarity (0–2) | 1.4 | 1.3 |
| **Total (0–8)** | **5.4** | **5.4** |

B scored higher on three prompts, lower on two, and tied on five. These judgments are provisional and subjective; they have not been independently validated by additional raters.

## Qualitative findings
- Both conditions confused machine-learning data leakage with privacy leakage on the targeted prompt.
- Both violated the exactly-two-sentences instruction, while both followed the exactly-three-numbered-items instruction.
- On the code-only task, baseline added prose; system output kept code-only formatting but included incorrect example-output comments.
- Some responses were cut short before completing requested answers; the token limit is a major confounder.
- Additional B repeats for test IDs 1, 6, and 7 yielded mean pairwise **character-sequence** similarity of 0.223, 0.322, and 0.153 respectively. This is not semantic similarity or an accuracy metric.

## Conclusion and limitations
A concise system instruction changed some behaviors and improved the provisional instruction-following mean, but **did not improve overall provisional quality** (both 5.4/8). No general improvement claim is warranted. The study is exploratory: one small model, ten hand-selected prompts, one primary sample per condition, incomplete and uneven repeats, a single provisional reviewer, stochastic decoding, and substantial output truncation. Results should not be generalized to other models or prompts.

## Reproducibility and provenance
The notebook contains experiment code and definitions. `data/raw_generation_results.csv` and `.jsonl` preserve the 26 recorded generations, while `data/runtime_metadata.json` records execution settings. The CSV and JSONL contain the same recorded response texts and experiment rows. The 20 primary response texts also match the earlier reviewed package; latency measurements differ between exports, so the operational figures in this report and `data/operational_summary.csv` are recomputed from the bundled CSV primary rows only. Human review was completed separately after generation and is distributed in `reports/`; ratings are keyed by test ID and condition and remain provisional single-reviewer judgments. No new generations were produced while packaging this repository.
