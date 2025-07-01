import requests
import json
import re
import urllib.parse

# TODO: optimise this -- a bit slow at the moment (~150 tracks takes about a minute)
def get_youtube_url(track):
    query = f"{track['artist']} {track['title']}"
    search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(query)}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch search results.")
        return None

    # Extract ytInitialData from response text
    match = re.search(r"var ytInitialData = ({.*?});</script>", response.text, re.DOTALL)
    if not match:
        print("Could not find ytInitialData in page.")
        return None

    data = json.loads(match.group(1))

    try:
        contents = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]\
                    ["sectionListRenderer"]["contents"]

        for section in contents:
            items = section.get("itemSectionRenderer", {}).get("contents", [])
            for item in items:
                video = item.get("videoRenderer")
                if video:
                    video_id = video.get("videoId")
                    return f"https://www.youtube.com/watch?v={video_id}"
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        return None

    return None
