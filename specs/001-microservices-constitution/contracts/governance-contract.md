# Customer Profile Contract

## Purpose

This contract describes the API expectations for the customer profile microservice and the shape of its primary resources.

## Resource: Customer Profile

### Representation
- `id`: string
- `first_name`: string
- `last_name`: string
- `email`: string
- `phone`: string
- `birth_date`: string
- `address`: string
- `demographic_segment`: string
- `preferred_language`: string
- `status`: string
- `created_at`: string
- `updated_at`: string
- `archived_at`: string
- `deleted_at`: string

### Constraints
- `id` MUST be present for all persisted profiles.
- `first_name`, `last_name`, and `email` MUST be present for active profiles.
- `email` SHOULD follow a valid address format and MUST be unique across active profiles.
- `status` MUST be one of `active`, `archived`, or `removed`.
- Timestamps MUST use ISO 8601 format.

## API Contract

### GET /profiles
- Returns a list of customer profiles.
- Supports optional filtering by `status` and `demographic_segment`.

### GET /profiles/{id}
- Returns the customer profile with the requested identifier.
- Responds with 404 if the profile is missing or removed.

### POST /profiles
- Creates a new customer profile.
- Accepts a payload containing required identity and demographic fields.
- Responds with 201 and the created profile representation.

### PUT /profiles/{id}
- Updates an existing customer profile.
- Accepts partial or full profile updates while preserving the profile identifier.
- Responds with 200 and the updated profile representation.

### DELETE /profiles/{id}
- Soft-deletes or archives the profile, preserving audit state.
- Responds with 204 for a successful archival request.

### GET /profiles/{id}/events
- Returns a list of `ProfileEvent` objects for the given profile id.

### GET /profiles/{id}/audit
- Returns a reviewable audit representation (id, event_type, timestamp, changed_by, notes) for lifecycle review.

## Validation Notes

- Invalid payloads MUST return clear validation errors.
- Missing profiles MUST return a 404 response.
- Authorization and authenticated access MUST be required for profile operations.
 - Lifecycle events (`ProfileEvent`) include `id`, `profile_id`, `event_type`, `timestamp` (ISO 8601), `changed_by`, and optional `notes`.
