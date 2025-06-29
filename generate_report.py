import os
import subprocess
import csv
from collections import defaultdict
import matplotlib.pyplot as plt

# Ensure reports directory exists
os.makedirs('reports/charts', exist_ok=True)

def run_git_command(args):
    result = subprocess.run(['git'] + args, stdout=subprocess.PIPE, text=True)
    return result.stdout.strip()

def get_commit_authors():
    result = run_git_command(['shortlog', '-sne'])
    authors = []
    for line in result.split('\n'):
        if line.strip():
            parts = line.strip().split('\t')
            if len(parts) == 2:
                commit_count, author = parts
                authors.append((int(commit_count.strip()), author.strip()))
    return authors

def get_commit_hashes_by_author(author_name):
    log = run_git_command(['log', '--author=' + author_name, '--pretty=format:%H'])
    return log.splitlines()

def get_commit_details(commit_hash):
    show = run_git_command(['show', '--stat', '--oneline', commit_hash])
    diff = run_git_command(['show', '--shortstat', commit_hash])
    lines_added = 0
    lines_deleted = 0
    if "insertion" in diff or "deletion" in diff:
        parts = diff.split(',')
        for part in parts:
            if 'insertion' in part:
                lines_added += int(''.join(filter(str.isdigit, part)))
            elif 'deletion' in part:
                lines_deleted += int(''.join(filter(str.isdigit, part)))
    files = run_git_command(['show', '--pretty=""', '--name-only', commit_hash]).splitlines()
    return lines_added, lines_deleted, files

# Main data structures
author_stats = defaultdict(lambda: {'commits': 0, 'files': set(), 'lines_added': 0, 'lines_deleted': 0})
file_changes = defaultdict(int)
file_types = defaultdict(lambda: defaultdict(int))
prefix_counts = defaultdict(lambda: defaultdict(int))

authors = get_commit_authors()

for _, author in authors:
    author_email = author.split('<')[-1].strip('>')
    commit_hashes = get_commit_hashes_by_author(author_email)
    for commit in commit_hashes:
        lines_added, lines_deleted, files = get_commit_details(commit)

        author_stats[author]['commits'] += 1
        author_stats[author]['lines_added'] += lines_added
        author_stats[author]['lines_deleted'] += lines_deleted
        for f in files:
            author_stats[author]['files'].add(f)
            file_changes[(author, f)] += 1
            ext = os.path.splitext(f)[-1]
            file_types[author][ext] += 1

        show_msg = run_git_command(['log', '-1', '--pretty=%B', commit])
        for prefix in ['frontend/', 'backend/', 'testing/']:
            if show_msg.strip().startswith(prefix):
                prefix_counts[author][prefix] += 1

# Write CSVs
with open('reports/contribution_report.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Author', 'Commits', 'Files Changed', 'Lines Added', 'Lines Deleted'])
    for author, stats in author_stats.items():
        writer.writerow([author, stats['commits'], len(stats['files']), stats['lines_added'], stats['lines_deleted']])

with open('reports/file_list.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Author', 'Filename', 'Change Count'])
    for (author, fname), count in file_changes.items():
        writer.writerow([author, fname, count])

with open('reports/file_type_breakdown.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Author', 'File Type', 'Count'])
    for author, ftypes in file_types.items():
        for ext, count in ftypes.items():
            writer.writerow([author, ext, count])

with open('reports/commit_prefix_breakdown.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Author', 'Prefix', 'Commit Count'])
    for author, prefix_data in prefix_counts.items():
        for prefix, count in prefix_data.items():
            writer.writerow([author, prefix, count])

# Charts
def save_bar_chart(data, title, ylabel, filename):
    plt.figure(figsize=(10, 5))
    names = list(data.keys())
    values = list(data.values())
    plt.barh(names, values, color='skyblue')
    plt.xlabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(f'reports/charts/{filename}')
    plt.close()

save_bar_chart({k: v['commits'] for k, v in author_stats.items()}, 'Commits per Author', 'Commits', 'commits_per_author.png')
save_bar_chart({k: v['lines_added'] for k, v in author_stats.items()}, 'Lines Added per Author', 'Lines Added', 'lines_added_per_author.png')
save_bar_chart({k: v['lines_deleted'] for k, v in author_stats.items()}, 'Lines Deleted per Author', 'Lines Deleted', 'lines_deleted_per_author.png')

