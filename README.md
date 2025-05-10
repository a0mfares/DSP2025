# Audio Signal Processing and Digital Filtering
The project focuses on the primary areas of audio signal processing through MATLAB/Octave compatible Python tools. The project is recruited into two groups which include noise and interference removal through the digital filters design and implementation.
---
## 📁 Project Structure
### **Part 1: Audio Signal Analysis**
1. **Reading and Inspecting Audio**
   - Bringing in and checking an audio file.
   - The middle extract means a 3-second part.
2. **Time Domain Visualization**
   - A plot for the audio waveform.
3. **Interference Simulation**
   - Creating a synthesized tone to serve as a representation of an interfering signal.
   - Getting the tone and the audio superimposed, and then comparing the results.
4. **Frequency Domain Analysis**
   - Estimating the power spectral density (PSD) of an audio signal by Welch's method.
   - Experimenting with the impact of such things as:
     - The length of the window
     - The size of FFT
     - The percentage of overlap
     - How is the shape of the window
     - The frequencies of the signal and the interference
---
### **Part 2: Digital Filter Design and Application**
1. **Problem Formulation**
   - Specifying the filtration objective.
2. **Filter Constraints**
   - Setting up various parameters related to the passband, the stopband, the ripple, and the attenuation.
3. **Filter Specification and Design**
   - Doing a comparison of different filter categories (e.g., FIR, IIR).
   - The utilization of decision-making metrics to select the preferred filter.
4. **Filtering and Result Analysis**
   - The filter selected should be applied.
   - The noise-free signal must be compared with the noisy one.
---
## 🔧 Technologies Used
- Python (Jupyter Notebook)
- NumPy
- SciPy
- Matplotlib
- Signal processing libraries (`scipy.signal`)
---

## 📊 Results
- The frequency and time characteristics could be visualized successfully.
- The impact of the most important PSD parameters was shown.
- Different filters have been created and examined.
- A significant decrease in the reflections has been detected in the output after filtration. -->
## 📂 How to Run
1. Clone this repository.
2. Then open the `project.ipynb` by Jupyter Notebook.
3. Confirm the needed libraries are present by executing:
```bash
pip install -r requirements.txt
```
4. Next, go through all the cells.
---
## Testing

[Watch the video here](https://drive.google.com/file/d/1_MnXbUYTD1__S9Ltup_PumtJ3dsCvfml/view?usp=sharing)

---
## 📌 Notes
- This project has been designed in a way that its parts, as well as a separate study, can be chosen. Part 1 and Part 2.
- The code cells are allowing the audio files in the working directory to be updated or a new location can be specified.
