# Audio Signal Processing and Digital Filtering 🎵🔊
An all-inclusive project dedicated to audio signal analysis and digital filter design that was not only created using Jupyter Notebook but was also made interactive as a web application.
## 🌟 Features
- **Audio Analysis**: Representation of the signal in both time domain and frequency domain
- **Noise Simulation**: User is allowed to implement custom interference tones
- **Advanced Filtering**: Several filter types like Butterworth, Chebyshev, Elliptic, FIR
- **Web Interface**: A software front-end that is user-friendly for all processing capabilities
- **Comparative Results**: Comparison of side-by-side analysis of original/noisy/filtered signals
## 📁 Project Structure
```
├── Notebook/
│   └── project.ipynb            # The notebook contains all the code for analysis
├── Web app/
│   ├── static/                  # The web resources source
│   │   ├── styles.css           # Custom stylesheet
│   │   └── script.js            # Client-side functionality
│   ├── templates/
│   │   └── index.html           # The front-end of the application
│   └── app.py                   # Flask application backend
├── requirements.txt             # Python dependencies
└── README.md                    # This documentation
```
## 🛠️ Technologies Used

- **Core Processing**: 

  ![Python](https://img.shields.io/badge/Python-3.8%2B-blue)

  ![NumPy](https://img.shields.io/badge/NumPy-1.22+-orange)

  ![SciPy](https://img.shields.io/badge/SciPy-1.8+-blue)

- **Visualization**: 

  ![Matplotlib](https://img.shields.io/badge/Matplotlib-3.5+-brightgreen)

- **Web Framework**: 

  ![Flask](https://img.shields.io/badge/Flask-2.0+-lightgrey)

- **Audio Processing**: 

  ![Librosa](https://img.shields.io/badge/Librosa-0.9+-yellowgreen)

## 🚀 Getting Started
### For Jupyter Notebook Analysis

```bash

# Clone repository

git clone https://github.com/yourusername/audio-filtering-project.git

cd audio-filtering-project

# Install dependencies

pip install -r requirements.txt

# Launch Jupyter

jupyter notebook Notebook/project.ipynb

```

### For Web Application

```bash
cd Web app

# Install dependencies (if not already done)

pip install -r ../requirements.txt

# Run the application

python app.py

# Access at http://localhost:5000

# Public URL will appear in console (via ngrok)

```
## 🔍 Project Components
### Part 1: Audio Signal Analysis
1. **File Handling**
- Load and analyze audio files
- Extract 3 seconds segment from the middle of the audio file  
2. **Time Domain Visualization**
- Plot signal over time
3. **Interference Simulation**
- Creating a sine signal with a certain frequency to simulate interference 
4. **Frequency Analysis**
- Power Spectral Density (PSD) via Welch's technique
- Parameter exploration:
 - Window size/type (Hann, Hamming, Blackman, Rectangular)
 - FFT size
 - Overlap percentage

### Part 2: Digital Filter Design
1. **Filter Specification**
   - Set passband/stopband parameters
   - Configure ripple/attenuation
2. **Filter Types**
   - IIR: Butterworth, Chebyshev, Elliptic
   - FIR: Window-based design
3. **Performance Analysis**
   - Frequency response
   - Group delay
   - Stopband attenuation
4. **Application**
   - Filter noisy signal
   - Compare before/after results

## 🌐 Web Application Features
![Web App Interface](https://via.placeholder.com/800x400?text=Web+App+Screenshot)

The interactive web interface provides:
- **Drag-and-drop** audio upload
- **Real-time parameter** adjustment:
  - Interference frequency (Hz) and amplitude
  - FFT analysis settings
  - Filter design specifications
- **Interactive plots**:
  - Time-domain waveforms
  - Frequency spectra
  - Filter responses
- **Audio playback** of all stages
- **Performance metrics** display

### Part 2: Digital Filter Design
1. **Filter Specification**
   - Define passband/stopband characteristics
   - Specify ripple/attenuation parameters
2. **Filter Types**
   - IIR: Butterworth, Chebyshev, Elliptic
   - FIR: Window-based design
3. **Performance Analysis**
   - Frequency response
   - Group delay
   - Stopband attenuation
4. **Application**
   - Remove noise from the signal
   - Compare the result before/after filtration
## 🌐 Web Application Features
![Web App Interface](https://via.placeholder.com/800x400?text=Web+App+Screenshot)
An interactive web interface offers:
- **Audio uploading** 
- **Real-time parameter adjustment:**
  - Interference frequency (Hz) and amplitude
  - welch's method settings
  - Filter design specifications
- **Displaying plots**:
  - Time-domain waveforms
  - Frequency spectra
  - Filter responses
- **Audio playback of all stages** 
- **Display Performance metrics** 
## 📊 Example Results
1. **Time Domain Comparison**
   ![Waveform Comparison](https://via.placeholder.com/600x300?text=Waveform+Comparison)
2. **Frequency Analysis**
   ![Spectrum Analysis](https://via.placeholder.com/600x300?text=Spectrum+Plot)
3. **Filter Response**
   ![Filter Characteristics](https://via.placeholder.com/600x300?text=Filter+Response)
- Segments of 3 seconds are used for all audio processing to ensure that the results are comparable
- The parameters that come by default are set to the configuration of voice-frequency ranges ideal
- Ngrok gives you access to public URLs only for short periods of time - for stable hosting there is a wide range of solutions to choose from:
  - AWS Elastic Beanstalk ( Tried but face computation delays and some timeouts due to lack of resources ) 
  - Heroku 
  - PythonAnywhere ( couldn't even install dependencies because lack of storage )
