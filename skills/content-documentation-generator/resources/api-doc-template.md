---
title: "[API Name]"
description: "[API purpose ≤160 characters]"
keywords: [api, rest, endpoint, resource]
generated_at: "[ISO-8601 timestamp]"
style_guide: "write-the-docs"
---

# [API Name]

[One-sentence description of API purpose]

## Base URL

```
https://api.example.com/v1
```

## Authentication

[Authentication method description]

**Example:**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.example.com/v1/resource
```

## Endpoints

### [HTTP Method] /[resource-path]

[Endpoint description]

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| param1 | string | Yes | [Description] |
| param2 | integer | No | [Description] |

**Request Example:**
```json
{
  "param1": "value",
  "param2": 123
}
```

**Response (200 OK):**
```json
{
  "id": "resource_id",
  "status": "success"
}
```

**Response (400 Bad Request):**
```json
{
  "error": "invalid_parameter",
  "message": "param1 is required"
}
```

## Error Codes

| Code | Message | Description |
|------|---------|-------------|
| 400 | Bad Request | Invalid parameters |
| 401 | Unauthorized | Missing or invalid token |
| 404 | Not Found | Resource does not exist |
| 500 | Server Error | Internal error occurred |

## Rate Limiting

[Rate limit description]

- Rate: [X requests per minute]
- Headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`

## Resources

- [API Reference](https://api.example.com/docs)
- [OpenAPI Specification](https://api.example.com/openapi.json)
