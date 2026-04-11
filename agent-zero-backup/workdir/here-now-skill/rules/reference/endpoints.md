# API Endpoint Reference

## Base URL
`https://here.now/api/v1`

## Publish
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/publish` | Optional | Create site |
| PUT | `/publish/:slug` | Optional | Update site |
| POST | `/publish/:slug/finalize` | Optional | Finalize version |
| DELETE | `/publish/:slug` | Required | Delete site |
| POST | `/publish/:slug/claim` | Required | Claim anonymous site |
| POST | `/publish/:slug/duplicate` | Required | Duplicate site |
| PATCH | `/publish/:slug/metadata` | Required | Patch metadata |
| POST | `/publish/:slug/uploads/refresh` | Required | Refresh upload URLs |

## Query
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/publishes` | Required | List owned sites |
| GET | `/publish/:slug` | Required | Get site details |

## Variables
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| PUT | `/me/variables/:name` | Required | Create/update variable |
| GET | `/me/variables` | Required | List variables |
| DELETE | `/me/variables/:name` | Required | Delete variable |

## Wallet
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/wallet` | Required | Get wallet address |
| PATCH | `/wallet` | Required | Set/remove wallet |

## Domains
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/domains` | Required | Add domain |
| GET | `/domains` | Required | List domains |
| GET | `/domains/:domain` | Required | Check domain status |
| DELETE | `/domains/:domain` | Required | Remove domain |

## Handle
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/handle` | Required | Create handle |
| GET | `/handle` | Required | Get handle |
| PATCH | `/handle` | Required | Update handle |
| DELETE | `/handle` | Required | Delete handle |

## Links
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/links` | Required | Create link |
| GET | `/links` | Required | List links |
| GET | `/links/:location` | Required | Get link |
| PATCH | `/links/:location` | Required | Update link |
| DELETE | `/links/:location` | Required | Delete link |

## Auth
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/auth/agent/request-code` | None | Request verification code |
| POST | `/auth/agent/verify-code` | None | Verify code, get API key |

## Aliases
All `/publish` endpoints also work at `/artifact`.
All `/publishes` also works at `/artifacts`.
