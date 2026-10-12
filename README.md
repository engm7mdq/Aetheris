<p align="center"><img src="assets/aetheris_logo_light.svg" alt="Aetheris" width="300"></p>

# Aetheris — Intelligent Exam Scheduling

*Smarter Scheduling. Better Academic Planning.*

**Aetheris** is an intelligent university examination scheduling platform that combines
optimisation algorithms, constraint validation and scheduling analytics to generate and
evaluate examination timetables. (Project name: *University Exam Scheduling Agent*.)

An explicit AI agent schedules exams with a **Discrete Particle Swarm Optimiser**, allocates
rooms, validates every hard constraint independently, and compares itself with random and
greedy baselines.

Aetheris runs locally on Windows 11 with Python, Streamlit, SQLite/SQLAlchemy, pandas/NumPy,
Plotly and openpyxl. It needs no paid services or API keys.

> The bundled data are **synthetic** (generated with fixed seeds). They are not real
> university records and not an official benchmark.

> **Local demo sign-in:** username `admin`, password `Admin@123`. These are local
> demonstration credentials only. **Change the password before exposing the app to any
> network** (see [Changing the password](#changing-the-administrator-password)).

## Features

- **Sign-in**: a fixed local administrator login protects every page.
  - Masked password with a show/hide eye button.
  - Throttling after repeated failures.
  - Logout clears the session.
- **English and العربية**:
  - full UI translation, including validation and error messages;
  - a genuine right-to-left layout for Arabic.
- **Light and Dark Mode**, applied to the whole interface, including the sign-in page and
  charts.
- **Semesters**: create, edit, archive and select semesters. Each semester has its own
  students, exams, enrollments, rooms, dated time slots, room unavailability and schedules.
  The database enforces semester isolation through composite foreign keys.
- **Data import**:
  - CSV/XLSX per data type, or one multi-sheet workbook;
  - preview, row-level validation report, and accepted/rejected row lists;
  - explicit add / update / replace policies, with confirmation for replace;
  - downloadable templates and sample data.
- **Manual CRUD** with search. Records used by saved schedules are protected from deletion.
- **Agent**: perceive → model → conflict analysis → readiness check → plan (Random / Greedy /
  Discrete PSO) → room allocation → evaluation → learn (saved history, recommended
  configuration).
- **Hard constraints**: no student overlap; no room double booking; each exam exactly once;
  capacity, room type and availability; duration fits the slot; slot available; valid
  references. All checks use real interval overlap. The one-day rest rule is a **soft**
  constraint.
- **Comparison**: same data, same weights, same evaluator, same validator, fixed seeds.
- **Runs**: saved as drafts, then validated, then published. The previously published run
  becomes *superseded*; it is never deleted.
- **Timetable views**: rooms × time calendar, day × period grid, and a filterable table.
- **Analytics**: convergence, swarm diversity, method comparison and distributions.
- **Exports** per saved run: timetable CSV/XLSX, evaluation CSV/JSON, history, conflict
  report, daily distribution and room utilisation. Each file is stamped with
  *Aetheris 1.1.0 (Intelligent Exam Scheduling)* metadata.

## Installation (Windows 11)

You need Python 3.11 or newer; development and tests used Python 3.13.14. In PowerShell, from
the project folder:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1          # if blocked: Set-ExecutionPolicy -Scope Process RemoteSigned
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Tested versions: streamlit 1.65.0, SQLAlchemy 2.0.54, pandas 2.3.3, numpy 2.5.4, plotly 6.9.0,
openpyxl 3.1.5, pytest 8.4.2.

## Start Aetheris

```powershell
streamlit run app.py
```

1. Open http://localhost:8501.
2. Sign in with the local demo credentials: `admin` / `Admin@123`.
   - Enter submits the form.
   - The eye icon shows or hides the password.
3. Use **Logout** in the sidebar to end the session.

Refreshing the browser starts a new session, so you must sign in again (preferences reset to
English / Light).

## Language: English / العربية

Choose **Language** on the sign-in page or in the sidebar. Switching does not log you out and
does not touch any data.

**In Arabic, Aetheris translates:**
* navigation, headings, buttons, forms and tables;
* charts, validation and import messages, and the agent trace;
* the Methodology page.

**RTL behaviour in Arabic:**
* the main content and sidebar are laid out **right-to-left** with an Arabic font (Cairo
  from Google Fonts, falling back to Segoe UI/Tahoma when offline);
* charts, data grids, code and formulas stay left-to-right so numbers and axes remain
  readable;
* technical names (PSO, Greedy, Random, file formats, codes) are deliberately not
  translated.

All texts live in one place: `src/translations.py`, used through `src/i18n.py`.

## Theme: Light Mode / Dark Mode

Choose **Theme** on the sign-in page or in the sidebar. The theme is independent of the
language and changes nothing in the database.

## Changing the administrator password

The password is never stored in plain text. Aetheris checks a salted PBKDF2-SHA256 hash on
the server.

1. Create a hash. The command prompts without echoing the password:

   ```powershell
   python manage.py hash-password
   ```

2. Set it before starting the app. In the same PowerShell window, or as a user environment
   variable:

   ```powershell
   $env:AETHERIS_ADMIN_PASSWORD_HASH = "pbkdf2_sha256$260000$...$..."   # output of step 1
   $env:AETHERIS_ADMIN_USERNAME = "registrar"                          # optional, default "admin"
   streamlit run app.py
   ```

`AETHERIS_ADMIN_PASSWORD` (plain text, hashed in memory at start-up) is also accepted, but the
hash is preferred. Never commit real passwords or hashes to source control.

**Limits of the demo authentication.**
* One shared administrator account.
* Sessions end when the browser tab is refreshed or closed.
* Throttling: after 5 failed attempts for a username within 5 minutes, that username is
  locked for 60 seconds. The counter is in memory and per server process, and a third party
  could use it to lock the admin out temporarily.
* No HTTPS of its own and no audit trail.

It is suitable for local, single-machine use. It is **not** production-grade security; put a
proper reverse proxy with TLS and real identity management in front of it before any network
deployment.

## Database location and backup

* **Location:** the default database is `data\exam_scheduler.db`. It contains the two
  synthetic semesters and 80 saved experiment runs. Set `EXAM_DB_URL` to use another file
  (for example outside OneDrive):

  ```powershell
  $env:EXAM_DB_URL = "sqlite:///C:/ExamData/exam_scheduler.db"
  ```

* **Back up:** stop the app, then copy the file:

  ```powershell
  New-Item -ItemType Directory -Force backups | Out-Null
  Copy-Item data\exam_scheduler.db "backups\exam_scheduler_$(Get-Date -Format yyyyMMdd_HHmmss).db"
  ```

* **Restore:** stop the app and copy a backup over `data\exam_scheduler.db`.
* **Create a database from scratch:**

  ```powershell
  python manage.py init-db        # creates the tables (idempotent)
  python manage.py load-sample    # optional synthetic semesters
  ```

The Aetheris upgrade did not change the database schema. A pre-upgrade copy is in
`backups\pre_aetheris_20261012_164458\`.

## Run the tests

```powershell
python -m pytest                       # 149 automated tests (unit, database, auth, i18n, themes, headless UI)
```

**Optional real-browser tests.** These use the installed Chrome via Playwright.
* Always run them against a **copy** of the database.
* Restart the app on a fresh copy for each script.

```powershell
pip install -r requirements-dev.txt
Copy-Item data\exam_scheduler.db C:\temp\e2e.db
$env:EXAM_DB_URL = "sqlite:///C:/temp/e2e.db"
streamlit run app.py --server.port 8600                                     # terminal 1
python tests/e2e/browser_aetheris_ui.py C:\temp\ui_out                      # login, EN/AR, RTL, themes, auth gate
python tests/e2e/browser_workflow.py tests/e2e/fixtures C:\temp\e2e_out     # import, schedule, publish, export
python tests/e2e/browser_crud_cancel.py C:\temp\e2e_out2 C:\temp\e2e.db     # CRUD, protection, cancellation
```

## Importing data

On **Dataset management → Import files**:
1. Choose a policy.
2. Upload the files.
3. Click **Validate files**.
4. Review the report.
5. Click **Confirm import**.

Files are imported in dependency order: time slots → rooms → students → courses →
enrollments.

| File | Required columns | Optional columns |
|---|---|---|
| time_slots | slot_code, exam_date (YYYY-MM-DD), start_time, end_time (HH:MM) | is_available |
| rooms | room_name, capacity, room_type | building, is_active, unavailable_slots (`D1-AM;D2-PM`) |
| students | student_code | display_name, department, year_level, is_active |
| courses | course_code, course_name, duration_minutes | department, exam_type, required_room_type (`any` = no requirement), expected_enrollment |
| enrollments | student_code, course_code | – |

Templates are in `dataset/templates/`. Sample files are in `dataset/sample/`.

## Optimising and exporting

1. On **Exam Scheduling**, choose methods, seed, particles and iterations (optionally PSO
   parameters and soft-constraint weights), then click **Generate Schedule**.
2. Inspect the comparison, convergence, timetable, hard-constraint check and student conflict
   report.
3. Click **Save all candidates as drafts**. Then publish a feasible run here or on
   **Schedule Results**; publishing re-validates the run first.
4. To cancel a long run, use Streamlit's **Stop** button (top-right while running). The run is
   discarded and nothing is saved.
5. To export, use **Schedule Results → Open a run → Export Results**.

To reproduce the documented experiments:

```powershell
python manage.py experiments
python scripts/verify_results.py
```

## Project layout

```
app.py                 entry point: sign-in gate, navigation, sidebar (logo, semester, language, theme, logout)
assets/                Aetheris logo (SVG mark + light/dark wordmarks, PNG icons)
manage.py              CLI: init-db, load-sample, write-sample-csv, experiments, hash-password
config.py              paths, DB URL, branding, limits
src/auth.py            local administrator authentication (PBKDF2, throttling)
src/i18n.py            localisation API (t, Msg, localize)    src/translations.py  all EN/AR texts
src/ui/theme.py        Light/Dark palettes, Plotly theme, CSS layer (incl. RTL)
src/ui/common.py       page bootstrap, auth check, preferences, tables/charts helpers
src/ui/login.py        sign-in page
src/                   scheduling core, services, persistence (unchanged algorithms)
pages/                 Dashboard, Semesters, Dataset management, Exam Scheduling, Timetable,
                       Analytics, Schedule Results, Methodology
tests/                 pytest suite; tests/e2e/ real-browser scripts
docs/                  reports; docs/results/aetheris/ = evidence of the Aetheris upgrade
```

> The academic submission package in `submission/` (report PDF, diagrams, screenshots) was built
> **before** the Aetheris UI upgrade and documents that earlier version. The scheduling algorithm
> (version 1.0.1), its results and the database are unchanged by the upgrade. The package has
> **not** been regenerated for Aetheris: that would need new screenshots and updated report text.
> Current UI screenshots are in `docs/results/aetheris/`.

## Known limitations of the UI layer

* **Native theme cannot switch at runtime.** Streamlit 1.65 reads its native theme only at
  server start. Light/Dark switching is therefore a CSS layer per session.
  * Data grids (`st.dataframe`) and the JSON viewer are drawn on a canvas, so Dark Mode shows
    them through an invert filter. They are readable, but not a pixel-perfect native dark
    grid.
  * Streamlit's toolbar runs in `viewer` mode (`.streamlit/config.toml`). Its menu offers only
    Print / Record screen (verified in the browser), so it cannot change the theme behind the
    in-app selector. The running-status widget with the **Stop** button remains available.
* **Some Streamlit-internal labels stay English** even in Arabic: the file uploader's
  "Upload / 5MB per file", the "Page not found" notice, and the password eye button's
  accessible name. Streamlit does not expose them for translation.
* **RTL limits:**
  * The sidebar stays on the left in RTL; Streamlit cannot move it.
  * Data grids keep left-to-right column order.
* **Session lifetime:** preferences and login live in the browser session and reset on
  refresh.
* **Font:** the Cairo font loads from Google Fonts when online; otherwise the system Arabic
  font is used.

## Troubleshooting

- **`ModuleNotFoundError`**: activate the virtual environment, or run
  `.\.venv\Scripts\python -m streamlit run app.py`.
- **Port in use**: `streamlit run app.py --server.port 8502`.
- **"Too many failed attempts"**: wait 60 seconds, or restart the app.
- **`database is locked`**: close other app instances, or move the DB with `EXAM_DB_URL`.
- **"Readiness check failed"**: an exam has no long-enough slot or no suitable active room.
- **"Replace is blocked"**: the semester has saved schedules. Use add/update, or create a new
  semester.
- **A run shows "infeasible"**: no timetable satisfying all hard constraints was found. This
  is not a proof that none exists.
