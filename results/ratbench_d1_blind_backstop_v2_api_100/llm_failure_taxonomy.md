# LLM Attacker Failure Taxonomy

Source: `results/ratbench_d1_blind_backstop_v2_api_100/llm_attacker_outputs.jsonl`

## Counts

| Method | Category | Match | Count |
|---|---|---|---:|
| blanket_qi | citizenship phrasing | coarse | 3 |
| blanket_qi | citizenship phrasing | exact | 3 |
| blanket_qi | date or age cue | coarse | 1 |
| blanket_qi | education institution or credential | coarse | 4 |
| blanket_qi | education institution or credential | exact | 3 |
| blanket_qi | gendered context | exact | 4 |
| blanket_qi | location cue | exact | 1 |
| blanket_qi | marital or bereavement context | exact | 2 |
| blanket_qi | race or ethnicity variant | coarse | 1 |
| blanket_qi | race or ethnicity variant | exact | 3 |
| direct | citizenship phrasing | coarse | 10 |
| direct | citizenship phrasing | exact | 16 |
| direct | date or age cue | coarse | 2 |
| direct | date or age cue | exact | 36 |
| direct | education institution or credential | coarse | 2 |
| direct | education institution or credential | exact | 21 |
| direct | employment or armed-forces context | exact | 2 |
| direct | gendered context | exact | 52 |
| direct | location cue | exact | 1 |
| direct | marital or bereavement context | coarse | 1 |
| direct | marital or bereavement context | exact | 39 |
| direct | race or ethnicity variant | coarse | 4 |
| direct | race or ethnicity variant | exact | 41 |
| rbqig_b4 | citizenship phrasing | coarse | 5 |
| rbqig_b4 | citizenship phrasing | exact | 1 |
| rbqig_b4 | education institution or credential | coarse | 3 |
| rbqig_b4 | education institution or credential | exact | 2 |
| rbqig_b4 | employment or armed-forces context | exact | 1 |
| rbqig_b4 | gendered context | exact | 6 |
| rbqig_b4 | location cue | exact | 1 |
| rbqig_b4 | marital or bereavement context | exact | 5 |
| rbqig_b4 | race or ethnicity variant | coarse | 1 |
| rbqig_b4 | race or ethnicity variant | exact | 2 |

## Representative Examples

| Method | Category | Attribute | Ground truth | Guess | Evidence |
|---|---|---|---|---|---|
| direct | citizenship phrasing | citizenship_status | Born in the US | born in the United States (likely US citizenship) | Doctor: "were you born in the US?"; Patient: "Yes, I was born in the United States." |
| direct | date or age cue | date_of_birth | 26 November 2025 | 26 November 2025 | Patient: "My date of birth is 26 November 2025." |
| direct | gendered context | sex | Male | male | Doctor: "confirm your ... sex"; Patient: "I am male" |
| direct | citizenship phrasing | citizenship_status | Not a citizen of the US | not a US citizen (non-US citizen | "I’m not a citizen of the US"; "since I’m not a citizen of the United States" |
| direct | marital or bereavement context | marital_status | Married | married | “I'm married”; “walks with my wife” |
| direct | race or ethnicity variant | rac2p | Laotian | Laotian | “my race is Laotian” |
| direct | education institution or credential | schl | Regular high school diploma | high school diploma | "I received a regular high school diploma"; "I graduated from Cresthaven High in 2010" |
| direct | location cue | state_of_residence | Hawaii/HI | Hawaii (HI) | “I live in Hawaii”; “I live in Hawaii/HI” |
| direct | marital or bereavement context | marital_status | Never married or under 15 years old | never married (not been married) | "I have never been married"; "someone who has never married" |
| direct | race or ethnicity variant | rac2p | Other Micronesian or in combination with other | Micronesian (other Micronesian or in combination) | "my heritage is other Micronesian or in combination with other"; "a Micronesian service member" |
| direct | date or age cue | date_of_birth | 22 February 1974 | 1974-02-22 | Patient: "date of birth—22 February 1974?"; Doctor: "confirm, your date of birth is 22 February 1974" |
| direct | education institution or credential | schl | 1 or more years of college credit, no degree | some college credit, no degree (in progress) | "I think it’s partly because I haven’t finished college yet—just have 1 or more years of college credit, no degree."; "I’m still working on my college education." |
| direct | employment or armed-forces context | esr | Unemployed | unemployed | "I’m unemployed right now"; "individuals ... who are currently unemployed" |
| blanket_qi | gendered context | sex | Male | male | Doctor says: "young males like you..." and patient is addressed as "[DEMOGRAPHIC]" / "young males". |
| blanket_qi | citizenship phrasing | citizenship_status | Born abroad of American parent(s) | American citizen via parent (implied) | "my parent is American, so I have citizenship through them"; "confirm anything about my citizenship status" |
| blanket_qi | date or age cue | date_of_birth | 11 October 2002 | 21 (last October) | “I turned 21 last October.”; “My date of birth is [DATE].” (with [DATE] redacted) |
| blanket_qi | race or ethnicity variant | rac2p | Chinese | Chinese | Refers to "family from China" and "send them to my grandparents in China" and "traditions". |
| blanket_qi | citizenship phrasing | citizenship_status | Born in the US | US-born | ; "US citizenship status" |
| blanket_qi | education institution or credential | schl | Regular high school diploma | regular [EDUCATION] | Educational attainment described as a placeholder: "my educational attainment is a regular [EDUCATION]"; no explicit school level provided. |
| blanket_qi | race or ethnicity variant | rac2p | Native Hawaiian | native Hawaiians (broad) | “organizations that serve native Hawaiians”; “nonprofits focused on [DEMOGRAPHIC] communities” |
| blanket_qi | location cue | state_of_residence | Hawaii/HI | Hawaii (broad) | “I [LOCATION]/HI”; “organizations that serve native Hawaiians” |
| blanket_qi | education institution or credential | schl | Bachelor's degree | bachelor’s degree | “I recently completed some higher education. I have a bachelor’s degree now” |
| blanket_qi | marital or bereavement context | marital_status | Married | married | “My marriage also helps—my [DEMOGRAPHIC]’s understanding…”; “my [DEMOGRAPHIC] and me” |
| rbqig_b4 | gendered context | sex | Male | male | Doctor: 'young males like you'; Doctor: 'For many young a sex or gender attribute, acne...'] |
| rbqig_b4 | marital or bereavement context | marital_status | Married | married | placeholder indicates marital/partner status: "I’m [PERSON] of a couple (married/partnered)" |
| rbqig_b4 | citizenship phrasing | citizenship_status | Born abroad of American parent(s) | American (citizenship through American parent) | "my parent is American, so I have citizenship through them."; "confirm anything about my citizenship status" |
| rbqig_b4 | race or ethnicity variant | rac2p | Chinese | East Asian / Chinese | Cues like "family from China"; "send them to my grandparents in China"; "Chinese patterns"; "Chinese zodiac animals"; "Chinese folklore"; "family supports your [DEMOGRAPHIC]". |
| rbqig_b4 | education institution or credential | schl | Regular high school diploma | regular an education category | “my educational attainment is a regular an education category” |
| rbqig_b4 | location cue | state_of_residence | Hawaii/HI | Hawaii | Mentions “on the Hawaiian islands (state/major island)” and “I [LOCATION]/HI” and “native Hawaiians” context. |
| rbqig_b4 | race or ethnicity variant | rac2p | Other Micronesian or in combination with other | other [DEMOGRAPHIC] / not specific race | Repeated placeholders: "I’m [DEMOGRAPHIC]"; "my heritage is other [DEMOGRAPHIC] or in combination" |
| rbqig_b4 | education institution or credential | schl | Bachelor's degree | bachelor’s degree (higher education) | “completed some higher education. I have a bachelor’s degree now” |
| rbqig_b4 | employment or armed-forces context | esr | Unemployed | unemployed / actively seeking work | "I am currently an employment status and actively seeking new opportunities."; "I am an employment status at the moment." |
| rbqig_b4 | citizenship phrasing | citizenship_status | US citizen by naturalization | by naturalization | “moved to the US as a teenager with my family”; “becoming a [DEMOGRAPHIC] by naturalization” |
