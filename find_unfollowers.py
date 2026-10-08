import json
from pathlib import Path
import sys


def extract_usernames(data, filename):
    if isinstance(data, list):
        values = [
            item.get("value")
            for entry in data
            if isinstance(entry, dict)
            for item in entry.get("string_list_data", [])
            if isinstance(item, dict)
        ]
    elif isinstance(data, dict) and isinstance(data.get("relationships_following"), list):
        values = [
            entry.get("title")
            for entry in data["relationships_following"]
            if isinstance(entry, dict)
        ]
    else:
        raise ValueError(f"Unrecognized Instagram export format in {filename}")

    return [value for value in values if isinstance(value, str) and value]


def load_json(path):
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def main():
    folder = Path(__file__).resolve().parent
    followers_path = Path(sys.argv[1]) if len(sys.argv) > 1 else folder / "followers.json"
    following_path = Path(sys.argv[2]) if len(sys.argv) > 2 else folder / "following.json"

    followers = extract_usernames(load_json(followers_path), followers_path.name)
    following = extract_usernames(load_json(following_path), following_path.name)

    follower_names = {username.casefold() for username in followers}
    not_following_back = [
        username
        for username in following
        if username.casefold() not in follower_names
    ]

    output_path = folder / "unfollowers.txt"
    output_path.write_text("\n".join(not_following_back) + "\n", encoding="utf-8")
    print(f"Wrote {len(not_following_back)} usernames to {output_path.name}")


if __name__ == "__main__":
    main()