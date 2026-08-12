# Data Model: Customer Profile Microservice

## Core Entities

### Customer Profile
- **id**: unique profile identifier
- **first_name**: customer's first name
- **last_name**: customer's last name
- **email**: contact email address
- **phone**: contact phone number
- **birth_date**: date of birth or age indicator
- **address**: primary mailing address or contact location
- **demographic_segment**: category such as region, age group, or customer tier
- **preferred_language**: customer language preference
- **status**: active, archived, or removed
- **created_at**: timestamp when the profile was created
- **updated_at**: timestamp when the profile was last updated
- **archived_at**: timestamp when the profile was soft-deleted or archived
- **deleted_at**: timestamp when the profile is no longer active

### Demographic Details
- **profile_id**: reference to the customer profile
- **region**: geographic region or market
- **age_group**: demographic age classification
- **segment**: customer segment or persona grouping
- **classification_notes**: optional context for demographic assignment

### Profile Event
- **id**: unique event identifier
- **profile_id**: reference to the customer profile
- **event_type**: created, updated, archived, restored
- **timestamp**: event occurrence time
- **changed_by**: actor or system that triggered the event
- **notes**: optional rationale or context for the lifecycle change

## Relationships

- A Customer Profile owns one Demographic Details record.
- A Customer Profile can have many Profile Events for audit and lifecycle tracking.
- Demographic Details are derived from, and directly associated with, a Customer Profile.

## Validation Rules

- Customer Profile records MUST have a non-empty id, first_name, last_name, and email.
- Email values SHOULD follow a valid email format and MUST be unique across active profiles.
- Profile status MUST be one of active, archived, or removed.
- Archived or removed profiles MUST preserve their created_at and updated_at history.
- Profile Event records MUST capture the event_type, timestamp, and changed_by details.
