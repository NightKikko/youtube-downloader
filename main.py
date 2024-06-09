import os
from pytube import YouTube
from youtubesearchpython import VideosSearch
from art import text2art

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def search_youtube(query):
    try:
        videos_search = VideosSearch(query, limit=5)
        results = videos_search.result()['result']
        
        if not results:
            raise Exception("No search results found")
        
        print("\nSearch results")
        for idx, video in enumerate(results):
            print(f"   \033[94m{idx + 1}. {video['title']} ({video['duration']})\033[0m")
            print(f"   \033[96mhttps://www.youtube.com/watch?v={video['id']}\033[0m\n")
        
        choice = int(input("Enter the number of the video you want to download: ")) - 1
        return f"https://www.youtube.com/watch?v={results[choice]['id']}"
    except Exception as e:
        print(f"An error occurred during search: {e}\n")
        return None

def download_youtube_audio(url, download_path):
    try:
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        
        if not audio_stream:
            raise Exception("No audio stream available")

        audio_file_path = audio_stream.download(output_path=download_path)
        base, ext = os.path.splitext(audio_file_path)
        mp3_file_path = base + '.mp3'
        os.rename(audio_file_path, mp3_file_path)
        print(f"   Download complete!\n   Audio saved as: \033[92m{mp3_file_path}\033[0m\n")
        return mp3_file_path
    except Exception as e:
        print(f"An error occurred: {e}\n")
        return None

def main_menu():
    clear_screen()
    options = ["Search for a song", "Download by URL", "Exit"]
    selected_option = 0

    def print_menu(selected):
        clear_screen()
        print(text2art("YouTube Downloader"))
        print("\n    \033[93m[?]\033[0m What do you want to do?\n")
        for i, option in enumerate(options):
            if i == selected:
                print(f"      \033[91m{i+1}.   {option}\033[0m\n")
            else:
                print(f"      \033[91m{i+1}.   {option}\033[0m\n")

    print_menu(selected_option)
    
    while True:
        try:
            choice = int(input("\n    \033[95m[$]\033[0m Enter your choice: "))
            if 1 <= choice <= len(options):
                selected_option = choice - 1
                if choice == 1:
                    query = input("   Enter the song title to search: ")
                    url = search_youtube(query)
                    if not url:
                        print("Failed to get the URL from search results\n")
                        return
                elif choice == 2:
                    url = input("   Enter the YouTube URL: ")
                elif choice == 3:
                    print("   Exiting...")
                    break
                download_path = input("   Enter the download path (or leave empty for current directory): ")
                if not download_path:
                    download_path = os.getcwd()
                audio_file_path = download_youtube_audio(url, download_path)
                if audio_file_path:
                    print(f"   Downloaded and saved as MP3: \033[92m{audio_file_path}\033[0m\n")
                else:
                    print("   Failed to download the audio\n")
            else:
                print("   Invalid choice. Please enter a number between 1 and 3.\n")
        except ValueError:
            print(f"   Invalid choice. Please enter a number.\n")
        input("   \033[95m[$] Press enter to continue\033[0m\n")
        print_menu(selected_option)

if __name__ == "__main__":
    main_menu()
