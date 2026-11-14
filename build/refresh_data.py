"""Read public GitHub data with gh; credentials stay in gh/the environment."""
from datetime import datetime, timezone
from pathlib import Path
import json
import os
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
LOGIN = 'USERSATOSHI'

def graphql(query, **variables):
    result = subprocess.run(
        ['gh', 'api', 'graphql', '--input', '-'],
        input=json.dumps({'query': query, 'variables': variables}),
        text=True, capture_output=True,
    )
    if result.returncode:
        raise RuntimeError('GitHub data request failed. Check token access and API limits. ' + result.stderr.strip())
    response = json.loads(result.stdout)
    if response.get('errors'):
        raise RuntimeError('GitHub GraphQL returned errors: ' + json.dumps(response['errors']))
    return response

def write_json(path, value):
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(value, indent=2) + '\n')
    os.replace(temporary, path)

def main():
    response = graphql('''query($login: String!) {
      user(login: $login) {
        id login name avatarUrl url bio
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks { contributionDays { contributionCount date weekday } }
          }
        }
      }
    }''', login=LOGIN)
    user = response['data']['user']
    if not user:
        raise RuntimeError('Profile user was not found')
    calendar = user['contributionsCollection']['contributionCalendar']
    days = [d for w in calendar['weeks'] for d in w['contributionDays']]
    if not days or sum(d['contributionCount'] for d in days) != calendar['totalContributions']:
        raise RuntimeError('Contribution data is incomplete; keeping the previous snapshot')
    selected = json.loads((ROOT / 'build/selected.json').read_text())
    queries = []
    for i, repository in enumerate(selected):
        owner, name = repository['nameWithOwner'].split('/')
        if not re.fullmatch(r'[A-Za-z0-9_.-]+', owner) or not re.fullmatch(r'[A-Za-z0-9_.-]+', name):
            raise ValueError('Invalid configured repository name')
        queries.append(f'''r{i}: repository(owner: {json.dumps(owner)}, name: {json.dumps(name)}) {{
          nameWithOwner url isPrivate isArchived stargazerCount
          defaultBranchRef {{ name target {{ ... on Commit {{
            history(author: {{id: $author}}) {{ totalCount }}
          }} }} }}
        }}''')
    repositories = graphql('query($author: ID!) {' + '\n'.join(queries) + '}', author=user['id'])['data']
    refreshed = []
    for i in range(len(selected)):
        repository = repositories[f'r{i}']
        if not repository or repository['isPrivate'] or not repository['defaultBranchRef']:
            raise RuntimeError('A selected repository is unavailable or private; keeping the previous snapshot')
        repository['authoredCommits'] = repository['defaultBranchRef']['target']['history']['totalCount']
        refreshed.append(repository)
    # All requests and validation complete before replacing any data files.
    snapshot = datetime.now(timezone.utc).date()
    write_json(ROOT / 'data/calendar.json', response)
    write_json(ROOT / 'build/selected.json', refreshed)
    write_json(ROOT / 'data/snapshot.json', {'date': snapshot.isoformat(), 'login': LOGIN})
    readme = ROOT / 'README.md'
    text = re.sub(r'Activity snapshot: [^.]+\.', 'Activity snapshot: ' + snapshot.strftime('%d %B %Y').lstrip('0') + '.', readme.read_text())
    readme.write_text(text)
    print(f'Refreshed {len(days)} contribution days and {len(refreshed)} public projects for {snapshot}.')

if __name__ == '__main__':
    main()
