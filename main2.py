from conf import RUN_DIR, BASE_DIR
import os
from bifrost import dcp
import cv2
import random
import time

time_start = time.time()

demo = {"version":3,"id":"db4a4c82-12d9-470a-8f26-0af87d45f11a","address":"2ae0d4fe077747e82016bc108d0b87bca5c4651c","crypto":{"ciphertext":"b3009d3df844babbea903a9b0c2dae38dc81bac33e8d47e7de2bd07ded14fb5f","cipherparams":{"iv":"3622393fbb83a76126d5fa1f671c223d"},"cipher":"aes-128-ctr","kdf":"scrypt","kdfparams":{"dklen":32,"salt":"58c8247f9aa63ae8204e8e470254a6d3b3027603db9e2cead8af270c94e23c8d","n":1024,"r":8,"p":1},"mac":"2c4a44c346289c96077706cfba47703a29ebb3816087af20d8c8f0fbc3fb7ad2"},"label":"Queens"}

folder_to_run = os.path.join(RUN_DIR, 'run1')
all_files = [f for f in os.listdir(folder_to_run)]

files = random.sample(all_files, 4) # selects 4 random mp4 files

input_set = []  # list to put in work function
input_set_len_per_mp4 = []  # each elements are chunks of 31 frames

def process_video(vid, folder):
    source_path = os.path.join(folder, vid) # get source path to video
    video = cv2.VideoCapture(source_path)
    frame_is_present, prev = video.read() # get frame
    input_set_function = [] # chuck of frames per mp4
    input_set_elements = [] # chuck of frames per 31 iterations
    encoding_parameter = [int(cv2.IMWRITE_JPEG_QUALITY), 15] # lower the total size of payload by lowering quality

    while frame_is_present:
        is_prev_good, prev_buffer = cv2.imencode('.jpg', prev, encoding_parameter) # lower the total size of payload by encoding
        if not prev_buffer.any():
            raise ValueError("ahahahahahahahahaTThelp")
        if len(input_set_elements) < 30:
            input_set_elements.append(prev_buffer) # add to chunck
        else:
            input_set_elements.append(prev_buffer) # if chunk level is reached, append and reset
            input_set_function.append(input_set_elements)
            input_set_elements = []
            input_set_elements.append(prev_buffer)
        frame_is_present, prev = video.read()
    if input_set_elements:
        input_set_function.append(input_set_elements)
    return input_set_function, len(input_set_function)

for fifi in files:
    print(fifi)
    thirty, lenlen = process_video(fifi, folder_to_run)
    input_set.extend(thirty) # create input set
    input_set_len_per_mp4.append(lenlen) # range of each mp4 video

print(len(input_set))
print(input_set_len_per_mp4)


print("created input set", time.time() - time_start)

def work_function(small_frame):
    import numpy as np
    import cv2

    total_flow_change_list, total_histo_change_RGB_list, total_abs_diff_change_list, total_gray_mse_list = [], [], [], [] # initialize list to insert results

    for elele in range(1, len(small_frame)):

        prev = small_frame[elele - 1] # previous frame
        curr = small_frame[elele] # current frame      
        prev_frame = cv2.imdecode(np.frombuffer(prev, np.uint8), cv2.IMREAD_COLOR) # decode prev frame
        curr_frame = cv2.imdecode(np.frombuffer(curr, np.uint8), cv2.IMREAD_COLOR) # decode curr frame

        #1 ************ optical flow ****************
        prev_ready = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY) # converts frames to grayscale
        curr_ready = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY) # optical flow works well in gray
        optical_flow = cv2.calcOpticalFlowFarneback(prev_ready, curr_ready, None, 0.5, 3, 5, 3, 5, 15.5, 0) # height x width x 2
        magnitude, _angle = cv2.cartToPolar(optical_flow[..., 0], optical_flow[..., 1]) # x: [..., 0], y: [...,1]
        total_flow_change = np.sum(magnitude)

        #2 ************* histogram RGB **************
        bins = 64
        prev_hist_frame_RGB = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2RGB) # convert frames to RGB
        prev_hist_RGB = cv2.calcHist([prev_hist_frame_RGB], [0, 1, 2], None, [bins, bins, bins], [0, 256, 0, 256, 0, 256]) # create prev histo
        curr_hist_frame_RGB = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2RGB) # convert frames to RGB
        curr_hist_RGB = cv2.calcHist([curr_hist_frame_RGB], [0, 1, 2], None, [bins, bins, bins], [0, 256, 0, 256, 0, 256]) # create curr histo
        comparison_RGB = cv2.compareHist(prev_hist_RGB, curr_hist_RGB, cv2.HISTCMP_CHISQR) # compare histograms
        total_histo_change_RGB = round(comparison_RGB, 10) 

        #3 ************** total pixel change ************
        total_pixel_color_change = cv2.absdiff(prev_frame, curr_frame)
        total_abs_diff_change = int(sum(cv2.sumElems(total_pixel_color_change)))

        #4 ************** MSE GRAY **************
        gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        graygray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
        total_gray_mse = np.mean((gray - graygray)**2) # difference and square

        #append results to list
        total_flow_change_list.append(total_flow_change)
        total_histo_change_RGB_list.append(total_histo_change_RGB)
        total_abs_diff_change_list.append(total_abs_diff_change)
        total_gray_mse_list.append(total_gray_mse)

    return (total_flow_change_list, total_histo_change_RGB_list, total_abs_diff_change_list, total_gray_mse_list)



job = dcp.compute_for(input_set, work_function)

job.requires('numpy')

job.requires('opencv-python')

job.compute_groups = [{'joinKey': 'demo', 'joinSecret': 'dcp'}]

job.public['name'] = 'Sasageyo'

print(job.id)

result_set = job.exec(payment_account=demo)

print(len(result_set))
print(len(result_set[0]))
print(len(result_set[0][0]))


import os
import numpy as np
import cv2
from collections import defaultdict, deque, OrderedDict
from moviepy.editor import *

tfc, thcRGB, tadc, tgmse = [], [], [], []

for row in result_set:
    for i, col in enumerate(row):
        if i == 0:
            tfc.extend(col)
        elif i == 1:
            thcRGB.extend(col)
        elif i == 2:
            tadc.extend(col)
        elif i == 3:
            tgmse.extend(col)


# tfc, thcRGB, tadc, tgmse = [[elem for sub_list in zip(*result_set) for elem in sub_list] for _ in range(4)]
# tfc = [item for sublist in tfc for item in sublist]
# thcRGB = [item for sublist in thcRGB for item in sublist]
# tadc = [item for sublist in tadc for item in sublist]
# tgmse = [item for sublist in tgmse for item in sublist]

print("incoming lengths")
print(len(tfc))
print(len(thcRGB))
print(len(tadc))
print(len(tgmse))



tfc_avg, thcRGB_avg, tadc_avg, tgmse_avg = sum(tfc)/len(tfc), sum(thcRGB)/len(thcRGB), sum(tadc)/len(tadc), sum(tgmse)/len(tgmse)

tfc = [round(elem/tfc_avg, 5) for elem in tfc]
thcRGB = [round(elem/thcRGB_avg, 5) for elem in thcRGB]
tadc = [round(elem/tadc_avg, 5) for elem in tadc]
tgmse = [round(elem/tgmse_avg, 5) for elem in tgmse]


print("incoming lengths")
print(len(tfc))
print(len(thcRGB))
print(len(tadc))
print(len(tgmse))

# tfc = [0.06007, 0.10775, 0.14029, 0.05949, 0.00168, 0.0093, 0.00743, 0.06566, 0.0033, 0.00984, 0.00575, 0.02902, 0.0182, 0.02058, 0.0183, 0.03852, 0.01044, 0.01633, 0.01415, 0.03752, 0.00899, 0.01848, 0.01515, 0.03513, 0.01101, 0.0212, 0.01606, 0.04095, 0.01635, 0.02755, 0.01008, 0.03163, 0.01497, 0.0184, 0.01622, 0.02998, 0.01205, 0.01937, 0.01401, 0.03537, 0.01488, 0.02051, 0.02146, 0.02477, 0.01626, 0.02015, 0.0259, 0.03704, 0.01545, 0.02685, 0.0166, 0.02211, 0.01319, 0.0207, 0.01924, 0.0262, 0.01066, 0.01658, 0.01486, 0.02713, 0.0124, 0.01865, 0.0188, 0.02286, 0.01317, 0.01721, 0.01649, 0.01556, 0.00903, 0.01928, 0.01562, 0.01608, 0.61775, 0.53005, 1.69854, 0.03573, 0.1198, 0.13428, 0.09277, 0.1138, 0.08306, 0.10327, 0.09174, 0.07157, 0.08478, 0.81796, 0.78468, 0.19957, 0.53708, 2.2565, 1.03504, 1.0113, 0.83864, 0.41533, 0.36385, 0.92726, 7.64162, 4.3765, 5.20335, 0.67667, 0.20755, 0.27483, 0.15077, 0.21522, 5.06525, 6.068, 4.19272, 0.85064, 0.00691, 0.01159, 0.06957, 0.06932, 0.03435, 0.03493, 0.1235, 0.13652, 0.15376, 0.17633, 0.1837, 0.20113, 0.17734, 0.18902, 0.14062, 0.11331, 0.00513, 0.00667, 0.01041, 0.07773, 0.00203, 0.0023, 0.00321, 0.01068, 0.00708, 0.00499, 0.00635, 0.00648, 0.00509, 0.00417, 0.00607, 0.00383, 0.00337, 0.0028, 0.00452, 0.00403, 0.00449, 4.91234, 3.36986, 0.15337, 0.08541, 0.62695, 0.47767, 0.44377, 0.4277, 0.54631, 0.50839, 0.49638, 0.49059, 0.49415, 0.51604, 0.55951, 0.56323, 0.53894, 0.58016, 0.56965, 0.52429, 0.52912, 0.54069, 0.56123, 0.52395, 0.58092, 0.49162, 0.48594, 0.52738, 0.46447, 0.51275, 0.48473, 0.54769, 0.57152, 0.48632, 0.51925, 0.46722, 0.54319, 0.45645, 0.48272, 0.66405, 0.94249, 1.54642, 2.25403, 2.73883, 2.73725, 2.90207, 2.99541, 2.87717, 3.02965, 2.88467, 3.17399, 2.86924, 2.84013, 2.64572, 2.84439]
# thcRGB = [0.22581, 0.59962, 0.57911, 0.00025, 0.0, 1e-05, 2e-05, 0.00023, 0.0, 2e-05, 1e-05, 8e-05, 5e-05, 5e-05, 7e-05, 0.00017, 3e-05, 4e-05, 3e-05, 0.0002, 2e-05, 5e-05, 6e-05, 0.00011, 6e-05, 6e-05, 3e-05, 0.00018, 3e-05, 0.00011, 2e-05, 0.00012, 5e-05, 4e-05, 4e-05, 7e-05, 1e-05, 3e-05, 5e-05, 0.00019, 4e-05, 6e-05, 7e-05, 8e-05, 5e-05, 0.00011, 0.00014, 0.00016, 6e-05, 0.00011, 8e-05, 8e-05, 2e-05, 5e-05, 0.00011, 9e-05, 6e-05, 7e-05, 4e-05, 0.00012, 3e-05, 8e-05, 5e-05, 9e-05, 3e-05, 4e-05, 6e-05, 3e-05, 2e-05, 0.00011, 3e-05, 4e-05, 0.00079, 37.77967, 0.21527, 0.00448, 0.00956, 0.56392, 0.009, 0.00297, 0.0004, 0.00075, 0.00045, 0.00032, 0.00037, 1.11983, 0.83413, 0.30305, 0.02977, 0.06215, 0.00203, 0.00278, 0.00236, 0.00175, 0.00146, 0.00469, 0.04364, 1.48467, 0.08455, 0.00136, 0.00099, 0.00111, 0.00076, 0.00101, 0.37108, 1.39925, 0.41669, 0.01714, 2e-05, 0.0026, 0.00013, 0.00114, 0.00115, 0.00113, 0.00214, 0.0039, 0.00448, 0.0054, 0.00946, 0.01062, 0.00695, 0.0053, 0.00305, 0.00179, 1e-05, 2e-05, 2e-05, 0.00081, 1e-05, 1e-05, 2e-05, 7e-05, 3e-05, 2e-05, 2e-05, 2e-05, 1e-05, 1e-05, 2e-05, 3e-05, 2e-05, 1e-05, 1e-05, 2e-05, 1e-05, 0.01567, 0.45007, 2.58257, 0.57804, 0.00972, 0.001, 0.00087, 0.00084, 0.00108, 0.00083, 0.00095, 0.00096, 0.00105, 0.00086, 0.00121, 0.00095, 0.00105, 0.00139, 0.00087, 0.00111, 0.00107, 0.00105, 0.00099, 0.00123, 0.00106, 0.00104, 0.00118, 0.0009, 0.00104, 0.0011, 0.00093, 0.00073, 0.00102, 0.00065, 0.00076, 0.001, 0.00074, 0.00068, 0.00089, 0.00099, 0.00127, 0.00154, 0.00161, 0.00091, 0.00094, 0.00076, 0.0009, 0.00075, 0.00076, 0.00066, 0.00084, 0.00091, 0.00094, 0.00088, 0.0008]
# tadc = [2.20092, 2.13359, 2.2659, 0.10009, 0.00153, 0.0106, 0.00899, 0.11358, 0.00454, 0.01367, 0.0068, 0.03917, 0.02183, 0.02701, 0.02303, 0.05453, 0.01195, 0.0208, 0.01793, 0.05495, 0.01143, 0.02281, 0.01881, 0.04906, 0.01372, 0.02591, 0.02109, 0.05506, 0.01955, 0.03932, 0.0121, 0.04342, 0.01847, 0.02196, 0.02093, 0.03842, 0.01307, 0.02277, 0.01797, 0.05028, 0.01853, 0.02559, 0.02733, 0.03253, 0.0193, 0.02766, 0.03399, 0.05184, 0.01945, 0.03733, 0.02205, 0.03141, 0.01709, 0.02855, 0.027, 0.03838, 0.01594, 0.02409, 0.01934, 0.0415, 0.01823, 0.02843, 0.0278, 0.03497, 0.01797, 0.0249, 0.02223, 0.02137, 0.01182, 0.02935, 0.02048, 0.01879, 0.84136, 2.78934, 3.29968, 0.34788, 0.41034, 1.13091, 0.6565, 0.1844, 0.12935, 0.16502, 0.14512, 0.11203, 0.13115, 2.42961, 3.48015, 9.07356, 10.31752, 2.52796, 1.77848, 1.75702, 1.5317, 0.94834, 0.76821, 1.36093, 5.05438, 3.7985, 3.83567, 1.23087, 0.46295, 0.61181, 0.3199, 0.48861, 3.3003, 5.13417, 5.18233, 1.32663, 0.0074, 0.02177, 0.04664, 0.13586, 0.09348, 0.08544, 0.22504, 0.45027, 0.58357, 0.58743, 0.6059, 0.59374, 0.62488, 0.53194, 0.37476, 0.23714, 0.00562, 0.00808, 0.01125, 0.15015, 0.00219, 0.00273, 0.00381, 0.015, 0.00888, 0.00589, 0.00744, 0.00874, 0.0058, 0.00565, 0.0075, 0.00492, 0.0038, 0.00337, 0.00511, 0.00534, 0.00535, 3.0155, 5.24649, 3.34313, 2.91908, 1.94497, 1.44613, 1.45025, 1.4592, 1.46507, 1.47111, 1.46676, 1.44694, 1.48712, 1.52657, 1.52459, 1.55502, 1.56847, 1.57729, 1.59512, 1.59009, 1.59621, 1.59857, 1.62131, 1.59199, 1.61106, 1.5581, 1.51073, 1.60681, 1.57072, 1.62063, 1.60776, 1.63009, 1.66986, 1.63955, 1.65834, 1.59626, 1.65254, 1.5786, 1.54394, 1.58831, 1.63457, 1.69899, 1.77031, 1.8015, 1.80117, 1.81267, 1.85188, 1.85475, 1.88441, 1.86126, 1.91237, 1.86292, 1.86199, 1.79241, 1.87447]
# tgmse = [2.72025, 3.22793, 3.10553, 0.20333, 0.00369, 0.02299, 0.01918, 0.22489, 0.01067, 0.02855, 0.01512, 0.07866, 0.0456, 0.05739, 0.04733, 0.10626, 0.0248, 0.04089, 0.03685, 0.10847, 0.02153, 0.04736, 0.03934, 0.10016, 0.02843, 0.05629, 0.04479, 0.11282, 0.03999, 0.07623, 0.02369, 0.08968, 0.03987, 0.04655, 0.04264, 0.08051, 0.0288, 0.05066, 0.03552, 0.09563, 0.03917, 0.05329, 0.05612, 0.06897, 0.04504, 0.05901, 0.07111, 0.10416, 0.04185, 0.07256, 0.04504, 0.06464, 0.03725, 0.06225, 0.05401, 0.07902, 0.03244, 0.04886, 0.04072, 0.08426, 0.03923, 0.05777, 0.06046, 0.07371, 0.04215, 0.05161, 0.04686, 0.04559, 0.02382, 0.05754, 0.04783, 0.04089, 1.64897, 3.08219, 2.50544, 0.88705, 0.95481, 2.78899, 2.18496, 0.42248, 0.30986, 0.38706, 0.35364, 0.26463, 0.31392, 2.87658, 2.73847, 2.81739, 2.74856, 2.69446, 1.87982, 1.86753, 1.76512, 1.45669, 1.36791, 1.80666, 2.72907, 2.57922, 2.49996, 1.57032, 0.96688, 1.13338, 0.76407, 0.99371, 2.45268, 2.75882, 2.76921, 2.48702, 0.0163, 0.04836, 0.0838, 0.25808, 0.17575, 0.18261, 0.48027, 1.27662, 1.77678, 1.76206, 1.84079, 1.71372, 1.80124, 1.29483, 0.88784, 0.54331, 0.01283, 0.01786, 0.0253, 0.29316, 0.00482, 0.00579, 0.00792, 0.02825, 0.01754, 0.01284, 0.01566, 0.01865, 0.01334, 0.01263, 0.01599, 0.01042, 0.00742, 0.00673, 0.01186, 0.01153, 0.01224, 2.43717, 2.80853, 2.90183, 2.8771, 2.53359, 2.02922, 2.02819, 2.04882, 2.0258, 2.06755, 2.06392, 2.03039, 2.06516, 2.08521, 2.05847, 2.08485, 2.07883, 2.09939, 2.12688, 2.11314, 2.11532, 2.11293, 2.12107, 2.1044, 2.13512, 2.0901, 2.05888, 2.1031, 2.05044, 2.09286, 2.08749, 2.11594, 2.15431, 2.12424, 2.15067, 2.09315, 2.16631, 2.1096, 2.07081, 2.11794, 2.1476, 2.15705, 2.12933, 2.09651, 2.00432, 1.96375, 1.97786, 1.97244, 1.98877, 1.94975, 1.97826, 1.94554, 1.94539, 1.90187, 1.94914]

import matplotlib.pyplot as plt
plotplotplot = range(len(tfc))

plt.plot(plotplotplot, tfc, label='optical flow')
plt.plot(plotplotplot, thcRGB, label='RGB histogram')
plt.plot(plotplotplot, tadc, label='total pixel change')
plt.plot(plotplotplot, tgmse, label='gray mean squared error')

plt.xlabel('X axis')
plt.ylabel('Y axis')
plt.title('Birds Eye View')

plt.legend()

plt.show()

#####

plottolp = range(len(tfc[:2100]))

plt.plot(plottolp, tfc[:2100], label='optical flow')
plt.plot(plottolp, thcRGB[:2100], label='RGB histogram')
plt.plot(plottolp, tadc[:2100], label='total pixel change')
plt.plot(plottolp, tgmse[:2100], label='gray mean squared error')

plt.xlabel('X axis')
plt.ylabel('Y axis')
plt.title(f"{files[0]}")

plt.legend()

plt.show()


print(tfc[:200])
print("--------------")
print(thcRGB[:200])
print("--------------")
print(tadc[:200])
print("---------")
print(tgmse[:200])
print("---------------")
    
def get_surrounding_lines(arr, line_number, distance, cap):
    start = max(0, line_number - distance)
    end = min(cap, line_number + distance)
    return arr[start:line_number], arr[line_number], arr[line_number+1:end] 

def individual_frame_information_helper(scale, largest, threshold):
    if scale > threshold and largest:
        return True
    return False

def individual_frame_information_per_arr_type(arr_type, line_num, reach):
    if line_num < reach or line_num > len(arr_type) - (reach - 5): # quick fix
        print(len(arr_type), line_num, reach)
        raise IndexError(f"line number {line_num} is out of bounds")

    start, current, end = get_surrounding_lines(arr_type, line_num, reach, len(arr_type))
    start_sum = sum(start) if sum(start) else 0.00001
    end_sum = sum(end) if sum(end) else 0.00001

    # if line_num == 2000:
    #     print(start, current, end)

    average_of_start = start_sum/len(start)
    average_of_end = end_sum/len(end)

    scale_of_curr_to_start = round(current/average_of_start, 2)
    is_curr_largest_start = max(max(start), current) == current

    scale_of_curr_to_end = round(current/average_of_end, 2)
    is_curr_largest_end = max(max(end), current) == current

    scale_of_curr_to_total = round(current/average_of_start+average_of_end/2, 2)
    is_curr_largest_total = is_curr_largest_start and is_curr_largest_end

    boolean_count = []

    boolean_count.append(individual_frame_information_helper(scale_of_curr_to_start, is_curr_largest_start, 4.5))
    boolean_count.append(individual_frame_information_helper(scale_of_curr_to_end, is_curr_largest_end, 4.5))
    boolean_count.append(individual_frame_information_helper(scale_of_curr_to_total, is_curr_largest_total, 2.5))

    return sum(boolean_count) >= 1

def individual_frame_information(line_num, reach):
    boolean_count = []
    boolean_count.append(individual_frame_information_per_arr_type(curr_tadc, line_num, reach))
    boolean_count.append(individual_frame_information_per_arr_type(curr_tfc, line_num, reach))
    boolean_count.append(individual_frame_information_per_arr_type(curr_tgmse, line_num, reach))
    boolean_count.append(individual_frame_information_per_arr_type(curr_thcRGB, line_num, reach))

    return sum(boolean_count) >= 3

def create_barriers(line_num_start, line_num_end): # 50 2117
    barriers = []
    for line_num in range(line_num_start, line_num_end - 50):
        if individual_frame_information(line_num, 50):
            barriers.append(line_num)
    return barriers

def create_every_dictionary(total_pixel_change_arr, window):
    dictionary_to_iterate_over = defaultdict(float)
    for k in range(window, len(total_pixel_change_arr)):
        start_index = k - window
        current_average = sum(total_pixel_change_arr[start_index:k])
        dictionary_to_iterate_over[(start_index, k)] = round(current_average, 3)
    return dictionary_to_iterate_over


def final_filter_dictionary(dictionary_yay, barriers, desired_options):
    dictionary_ordered = sorted(dictionary_yay.items(), key=lambda x: x[1], reverse=True)
    final = []
    iteration_count = 0
    for key, value in dictionary_ordered:
        iteration_count += 1
        left, right = key[0], key[1]
        interfere = False
        for pair in final:
            pair_left, pair_right = pair[0][0], pair[0][1]
            if pair_left <= left <= pair_right or pair_left <= right <= pair_right: 
                interfere = True
                break
        if not interfere:
            for blockage in barriers:
                if left <= blockage <= right:
                    interfere = True
                    break
        if interfere: continue
        # if value > 280: 
        #     print("aaaaaaaaaaa", key, value)
        #     continue
        final.append((key, value, iteration_count))
        if len(final) > desired_options:
            return final
    return final


all_the_frames_PER_SECOND = []
for test_video in files:
    source_path = os.path.join(RUN_DIR, 'run1', test_video)

    cap = cv2.VideoCapture(source_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
    cap.release()
    # clip = VideoFileClip(source_path)
    # total_frames = int(clip.duration * clip.fps)
    print(total_frames)
    all_the_frames_PER_SECOND.append(total_frames)

start_index = 0

video_list = [] # video stuff

video_short_list = []

for i in range(len(files)):
    print(files[i], i)

    end_index = start_index + all_the_frames_PER_SECOND[i]

    curr_tadc = tadc[start_index: end_index]
    curr_tfc = tfc[start_index: end_index]
    curr_tgmse = tgmse[start_index: end_index]
    curr_thcRGB = thcRGB[start_index: end_index]


    barbar = create_barriers(50, all_the_frames_PER_SECOND[i]) # 50, 2117

    print(f"{files[i]}: ",barbar)

    dictdict = create_every_dictionary(curr_tadc, 72)

    finalfinal = final_filter_dictionary(dictdict, barbar, 3)

    start_index += all_the_frames_PER_SECOND[i]

    print(finalfinal)

    source_path = os.path.join(RUN_DIR, 'run1', files[i])

    clip = VideoFileClip(source_path)
    fps = clip.reader.fps

    found = False
    if finalfinal:
        clippyclippy = finalfinal[0]
        if clippyclippy[1] < 100:
            pass
        else:
            found = True
            filefilefile = files[i]
            startstartstart = round(finalfinal[0][0][0]/fps, 3)
            endendend = round(finalfinal[0][0][1]/fps, 3)
            tupletupletuple = (filefilefile, startstartstart, endendend)
            video_list.append(tupletupletuple)
    
    if found: 
        print("so far: ", video_list)
        found = False
    else:
        temp_bar_bar = []
        temp_dictdict = create_every_dictionary(curr_tadc, 72)
        temp_finalfinal = final_filter_dictionary(temp_dictdict, temp_bar_bar, 3)
        if not temp_finalfinal:
            print("oh no!!!!!!")
            pass
        temp_filefilefile = files[i]
        temp_startstartstart = round(temp_finalfinal[0][0][0]/fps, 3)
        temp_endendend = round(temp_finalfinal[0][0][1]/fps, 3)
        temp_tupletupletuple = (temp_filefilefile, temp_startstartstart, temp_endendend)
        video_list.append(temp_tupletupletuple)

    found2 = False
    if len(finalfinal) > 1:
        shortshort = finalfinal[1]
        if shortshort[1] < 50:
            pass
        filefilefile2 = files[i]
        startstartstart2 =  round(finalfinal[1][0][0]/fps, 3)
        endendend2 = round(finalfinal[1][0][1]/fps, 3)
        tupletupletuple2 = (filefilefile2, startstartstart2, endendend2)
        video_short_list.append(tupletupletuple2)
        found2 = True
    if found2:
        print("so far small: ", video_short_list)
        continue
    else:
        temp_bar_bar_2 = []
        temp_dictdict_2 = create_every_dictionary(curr_tadc, 72)
        temp_finalfinal_2 = final_filter_dictionary(temp_dictdict_2, temp_bar_bar_2, 3)
        if not temp_finalfinal_2:
            print("oh no!!!!!! round 2!!!!")
            pass
        temp_filefilefile_2 = files[i]
        temp_startstartstart_2 = round(temp_finalfinal_2[0][0][0]/fps, 3)
        temp_endendend_2 = round(temp_finalfinal_2[0][0][1]/fps, 3)
        temp_tupletupletuple_2 = (temp_filefilefile_2, temp_startstartstart_2, temp_endendend_2)
        video_short_list.append(temp_tupletupletuple_2)


print("final clips")
print(video_list)
print(video_short_list)


video_clips = []
video_clips_short = []

audio_clip_path_4 = os.path.join(BASE_DIR, "sasageyo_4.mp3")
audio_clip_path_8 = os.path.join(BASE_DIR, "sasageyo_8.mp3")

audio_clip_4 = AudioFileClip(audio_clip_path_4)
audio_clip_8 = AudioFileClip(audio_clip_path_8)

for video_file, start_time, end_time in video_list:
    source_path = os.path.join(RUN_DIR, 'run1', video_file)
    video = VideoFileClip(source_path).subclip(start_time, end_time)
    video_clips.append(video)

for video_file_short, start_time_short, end_time_short in video_short_list:
    source_path_short = os.path.join(RUN_DIR, 'run1', video_file_short)
    video_short = VideoFileClip(source_path_short).subclip(start_time_short, end_time_short)
    video_clips_short.append(video_short)


import random

random.shuffle(video_clips)
random.shuffle(video_clips_short)

print("heheheh", video_clips)
print("fefefef", video_clips_short)

final_video_4 = []

for i1 in range(len(video_clips)):
    final_video_4.append(video_clips[i1])

final_clip_4 = concatenate_videoclips(final_video_4)
print(final_clip_4.fps)
print("------")
print(audio_clip_4.fps)
audio_clip_4 = audio_clip_4.set_fps(final_clip_4.fps)
final_clip_4 = final_clip_4.set_audio(audio_clip_4)
# final_clip_4.preview()
final_clip_4.write_videofile("final_video_4.mp4", codec='libx264', audio_codec='aac', audio=True)

final_video_clips = []
for i2 in range(len(video_clips_short)):
    final_video_clips.append(video_clips_short[i2])

final_video_clips.extend(final_video_4)


print("ooo", final_video_clips)
final_clip = concatenate_videoclips(final_video_clips)
print(final_clip.fps)
audio_clip = audio_clip_8.set_fps(final_clip.fps)
print("------")
print(audio_clip.fps)
final_clip = final_clip.set_audio(audio_clip)
# final_clip.preview()
final_clip.write_videofile("final_video_8.mp4", codec='libx264', audio_codec='aac', audio=True)


final_clip_4.preview()

final_clip.preview()



print(time.time() - time_start)

