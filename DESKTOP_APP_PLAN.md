# TestGen Desktop Conversion Plan (PyQt6/PySide6 + PyInstaller)

## Objective
Transform the current TestGen web application into a standalone desktop application that embeds the Django backend, offers a native GUI for all features (LLM providers, projects, test generation, CI/CD), and ships as a single executable for Windows, macOS, and Linux using PyInstaller.

## Proposed Architecture

### 1) Embedded Backend (Django)
- **Run Django in-process** using WSGI to avoid an external server dependency.
- **Local-only API** bound to `127.0.0.1` on an ephemeral port to keep existing DRF viewsets usable.
- **Desktop settings module** (`precostcalc/settings_desktop.py`) to:
  - Default to a local SQLite database in the app data directory.
  - Disable CORS or set it to `localhost` only.
  - Configure `ALLOWED_HOSTS` for `127.0.0.1` and `localhost`.
  - Adjust authentication to support desktop usage (token or session with relaxed CSRF for local loopback only).

### 2) Native GUI (PyQt6/PySide6)
- **Qt Widgets-based UI** with pages matching the existing React features:
  - Dashboard
  - LLM Providers (list, add, delete)
  - Projects (list, create, edit)
  - Project Detail (generate tests, download tests, view history)
  - CI/CD pipeline generation and download
- **Navigation** via a left sidebar + `QStackedWidget`.
- **Service layer** (`desktop_app/services/api_client.py`) that calls the embedded API using `requests`.
- **State models** for lists and forms with `QAbstractListModel` or lightweight dataclasses.

### 3) Desktop Entry Point
- `desktop_app/main.py`:
  - Initializes app data paths.
  - Bootstraps Django with desktop settings.
  - Starts embedded WSGI server on a background thread.
  - Launches the Qt main window and connects it to the API client.
  - Graceful shutdown (stop WSGI server, flush DB writes).

### 4) Data & Config Storage
- **Database**: SQLite stored under an OS-appropriate app directory (via `appdirs`).
- **Secrets**: Use OS keyring if available; fallback to encrypted local storage.
- **Downloads**: Use a user-specified output directory for generated tests/pipelines.

## Implementation Plan

### Phase 1: Backend Desktop Configuration
1. Add `precostcalc/settings_desktop.py` to:
   - Override DB path to app data directory.
   - Configure static/media root in app data.
   - Limit hosts and set DEBUG off for packaged builds.
2. Add helper to initialize app data folder and create DB if missing.
3. Add `desktop_app/backend.py` to:
   - Configure `DJANGO_SETTINGS_MODULE`.
   - Start the WSGI server in a background thread.
   - Return port and shutdown hooks.

### Phase 2: Native UI Skeleton
1. Create `desktop_app/ui/` with:
   - `main_window.py` (layout + navigation)
   - `pages/` for each feature page
   - Shared components (dialogs, forms, status banners)
2. Implement UI flows that mirror the React UI:
   - LLM Provider CRUD
   - Project CRUD
   - Test generation configuration
   - Generated test history
   - CI/CD pipeline configuration + download

### Phase 3: API Client & Data Models
1. Implement `desktop_app/services/api_client.py` with typed methods for each endpoint.
2. Create request/response DTOs for form validation and UI state.
3. Add centralized error handling (timeouts, API errors, invalid input).

### Phase 4: Packaging & Distribution
1. Add a PyInstaller spec file (`desktop_app/testgen.spec`) to:
   - Bundle Django code, migrations, static files, and templates.
   - Include required Qt plugins and assets.
   - Package Python dependencies as a single executable.
2. Add `desktop_app/resources/` for app icon, brand assets, and license.
3. Document build steps per platform.

### Phase 5: UX Enhancements
- Loading spinners for API calls
- Toast notifications
- Inline validation messages
- Save last used configuration in local settings

## Key Technical Considerations

### Authentication & Security
- Prefer token authentication for desktop to avoid CSRF complications.
- Generate a local token on first run.
- Maintain token in the app data directory or OS keyring.

### Performance
- Use async requests or background threads to keep UI responsive.
- Batch loads for dashboard metrics.

### Compatibility
- Use PySide6 or PyQt6 consistently; PySide6 preferred for LGPL.
- Ensure PyInstaller hooks for Qt WebEngine if needed for embedded docs.

## Files/Modules to Add
```
/desktop_app/
  main.py
  backend.py
  resources/
  services/
    api_client.py
  ui/
    main_window.py
    pages/
      dashboard_page.py
      llm_providers_page.py
      projects_page.py
      create_project_page.py
      project_detail_page.py
  testgen.spec
precostcalc/settings_desktop.py
```

## Deliverables
- Embedded desktop backend startup
- Native PyQt6/PySide6 UI for all TestGen features
- Single-file PyInstaller builds for Windows/macOS/Linux
- Updated documentation with installation and build instructions

## Suggested Next Steps
- Confirm preferred Qt binding (PyQt6 vs PySide6).
- Decide authentication model for desktop (token vs session).
- Implement Phase 1-2 (backend config + UI skeleton) as the first milestone.
