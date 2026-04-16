# Email Domain Classification Rules

**Created:** 2026-04-14
**Updated:** 2026-04-14
**Purpose:** Pre-filter incoming emails for daily summary. Emails are classified into categories to determine which are summarized, auto-deleted, or flagged for attention.
**Script:** `/a0/usr/workdir/daily_email_digest.py`
**Scheduled Task:** Daily Email Digest (runs every morning at 8AM)

## Classification Categories

### 🗑️ AUTO-DELETE
Automatically trashed — never shown in daily summary.

| Domain / Sender Pattern | Reason |
|---|---|
| `adultfriendfinder.com` | Spam |
| `sexmatchbook.com` | Spam |
| `eroticads.com` | Spam |
| `bumoftheday.net` | Spam |
| `noreply@youtube.com` | Notification clutter |
| `plus.google.com` | Dead service |
| `InsideApple.Apple.com` | Marketing promo |
| `News@InsideApple.Apple.com` | Marketing promo |

### 📢 PROMO / MARKETING
Shown in summary as count only — not individual emails.

| Domain / Sender Pattern | Reason |
|---|---|
| `medium.com` | Newsletter |
| `masterclass.com` | Promo |
| `adidas.com` | Retail promo |
| `roadtrippers.com` | Newsletter |
| `expedia.com` | Travel promo |
| `coach.com` | Retail promo |
| `moneylion.com` / `beehiiv.com` | Finance promo |
| `bestegg.com` | Finance promo |
| `upgrade.com` | Finance promo |
| `projectmanagement.com` | Newsletter |
| `simplydigital.gr` | Newsletter |
| `linkedin.com` (notifications) | Social notifications |
| `glassdoor.com` | Job notifications |
| `indeed.com` | Job notifications |
| `discord.com` (notifications) | Social notifications |
| `instagram.com` (notifications) | Social notifications |
| `macys.com` | Retail promo |
| `sephora.com` | Retail promo |
| `homedepot.com` | Retail promo |
| `m.starbucks.com` | Promo |
| `thexebec.com` | Promo |
| `overstock.com` | Retail promo |
| `hm.com` | Retail promo |
| `celebritycruises.com` | Travel promo |
| `on.com` | Retail promo |
| `substack.com` | Newsletter |
| `nocode.mba` | Newsletter |
| `frontendmasters.com` | Newsletter |
| `datacamp.com` | Newsletter |
| `unstoppabledomains.com` | Promo |
| `skool.com` | Notification |
| `coindesk.com` | Newsletter |
| `ideabrowser.com` | Newsletter |
| `maven.com` | Newsletter |
| `luma-mail.com` | Calendar notification |
| `thecut.co` | Promo |
| `nextdoor.com` | Community notification |

### ⚠️ IMPORTANT — Always Show Individually

| Domain / Sender Pattern | Reason |
|---|---|
| Any `.edu` address | Academic/educational |
| Any `.gov` address | Government |
| `bankofamerica.com` / `bofa.com` | Banking |
| `wellsfargo.com` | Banking |
| `chase.com` | Banking |
| `americanexpress.com` | Banking |
| `github.com` | Development |
| `microsoft.com` | Work/account |
| `accounts.google.com` | Account/security |
| `notify.cloudflare.com` | Infrastructure |
| `uphold.com` | Finance |
| SUBJECT contains: `statement`, `invoice`, `receipt`, `confirmation`, `verification`, `password`, `security`, `alert`, `urgent` | Financial/security |
| SUBJECT contains: `interview`, `offer`, `contract`, `agreement`, `lease` | Career/legal |
| SUBJECT contains: `security alert`, `account recovered`, `new sign-in`, `verify your email`, `new login`, `domain registered`, `webhook` | Security alerts |
| Has attachments | Potential important docs |

### 📬 PERSONAL — Always Show Individually
Any email from a real person (not matching automated sender patterns like noreply, no-reply, newsletter, shop@, team@, etc.).

### 🔧 Rules Engine

```
FOR each email:
  1. Check AUTO-DELETE list → trash immediately, skip summary
  2. Check IMPORTANT patterns → show individually in summary
  3. Check PROMO list → aggregate count in summary
  4. Check PERSONAL (human sender, not automated) → show individually
  5. Everything else → show individually (uncategorized)
```

## Daily Summary Format

```
# 📬 Email Daily Digest — {date}

## ⚠️ Action Needed ({count})
[Individual emails requiring attention]

## 📬 Personal Emails ({count})
[Individual emails from real people]

## 📢 Promo/Newsletter Summary ({total_count} from {sender_count} senders)
| Sender | Count |

## 🗑️ Auto-Deleted ({count})
| Sender | Count |

## ❓ Uncategorized ({count})
[Individual emails not yet classified]
```

## Adding New Rules
To add a new domain to a category, edit BOTH:
1. This file: `memory-palace/wings/technical/rooms/email-domain-rules.md`
2. The script: `/a0/usr/workdir/daily_email_digest.py`
