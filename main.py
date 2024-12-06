import os, spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

def search_spotify_album(query):
    results = sp.search(q=query, type="album", limit=5)
    if results["albums"]["items"]:
        return results["albums"]["items"]
    else:
        return None

def get_album_details(album_id):
    album = sp.album(album_id)
    tracklist = [track["name"] for track in album["tracks"]["items"]]
    runtime_ms = sum(track["duration_ms"] for track in album["tracks"]["items"])
    runtime_minutes = runtime_ms // 60000
    runtime_hours = runtime_minutes // 60
    runtime_remaining_minutes = runtime_minutes % 60
    if runtime_hours > 0:
        runtime = f"{runtime_hours} hour{'s' if runtime_hours > 1 else ''} & {runtime_remaining_minutes} minute{'s' if runtime_remaining_minutes > 1 else ''}"
    else:
        runtime = f"{runtime_minutes} minute{'s' if runtime_minutes > 1 else ''}"
    album_cover_link = album["images"][0]["url"] if album["images"] else "No image available"
    return {
        "album_name": album["name"],
        "tracklist": tracklist,
        "runtime": runtime,
        "album_cover_link": album_cover_link,
    }

def format_album_details(album_name, tracklist, runtime, album_cover_link):
    output = f"**{album_name}**\n\n"
    output += "**Tracklist**\n"
    for idx, track in enumerate(tracklist, 1):
        output += f"{idx}. {track}\n"
    output += f"\n**Overall Runtime: {runtime}**\n\n"
    output += "**Download:**\n\n\n"
    output += f"{album_cover_link}\n"
    return output

query = input("Enter the album you want to search for: ")
results = search_spotify_album(query)

if results:
    print("Select an album from the results below:")
    for idx, album in enumerate(results, 1):
        print(f"{idx}. {album['name']} by {album['artists'][0]['name']}")

    choice = int(input("Enter the number of the album you want to select: ")) - 1

    if 0 <= choice < len(results):
        selected_album = results[choice]
        album_details = get_album_details(selected_album["id"])

        formatted_details = format_album_details(
            album_details["album_name"],
            album_details["tracklist"],
            album_details["runtime"],
            album_details["album_cover_link"]
        )

        file_name = "album_details.txt"
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(formatted_details)
        print(f"Album details saved to {file_name}")
else:
    print("No results found.")
