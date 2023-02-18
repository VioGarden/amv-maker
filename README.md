# DCP AMV v1

works on node v14.21.2

Step 1 :  
pip3 install -r requirements.txt  

Step 2 :  
create 2 empty folders in 'runs' folder called 'run1' and 'run1_output'  
(folder structure should look like)  
/data/runs  
&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;/run1  
&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;/run1_output  
&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;/storage  
    
Step 3 :  
uncomment/comment videos in create_run.py  
run >create_run.py< (with at least 4 videos uncommented, might take 30-40 seconds)

Step 4 :  
run >main.py<   

Step 5 :   
dcp part runs, then plot shows up, click x on the plot and rest of code will run creating videos stored into 'run1_output' folder  

<br>
<br>
<br>
note 1 : if you do use anime opening videos, there may be very slight spoilers, proceed with caution  
<br>
<br>
note 2 : I do not own any audio/video/technology used in this project
<br>
<br>
note 3 : may take 30 seconds to clone
<br>
<br>
note 4 : currently configured on the demo compute group
<br>
<br>
note 5 : works on Mac Os Monterey
