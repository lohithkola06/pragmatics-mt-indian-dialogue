# Pilot Annotation App

A small static web app that walks native-speaker annotators through the pilot in
[../benchmark/pilot/](../benchmark/pilot/). It covers both annotation stages:

- **Stage 1, item review.** All 47 draft items, free navigation. The source
  utterance shows first with the context covered, so reviewers can apply the
  cover-the-context test. Reviewers answer the eight review questions, re-rate
  severity without seeing the assigned label, recommend Accept, Revise or Reject,
  and can suggest an Indian English reference.
- **Stage 2, blind rating.** The 94 candidate translations, one at a time, on the
  twelve dimensions of the human evaluation protocol. Annotators never see item
  IDs, labels, the preservation requirement, or which candidate is the reference.
  The first 10 candidates are a shared calibration set, followed by a checkpoint
  that locks them.

There is **no backend**. Work autosaves in the annotator's browser, and they
download a CSV and a JSON backup to send to you. The CSVs are the same format the
Python tooling already reads, so `scripts/calculate_agreement.py` runs on them
directly.

Adjudication (pilot stages 4 and 5) is not part of the app. It stays with
[../benchmark/pilot/pilot_adjudication_template.csv](../benchmark/pilot/pilot_adjudication_template.csv).

---

## Local development

Needs Node 20 or later.

```bash
cd annotation-app
npm ci
npm run dev        # http://localhost:5173
npm test           # vitest: CSV bytes, ordering, completion rules, backups
npm run build      # type-check, then build into dist/
```

Stage 2 is locked until you unlock it in the config (see below). To try it locally
while it is locked, open `http://localhost:5173/?stage2=1`. That override only
works in the dev server, never in a deployed build.

---

## Where the data comes from

The app does not read the JSONL directly. `scripts/build_annotation_app_data.py`
turns the pilot items, the app config and the annotator-facing guidelines into
`src/generated/`, and those generated files are committed.

```bash
# from the repository root
python scripts/build_annotation_app_data.py          # rebuild src/generated/
python scripts/build_annotation_app_data.py --check  # fail if it is stale
```

Rebuild and commit whenever you change a pilot item, one of the synced guideline
docs, or [../benchmark/pilot/annotation_app_config.json](../benchmark/pilot/annotation_app_config.json).
`python -m unittest discover scripts/tests` runs the `--check`, so stale data fails
the test suite.

Committing the generated files means each deploy freezes exactly what annotators
see. It also keeps this directory self-contained, so Vercel does not need Python.

**The priming guard.** Before writing anything, the build script checks that no
guideline doc shown in the app quotes a pilot item: its source utterance, context
turns, reference or contrastive translation, or item ID. Annotators read those docs
before rating, so a quoted item would hand them the intended answer. If you add an
example to a guideline and the build fails, write a fresh example instead.

### The config file

| Key | What it does |
|---|---|
| `stage2_enabled` | `false` shows Stage 2 as locked on the start screen |
| `calibration_items` | The 5 items (10 candidates) every annotator rates first, in a shared order |
| `synced_docs` | Guideline docs shown in the in-app viewer |
| `contact_instructions` | Shown at the checkpoint and the finish screen, telling annotators where to send files |

`contact_instructions` is deliberately generic. The repository is public and so is
the deployed site, so point annotators to their invitation rather than publishing an
email address here.

---

## Deploying to Vercel

1. Push the branch and merge it into `main`.
2. On vercel.com choose **Add New → Project** and import this GitHub repository.
3. Set **Root Directory** to `annotation-app`.
4. Leave the framework preset as **Vite**. The defaults are right: build command
   `npm run build`, output directory `dist`.
5. Deploy. Every later push to `main` redeploys production.

No environment variables are needed.

**Share only the production URL** (`<project>.vercel.app`, or a custom domain).
Browsers keep saved work separately for each web address. An annotator who starts
on one URL and comes back on another will not see their work. So:

- Don't send preview deployment links. Each preview has its own address, and Vercel
  puts previews behind a login by default anyway.
- If you want a custom domain, set it up **before** sending the link, not partway
  through the pilot.

**Redeploying during a stage is safe but visible.** Saved sessions carry a
fingerprint of the dataset and a hash of each item. If an item changes after an
annotator answered it, the app shows a notice and marks that answer for
re-checking. Avoid changing items mid-stage unless something is actually broken.

---

## Running the pilot with the app

This follows [../benchmark/pilot/pilot_plan.md](../benchmark/pilot/pilot_plan.md).

**1. Before sending the link.** Assign each annotator a pseudonymous ID
(`ANN_01`, `ANN_02`, …) and keep the mapping to real names outside the repository.
The app accepts only `ANN_` IDs, so real names never reach an export.

**2. Stage 1.** Send each annotator the production URL and their ID. They read the
guidelines in the app, confirm the training checklist, and review all 47 items.
They send back two files:

- `pilot-stage1-review_ANN_01_<date>.csv`
- `pilot-stage1-backup_ANN_01_<date>.json`

Measure review agreement:

```bash
python scripts/calculate_agreement.py \
    pilot-stage1-review_ANN_01_*.csv pilot-stage1-review_ANN_02_*.csv \
    --unit-column item_id --annotator-column reviewer_id
```

**3. Revise.** Fix or reject items that failed review, update `review_status`,
revalidate, rebuild the app data and commit.

**4. Unlock Stage 2.** Set `"stage2_enabled": true` in the config, rebuild, commit
and push. The redeploy opens Stage 2 on the same URL.

**5. Calibration.** After 10 candidates the app stops at a checkpoint and asks for
`pilot-stage2-calibration_ANN_xx_<date>.csv` plus a backup. When you have both
annotators' files:

```bash
python scripts/calculate_agreement.py \
    pilot-stage2-calibration_ANN_01_*.csv pilot-stage2-calibration_ANN_02_*.csv
```

Run the calibration discussion on how the scale is used, not on answers to specific
items. When an annotator continues past the checkpoint, their calibration ratings
lock, so the final export shows what they rated before the discussion.

**6. Stage 2.** Annotators rate the remaining 84 candidates. The app suggests a
break every 25 and nudges them to download a backup every 10. They send back
`pilot-stage2-ratings_ANN_xx_<date>.csv` and a backup.

```bash
python scripts/calculate_agreement.py \
    pilot-stage2-ratings_ANN_01_*.csv pilot-stage2-ratings_ANN_02_*.csv \
    --out agreement_report.md

# Code-switch agreement on the Hinglish code-switching items only. Monolingual
# Hindi candidates are fixed at NOT_APPLICABLE and would inflate the figure.
python scripts/calculate_agreement.py \
    pilot-stage2-ratings_ANN_01_*.csv pilot-stage2-ratings_ANN_02_*.csv \
    --where primary_phenomenon=CODE_SWITCHING
```

Candidate IDs ending in `-A` are the reference and `-B` the contrastive, the same
convention as `create_annotation_sheet.py`.

### If something goes wrong

- **An annotator lost their work** (cleared browsing data, new laptop): they choose
  **Restore from backup** on the start screen and pick their latest JSON file.
- **An annotator opened the app in two tabs:** the second tab goes read-only with a
  notice, so the two can't overwrite each other.
- **The CSV looks wrong in Excel:** the export is UTF-8 without a byte order mark,
  which Excel can misread as another encoding. Open it with Data → From Text/CSV, or
  just use the file as sent. Ask annotators not to re-save it in Excel. If one does,
  the byte order mark Excel adds is handled, but other changes Excel makes may not be.

---

## What the app does not protect against

- **Blinding is a matter of trust.** The app hides labels and the reference, but
  the repository is public, the exported CSV contains candidate IDs that end in `-A`
  or `-B`, and the item data ships with the site. A determined annotator could find the answer key.
  Ask annotators not to look, as the guidelines already do.
- **Saved work lives only in one browser.** Nothing is sent anywhere until the
  annotator emails you the files. The backups are the safety net.
- **Independence is up to the annotators.** The app can't stop two people
  discussing items.

---

## Layout

```text
annotation-app/
├── index.html
├── src/
│   ├── App.tsx               screens, navigation, saving, downloads
│   ├── data.ts               loads the generated files
│   ├── generated/            written by build_annotation_app_data.py (don't edit)
│   ├── lib/                  pure logic, unit-tested
│   │   ├── csv.ts            RFC 4180 writer matching Python's csv module
│   │   ├── export.ts         Stage 1 and Stage 2 CSV rows
│   │   ├── order.ts          seeded Stage 2 order, siblings never adjacent
│   │   ├── completion.ts     what counts as done, when a note is required
│   │   ├── session.ts        localStorage, backups, annotator IDs, tab lock
│   │   └── mdLinks.ts        which guideline links open in the app
│   ├── components/           dialogue, choice buttons, guideline viewer
│   └── views/                start, instructions, tasks, checkpoint, finish
└── package.json
```

**The export contract.** `scripts/tests/fixtures/app_export_*.csv` are rendered by
the Python build script. The vitest suite checks that the app produces the same
files byte for byte, and the Python suite runs `calculate_agreement.py` on them. A
change to either side that breaks the format fails a test.
