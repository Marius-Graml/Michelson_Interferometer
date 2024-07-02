# Michelson_Interferometer

The basic idea of this project was to set up a michelson interferometer, which is able to adjust to a specific fringe pattern. This means, the fringe pattern of the interferometer is supposed to stay the same regardless of any disturbations from outside (e.g., sound waves, vibrations, wind)

The interferometer was mainly et up using mirrors and other optical equipment from ThorLabs. The whole control loop was implemented using Python. For measuring the intensity of the fringe pattern, the oscilloscope of a Moku:Go was used, which was accessed by an API.
In order to display all relevant signals of the system, i.e., the input signal of the oscilloscpe, the filter output and the output of the PID controller, a GUI was implemented, which was also done in Python. The following image shows the main screen of the user interface, when the control loop is active, i.e.. the fringe pattern of the interferometer is tried to keep steady. 

