import os
import requests
import matplotlib.pyplot as plt

# GitHub API endpoint
API_URL = "https://api.github.com/repos/ryo-ngked/data-science-training-2025/contents/"

# Get the GitHub token from an environment variable for security
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError(
        "GITHUB_TOKEN environment variable not set. Please set it securely."
    )

REPO_OWNER = "ryo-ngked"
REPO_NAME = "data-science-training-2025"

# Request headers
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}


def count_ipynb_files(path):
    """
    Recursively count ipynb files in the specified path
    """
    url = API_URL.format(owner=REPO_OWNER, repo=REPO_NAME) + path
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    contents = response.json()

    count = 0
    for item in contents:
        if item["type"] == "dir":
            # If it's a folder, count recursively
            count += count_ipynb_files(item["path"])
        elif item["type"] == "file" and item["name"].endswith(".ipynb"):
            # Count if it's an .ipynb file
            count += 1
    return count


def get_member_progress():
    """
    Get the number of ipynb files (learning records) for each member
    """
    print("Counting progress for each member...")

    url = API_URL.format(owner=REPO_OWNER, repo=REPO_NAME)
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # Get the contents of the repository root directory
    contents = response.json()

    progress = {}
    for item in contents:
        if item["type"] == "dir":
            member_name = item["name"]
            # Count ipynb files in the member's folder
            file_count = count_ipynb_files(member_name)
            progress[member_name] = file_count

    return progress


if __name__ == "__main__":
    try:
        progress_data = get_member_progress()
        print("\n--- Learning Records by Member ---")
        for member, count in progress_data.items():
            print(f"{member}: {count} ipynb files")

        # Sort members by file count in descending order
        sorted_progress = sorted(
            progress_data.items(), key=lambda x: x[1], reverse=True
        )
        members = [x[0] for x in sorted_progress]
        counts = [x[1] for x in sorted_progress]
        plt.figure(figsize=(10, 6))
        plt.bar(members, counts, color="skyblue")
        plt.xlabel("Member")
        plt.ylabel("Number of ipynb files")
        plt.title("Number of ipynb files by Member")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("progress_chart.png")
        print("\nBar graph saved as 'progress_chrt.png'.")
    except requests.exceptions.HTTPError as e:
        print(f"An error occurred: {e}")
        print("Please check if the token, repository name, and owner name are correct.")
