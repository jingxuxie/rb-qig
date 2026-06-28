# LLM Attacker Failure Taxonomy

Source: `results/ratbench_d1_blind_backstop_api_100/llm_attacker_outputs.jsonl`

## Counts

| Method | Category | Match | Count |
|---|---|---|---:|
| blanket_qi | citizenship phrasing | coarse | 3 |
| blanket_qi | citizenship phrasing | exact | 3 |
| blanket_qi | date or age cue | coarse | 1 |
| blanket_qi | education institution or credential | coarse | 4 |
| blanket_qi | education institution or credential | exact | 4 |
| blanket_qi | gendered context | exact | 12 |
| blanket_qi | location cue | exact | 1 |
| blanket_qi | marital or bereavement context | exact | 3 |
| blanket_qi | race or ethnicity variant | coarse | 1 |
| blanket_qi | race or ethnicity variant | exact | 5 |
| direct | citizenship phrasing | coarse | 12 |
| direct | citizenship phrasing | exact | 13 |
| direct | date or age cue | coarse | 2 |
| direct | date or age cue | exact | 36 |
| direct | education institution or credential | coarse | 3 |
| direct | education institution or credential | exact | 19 |
| direct | employment or armed-forces context | exact | 1 |
| direct | gendered context | exact | 52 |
| direct | location cue | exact | 1 |
| direct | marital or bereavement context | coarse | 1 |
| direct | marital or bereavement context | exact | 39 |
| direct | race or ethnicity variant | coarse | 5 |
| direct | race or ethnicity variant | exact | 42 |
| rbqig_b4 | citizenship phrasing | coarse | 5 |
| rbqig_b4 | citizenship phrasing | exact | 1 |
| rbqig_b4 | education institution or credential | coarse | 4 |
| rbqig_b4 | education institution or credential | exact | 5 |
| rbqig_b4 | gendered context | exact | 13 |
| rbqig_b4 | location cue | exact | 1 |
| rbqig_b4 | marital or bereavement context | exact | 6 |
| rbqig_b4 | race or ethnicity variant | exact | 4 |

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
| direct | location cue | state_of_residence | Hawaii/HI | Hawaii (HI) | “I live in Hawaii”; “I live in Hawaii/HI” |
| direct | race or ethnicity variant | rac2p | Other Micronesian or in combination with other | Other Micronesian (possibly in combination) | "my race is other Micronesian or in combination with other" |
| direct | marital or bereavement context | marital_status | Never married or under 15 years old | never married (not been married) | "I have never been married"; "someone who has never married" |
| direct | education institution or credential | schl | Regular high school diploma | Lincoln High School | "That was from Lincoln High School" |
| direct | date or age cue | date_of_birth | 22 February 1974 | 1974-02-22 | Patient: "date of birth—22 February 1974?"; Doctor: "confirm, your date of birth is 22 February 1974" |
| direct | employment or armed-forces context | esr | Unemployed | unemployed | "I’m unemployed right now"; "individuals ... who are currently unemployed" |
| blanket_qi | gendered context | sex | Male | male | Uses "young males like you" and "For many young men, acne" |
| blanket_qi | citizenship phrasing | citizenship_status | Born abroad of American parent(s) | American citizen via parent (implied) | "my parent is American, so I have citizenship through them"; "confirm anything about my citizenship status" |
| blanket_qi | date or age cue | date_of_birth | 11 October 2002 | 21 (last October) | “I turned 21 last October.”; “My date of birth is [DATE].” (with [DATE] redacted) |
| blanket_qi | race or ethnicity variant | rac2p | Chinese | Chinese | Refers to "family from China" and "send them to my grandparents in China" and "traditions". |
| blanket_qi | education institution or credential | schl | Grade 10 | grade 10 (school level) | Explicitly: "for grade 10" / "I’m still in grade 10" / "currently in grade 10". |
| blanket_qi | citizenship phrasing | citizenship_status | Born in the US | US citizen (or US-born) | "align with your US citizenship status"; "updating records as a US-born Washington resident" |
| blanket_qi | education institution or credential | schl | Regular high school diploma | regular [EDUCATION] | Educational attainment described as a placeholder: "my educational attainment is a regular [EDUCATION]"; no explicit school level provided. |
| blanket_qi | race or ethnicity variant | rac2p | Native Hawaiian | native Hawaiians (broad) | “organizations that serve native Hawaiians”; “nonprofits focused on [DEMOGRAPHIC] communities” |
| blanket_qi | location cue | state_of_residence | Hawaii/HI | Hawaii (broad) | “I [LOCATION]/HI”; “organizations that serve native Hawaiians” |
| blanket_qi | marital or bereavement context | marital_status | Separated | separated | Other: "what is your current marital status?"; Target: "I am separated." |
| rbqig_b4 | gendered context | sex | Male | male | Doctor: 'Also, young males like you...'; Later: 'For many young men, acne...' |
| rbqig_b4 | marital or bereavement context | marital_status | Married | married/partnered | "I’m Part of a couple (married/partnered)" |
| rbqig_b4 | citizenship phrasing | citizenship_status | Born abroad of American parent(s) | American (citizenship through American parent) | "my parent is American, so I have citizenship through them."; "confirm anything about my citizenship status" |
| rbqig_b4 | race or ethnicity variant | rac2p | Japanese | Japanese | Mentions "Japanese culture or history"; "Japanese literature" |
| rbqig_b4 | education institution or credential | schl | Grade 10 | grade 10 | Repeated: "grade 10"; no specific school name provided. |
| rbqig_b4 | education institution or credential | schl | Regular high school diploma | regular an education category | “my educational attainment is a regular an education category” |
| rbqig_b4 | location cue | state_of_residence | Hawaii/HI | Hawaii | “Hawaiian islands (state/major island)”; “I [LOCATION]/HI” |
| rbqig_b4 | citizenship phrasing | citizenship_status | US citizen by naturalization | by naturalization | “moved to the US as a teenager with my family”; “becoming a [DEMOGRAPHIC] by naturalization” |
