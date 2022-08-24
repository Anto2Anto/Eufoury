ABOUT:


The application is been created for processing audio files of the *.wav format.

One separated frequency band can be deleted from the audio file. 

It might be useful in case a user wants to get rid of noise in the file.

I used the Python programming language only, but a user doesn't have to know it at all, one shouldn't code while using the app.

------------------------------------------------------------------------------------------------------------------------------------------

REQUIRED LIBRARIES:


sys

numpy

soundfile

PyQt6

matplotlib

librosa

------------------------------------------------------------------------------------------------------------------------------------------

WORKFLOW:


	1. After opening and launching the main file - gui.py - the main window of the application appears 

(the second file check.py doesn't have to be opened, just be in the same direction as gui.py).

	2. By using File->Open a user can choose a *.wav file on his work station.

Just after that two plots in upper-left and upper-right corners of the window appear.

The first displays signal-time field, and how the amplitude evolves over time.

All data for the second plot is being calculated in real-time using Short-Time Fourier Transform.

So, the second plot shows how frequencies spread in time. 

But as far as it's a color map, the color brightness also shows the amplitude, just according to the first plot.

	3. After looking at the two plots, a user may decide, what frequencies should be deleted. It's able to choose one band only.

A user types frequency values (of float type) of the borders in the two blank field just under the first plot.

	4. After pushing "Get processed signal" button, two other plots are calculated.

The bottom-right plot shows almost the same frequency-time domain as top-right, but all chosen frequencies are deleted now.

At the same time the bottom-left plot shows the new (processed) signal, distrubution of new values of amplitude over time.

In the case user has to change the band, one can just type new values of borders again, and press the button. Third and forth plots will be overwritten.
		
	5. Finally the processed file can be written in *.wav file format by using File->Save.

----------------------------------------------------------------------------------------------------------------------------------------------

BENEFITS & DRAWBACKS OF THE APPICATION:


+ The simpliest user-friendly interface															- Only one frequency band can be chosen

+ Doesn't require resources (space, memory) to be launched					- Only *.wav format can be used in the app.

+ Open-sourced																											- Crashes in case of large files (more then 3 min). Not optimized yet.

+ Might be used quickly, when there's no time
  to install bigger applications or programs
	
+ Informative
