import csv
import os
from collections import defaultdict
from git import Repo

repo = Repo(os.getcwd())
main_branch = repo.heads.main

author_commits = defaultdict(int)
author_lines = defaultdict(int)
author_prefixes = defaultdict(lambda: {'frontend/': 0, 'backend/': 0, 'testing/': 0})
author_filetypes = defaultdict(lambda: defaultdict(int))
author_files = defaultdict(set)

EMPTY_TREE = '4b825dc642cb6eb9a060e54bf8d69288fbee4904'

for commit in repo.iter_commits(main_branch, no_merges=True):
    author = commit.author.name
    author_commits[author] += 1

    # Handle stats for first commit
    if commit.parents:
        diff = commit.diff(commit.parents[0], create_patch=True)
        stats = commit.stats
    else:
        # Diff against the empty tree
        diff = commit.diff(EMPTY_TREE, create_patch=True)
        stats = repo.git.diff('--numstat', EMPTY_TREE, commit.hexsha)
        # Parse numstat output manually for lines changed
        insertions = deletions = 0
        files_touched = []
        for line in stats.splitlines():
            parts = line.split('\t')
            if len(parts) >= 3:
                ins, dels, path = parts
                try:
                    insertions += int(ins)
                except ValueError:
                    pass
                try:
                    deletions += int(dels)
                except ValueError:
                    pass
                files_touched.append(path)
        author_lines[author] += insertions + deletions
        for path in files_touched:
            ext = os.path.splitext(path)[1] or 'NO_EXT'
            author_filetypes[author][ext] += 1
            author_files[author].add(path)
        # Continue with prefixes
        msg = commit.message.lower()
        for prefix in ['frontend/', 'backend/', 'testing/']:
            if msg.startswith(prefix):
                author_prefixes[author][prefix] += 1
        continue

    author_lines[author] += stats.total['insertions'] + stats.total['deletions']
    msg = commit.message.lower()
    for prefix in ['frontend/', 'backend/', 'testing/']:
        if msg.startswith(prefix):
            author_prefixes[author][prefix] += 1
    for filepath, fstats in stats.files.items():
        ext = os.path.splitext(filepath)[1] or 'NO_EXT'
        author_filetypes[author][ext] += 1
        author_files[author].add(filepath)

os.makedirs('stats', exist_ok=True)

# 1. author_commit_stats.csv
with open('stats/author_commit_stats.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Author', 'Commits', 'Lines Changed'])
    for author in author_commits:
        writer.writerow([author, author_commits[author], author_lines[author]])

# 2. author_commit_prefixes.csv
with open('stats/author_commit_prefixes.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Author', 'frontend/', 'backend/', 'testing/'])
    for author in author_prefixes:
        p = author_prefixes[author]
        writer.writerow([author, p['frontend/'], p['backend/'], p['testing/']])

# 3. author_filetypes.csv
filetypes = set()
for d in author_filetypes.values():
    filetypes.update(d.keys())
filetypes = sorted(filetypes)
with open('stats/author_filetypes.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Author'] + filetypes)
    for author in author_filetypes:
        row = [author] + [author_filetypes[author].get(ft, 0) for ft in filetypes]
        writer.writerow(row)

# 4. author_files_modified.csv
with open('stats/author_files_modified.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Author', 'Files Modified'])
    for author in author_files:
        files = sorted(author_files[author])
        writer.writerow([author, '; '.join(files)])
