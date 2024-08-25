import customtkinter as ctk
import downloader as yt
import threading
import os 

# tommorow add a few more things to video details
# change padding on the items in frame 2
# and get progress bar working 

main_window: ctk.CTk = ctk.CTk()
frame_width = 400
rstate: ctk.IntVar = ctk.IntVar(value=1) #this is the value for choosing either mp4 or mp3

vidNameString: ctk.StringVar = ctk.StringVar(value="")
viewcountString: ctk.StringVar = ctk.StringVar(value="")

# defining all our functions up here because python compiler is goofy
def search_for_video():
    inputLink: str = vidLinkTextbox.get('0.0', 'end')
    inputLink.replace(" ", "")
    if inputLink.__contains__("list"):
        obj = yt.get_yt_playlist(inputLink)
        vidNameLbl.configure(text=obj.title)
        vidViewcountLbl.configure(text=str(obj.views))
        mediaTypeLbl.configure(text="This is a playlist.")
    else:
        obj = yt.get_yt_video(inputLink)
        vidNameLbl.configure(text=obj.title)
        vidViewcountLbl.configure(text=str(obj.views))
        mediaTypeLbl.configure(text="This is a video.")
    return

def download_vid():
    downloadVideoButton.configure(state=ctk.DISABLED)
    search_for_video()
    inputLink: str = vidLinkTextbox.get('0.0', 'end')
    inputLink.replace(" ", "")

    filepath: str = fileLocTextbox.get('0.0', 'end')
    filepath = filepath.strip()

    if inputLink.__contains__("list"):
        if rstate.get() == 1:
            yt.download_playlist_video(link=inputLink, 
                                       outputPath=filepath, 
                                       progressCallback=update_progressbar,
                                       completeCallback=on_video_downloaded
                                       )
        elif rstate.get() == 2:
            yt.download_playlist_audio(link=inputLink, 
                                       outputPath=filepath, 
                                       progressCallback=update_progressbar,
                                       completeCallback=on_video_downloaded
                                       )
    else:
        if rstate.get() == 1:
            yt.download_video(link=inputLink, 
                              outputPath=filepath, 
                              progressCallback=update_progressbar,
                              completeCallback=on_video_downloaded
                              )
        elif rstate.get() == 2:
            yt.download_audio(link=inputLink, 
                              outputPath=filepath, 
                              progressCallback=update_progressbar,
                              completeCallback=on_video_downloaded
                              )
    return
    

def update_progressbar(chunk, filehandle, bytesRemaining):
    print("pg fsize: " + str(yt.get_filesize()))
    progressPercent = ((yt.get_filesize()-bytesRemaining)/yt.get_filesize())
    videoDownloadProgressBar.set(progressPercent)

def on_video_downloaded(stream, filepath):
    downloadVideoButton.configure(state=ctk.NORMAL)

def print_rstate():
    print(rstate.get())

# setting up THREADS
# downloadThread = threading.Thread(target=download_vid)
# searchThread = threading.Thread(target=search_for_video)

def on_search_button_pressed():
    searchThread = threading.Thread(target=search_for_video)
    searchThread.start()

def on_download_button_pressed():
    downloadThread = threading.Thread(target=download_vid)
    downloadThread.start()

#initial setup for main_window
main_window.title("Youtube Video Downloader V2")
main_window.geometry("400x500")

# searching for video/playlist
frame1: ctk.CTkFrame = ctk.CTkFrame(master=main_window, width=frame_width)
frame1.pack(padx=5, pady=5)

vidLinkLbl: ctk.CTkLabel = ctk.CTkLabel(master=frame1,
                                        text="Video/Playlist Link: "
                                        )
vidLinkLbl.grid(row=0, column=0, padx=10, pady=10)

vidLinkTextbox: ctk.CTkTextbox = ctk.CTkTextbox(master=frame1, 
                                                height = 30
                                                )
vidLinkTextbox.grid(row=0, column=1, padx=10, pady=10)

searchVidLinkButton: ctk.CTkButton = ctk.CTkButton(master=frame1, 
                                                   text="Search!", 
                                                   command=on_search_button_pressed
                                                   )
searchVidLinkButton.grid(row=1, columnspan=2, padx=10, pady=10)

# details about the video are stored in this frame
frame2: ctk.CTkFrame = ctk.CTkFrame(master=main_window, width=frame_width)
frame2.pack(padx=5, pady=5)

frame2_1: ctk.CTkFrame = ctk.CTkFrame(master=frame2, height=40)
frame2_1.grid(row=2, padx=5, pady=5)

titleVidDetailsLbl: ctk.CTkLabel = ctk.CTkLabel(master=frame2, text="--Video Details--")
titleVidDetailsLbl.grid(row=0, columnspan=2, padx=10, pady=5)

mediaTypeLbl: ctk.CTkLabel = ctk.CTkLabel(master=frame2, text="")
mediaTypeLbl.grid(row=1, columnspan=2, padx=5, pady=2)

vidNameTitleLbl: ctk.CTkLabel = ctk.CTkLabel(master=frame2_1,
                                        text="Title: "
                                        )
vidNameTitleLbl.grid(row=1, column=0, padx=5, pady=2)

vidViewcountTitleLbl: ctk.CTkLabel = ctk.CTkLabel(master=frame2_1,
                                        text="Viewcount: ")
vidViewcountTitleLbl.grid(row=2, column=0, padx=5, pady=2)

vidNameLbl: ctk.CTkLabel = ctk.CTkLabel(master=frame2_1,
                                        text=""
                                        )
vidNameLbl.grid(row=1, column=1, padx=10, pady=2)

vidViewcountLbl: ctk.CTkLabel = ctk.CTkLabel(master=frame2_1,
                                             text=""
                                             )
vidViewcountLbl.grid(row=2, column=1, padx=10, pady=2)

# file do bi do bi doo, where are you (set download location)
frame3: ctk.CTkFrame = ctk.CTkFrame(master=main_window, width=frame_width)
frame3.pack(padx=5, pady=5)

saveAsLbl: ctk.CTkLabel = ctk.CTkLabel(master=frame3,
                                       text="Download file as a... :"
                                       )
saveAsLbl.grid(row=0, column=0, padx=10, pady=10)

saveAsVideoRadBut: ctk.CTkRadioButton = ctk.CTkRadioButton(master=frame3,
                                                           text="Video (mp4)",
                                                           value=1,
                                                           variable=rstate,
                                                           command=print_rstate
                                                           )
saveAsVideoRadBut.grid(row=0, column=1, padx=10, pady=10)
saveAsAudioRadBut: ctk.CTkRadioButton = ctk.CTkRadioButton(master=frame3,
                                                           text="Audio (mp3)",
                                                           value=2,
                                                           variable=rstate,
                                                           command=print_rstate
                                                           )
saveAsAudioRadBut.grid(row=0, column=2, padx=10, pady=10)

setFileLocLbl: ctk.CTkLabel = ctk.CTkLabel(master=frame3,
                                           text="Save to: "
                                           )
setFileLocLbl.grid(row=1, padx=10, pady=10)

fileLocTextbox: ctk.CTkTextbox = ctk.CTkTextbox(master=frame3, 
                                                height = 30
                                                )
fileLocTextbox.grid(row=1, column=1, padx=10, pady=10, columnspan=2)

# frame that contains stuff related to downloading
frame4: ctk.CTkFrame = ctk.CTkFrame(master=main_window, width=frame_width)
frame4.pack(padx=5, pady=5)

videoDownloadProgressBar: ctk.CTkProgressBar = ctk.CTkProgressBar(master=frame4)
videoDownloadProgressBar.set(0.0)
videoDownloadProgressBar.grid(row=0, padx=10, pady=10)

downloadVideoButton: ctk.CTkButton = ctk.CTkButton(master=frame4,
                                                   text="Download!",
                                                   command=on_download_button_pressed
                                                   )
downloadVideoButton.grid(row=1, padx=10, pady=10)

main_window.mainloop()



