from pytubefix import *
import pytubefix.request
import os

pytubefix.request.default_range_size = 50000 # smaller chunk = more progress updates

fileSize = 0.0

videosToBeDownloaded = 0
videosThatHaveBeenDownloaded = 0

# contradiction: you did something
def doNothing():
    pass

def get_filesize():
    return fileSize

def get_vidsToBeDownloaded():
    return videosToBeDownloaded

def set_vidsToBeDownloaded(val):
    global videosToBeDownloaded
    videosToBeDownloaded = val

def get_vidsThatHaveBeenDownloaded():
    return videosThatHaveBeenDownloaded

def set_vidsThatHaveBeenDownloaded(val):
    global videosThatHaveBeenDownloaded
    videosThatHaveBeenDownloaded = val

# getting basic information and other shenannigans go here

def get_yt_video(link, progressCallback=doNothing, completeCallback=doNothing) -> YouTube:
    """Get a yotob video object to use"""
    video = YouTube(link, on_progress_callback=progressCallback, on_complete_callback=completeCallback)
    return video

# downloading the video, two functions for either using a youtueb obj or vid link

def download_video(link: str, outputPath, progressCallback=doNothing, completeCallback=doNothing, resolution='360p'):
    """Download a video using a link"""
    global fileSize
    global videosThatHaveBeenDownloaded
    fileSize = get_yt_video(link).streams.filter(resolution=resolution).first().filesize
    print(fileSize)
    print(get_yt_video(link).title)
    get_yt_video(link, progressCallback=progressCallback, completeCallback=completeCallback).streams.filter(resolution=resolution).first().download(output_path=outputPath)
    videosThatHaveBeenDownloaded += 1



def download_video_ytobj(ytObj: YouTube, outputPath, progressCallback=doNothing, completeCallback=doNothing, resolution='360p'):
    """Download a video using a Youtube object"""
    global fileSize
    global videosThatHaveBeenDownloaded
    fileSize = ytObj.streams.filter(resolution=resolution).first().filesize
    print(ytObj.title)
    print(fileSize)
    ytObj.register_on_progress_callback(progressCallback)
    ytObj.register_on_complete_callback(completeCallback)
    ytObj.streams.filter(resolution=resolution).first().download(output_path=outputPath)
    videosThatHaveBeenDownloaded += 1

# downloading audio, two functionz for either using youbtbe obj or video link

def download_audio(link: str, outputPath, progressCallback=doNothing, completeCallback=doNothing):
    """Downaloadio audio using a link"""
    global fileSize
    global videosThatHaveBeenDownloaded
    fileSize = get_yt_video(link).streams.filter(only_audio=True).first().filesize
    print(fileSize)
    print(get_yt_video(link).title)
    get_yt_video(link, progressCallback=progressCallback, completeCallback=completeCallback).streams.filter(only_audio=True).first().download(output_path=outputPath, mp3=True)
    videosThatHaveBeenDownloaded += 1

def download_audio_ytobj(ytObj: YouTube, outputPath, progressCallback=doNothing, completeCallback=doNothing):
    """Download audio using a yotuooobe link"""
    global fileSize
    global videosThatHaveBeenDownloaded
    fileSize = ytObj.streams.filter(only_audio=True).first().filesize
    print(fileSize)
    print(ytObj.title)
    ytObj.register_on_progress_callback(progressCallback)
    ytObj.register_on_complete_callback(completeCallback)
    ytObj.streams.filter(only_audio=True).first().download(output_path=outputPath, mp3=True)
    videosThatHaveBeenDownloaded += 1

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

def download_playlist_video(link, outputPath, progressCallback=doNothing, completeCallback=doNothing, resolution='360p'):
    """Download an entire playlist of videos"""
    set_vidsToBeDownloaded(get_yt_playlist(link).length)
    filepath =  make_dir_for_playlist(link, outputPath)
    for video in get_yt_playlist(link).videos:
        download_video_ytobj(ytObj=video, outputPath=filepath, progressCallback=progressCallback, completeCallback=completeCallback, resolution=resolution)


def download_playlist_audio(link, outputPath, progressCallback=doNothing, completeCallback=doNothing):
    """Download an enitre playlist of audio"""
    set_vidsToBeDownloaded(get_yt_playlist(link).length)
    filepath =  make_dir_for_playlist(link, outputPath)
    for video in get_yt_playlist(link).videos:
        download_audio_ytobj(ytObj=video, outputPath=filepath, progressCallback=progressCallback, completeCallback=completeCallback)

