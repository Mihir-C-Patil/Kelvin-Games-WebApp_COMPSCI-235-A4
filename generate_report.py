
import os
import subprocess
import csv
from collections import defaultdict, Counter
from pathlib import Path
import matplotlib.pyplot as plt

# Ensure reports directory exists
os.makedirs("reports/charts", exist_ok=True)

# Get git log information
log_output = subprocess.check_output(
    ["git", "log", "--pretty=format:%an|%ae|%s", "--numstat"],
    text=True
)

lines = log_output.strip().split("\n")
contrib_stats = defaultdict(lambda: {
    "commits": 0,
    "lines_added": 0,
    "lines_deleted": 0,
    "files_changed": set(),
    "file_types": Counter(),
    "files_list": Counter(),
    "prefixes": Counter()
})

current_author = None
current_email = None

for line in lines:
    if '|' in line:
        # New commit line
        parts = line.split('|', 2)
        if len(parts) < 3:
            continue
        current_author, current_email, message = parts
        author_key = f"{current_author} <{current_email}>"
        contrib_stats[author_key]["commits"] += 1

        # Count prefix
        if message.startswith("frontend/"):
            contrib_stats[author_key]["prefixes"]["frontend"] += 1
        elif message.startswith("backend/"):
            contrib_stats[author_key]["prefixes"]["backend"] += 1
        elif message.startswith("testing/"):
            contrib_stats[author_key]["prefixes"]["testing"] += 1
        elif message.startswith("infra/"):
            contrib_stats[author_key]["prefixes"]["infra"] += 1
    elif line.strip():
        parts = line.split("\t")
        if len(parts) != 3:
            continue
        try:
            added = int(parts[0])
            deleted = int(parts[1])
            filename = parts[2]
        except ValueError:
            continue

        file_type = Path(filename).suffix
        contrib_stats[author_key]["lines_added"] += added
        contrib_stats[author_key]["lines_deleted"] += deleted
        contrib_stats[author_key]["files_changed"].add(filename)
        contrib_stats[author_key]["file_types"][file_type] += 1
        contrib_stats[author_key]["files_list"][filename] += 1

# Write contribution_report.csv
with open("reports/contribution_report.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Author", "Commits", "Files Changed", "Lines Added", "Lines Deleted"])
    for author, data in contrib_stats.items():
        writer.writerow([
            author,
            data["commits"],
            len(data["files_changed"]),
            data["lines_added"],
            data["lines_deleted"]
        ])

# Write commit_prefix_breakdown.csv
with open("reports/commit_prefix_breakdown.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Author", "frontend", "backend", "testing", "infra", "total_commits"])
    for author, data in contrib_stats.items():
        writer.writerow([
            author,
            data["prefixes"]["frontend"],
            data["prefixes"]["backend"],
            data["prefixes"]["testing"],
            data["prefixes"]["infra"],
            data["commits"]
        ])

# Write file_type_breakdown.csv
with open("reports/file_type_breakdown.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Author", "File Type", "Count"])
    for author, data in contrib_stats.items():
        for ftype, count in data["file_types"].items():
            writer.writerow([author, ftype, count])

# Write file_list.csv
with open("reports/file_list.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Author", "Filename", "Change Count"])
    for author, data in contrib_stats.items():
        for fname, count in data["files_list"].items():
            writer.writerow([author, fname, count])

# Plotting helper
def save_bar_chart(data_dict, title, filename, ylabel):
    authors = list(data_dict.keys())
    values = list(data_dict.values())

    plt.figure(figsize=(10, 6))
    plt.barh(authors, values, color='steelblue')
    plt.title(title)
    plt.xlabel(ylabel)
    plt.tight_layout()
    plt.savefig(f"reports/charts/{filename}")
    plt.close()

# Create charts
save_bar_chart({a: d["commits"] for a, d in contrib_stats.items()}, "Commits per Author", "commits_per_author.png", "Commits")
save_bar_chart({a: d["lines_added"] for a, d in contrib_stats.items()}, "Lines Added per Author", "lines_added_per_author.png", "Lines Added")
save_bar_chart({a: d["lines_deleted"] for a, d in contrib_stats.items()}, "Lines Deleted per Author", "lines_deleted_per_author.png", "Lines Deleted")

print("✅ Contribution reports generated in /reports/")
