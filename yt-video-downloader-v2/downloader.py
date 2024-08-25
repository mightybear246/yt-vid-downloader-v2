from pytubefix import *
import pytubefix.request
import os

pytubefix.request.default_range_size = 50000 # smaller chunk = more progress updates

fileSize = 0.0

# contradiction: you did something
def doNothing():
    pass

def get_filesize():
    return fileSize

# getting basic information and other shenannigans go here

def get_yt_video(link, progressCallback=doNothing, completeCallback=doNothing) -> YouTube:
    """Get a yotob video object to use"""
    video = YouTube(link, on_progress_callback=progressCallback, on_complete_callback=completeCallback)
    return video

# downloading the video, two functions for either using a youtueb obj or vid link

def download_video(link: str, outputPath, progressCallback=doNothing, completeCallback=doNothing):
    """Download a video using a link"""
    global fileSize
    fileSize = get_yt_video(link).streams.first().filesize
    print(fileSize)
    print(get_yt_video(link).title)
    get_yt_video(link, progressCallback=progressCallback, completeCallback=completeCallback).streams.first().download(output_path=outputPath)


def download_video_ytobj(ytObj: YouTube, outputPath, progressCallback=doNothing, completeCallback=doNothing):
    """Download a video using a Youtube object"""
    global fileSize
    fileSize = ytObj.streams.first().filesize
    print(ytObj.title)
    print(fileSize)
    ytObj.register_on_progress_callback(progressCallback)
    ytObj.register_on_complete_callback(completeCallback)
    ytObj.streams.first().download(output_path=outputPath)

# downloading audio, two functionz for either using youbtbe obj or video link

def download_audio(link: str, outputPath, progressCallback=doNothing, completeCallback=doNothing):
    """Downaloadio audio using a link"""
    global fileSize
    fileSize = get_yt_video(link).streams.filter(only_audio=True).first().filesize
    print(fileSize)
    print(get_yt_video(link).title)
    get_yt_video(link, progressCallback=progressCallback, completeCallback=completeCallback).streams.filter(only_audio=True).first().download(output_path=outputPath, mp3=True)


def download_audio_ytobj(ytObj: YouTube, outputPath, progressCallback=doNothing, completeCallback=doNothing):
    """Download audio using a yotuooobe link"""
    global fileSize
    fileSize = ytObj.streams.filter(only_audio=True).first().filesize
    print(fileSize)
    print(ytObj.title)
    ytObj.register_on_progress_callback(progressCallback)
    ytObj.register_on_complete_callback(completeCallback)
    ytObj.streams.filter(only_audio=True).first().download(output_path=outputPath, mp3=True)

# downloading playlists

def get_yt_playlist(link) -> Playlist:
    """Get a playlist"""
    playlist = Playlist(link)
    return playlist

def make_dir_for_playlist(link, outputPath):
    playlist: Playlist = get_yt_playlist(link)
    folderName = playlist.title
    newPath = os.path.join(outputPath, folderName)
    try:
        os.mkdir(path=newPath)
    except FileExistsError as e:
        print("Directory exists :3")
    return newPath
# please finish this tommorow

def download_playlist_video(link, outputPath, progressCallback=doNothing, completeCallback=doNothing):
    """Download an entire playlist of videos"""
    filepath =  make_dir_for_playlist(link, outputPath)
    for video in get_yt_playlist(link).videos:
        download_video_ytobj(ytObj=video, outputPath=filepath, progressCallback=progressCallback, completeCallback=completeCallback)


def download_playlist_audio(link, outputPath, progressCallback=doNothing, completeCallback=doNothing):
    """Download an enitre playlist of audio"""
    filepath =  make_dir_for_playlist(link, outputPath)
    for video in get_yt_playlist(link).videos:
        download_audio_ytobj(ytObj=video, outputPath=filepath, progressCallback=progressCallback, completeCallback=completeCallback)

