# Tasks: Customer Profile Microservice

**Input**: Design documents from `/specs/001-microservices-constitution/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Task-driven unit and integration tests are included so each story can be validated independently.

**Organization**: Tasks are grouped by user story for independent implementation and verification.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize the customer profile microservice project structure, dependencies, and shared tooling.

- [x] T001 Create the project directory structure in `src/models/`, `src/repositories/`, `src/services/`, `src/api/`, `src/db/`, and `tests/`
- [x] T002 Initialize Python 3.11 project metadata and dependency configuration in `pyproject.toml` and `requirements.txt`
- [x] T003 [P] Add linting, formatting, and pre-commit tooling in `.pre-commit-config.yaml` and `pyproject.toml`
- [x] T004 [P] Add feature context and implementation notes to `README.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Establish the core customer profile data model, persistence interfaces, validation, error handling, API shell, and observability.

- [x] T005 Implement the `CustomerProfile` entity in `src/models/customer_profile.py`
- [x] T006 Implement the `ProfileEvent` audit entity in `src/models/profile_event.py`
- [x] T007 Create the customer profile repository interface in `src/repositories/customer_profile_repository.py`
- [x] T008 Create the PostgreSQL schema definition and migration stub in `src/db/schema.py`
- [x] T009 Implement shared payload validation and business rule helpers in `src/services/validation.py`
- [x] T010 Implement shared API error handling and response models in `src/api/errors.py`
- [x] T011 Create the FastAPI application shell and router wiring in `src/api/main.py`
- [x] T012 Create the profiles router and wire it into `src/api/main.py`
- [x] T013 Implement the customer profile service layer in `src/services/customer_profile_service.py`
- [x] T014 Implement authorization and request context placeholders in `src/api/auth.py`
- [x] T015 Implement observability and health endpoints (`/healthz`, `/readyz`, `/livez`) in `src/api/main.py` and structured logging scaffolding in `src/api/errors.py`

**Checkpoint**: Foundation ready and unblocks all user story implementation.

---

## Phase 3: User Story 1 - Manage customer profiles (Priority: P1) **MVP1**

**Goal**: Build customer profile CRUD operations so profiles can be created, retrieved, updated, and referenced.

**Independent Test**: Create a profile, retrieve it by ID, update the record, and confirm the persisted values.

- [ ] T016 [MVP1] [US1] Implement profile creation logic in `src/services/customer_profile_service.py`
- [ ] T017 [MVP1] [US1] Implement profile retrieval by ID in `src/services/customer_profile_service.py`
- [ ] T018 [MVP1] [US1] Implement profile update logic in `src/services/customer_profile_service.py`
- [ ] T019 [MVP1] [US1] Implement POST `/profiles` and GET `/profiles/{id}` endpoints in `src/api/routes/profiles.py`
- [ ] T020 [MVP1] [US1] Add request validation and error mapping for profile creation and retrieval in `src/api/routes/profiles.py`
- [ ] T021 [MVP1] [US1] Add unique identifier handling and active-profile lookup in `src/repositories/customer_profile_repository.py`
- [ ] T022 [MVP1] [US1] Implement duplicate-profile detection and prevention in `src/repositories/customer_profile_repository.py`
- [ ] T023 [MVP1] [US1] Create unit tests for profile creation, retrieval, and update in `tests/unit/test_customer_profile_service.py`
- [ ] T024 [MVP1] [US1] Create integration tests for profile CRUD flows in `tests/integration/test_profiles_api.py`

**Checkpoint**: User Story 1 is complete when core CRUD flows are working and testable.

---

## Phase 4: User Story 2 - Keep demographic information accurate (Priority: P2) **MVP1**

**Goal**: Ensure demographic fields are stored, updated, and surfaced consistently for customer profiles.

**Independent Test**: Update demographic attributes and verify the revised values are returned through the API.

- [ ] T025 [MVP1] [US2] Extend the `CustomerProfile` model with demographic fields in `src/models/customer_profile.py`
- [ ] T026 [MVP1] [US2] Implement demographic update handling in `src/services/customer_profile_service.py`
- [ ] T027 [MVP1] [US2] Implement demographic validation and missing-field reporting in `src/services/validation.py`
- [ ] T028 [MVP1] [US2] Implement GET `/profiles` with filtering by `status` and `demographic_segment` in `src/api/routes/profiles.py`
- [ ] T029 [MVP1] [US2] Enhance PUT `/profiles/{id}` to support demographic field updates in `src/api/routes/profiles.py`
- [ ] T030 [MVP1] [US2] Create unit tests for demographic update handling in `tests/unit/test_customer_profile_service.py`
- [ ] T031 [MVP1] [US2] Create integration tests for demographic update and filtering scenarios in `tests/integration/test_profiles_api.py`

**Checkpoint**: User Story 2 is complete when demographic updates and filters behave as expected.

---

## Phase 5: User Story 3 - Support controlled profile lifecycle operations (Priority: P3)

**Goal**: Implement profile archival and soft-delete lifecycle behavior with auditability.

**Independent Test**: Archive or remove a profile and verify the lifecycle state is preserved and returned consistently.

- [ ] T032 [US3] Add profile status and lifecycle timestamps to `CustomerProfile` in `src/models/customer_profile.py`
- [ ] T033 [US3] Implement lifecycle event creation in `src/services/customer_profile_service.py`
- [ ] T034 [US3] Implement DELETE `/profiles/{id}` as a soft-delete/archival endpoint in `src/api/routes/profiles.py`
- [ ] T035 [US3] Implement removed/archived profile validation and state transitions in `src/services/customer_profile_service.py`
- [ ] T036 [US3] Add 404 handling for missing or removed profiles in `src/api/routes/profiles.py`
- [ ] T037 [US3] Create unit tests for profile lifecycle and soft-delete behavior in `tests/unit/test_customer_profile_service.py`
- [ ] T038 [US3] Create integration tests for archive/remove workflows in `tests/integration/test_profiles_api.py`
- [ ] T039 [US3] Implement lifecycle audit review support and event persistence verification in `src/services/customer_profile_service.py`

**Checkpoint**: User Story 3 is complete when lifecycle operations are auditable and consistent.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Finalize the API contract, quickstart guidance, and shared reliability behavior.

- [ ] T040 [P] Update `specs/001-microservices-constitution/contracts/governance-contract.md` to reflect the customer profile endpoint schema, including profile creation, update, filtering, and lifecycle status fields
- [ ] T041 [P] Update `specs/001-microservices-constitution/quickstart.md` with profile creation, retrieval, update, archival, and health-check validation scenarios
- [ ] T042 [P] Create integration tests for error responses in `tests/integration/test_profiles_api_errors.py`
- [ ] T043 [P] Review authorization placeholders and request context handling in `src/api/auth.py` and `src/api/main.py`
- [ ] T044 [P] Review data model audit semantics in `specs/001-microservices-constitution/data-model.md`
- [ ] T045 [P] Add README validation notes referencing profile lifecycle and health endpoints in `README.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies, can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion and blocks all user story implementation.
- **User Stories (Phase 3+)**: Depend on Foundational completion.
- **Polish (Phase 6)**: Depends on user story completion.

### User Story Dependencies

- **User Story 1 (P1)**: Requires Foundational completion.
- **User Story 2 (P2)**: Requires Foundational completion; can proceed in parallel with US1 after that.
- **User Story 3 (P3)**: Requires Foundational completion; can proceed in parallel with US1 and US2 after that.

### Parallel Opportunities

- T003, T004, T030, T031, T037, T038, T042, T043, T044, and T045 are parallelizable across different files.
- T025–T029 and T032–T036 can proceed in parallel across stories once foundational work is complete.
- Profile model, repository, service, and route tasks can be split across team members after Phase 2.

### Execution Order by Story

- **MVP1**: US1 and US2 together, delivered after Foundational.
- **Next Scope**: US3 follows once US1 and US2 are validated.

---

## Parallel Example: User Story 1

- Write unit tests and implement profile creation, retrieval, and update logic in parallel where possible.
- Implement POST `/profiles` and GET `/profiles/{id}` endpoints after the service layer is available.

## Parallel Example: User Story 2

- Extend the model and add demographic validation in parallel with demographic endpoint wiring.
- Add filtering and update support after the base profile retrieval flow is stable.

## Implementation Strategy

### MVP First

1. Complete Phase 1: Setup.
2. Complete Phase 2: Foundational.
3. Deliver User Story 1 and User Story 2 as MVP1.
4. Validate the profile CRUD path and demographic update flow independently.
5. Continue with User Story 3 and polish.

### Incremental Delivery

1. Establish the shared service shell, validation, and health endpoint scaffolding.
2. Deliver each story in priority order while keeping them independently testable.
3. Finalize with contract updates and quickstart validation.
