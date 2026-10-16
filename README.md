# 🧭 The Forgotten Patient — CareCompass & CareSlot

> Two connected web apps for the **DATATHON — Health: The Forgotten Patient** challenge.
> **CareCompass** helps hospital managers see where patients are stuck. **CareSlot** helps patients find a free slot.

⚠️ **Demo project.** The dataset is synthetic (made up for the datathon). CareSlot's hospitals, queues and bookings are simulated. Nothing here is real hospital data or medical advice.

## 🔗 Live demo
After you turn on GitHub Pages (see [Deploy](#-deploy-on-github-pages)) replace `YOUR-USERNAME` and `REPO-NAME`:

| App | Link |
|---|---|
| Home page | `https://YOUR-USERNAME.github.io/REPO-NAME/` |
| CareCompass (managers) | `https://YOUR-USERNAME.github.io/REPO-NAME/carecompass/` |
| CareSlot (patients) | `https://YOUR-USERNAME.github.io/REPO-NAME/careslot/` |

## 🎯 The problem
Hospital staff struggle to see where patients wait, which services are overloaded, and which patients risk being neglected. The challenge asks for a hospital-flow product for **hospital operations managers, department coordinators and service administrators**.

## 💡 Our solution

| | CareCompass | CareSlot |
|---|---|---|
| **For** | Managers, coordinators, administrators | Patients and families |
| **Question it answers** | “Where are patients stuck and what should we look at first?” | “Which hospital has a free slot now, and when is mine?” |
| **Data** | The real 4-table dataset (patients, encounters, departments, diagnostic tests) | Simulated hospitals shaped by dataset patterns |
| **Chat** | Ask the data in plain English | FAQ and slot assistant |

### CareCompass — covers all six build ideas from the problem page

| Idea on the problem page | Where in CareCompass |
|---|---|
| 1. Patient-flow dashboard with department queues and wait times | **Flow** tab: department queue table, KPI tiles, patient-journey bar (wait → service → discharge) |
| 2. Forecast of demand or delays | **Forecast** tab: expected visits by weekday and time of day, with an honest backtest |
| 3. Alerts for unusual waits or overloaded services | **Alerts** tab: unusual-wait list and overload watch (load per staff and bed) |
| 4. Diagnostic-test turnaround monitor | **Tests** tab: adjustable alert threshold, by test type, urgent vs routine, by month and department |
| 5. “What should we investigate first?” queue ranked by impact and confidence | **Investigate first** tab |
| 6. Explanation panel showing which data signals led to each alert | Click any alert or queue item |

Plus a **chat** that understands questions like “seniors with diabetes waiting by department”, shows a clear error for off-topic questions, and says plainly when the data can’t answer (for example, there is no disease column, so no COVID analysis).

### CareSlot — two journeys, as requested
1. **Which hospital is free now?** Pick a service; six hospitals are ranked by earliest free slot, with patients online and wait time.
2. **Check one hospital.** See patients already online, patients ahead of you, your earliest slot, free slots to book, and an hour-by-hour “how busy is it today” chart.
Plus an **Ask & FAQ** tab (17 answers, searchable, optional AI) and one-tap demo booking saved in your browser.

## 📊 What the data shows
Every number below is reproduced by `python analysis/facts.py`.

- **Average wait 52 min** (median 52, 90th percentile 84, max 153).
- **Triage works:** average wait is 16.5 min for Critical, 27.2 High, 48.8 Medium and 71.7 Low.
- **“Forgotten” visits** (Low/Medium triage waiting over 90 min): **491 visits, 6.1%** of all visits.
- **Longest waits beyond what triage explains:** Pediatrics (about +8.6 min), Laboratory (+7.6), Outpatient (+6.4). Cardiology, Pharmacy and Admissions wait less than expected.
- **Urgent tests are not faster:** 69 min vs 70 min for routine; tests average 70 min (median 57).
- **Overload candidate:** Radiology has about 2.4× the typical visits per staff member and above-expected waits.

**Things the data does *not* show (we report them honestly):**
- Waits barely change by hour, weekday, visit type, insurance or chronic condition.
- A weekday forecast was no better than a flat average (3.84 vs 3.79 visits/day error), so the forecast is a planning baseline only.
- Longer waits are **not** linked to more patients leaving before care (3.0% of all visits; 2.4% among the “forgotten” group). The “forgotten patient” risk is a hypothesis to test with real data, not a finding.
- Recorded `daily_capacity` is far above actual daily visits, so load is compared between departments, not against capacity.

## 🧠 Method in brief
- **Joins:** `patients.patient_id = encounters.patient_id`, `departments.department_id = encounters.department_id`, `diagnostic_tests.encounter_id = encounters.encounter_id`. No duplicate encounters, no negative waits, every test links to an encounter. The only blanks are `chronic_condition` (747 patients, read as “none recorded”).
- **Triage-adjusted wait:** each visit’s expected wait is the average wait for its triage level; a department or slice’s *excess* is how far it exceeds that (so Low-triage patients aren’t blamed for waiting longer by design).
- **Investigate-first score:** excess patient-hours × confidence (from a z-score), minimum 30 visits per slice. About 230 slices are screened, so a few strong results can appear by chance — treat them as leads to verify.
- **Forecast:** weekday average trained on January–September and tested on later days, compared with a flat average.
- **CareSlot simulation:** each hospital offers some services with a number of doctors; slot bookings follow a repeatable pseudo-random rule where busier services (longer waits in the dataset, e.g. Laboratory and Pediatrics) fill up more. The busy-hour curve, hospital names, distances and opening hours are design assumptions.

## 🤖 About the AI
| Where it runs | AI behaviour |
|---|---|
| **CareCompass on GitHub Pages** | Chat works with built-in keyword understanding. (The AI question decoder only runs when the page is hosted on Claude.) |
| **CareSlot on GitHub Pages** | Quick-answer mode by default. For AI answers, set up the optional proxy in [`careslot/README.md`](careslot/README.md) (`worker.js`). **Never put an API key in the HTML.** |
| **Both hosted as Claude artifacts** | Built-in AI works for viewers with a Claude account. |

In every mode, numbers always come from the data or the slot simulation, never from the AI. The AI only interprets the question or rewrites FAQ text. Emergencies, medical-advice requests and off-topic questions get fixed, polite messages.

## 🗂 Repository structure
```
├── index.html            Home page linking both apps
├── README.md             This file
├── carecompass/          Manager dashboard (single-file web app)
├── careslot/             Patient slot finder
│   ├── index.html
│   ├── worker.js         Optional AI proxy (Cloudflare Worker)
│   └── README.md         CareSlot details and AI setup
├── analysis/facts.py     Re-computes every number quoted above
└── data/                 The four CSVs from the datathon + its README
```

## ▶️ Run locally
- **No install:** double-click `index.html` (or `carecompass/index.html`, `careslot/index.html`).
- **Check the numbers:** `pip install pandas` then `python analysis/facts.py`.

## 🚀 Deploy on GitHub Pages
1. Create a **public** repository on GitHub and upload everything in this folder (keep the folder structure).
2. Open **Settings → Pages**, set **Source** to *Deploy from a branch*, choose **main** and **/ (root)**, then save.
3. After a minute or two the site is live at `https://YOUR-USERNAME.github.io/REPO-NAME/`.
4. Edit the links in the table near the top of this README.

## ⚠️ Limitations
- Synthetic data; findings illustrate the method, not real hospitals.
- CareCompass has no trained prediction model yet; the forecast and alert scoring are statistical methods.
- CareSlot is a simulation with no live hospital connection or real bookings.
- Screening alerts need verification by hospital staff.

## 🛣 Roadmap
1. Train a **left-before-care risk model** (logistic regression, recall/precision on a stratified split).
2. Export the “forgotten patient” list for staff action.
3. Connect CareSlot to a real booking system by replacing the `booked()` function.
4. Add diagnosis (ICD-10) codes and staffing rosters for richer analysis.
5. Add regional language support to CareSlot.

## 👥 Team
Add team name, members and college here.

## 📄 Credits
Dataset: *Health — The Forgotten Patient*, provided by the DATATHON organisers (synthetic, educational). Apps built in plain HTML, CSS and JavaScript.
