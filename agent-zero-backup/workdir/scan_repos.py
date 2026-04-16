#!/usr/bin/env python3
"""Scan all ToXMon and wijnaldum-eth GitHub repos for commits authored by 'Tolu'."""
import subprocess
import requests
import json
import time
import sys

# Get token from git remote
token = subprocess.check_output(
    "cd /a0/usr/workdir/sentient && git remote get-url origin",
    shell=True
).decode().strip()
# Extract token from URL
import re
m = re.search(r'://[^:]+:([^@]+)@', token)
token = m.group(1) if m else ''
headers = {"Authorization": f"token {token}"}

# Check both accounts
accounts = ['ToXMon', 'wijnaldum-eth']
all_affected = []

for account in accounts:
    print(f"\n{'='*60}")
    print(f"Scanning repos for account: {account}")
    print(f"{'='*60}")
    
    # Get all repos (including forks - we'll check them too)
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{account}/repos?per_page=100&page={page}&type=all"
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            print(f"  API error for {account}: {r.status_code} - {r.text[:200]}")
            break
        data = r.json()
        if not data:
            break
        repos.extend(data)
        page += 1
        time.sleep(0.3)
    
    print(f"Found {len(repos)} repos for {account}")
    
    for repo in repos:
        name = repo['full_name']
        branch = repo.get('default_branch', 'main')
        is_fork = repo.get('fork', False)
        
        # For forks, we only care if user made commits
        try:
            # Get commits - use author=email filter
            r = requests.get(
                f"https://api.github.com/repos/{name}/commits?author=tolu@users.noreply.github.com&per_page=5",
                headers=headers
            )
            if r.status_code == 200 and r.json():
                commits = r.json()
                all_affected.append({
                    'repo': name,
                    'branch': branch,
                    'fork': is_fork,
                    'account': account,
                    'sample_commits': [c.get('sha', '')[:8] for c in commits[:3]]
                })
                fork_tag = ' (FORK)' if is_fork else ''
                print(f"  FOUND: {name}{fork_tag} - branch: {branch}")
                for c in commits[:3]:
                    msg = c.get('commit', {}).get('message', '').split('\n')[0][:60]
                    print(f"    {c.get('sha','')[:8]} - {msg}")
        except Exception as e:
            print(f"  Error checking {name}: {e}")
        time.sleep(0.5)

print(f"\n{'='*60}")
print(f"SUMMARY: {len(all_affected)} affected repos")
print(f"{'='*60}")
for a in all_affected:
    fork_tag = ' (FORK)' if a['fork'] else ''
    print(f"  {a['repo']}{fork_tag} [{a['account']}] branch: {a['branch']}")

# Save results
with open('/a0/usr/workdir/affected_repos.json', 'w') as f:
    json.dump(all_affected, f, indent=2)
print(f"\nResults saved to /a0/usr/workdir/affected_repos.json")
