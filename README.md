# 🧭 CareConnect — The Forgotten Patient

> One web app, two views, built for the **DATATHON — Health: The Forgotten Patient** challenge.
> **🏥 I'm a patient** (*CareSlot*) finds a free hospital slot. **🧭 Hospital team** (*CareCompass*) shows managers where patients are stuck.

⚠️ **Demo project.** The dataset is synthetic. In the patient view, hospitals, queues and bookings are simulated. Nothing here is real hospital data or medical advice.

## 🔗 Live demo
After turning on GitHub Pages (see [Deploy](#-deploy-on-github-pages)), replace `YOUR-USERNAME` and `REPO-NAME`:

| View | Link |
|---|---|
| Patient (opens by default) | `https://YOUR-USERNAME.github.io/REPO-NAME/` or `…/#patient` |
| Hospital team | `https://YOUR-USERNAME.github.io/REPO-NAME/#team` |

Use the switch at the top of the page to move between views.

## 🎯 The problem
Hospital staff struggle to see where patients wait, which services are overloaded and which patients risk being neglected, while patients can't tell which hospital can see them soon. The challenge asks for a hospital-flow product for **operations managers, department coordinators and service administrators**. We added the patient side so one product covers both ends of the queue.

## 💡 What it does

### 🏥 Patient view (CareSlot)
1. **Which hospital is free now?** Pick a service; six hospitals are ranked by earliest free slot, with patients online and minutes to wait. An “Open now only” filter is included.
2. **Check one hospital.** See patients already online, how many are ahead of you, your earliest slot, free slots to book, and an hour-by-hour “how busy is it today” chart.
3. **Book in one tap.** A demo booking with a token, saved only in your browser; one active booking, cancel any time.
4. **Ask & FAQ.** A chat assistant plus 17 searchable answers (waiting times, triage, tests, cancelling, privacy). It finds slots by conversation, e.g. “free slot for my child today”.

### 🧭 Hospital-team view (CareCompass) — covers all six build ideas

| Idea on the problem page | Where |
|---|---|
| 1. Patient-flow dashboard with department queues and wait times | **Flow** tab: queue table, KPI tiles, patient-journey bar (wait → service → discharge) |
| 2. Forecast of demand or delays | **Forecast** tab with an honest backtest |
| 3. Alerts for unusual waits or overloaded services | **Alerts** tab: unusual waits and overload watch |
| 4. Diagnostic-test turnaround monitor | **Tests** tab with adjustable threshold |
| 5. “What should we investigate first?” ranked by impact and confidence | **Investigate first** tab |
| 6. Explanation panel for each alert | Click any alert or queue item |

Plus a chat for questions like “seniors with diabetes waiting by department”. Off-topic questions get a clear “not related to the data” message, and questions the data can't answer (e.g. a disease) get an honest explanation.

### 🔗 How the two views connect
Both use the same dataset: the team view analyses it directly; the patient view uses its patterns (e.g. Laboratory and Pediatrics have longer waits, so they fill up faster in the simulation) and quotes its facts in the FAQ. Each view links to the other.

## 📊 What the data shows
Every number is reproduced by `python analysis/facts.py`.

- **Average wait 52 min** (median 52, 90th percentile 84, max 153).
- **Triage works:** 16.5 min Critical, 27.2 High, 48.8 Medium, 71.7 Low.
- **“Forgotten” visits** (Low/Medium triage waiting over 90 min): **491 visits, 6.1%**.
- **Longest waits beyond what triage explains:** Pediatrics (about +8.6 min), Laboratory (+7.6), Outpatient (+6.4).
- **Urgent tests are not faster:** 69 vs 70 min for routine; tests average 70 min (median 57).
- **Overload candidate:** Radiology (about 2.4× the typical visits per staff member, with above-expected waits).

**What the data does *not* show (reported honestly):**
- Waits barely change by hour, weekday, visit type, insurance or chronic condition.
- A weekday forecast was no better than a flat average (3.84 vs 3.79 visits/day error), so it is a planning baseline only.
- Longer waits are **not** linked to more patients leaving before care (3.0% overall; 2.4% in the “forgotten” group). The neglect risk is a hypothesis for real data, not a finding.
- Recorded `daily_capacity` is far above actual daily visits, so load is compared between departments, not to capacity.

## 🧠 Method in brief
- **Joins:** `patients.patient_id = encounters.patient_id`, `departments.department_id = encounters.department_id`, `diagnostic_tests.encounter_id = encounters.encounter_id`. No duplicate encounters, no negative waits, every test links to an encounter; the only blanks are `chronic_condition` (747 patients, read as “none recorded”).
- **Triage-adjusted wait:** a visit's expected wait is the average for its triage level; a slice's *excess* is how far it exceeds that, so Low-triage patients aren't blamed for waiting longer by design.
- **Investigate-first score:** excess patient-hours × confidence (z-score), minimum 30 visits per slice. About 230 slices are screened, so a few strong results can appear by chance; treat them as leads to verify.
- **Patient simulation:** each hospital offers some services with a number of doctors; slot bookings follow a repeatable pseudo-random rule where busier services fill up more. The busy-hour curve, hospital names, distances and opening hours are design assumptions.

## 🤖 About the AI
| Where it runs | AI behaviour |
|---|---|
| **GitHub Pages, default** | No AI. Both chats use built-in keyword understanding and still work. |
| **GitHub Pages + proxy** | AI-powered chats (see below). |
| **Hosted as a Claude artifact** | Built-in AI for viewers with a Claude account. |

In every mode, numbers come from the data or the simulation, never from the AI. The AI only interprets a question or rewrites FAQ text. Emergencies, medical-advice requests and off-topic questions get fixed, polite messages, and the chat falls back to keyword mode if the AI is slow or offline.

### Turn on AI answers (optional)
1. Get an Anthropic API key at console.anthropic.com. **Never put it in `index.html`**; a public site would expose it.
2. Create a free Cloudflare account → **Workers & Pages → Create → Worker**, and paste `ai-proxy/worker.js`.
3. In the Worker's **Settings → Variables and Secrets**, add the secret `ANTHROPIC_API_KEY` and a variable `ALLOW_ORIGIN` = `https://YOUR-USERNAME.github.io`.
4. Deploy, copy the Worker URL, and paste it into `index.html` where it says `window.APP_CONFIG={AI_ENDPOINT:''}` (search for `AI_ENDPOINT`).
5. Commit. The patient chat header now says “✨ AI-powered answers”.

API use is billed to your Anthropic account, so set a spending limit. If a request fails, check the model name in `worker.js` against Anthropic's docs.

## 🗂 Repository structure
```
├── index.html          The whole product (patient + hospital-team views)
├── README.md           This file
├── ai-proxy/worker.js  Optional AI proxy (Cloudflare Worker)
├── analysis/facts.py   Re-computes every number quoted above
├── data/               The four CSVs from the datathon + its README
└── .nojekyll           Tells GitHub Pages to serve files as they are
```

## ▶️ Run locally
- **No install:** double-click `index.html`.
- **Check the numbers:** `pip install pandas` then `python analysis/facts.py`.

## 🚀 Deploy on GitHub Pages
1. Create a **public** repository on GitHub and upload everything in this folder (keep `index.html` at the top level).
2. Open **Settings → Pages**, set **Source** to *Deploy from a branch*, choose **main** and **/ (root)**, then save.
3. After a minute or two the site is live at `https://YOUR-USERNAME.github.io/REPO-NAME/`.
4. Edit the links in the table near the top of this README.

## ⚠️ Limitations
- Synthetic data; findings illustrate the method, not real hospitals.
- The team view has no trained prediction model yet; the forecast and alert scoring are statistical methods.
- The patient view is a simulation with no live hospital connection or real bookings.
- Screening alerts need verification by hospital staff.

## 🛣 Roadmap
1. Train a **left-before-care risk model** (logistic regression; recall and precision on a stratified split).
2. Export the “forgotten patient” list for staff action.
3. Connect the patient view to a real booking system by replacing the `booked()` function.
4. Add diagnosis (ICD-10) codes and staffing rosters.
5. Add regional language support.

## 👥 Team
Add team name, members and college here.

## 📄 Credits
Dataset: *Health — The Forgotten Patient*, provided by the DATATHON organisers (synthetic, educational). Plain HTML, CSS and JavaScript; no libraries.
