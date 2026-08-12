# Quickstart

This quickstart shows basic usage of the Customer Profile microservice.

## Create a profile

POST /profiles/

Sample payload:

{
  "first_name": "Jane",
  "last_name": "Doe",
  "email": "jane.doe@example.com",
  "demographic_segment": "adult",
  "status": "active"
}

## Retrieve audit

GET /profiles/{id}/audit

Returns a reviewable list of lifecycle events with fields: `id`, `event_type`, `timestamp`, `changed_by`, `notes`.
