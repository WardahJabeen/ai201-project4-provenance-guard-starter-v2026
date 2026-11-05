# Appeal path (criterion 4) — before

- Produced by: `eval_appeals.py::main`
- Service: `app.py::submit`, `app.py::appeal`

## Trial 1

```json
{
  "appeals": [
    {
      "submit_status": 200,
      "content_id": "7c2f80d8-0b02-4520-872e-a3e9b9c7f335",
      "appeal_status": 200,
      "appeal_response": {
        "content_id": "7c2f80d8-0b02-4520-872e-a3e9b9c7f335",
        "message": "Thanks, we've received your appeal. A person will review your writing.",
        "status": "under_review"
      },
      "appeal_in_log_as_under_review": true
    },
    {
      "submit_status": 200,
      "content_id": "2036c055-f676-47e2-9d89-07aa2671492f",
      "appeal_status": 200,
      "appeal_response": {
        "content_id": "2036c055-f676-47e2-9d89-07aa2671492f",
        "message": "Thanks, we've received your appeal. A person will review your writing.",
        "status": "under_review"
      },
      "appeal_in_log_as_under_review": true
    },
    {
      "submit_status": 200,
      "content_id": "c385f7ec-9f87-47bc-9f67-bae7d98874dd",
      "appeal_status": 200,
      "appeal_response": {
        "content_id": "c385f7ec-9f87-47bc-9f67-bae7d98874dd",
        "message": "Thanks, we've received your appeal. A person will review your writing.",
        "status": "under_review"
      },
      "appeal_in_log_as_under_review": true
    },
    {
      "submit_status": 200,
      "content_id": "23b48fad-2df8-4629-b5ed-9604f7d39701",
      "appeal_status": 200,
      "appeal_response": {
        "content_id": "23b48fad-2df8-4629-b5ed-9604f7d39701",
        "message": "Thanks, we've received your appeal. A person will review your writing.",
        "status": "under_review"
      },
      "appeal_in_log_as_under_review": true
    },
    {
      "submit_status": 200,
      "content_id": "7b96608f-50bf-43ef-9cd5-23bbd04a4aca",
      "appeal_status": 200,
      "appeal_response": {
        "content_id": "7b96608f-50bf-43ef-9cd5-23bbd04a4aca",
        "message": "Thanks, we've received your appeal. A person will review your writing.",
        "status": "under_review"
      },
      "appeal_in_log_as_under_review": true
    },
    {
      "submit_status": 200,
      "content_id": "540721e5-d8e0-4494-9601-ce2b345d4bfd",
      "appeal_status": 200,
      "appeal_response": {
        "content_id": "540721e5-d8e0-4494-9601-ce2b345d4bfd",
        "message": "Thanks, we've received your appeal. A person will review your writing.",
        "status": "under_review"
      },
      "appeal_in_log_as_under_review": true
    },
    {
      "submit_status": 200,
      "content_id": "9fbdce2b-fc1b-488c-849d-f0f2854c8ff9",
      "appeal_status": 200,
      "appeal_response": {
        "content_id": "9fbdce2b-fc1b-488c-849d-f0f2854c8ff9",
        "message": "Thanks, we've received your appeal. A person will review your writing.",
        "status": "under_review"
      },
      "appeal_in_log_as_under_review": true
    },
    {
      "submit_status": 200,
      "content_id": "0328c54e-2839-4f56-9ce6-3f5bdae89c11",
      "appeal_status": 200,
      "appeal_response": {
        "content_id": "0328c54e-2839-4f56-9ce6-3f5bdae89c11",
        "message": "Thanks, we've received your appeal. A person will review your writing.",
        "status": "under_review"
      },
      "appeal_in_log_as_under_review": true
    },
    {
      "submit_status": 200,
      "content_id": "9cf8a67f-0a57-4230-a41c-41f06e89a729",
      "appeal_status": 200,
      "appeal_response": {
        "content_id": "9cf8a67f-0a57-4230-a41c-41f06e89a729",
        "message": "Thanks, we've received your appeal. A person will review your writing.",
        "status": "under_review"
      },
      "appeal_in_log_as_under_review": true
    },
    {
      "submit_status": 200,
      "content_id": "31d53601-40b6-4427-a33f-1cae60883712",
      "appeal_status": 200,
      "appeal_response": {
        "content_id": "31d53601-40b6-4427-a33f-1cae60883712",
        "message": "Thanks, we've received your appeal. A person will review your writing.",
        "status": "under_review"
      },
      "appeal_in_log_as_under_review": true
    }
  ],
  "unknown_id": {
    "status": 404,
    "response": {
      "error": "unknown_content_id",
      "message": "We couldn't find a submission with that content_id. Please check it matches your result."
    },
    "log_entries_added": 1,
    "entries_added": [
      {
        "creator_id": "unknown",
        "endpoint": "/appeal",
        "event": "rejected",
        "http_status": 404,
        "reason": "unknown_content_id",
        "status": "rejected",
        "timestamp": "2026-11-05T00:46:32+00:00"
      }
    ],
    "appeal_recorded_for_made_up_id": false
  }
}
```

## Trial 2

```json
{
  "appeals": [
    {
      "submit_status": 200,
      "content_id": "819f35a8-4d5d-49e2-be46-b8ca34012293",
      "appeal_status": 200,
      "appeal_response": {
        "content_id": "819f35a8-4d5d-49e2-be46-b8ca34012293",
        "message": "Thanks, we've received your appeal. A person will review your writing.",
        "status": "under_review"
      },
      "appeal_in_log_as_under_review": true
    },
    {
      "submit_status": 200,
      "content_id": "dbb68d9b-6b54-4583-9a0c-19d76d8408e2",
      "appeal_status": 200,
      "appeal_response": {
        "content_id": "dbb68d9b-6b54-4583-9a0c-19d76d8408e2",
        "message": "Thanks, we've received your appeal. A person will review your writing.",
        "status": "under_review"
      },
      "appeal_in_log_as_under_review": true
    },
    {
      "submit_status": 200,
      "content_id": "12cdf967-5af7-4383-a4f4-1324b89ec853",
      "appeal_status": 200,
      "appeal_response": {
        "content_id": "12cdf967-5af7-4383-a4f4-1324b89ec853",
        "message": "Thanks, we've received your appeal. A person will review your writing.",
        "status": "under_review"
      },
      "appeal_in_log_as_under_review": true
    },
    {
      "submit_status": 200,
      "content_id": "96e1a3ca-1e95-4899-bf8b-92469a962be3",
      "appeal_status": 200,
      "appeal_response": {
        "content_id": "96e1a3ca-1e95-4899-bf8b-92469a962be3",
        "message": "Thanks, we've received your appeal. A person will review your writing.",
        "status": "under_review"
      },
      "appeal_in_log_as_under_review": true
    },
    {
      "submit_status": 200,
      "content_id": "bbe9680b-60c4-4aec-9981-23070eb7e104",
      "appeal_status": 200,
      "appeal_response": {
        "content_id": "bbe9680b-60c4-4aec-9981-23070eb7e104",
        "message": "Thanks, we've received your appeal. A person will review your writing.",
        "status": "under_review"
      },
      "appeal_in_log_as_under_review": true
    },
    {
      "submit_status": 200,
      "content_id": "ca574905-e964-45bd-8efb-144958ed19ce",
      "appeal_status": 200,
      "appeal_response": {
        "content_id": "ca574905-e964-45bd-8efb-144958ed19ce",
        "message": "Thanks, we've received your appeal. A person will review your writing.",
        "status": "under_review"
      },
      "appeal_in_log_as_under_review": true
    },
    {
      "submit_status": 200,
      "content_id": "f55807e6-8eb5-46ab-9dec-abb3639ceded",
      "appeal_status": 200,
      "appeal_response": {
        "content_id": "f55807e6-8eb5-46ab-9dec-abb3639ceded",
        "message": "Thanks, we've received your appeal. A person will review your writing.",
        "status": "under_review"
      },
      "appeal_in_log_as_under_review": true
    },
    {
      "submit_status": 200,
      "content_id": "576fa87d-514d-45ff-a726-c3eceda222c5",
      "appeal_status": 200,
      "appeal_response": {
        "content_id": "576fa87d-514d-45ff-a726-c3eceda222c5",
        "message": "Thanks, we've received your appeal. A person will review your writing.",
        "status": "under_review"
      },
      "appeal_in_log_as_under_review": true
    },
    {
      "submit_status": 200,
      "content_id": "5756f5fd-4e7e-4d61-84d1-ec69911404a4",
      "appeal_status": 200,
      "appeal_response": {
        "content_id": "5756f5fd-4e7e-4d61-84d1-ec69911404a4",
        "message": "Thanks, we've received your appeal. A person will review your writing.",
        "status": "under_review"
      },
      "appeal_in_log_as_under_review": true
    },
    {
      "submit_status": 200,
      "content_id": "245e53a8-6066-4fc3-a805-6de04e0a762f",
      "appeal_status": 200,
      "appeal_response": {
        "content_id": "245e53a8-6066-4fc3-a805-6de04e0a762f",
        "message": "Thanks, we've received your appeal. A person will review your writing.",
        "status": "under_review"
      },
      "appeal_in_log_as_under_review": true
    }
  ],
  "unknown_id": {
    "status": 404,
    "response": {
      "error": "unknown_content_id",
      "message": "We couldn't find a submission with that content_id. Please check it matches your result."
    },
    "log_entries_added": 1,
    "entries_added": [
      {
        "creator_id": "unknown",
        "endpoint": "/appeal",
        "event": "rejected",
        "http_status": 404,
        "reason": "unknown_content_id",
        "status": "rejected",
        "timestamp": "2026-11-05T00:46:34+00:00"
      }
    ],
    "appeal_recorded_for_made_up_id": false
  }
}
```

## Trial 3

```json
{
  "appeals": [
    {
      "submit_status": 200,
      "content_id": "e7e8001a-275d-4a08-9943-9445708b9102",
      "appeal_status": 200,
      "appeal_response": {
        "content_id": "e7e8001a-275d-4a08-9943-9445708b9102",
        "message": "Thanks, we've received your appeal. A person will review your writing.",
        "status": "under_review"
      },
      "appeal_in_log_as_under_review": true
    },
    {
      "submit_status": 200,
      "content_id": "c5745382-2572-4081-92bf-722f2ff57bde",
      "appeal_status": 200,
      "appeal_response": {
        "content_id": "c5745382-2572-4081-92bf-722f2ff57bde",
        "message": "Thanks, we've received your appeal. A person will review your writing.",
        "status": "under_review"
      },
      "appeal_in_log_as_under_review": true
    },
    {
      "submit_status": 200,
      "content_id": "483b43cf-faa8-497e-a270-2e0e9d250114",
      "appeal_status": 200,
      "appeal_response": {
        "content_id": "483b43cf-faa8-497e-a270-2e0e9d250114",
        "message": "Thanks, we've received your appeal. A person will review your writing.",
        "status": "under_review"
      },
      "appeal_in_log_as_under_review": true
    },
    {
      "submit_status": 200,
      "content_id": "ba87d058-2234-4a83-8426-79d4a6b2ba45",
      "appeal_status": 200,
      "appeal_response": {
        "content_id": "ba87d058-2234-4a83-8426-79d4a6b2ba45",
        "message": "Thanks, we've received your appeal. A person will review your writing.",
        "status": "under_review"
      },
      "appeal_in_log_as_under_review": true
    },
    {
      "submit_status": 200,
      "content_id": "e2ef4039-e7ab-43d0-ba11-2d79f9fda20c",
      "appeal_status": 200,
      "appeal_response": {
        "content_id": "e2ef4039-e7ab-43d0-ba11-2d79f9fda20c",
        "message": "Thanks, we've received your appeal. A person will review your writing.",
        "status": "under_review"
      },
      "appeal_in_log_as_under_review": true
    },
    {
      "submit_status": 200,
      "content_id": "2d3ef2a7-afd5-4a34-a50e-67d0039a647b",
      "appeal_status": 200,
      "appeal_response": {
        "content_id": "2d3ef2a7-afd5-4a34-a50e-67d0039a647b",
        "message": "Thanks, we've received your appeal. A person will review your writing.",
        "status": "under_review"
      },
      "appeal_in_log_as_under_review": true
    },
    {
      "submit_status": 200,
      "content_id": "c76bb2ed-3bd0-40ef-b95e-5e4fa4243300",
      "appeal_status": 200,
      "appeal_response": {
        "content_id": "c76bb2ed-3bd0-40ef-b95e-5e4fa4243300",
        "message": "Thanks, we've received your appeal. A person will review your writing.",
        "status": "under_review"
      },
      "appeal_in_log_as_under_review": true
    },
    {
      "submit_status": 200,
      "content_id": "94144d6f-5a48-4a82-97e4-108013cede78",
      "appeal_status": 200,
      "appeal_response": {
        "content_id": "94144d6f-5a48-4a82-97e4-108013cede78",
        "message": "Thanks, we've received your appeal. A person will review your writing.",
        "status": "under_review"
      },
      "appeal_in_log_as_under_review": true
    },
    {
      "submit_status": 200,
      "content_id": "d120d9d5-a623-438e-825f-d984e0d26ac2",
      "appeal_status": 200,
      "appeal_response": {
        "content_id": "d120d9d5-a623-438e-825f-d984e0d26ac2",
        "message": "Thanks, we've received your appeal. A person will review your writing.",
        "status": "under_review"
      },
      "appeal_in_log_as_under_review": true
    },
    {
      "submit_status": 200,
      "content_id": "e206bd33-8bf0-4ad3-8d5a-62988c0106d0",
      "appeal_status": 200,
      "appeal_response": {
        "content_id": "e206bd33-8bf0-4ad3-8d5a-62988c0106d0",
        "message": "Thanks, we've received your appeal. A person will review your writing.",
        "status": "under_review"
      },
      "appeal_in_log_as_under_review": true
    }
  ],
  "unknown_id": {
    "status": 404,
    "response": {
      "error": "unknown_content_id",
      "message": "We couldn't find a submission with that content_id. Please check it matches your result."
    },
    "log_entries_added": 1,
    "entries_added": [
      {
        "creator_id": "unknown",
        "endpoint": "/appeal",
        "event": "rejected",
        "http_status": 404,
        "reason": "unknown_content_id",
        "status": "rejected",
        "timestamp": "2026-11-05T00:46:35+00:00"
      }
    ],
    "appeal_recorded_for_made_up_id": false
  }
}
```
