# Payment Gating

Require visitors to pay with stablecoins on the Tempo network before accessing your site.

## Setup

1. Set your Tempo wallet address:
```bash
curl -sS -X PATCH https://here.now/api/v1/wallet \
  -H "Authorization: Bearer $API_KEY" \
  -H "content-type: application/json" \
  -d '{"address": "0xYOUR_TEMPO_ADDRESS"}'
```

2. Set a price on a site:
```bash
curl -sS -X PATCH https://here.now/api/v1/publish/$SLUG/metadata \
  -H "Authorization: Bearer $API_KEY" \
  -H "content-type: application/json" \
  -d '{"price": {"amount": "0.50", "currency": "USD"}}'
```

3. Override recipient per site:
```json
{"price": {"amount": "1.00", "currency": "USD", "recipientAddress": "0xOTHER_ADDRESS"}}
```

4. Remove price: `{"price": null}`

## 402 Response for Agents
When a programmatic client hits a paid site, the 402 response includes:
```json
{
  "price": {"amount": "0.10", "currency": "USD", "recipientAddress": "0xe661..."},
  "paymentSession": {
    "createUrl": "https://here.now/api/pay/<slug>/session",
    "pollUrl": "https://here.now/api/pay/<slug>/poll",
    "grantUrl": "https://here.now/api/pay/<slug>/grant"
  }
}
```

Session flow: POST createUrl → poll pollUrl every 3s → POST grantUrl with session ID + tx hash → fetch with `?__hn_grant=<token>`

## Notes
- Mutually exclusive with password protection and forkable
- Payment gating survives redeploys
