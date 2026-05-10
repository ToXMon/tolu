# Kronos Condor Cup Planning Session

Date: 2026-05-10

## Summary

Created a local planning repository for the Condor Builders Cup trading-agent project:

- Repo path: `/a0/usr/workdir/kronos-condor-cup`
- Initial commit: `b09b2aa Initialize Kronos Condor Cup planning repository`
- ASE run: `/a0/usr/workdir/.ase/runs/run-20260510-203809-6ba2`

## Inputs inspected

- Condor source: `/a0/usr/workdir/condor-main/condor-main`
- Kronos source: `/a0/usr/workdir/kronos-main/Kronos-master`
- X-monitor: `/a0/usr/workdir/x-monitor`
- Geo-Alpha report: `/a0/usr/workdir/Geo-Alpha Trading Scan Report.md`
- Condor docs intro and llms index via browser
- Botcamp Condor Builders Cup page via browser DOM extraction and screenshot

## Key competition facts

- Hackathon: May 22-Jun 22, 2026
- Live competition: July 6-8, 2026, 48h live event
- Selected agents receive $2,000 trading capital
- No manual intervention during competition
- Scoring includes returns, risk-adjusted performance, and consistency
- Submit agent and backtesting results

## Planning decisions

- No implementation or live trading was performed.
- Live trading remains disabled until human approval.
- Architecture centers on Condor routines, Hummingbot executors, Kronos forecasting, X-monitor social signals, and Geo-Alpha macro/on-chain regime signals.
- Ranked strategy archetypes:
  1. Major-asset regime positioning
  2. Adaptive grid/range scalping
  3. Social-macro momentum confirmation

## Open decisions for Tolu

- Target venue/team
- Asset universe
- Max drawdown and sizing rules
- Kronos model size
- Single-strategy vs multi-strategy allocation
- Private vs public GitHub remote
