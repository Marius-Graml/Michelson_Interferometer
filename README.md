# Michelson_Interferometer

The basic idea of this project was to set up a michelson interferometer, which is able to adjust to a specific fringe pattern. This means, the fringe pattern of the interferometer is supposed to stay the same regardless of any disturbations from outside (e.g., sound waves, vibrations, wind).

The interferometer was mainly set up using optical equipment from ThorLabs. The control loop and a corresponding user interface for the controlling was implemented in Python. For measuring the intensity of the fringe pattern, the oscilloscope of a Moku:Go was used, which was accessed by an API.
The implemented user displays all relevant signals of the system, i.e., the input signal of the oscilloscpe, the demodulation of the input signal, the filtered signal and the output of the PID controller. The following image shows the main screen of the user interface, when the control loop is active. 

