# DNS Hijacking Campaign Targeting .fi DeFi Domains

**Date saved**: 2026-04-15
**Source**: Web3Sec News Newsletter — "The .fi Files: A Field Report on DNS Hijacking in DeFi"
**Source URL**: https://web3secnews.substack.com/p/the-fi-files-a-field-report-on-dns

## Summary

Coordinated DNS hijacking campaign hitting DeFi protocols on `.fi` domains. Four protocols compromised within weeks — all through registrar social engineering, not code exploits. Smart contracts and frontend code were fine; the attack surface was infrastructure-level.

## Affected Protocols

| Protocol | Domain | Attack Vector |
|----------|--------|---------------|
| Cow.fi | cow.fi | Registrar compromise, iframe shell served |
| Steakhouse | — | DNS hijack |
| HypurrFi | — | DNS hijack |
| Neutrl | — | DNS hijack |

All four hit within a few weeks. All `.fi` domains. All infrastructure takeover.

## Attacker TTPs

### TTP-1: Registrar Social Engineering via Email Change
Bypass credentials entirely. Go straight to registrar support. Request email account change using OSINT + convincing story + receiving domain that looks plausible to the support agent.

### TTP-2: Time-Based Rapid Execution
Rapid exploitation of open window. Suggests automation supporting the SE layer, or multiple targets worked simultaneously.

### TTP-3: Registrar as the Weak Link
Registrar approved the request before notifying the account holder. If you're slower than 30 minutes, it's already done. Procedural failure, systematically exploited.

### TTP-4: Consistent Initial Access Across All .fi Incidents
Same entry point every time: convince a human at a registrar to make a change. The core move is identical across all four incidents.

## Attack Chain

1. Attacker registers a domain visually similar to target
2. Social-engineers registrar support to change account email to their controlled domain
3. Once email changed → password reset → full account ownership
4. Nameserver changes → DNS redirect → TLS cert issuance → frontend replacement
5. Fresh TLS cert issued same day (Let's Encrypt, domain-validated — only requires DNS control)
6. Malicious frontend serves iframe shell loading attacker-controlled content

## Detection Signals

- **CERT_FRESHLY_ISSUED** on an established domain = clean indicator of active takeover
- Certificate Transparency logs make this detectable in near-real-time
- `dig NS <domain> +short` for nameserver change monitoring
- WHOIS change detection

## Defensive Recommendations

### Immediate Actions
- **Move to enterprise-grade DNS**: AWS Route 53, Cloudflare, or equivalent
- **Registrar hygiene**: TOTP or hardware key 2FA (not SMS). Dedicated registration email. Registry lock enabled if supported.
- **Split DNS from registrar**: Two accounts = two separate compromises required
- **Implement DNSSEC**: Cryptographic signing of DNS records. Supported on `.fi`

### Monitoring
- CT log watching for unexpected cert issuance
- WHOIS change detection
- Nameserver modification alerts
- Continuous domain integrity verification

### Incident Response Playbook
- Pre-establish security contacts at registrar's security team
- Pre-authorize emergency transfer procedures
- Have a trusted fallback domain ready
- Enable every MFA form available immediately
- Contact attacker's domain registrar to report abuse and block SMTP
- Threaten ICANN complaint if registrar is slow
- Prepare user migration to alternate domain

## Key Insight

The ecosystem spent five years on audits, formal verification, bug bounties, immutable proxies, timelocks — solving hard technical problems. Then someone called a registrar, pretended to be the domain owner, changed a nameserver, and none of that mattered.

Infrastructure security needs normative pressure matching what the ecosystem built around contract security.

## Tools Mentioned

- **DigiBastion** (digibastion.com): Continuous domain security and frontend integrity monitoring for Web3 protocols
- **Guardix.io**: AI-powered security audits for Solidity smart contracts

## Tags

`dns-hijacking` `defi-security` `fi-domains` `registrar-compromise` `social-engineering` `infrastructure-security` `web3` `certificate-transparency` `dnssec` `incident-response`
