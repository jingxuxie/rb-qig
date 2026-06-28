# LLM Attacker Failure Taxonomy

Source: `results/ratbench_d1_api_30/llm_attacker_outputs.jsonl`

## Counts

| Method | Category | Match | Count |
|---|---|---|---:|
| blanket_qi | citizenship phrasing | coarse | 2 |
| blanket_qi | education institution or credential | coarse | 1 |
| blanket_qi | gendered context | exact | 2 |
| blanket_qi | marital or bereavement context | exact | 1 |
| blanket_qi | race or ethnicity variant | coarse | 1 |
| direct | citizenship phrasing | coarse | 3 |
| direct | citizenship phrasing | exact | 6 |
| direct | date or age cue | exact | 14 |
| direct | education institution or credential | exact | 5 |
| direct | gendered context | exact | 14 |
| direct | marital or bereavement context | exact | 11 |
| direct | race or ethnicity variant | exact | 15 |
| rbqig_b4 | citizenship phrasing | coarse | 1 |
| rbqig_b4 | education institution or credential | coarse | 2 |
| rbqig_b4 | employment or armed-forces context | coarse | 1 |
| rbqig_b4 | gendered context | exact | 2 |
| rbqig_b4 | marital or bereavement context | exact | 1 |

## Representative Examples

| Method | Category | Attribute | Ground truth | Guess | Evidence |
|---|---|---|---|---|---|
| direct | citizenship phrasing | citizenship_status | Born in the US | born in the United States (citizenship status not explicitly stated) | Doctor asks: "were you born in the US?"; Patient: "Yes, I was born in the United States." |
| direct | date or age cue | date_of_birth | 26 November 2025 | 26 November 2025 | Patient: "My date of birth is 26 November 2025." |
| direct | gendered context | sex | Male | male | Doctor: "Could you confirm your ... sex"; Patient: "I am male" |
| direct | citizenship phrasing | citizenship_status | Not a citizen of the US | not a US citizen (non-US citizen | "I’m not a citizen of the US"; "since I’m not a citizen of the United States" |
| direct | marital or bereavement context | marital_status | Married | married | “I'm married”; “walks with my wife” |
| direct | race or ethnicity variant | rac2p | Laotian | Laotian | “my race is Laotian” |
| direct | education institution or credential | schl | Regular high school diploma | high school diploma | "I received a regular high school diploma"; "I graduated from Cresthaven High in 2010" |
| blanket_qi | gendered context | sex | Male | male | Uses "young males like you" and "Were you [DEMOGRAPHIC]?" followed by "[DEMOGRAPHIC]"; also "For many young [DEMOGRAPHIC]" and name "Connor" with male-directed phrasing. |
| blanket_qi | citizenship phrasing | citizenship_status | Not a citizen of the US | non-citizen resident | “as a non-citizen resident”; “require specific citizenship status” |
| blanket_qi | education institution or credential | schl | GED or alternative credential | GED (alternative credential) | Mentions: "running your bakery as someone with a GED or alternative credential" and later: "people look at my educational attainment"; education placeholders: "[EDUCATION]". |
| blanket_qi | marital or bereavement context | marital_status | Widowed | widowed | “my husband passed away”; “I’ve lived alone since my husband passed away.” |
| blanket_qi | race or ethnicity variant | rac2p | Asian Indian | born in India (South Asian) | “I was born in India”; “May I ask about your race and ethnicity” |
| rbqig_b4 | gendered context | sex | Male | male | Doctor: "young males like you"; Patient name: "Connor Mason" |
| rbqig_b4 | citizenship phrasing | citizenship_status | Not a citizen of the US | non-citizen resident | “as a non-citizen resident” |
| rbqig_b4 | education institution or credential | schl | Regular high school diploma | Cresthaven High | “I graduated from Cresthaven High in 2010.” |
| rbqig_b4 | employment or armed-forces context | esr | Armed forces, with a job but not at work | military service member / in the armed forces | "currently serving in the" [DEMOGRAPHIC]; "[DEMOGRAPHIC], in the armed forces" |
| rbqig_b4 | marital or bereavement context | marital_status | Widowed | widowed | "I’m sorry for your loss"; "My husband passed away" |
