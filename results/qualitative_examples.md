# Qualitative Examples

## synth_0000: medical_admin

### Original

Leo Martinez, a 34-year-old oncology infusion pharmacist at a small oncology startup in Asheville, North Carolina, called from 555-0100-0000 and emailed leo.martinez0@example.org about prior authorization for a younger brother with guardianship needs who had April 17, 2025 surgery for familial adenomatous polyposis.

### Direct

[PERSON], a 34-year-old oncology infusion pharmacist at a small oncology startup in Asheville, North Carolina, called from [PHONE] and emailed [EMAIL] about prior authorization for a younger brother with guardianship needs who had April 17, 2025 surgery for familial adenomatous polyposis.

Document risk: 36.5 -> 36.5

### Blanket QI

[PERSON], a [AGE] [OCCUPATION] at [EMPLOYER] in [LOCATION], called from [PHONE] and emailed [EMAIL] about prior authorization for a [FAMILY] who had [DATE] surgery for [MEDICAL].

Document risk: 36.5 -> 0.0

### RB-QIG balanced

[PERSON], a [AGE] [OCCUPATION] at a healthcare technology company in a city in the southeastern U.S., called from [PHONE] and emailed [EMAIL] about prior authorization for a dependent family member who had [DATE] surgery for [MEDICAL_CONDITION].

Document risk: 36.5 -> 3.0

---

## synth_0001: legal_intake

### Original

Leo Martinez, a 51-year-old assistive-technology coordinator at St. Agnes Regional Hospital in Boise, Idaho, sent intake notes from leo.martinez1@example.org about a protective-order hearing after a January 2025 incident; the issue also affects a 7-year-old daughter.

### Direct

[PERSON], a 51-year-old assistive-technology coordinator at St. Agnes Regional Hospital in Boise, Idaho, sent intake notes from [EMAIL] about a protective-order hearing after a January 2025 incident; the issue also affects a 7-year-old daughter.

Document risk: 30.5 -> 30.5

### Blanket QI

[PERSON], a [AGE] [OCCUPATION] at [EMPLOYER] in [LOCATION], sent intake notes from [EMAIL] about [LEGAL]; the issue also affects a [FAMILY].

Document risk: 30.5 -> 0.0

### RB-QIG balanced

[PERSON], a [AGE] [OCCUPATION] at a regional hospital in a city in the U.S. Mountain West, sent intake notes from [EMAIL] about [LEGAL_FACT]; the issue also affects a young child.

Document risk: 30.5 -> 3.0

---

## synth_0002: financial_support

### Original

Hannah Kim is a 29-year-old lead Rust compiler engineer at Mesa County School District near Burlington, Vermont. In a support ticket sent from hannah.kim2@example.org, Hannah asked for hardship review because of a Chapter 13 bankruptcy filed in May 2025 while supporting a 7-year-old daughter.

### Direct

[PERSON] is a 29-year-old lead Rust compiler engineer at Mesa County School District near Burlington, Vermont. In a support ticket sent from [EMAIL], [PERSON] asked for hardship review because of a Chapter 13 bankruptcy filed in May 2025 while supporting a 7-year-old daughter.

Document risk: 29.5 -> 29.5

### Blanket QI

[PERSON] is a [AGE] [OCCUPATION] at [EMPLOYER] near [LOCATION]. In a support ticket sent from [EMAIL], [PERSON] asked for hardship review because of [FINANCIAL] while supporting a [FAMILY].

Document risk: 29.5 -> 0.0

### RB-QIG balanced

[PERSON] is a [AGE] [OCCUPATION] at a school district near a small city in New England. In a support ticket sent from [EMAIL], [PERSON] asked for hardship review because of [FINANCIAL_FACT] while supporting a young child.

Document risk: 29.5 -> 3.0

---
