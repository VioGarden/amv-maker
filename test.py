# # from pytube import YouTube
# # from moviepy.editor import *

# # # replace the YouTube video URL below with the one you want to download
# # yt = YouTube("https://www.youtube.com/shorts/mOK02KbjFMM")
# # stream = yt.streams.filter(only_audio=True).first()
# # stream.download(output_path='.')

# # mp3_file = AudioFileClip(stream.default_filename)
# # mp3_file.write_audiofile(f"boku_no_sensou.mp3")
# # mp3_file.close()

from moviepy.editor import *
from conf import RUN_DIR, ABS_PATH, BASE_DIR
import os


audio_clip_path = os.path.join(BASE_DIR, "boku_no_sensou.mp3")

audio_clip = AudioFileClip(audio_clip_path)

x = [((1532, 1604), 206.665, 1), ((1637, 1709), 200.502, 22), ((1149, 1221), 170.798, 157), ((1894, 1966), 143.623, 263)]

video_list = [("attack_on_titan.mp4", 5, 25), ("bleach.mp4", 10, 20)]

video_clips = []
for video_file, start_time, end_time in video_list:
    source_path = os.path.join(RUN_DIR, 'run1', video_file)
    video = VideoFileClip(source_path).subclip(start_time, end_time)
    video_clips.append(video)

final_clip = concatenate_videoclips(video_clips)
print(final_clip.fps)
audio_clip = audio_clip.set_fps(final_clip.fps)
print("------")
print(audio_clip.fps)

final_clip = final_clip.set_audio(audio_clip)

# final_clip.preview()

from moviepy.editor import *


final_clip.write_videofile("final_video.mp4", codec='libx264', audio_codec='aac', audio=True)




#------------------------------------------------------------#
# from conf import RUN_DIR, BASE_DIR
# import os
# # from bifrost import dcp
# import cv2
# from moviepy.editor import *
# from collections import defaultdict


# folder_to_run = os.path.join(RUN_DIR, 'run1')
# files = [f for f in os.listdir(folder_to_run)]

# all_the_frames_PER_SECOND = []
# for test_video in files:
#     source_path = os.path.join(RUN_DIR, 'run1', test_video)

#     cap = cv2.VideoCapture(source_path)
#     total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
#     cap.release()
#     # clip = VideoFileClip(source_path)
#     # total_frames = int(clip.duration * clip.fps)
#     print(total_frames)
#     all_the_frames_PER_SECOND.append(total_frames)

# def create_every_dictionary(total_pixel_change_arr, window):
#     dictionary_to_iterate_over = defaultdict(float)
#     for k in range(window, len(total_pixel_change_arr)):
#         start_index = k - window
#         current_average = sum(total_pixel_change_arr[start_index:k])
#         dictionary_to_iterate_over[(start_index, k)] = round(current_average, 3)
#     return dictionary_to_iterate_over

# def final_filter_dictionary(dictionary_yay, barriers, desired_options):
#     dictionary_ordered = sorted(dictionary_yay.items(), key=lambda x: x[1], reverse=True)
#     final = []
#     iteration_count = 0
#     for key, value in dictionary_ordered:
#         # if value < 100: #
#         #     break #
#         iteration_count += 1
#         left, right = key[0], key[1]
#         interfere = False
#         for pair in final:
#             pair_left, pair_right = pair[0][0], pair[0][1]
#             if pair_left <= left <= pair_right or pair_left <= right <= pair_right: 
#                 interfere = True
#                 break
#         if not interfere:
#             for blockage in barriers:
#                 if left <= blockage <= right:
#                     interfere = True
#                     break
#         if interfere: continue
#         final.append((key, value, iteration_count))
#         if len(final) > desired_options:
#             return final
#     return final


# video_list = [] # video stuff

# start_index = 0

# for i in range(len(files)):

#     end_index = start_index + all_the_frames_PER_SECOND[i]

#     # if i == 0:
#     #     finalfinal = [((1330, 1410), 498885981.947, 33), ((29, 109), 8262072.695, 2008)]
#     # else:
#     #     finalfinal = [((1196, 1276), 606281052.812, 255), ((1994, 2074), 586588488.125, 277), ((630, 710), 266210285.312, 861), ((374, 454), 264958271.375, 870)]

#     start_index += all_the_frames_PER_SECOND[i]

#     print(finalfinal)

#     source_path = os.path.join(RUN_DIR, 'run1', files[i])

#     clip = VideoFileClip(source_path)
#     fps = clip.reader.fps

#     found = False
#     if finalfinal:
#         clippyclippy = finalfinal[0]
#         if clippyclippy[1] < 300000000:
#             pass
#         else:
#             found = True
#             filefilefile = files[i]
#             startstartstart = round(finalfinal[0][0][0]/fps, 3)
#             endendend = round(finalfinal[0][0][1]/fps, 3)
#             tupletupletuple = (filefilefile, startstartstart, endendend)
#             video_list.append(tupletupletuple)
    
#     if found: 
#         print(video_list)
#         found = False
#         continue
#     else:
#         temp_bar_bar = []
#         temp_dictdict = create_every_dictionary(curr_tadc, 80)
#         temp_finalfinal = final_filter_dictionary(temp_dictdict, temp_bar_bar, 3)
#         if not temp_finalfinal:
#             print("oh no!!!!!!")
#             pass
#         temp_filefilefile = files[i]
#         temp_startstartstart = round(temp_finalfinal[0][0][0]/fps, 3)
#         temp_endendend = round(temp_finalfinal[0][0][1]/fps, 3)
#         temp_tupletupletuple = (temp_filefilefile, temp_startstartstart, temp_endendend)
#         video_list.append(temp_tupletupletuple)


# video_clips = []


# audio_clip_path = os.path.join(BASE_DIR, "boku_no_sensou.mp3")

# audio_clip = AudioFileClip(audio_clip_path)

# for video_file, start_time, end_time in video_list:
#     source_path = os.path.join(RUN_DIR, 'run1', video_file)
#     video = VideoFileClip(source_path).subclip(start_time, end_time)
#     video_clips.append(video)

# final_clip = concatenate_videoclips(video_clips)
# print(final_clip.fps)
# audio_clip = audio_clip.set_fps(final_clip.fps)
# print("------")
# print(audio_clip.fps)

# final_clip = final_clip.set_audio(audio_clip)

# final_clip.preview()






    
result_set = [[[3,5,2], [2,5,2], [7,3,6], [8,3,6]], [[2,6,2], [78,74,3], [1,3,4], [7,4,6]], [[2,4,2], [4,2,45], [3,4,5], [8,4,4]]]

a = [3,5,2,2,6,2,2,4,2]
b = [2,5,2,78,74,3,4,2,45]
c = [7,3,6,1,3,4,3,4,5]
d = [8,3,6,7,4,6,8,4,4]


a, b, c, d = [[elem for sub_list in result_set for elem in sub_list] for _ in range(4)]

print(a)
print(b)
print(c)
print(d)