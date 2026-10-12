# Progress log

## Status (2026-10-12): Aetheris 1.1.0 UI upgrade complete (algorithm unchanged at 1.0.1)

| Phase | Status | Evidence |
|---|---|---|
| 1 Inspect environment | Done | Workspace was empty. Python 3.13.14; `.venv` created |
| 2 Architecture and files | Done | `app.py`, `manage.py`, `config.py`, `src/`, `pages/`, `tests/`, `docs/` |
| 3 Database and semesters | Done | `src/models.py` (composite FKs), `semester_service.py` |
| 4 Import, validation, sample data | Done | `validation.py`, `import_service.py`, `sample_data.py`, `dataset/` |
| 5 Conflict graph, fitness, constraints | Done | `conflict_graph.py`, `fitness.py`, `schedule_validator.py` |
| 6 Greedy and Discrete PSO | Done | `greedy_baseline.py`, `pso_optimizer.py` |
| 7 Room allocation and validation | Done | `room_allocator.py` (Kuhn matching), independent validator |
| 8 Persistence, history, exports | Done | `history_service.py`, `export_service.py` |
| 9 Streamlit dashboard | Done | 8 pages via `st.navigation` |
| 10 Tests | Done | **80 passed** after the audit (`python -m pytest`); real-browser workflow 28/28 |
| 11 Experiments | Done | Re-run for 1.0.1 in the audit: 40 runs saved to DB and `docs/results/`, independently verified (`scripts/verify_results.py`) |
| 12 Defect fixing and start-up | Done | Fixed ambiguous SQL joins and run naming. App health check `ok`, HTTP 200 |
| 13 Documentation | Done | README, `docs/*.md` written from actual results |

## Defects found and fixed during this session

* SQLAlchemy joins starting from `Student`/`Course` produced ambiguous `FROM` clauses. Fixed
  with explicit `select_from(Enrollment)` / `select_from(RoomUnavailability)`.
* An identical time interval against an *existing* slot would have hit the DB unique
  constraint instead of a validation message. A validation rule was added.
* The sidebar semester selector did not follow programmatic changes. It now uses an
  on-change callback.
* The greedy run was named "seed None". It now has a label without a seed.

## Acceptance audit (2026-10-12)

| Workflow | Result | Evidence |
|---|---|---|
| Automated suite | PASS: 80 passed, 0 failed | `docs/results/pytest_output_audit_after.txt` |
| Create semester (browser) | PASS | `docs/results/browser/02_semester_created.png` |
| CSV + Excel import with validation (browser) | PASS | screenshots 06–07 |
| Invalid file / missing column / duplicates (browser) | PASS | screenshots 03–05 |
| Replace confirmation (browser) | PASS | screenshot 08 |
| Generate schedule, inspect conflicts, save, publish (browser) | PASS | screenshots 09–11 |
| Timetable, analytics, history (browser) | PASS | screenshots 12–14 |
| Exports downloaded and checked (browser) | PASS | `docs/results/browser/run83_*` |
| Existing semesters and saved schedules unchanged | PASS | identical hashes in `docs/results/browser/fingerprint_*.txt` |
| Sample data matches the documentation | PASS | `docs/evaluation.md` (Setup) |
| Experiment re-run and independent verification | PASS | `docs/results/verification_output.txt` |
| Cancelling a running optimisation (Stop button) | PASS (submission preparation) | `docs/results/browser/crud_cancel/` (screenshots 19–20) |
| Manual CRUD forms in a real browser | PASS (submission preparation) | `docs/results/browser/crud_cancel/` (screenshots 15–18) |

### Defects confirmed and fixed in the audit

| # | Defect | Fix | Regression test |
|---|---|---|---|
| D1 | Repair/local search accepted moves that swapped one hard violation for another at equal total (e.g. clash → unroomed exam) | `accept_move`: key must improve and no hard category may increase. Algorithm version bumped to 1.0.1 | `test_repair_never_trades_one_hard_violation_for_another` |
| D2 | Evaluation doc and Analytics summary averaged quality metrics over infeasible runs (PSO-core Fall soft "2605" included 4 invalid runs) | `algorithm_summary()` uses feasible runs only and groups by version; docs rewritten | `test_algorithm_summary_excludes_infeasible_runs_from_quality_stats` |
| D3 | Files stayed in the upload fields after a successful import and were silently included in the next import (seen in the browser: a "replace students" validated all 5 files) | Uploader keys get a generation counter that resets after import | Browser step "Upload fields are cleared after a successful import" |
| D4 | Every download click triggered a full page rerun; one browser download was cancelled | `on_click="ignore"` on all download buttons | Browser export step |

The "about 19%" claim was re-verified for 1.0.1. The soft penalty is 19.4% (Fall) and 20.2%
(Spring) below Greedy, paired, feasible runs only. Raw rest incidences are *worse* than
Greedy (+3.1% / +5.9%).

## Submission preparation (2026-10-12)

* **Suite:** re-run → **80 passed** (`docs/results/pytest_output_final.txt`).
* **App start:** health `ok`, HTTP 200.
* **Remaining browser workflows executed:** CRUD, reference protection and cancellation,
  **16/16 PASS** (`tests/e2e/browser_crud_cancel.py`).
* **Fresh installation verified** (`docs/results/install_verification_log.txt`):
  * venv, pip install, init-db and load-sample all exited 0;
  * pytest 80 passed;
  * the app started.
* **Evidence:** all 21 screenshots and 4 exported files exist and were checked against the report.
* **Documentation corrections:**
  * swarm diversity ranges were corrected to the values read from the database
    (0.47–2.60% full PSO);
  * PEAS wording;
  * an explicit hard/soft constraint section;
  * newly disclosed limitations: the missing slot-pattern soft preference, no "cancelled"
    message, two cosmetic UI quirks.
* **Submission package:** `submission/`, built by `python scripts/build_submission.py`. All
  numbers in it are generated from result files, and the build fails on unfilled placeholders or
  missing files.
* **No application code changed** in this phase. New files are only test, build and
  documentation scripts.

## Aetheris UI upgrade (2026-10-12)

**Scope:**
* product rename to **Aetheris** (logo in `assets/`);
* fixed local admin sign-in (`src/auth.py`);
* English/Arabic localisation (`src/i18n.py`, `src/translations.py`, 581 keys) with an RTL
  layout;
* Light/Dark themes (`src/ui/theme.py`);
* branded exports.

Scheduling algorithms, metrics, schema and data were not changed.

| Item | Result | Evidence |
|---|---|---|
| Backup before changes | Done | `backups/pre_aetheris_20261012_164458/` (DB, config, code, fingerprints, counts) |
| Automated tests | **149 passed** | `docs/results/aetheris/pytest_output.txt` |
| Browser: login / i18n / RTL / themes / auth gate | **44/44 PASS** | `docs/results/aetheris/ui_qa/` |
| Browser: import → schedule → publish → export | **28/28 PASS** | `docs/results/aetheris/workflow/` |
| Browser: CRUD, protection, cancellation | **16/16 PASS** | `docs/results/aetheris/crud_cancel/` |
| Live DB preserved (SHA-256 identical, 80 runs) | Verified | test report, section A |
| Fresh Windows install | 149 passed; app starts | `docs/results/aetheris/install_verification_log.txt` |

**Not updated:** the `submission/` package still documents the pre-Aetheris UI.

## Current database contents (`data/exam_scheduler.db`)

* Two synthetic semesters.
* 80 draft experiment runs: 40 from algorithm 1.0.0 (before the audit) and 40 from 1.0.1.
  The Analytics summary separates them by version. None is published; publishing is left
  to the user.

## Next step

The Aetheris upgrade is complete; no required work remains. Optional, in priority order:
1. Regenerate the academic submission package with Aetheris screenshots and branding.
2. Translate the remaining Streamlit-internal strings (uploader, "Page not found") with a custom
   component, if a fully Arabic UI is required.
3. Earlier optional items: fix the cosmetic edit-form quirks (`year_level` "3.0", stale record label);
   add swarm diversity control; a weight-sensitivity study; room sharing for ITC 2007.
