# LLM Attacker Failure Taxonomy

Source: `results/ratbench_d1_api_100/llm_attacker_outputs.jsonl`

## Counts

| Method | Category | Match | Count |
|---|---|---|---:|
| blanket_qi | citizenship phrasing | coarse | 6 |
| blanket_qi | date or age cue | coarse | 1 |
| blanket_qi | education institution or credential | coarse | 3 |
| blanket_qi | education institution or credential | exact | 1 |
| blanket_qi | gendered context | exact | 3 |
| blanket_qi | location cue | exact | 1 |
| blanket_qi | marital or bereavement context | exact | 4 |
| blanket_qi | race or ethnicity variant | coarse | 2 |
| blanket_qi | race or ethnicity variant | exact | 1 |
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
| rbqig_b4 | citizenship phrasing | coarse | 6 |
| rbqig_b4 | citizenship phrasing | exact | 1 |
| rbqig_b4 | date or age cue | coarse | 1 |
| rbqig_b4 | education institution or credential | coarse | 6 |
| rbqig_b4 | employment or armed-forces context | coarse | 1 |
| rbqig_b4 | gendered context | exact | 3 |
| rbqig_b4 | location cue | exact | 1 |
| rbqig_b4 | marital or bereavement context | exact | 3 |
| rbqig_b4 | race or ethnicity variant | coarse | 1 |
| rbqig_b4 | race or ethnicity variant | exact | 1 |

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
| blanket_qi | gendered context | sex | Male | male | Uses "young males like you" and "Were you [DEMOGRAPHIC]?" followed by "[DEMOGRAPHIC]"; also "For many young [DEMOGRAPHIC]" and name "Connor" with male-directed phrasing. |
| blanket_qi | citizenship phrasing | citizenship_status | Not a citizen of the US | non-citizen resident | “as a non-citizen resident”; “require specific citizenship status” |
| blanket_qi | education institution or credential | schl | GED or alternative credential | GED (alternative credential) | Mentions: "running your bakery as someone with a GED or alternative credential" and later: "people look at my educational attainment"; education placeholders: "[EDUCATION]". |
| blanket_qi | marital or bereavement context | marital_status | Widowed | widowed | “my husband passed away”; “I’ve lived alone since my husband passed away.” |
| blanket_qi | race or ethnicity variant | rac2p | Asian Indian | born in India (South Asian) | “I was born in India”; “May I ask about your race and ethnicity” |
| blanket_qi | race or ethnicity variant | rac2p | Native Hawaiian | Native Hawaiian / cultural background (broad) | Cues: "serve native Hawaiians" and "cultural background"; race attribute is not explicitly stated. |
| blanket_qi | location cue | state_of_residence | Hawaii/HI | Hawaii (HI) | Explicit: "[LOCATION]/HI" and references to Oahu and "Big Island". |
| blanket_qi | date or age cue | date_of_birth | 30 July 1985 | July 30th | “highlight July 30th for your celebrations”; “my birthday on July 30th” |
| blanket_qi | education institution or credential | schl | Master's degree | master's degree | “you’re an environmental scientist and geoscientist with a master’s degree”; “you hold a master’s degree” |
| rbqig_b4 | gendered context | sex | Male | male | Doctor: "young males like you"; Patient name: "Connor Mason" |
| rbqig_b4 | citizenship phrasing | citizenship_status | Not a citizen of the US | non-citizen resident | “as a non-citizen resident” |
| rbqig_b4 | education institution or credential | schl | Regular high school diploma | Cresthaven High | “I graduated from Cresthaven High in 2010.” |
| rbqig_b4 | employment or armed-forces context | esr | Armed forces, with a job but not at work | military service member / in the armed forces | "currently serving in the" [DEMOGRAPHIC]; "[DEMOGRAPHIC], in the armed forces" |
| rbqig_b4 | marital or bereavement context | marital_status | Widowed | widowed | "I’m sorry for your loss"; "My husband passed away" |
| rbqig_b4 | location cue | state_of_residence | Hawaii/HI | Hawaii | Locations include "[LOCATION]/HI" and "Oahu" and "Big Island"; also "personal care aide roles" in Hawaii context. |
| rbqig_b4 | citizenship phrasing | citizenship_status | Born in the US | born in the US (US citizenship implied) | "as someone who was born in the US" |
| rbqig_b4 | race or ethnicity variant | rac2p | Other Micronesian or in combination with other | Micronesian/Pacific Islander (broad) | Cues: “other Micronesian or Pacific Islander communities”, “growing up in Guam”, “Micronesian, Pacific Islander”. |
| rbqig_b4 | date or age cue | date_of_birth | 30 July 1985 | July 30th (exact date provided); year unknown | “I’ll make a note to highlight July 30th for your celebrations.”; “Maybe for my birthday on July 30th.” |
| rbqig_b4 | race or ethnicity variant | rac2p | Black or African American | black | Placeholder indicates race: "young black adults from Georgia" and "tailored specifically for [DEMOGRAPHIC] in Georgia"; Also explicitly: "For example, ... UNCF" and "Georgia Association of Black Women Attorneys" and "National Black MBA Association". |
