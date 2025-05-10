import os
import numpy as np
import matplotlib.pyplot as plt
import librosa
import scipy.signal as signal
import io
import base64
from flask import Flask, render_template, request
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)

# Configure upload folder 
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form parameters
        try:
            # Audio parameters
            sr = int(request.form.get('sr', 44100))
            
            # Interference parameters
            interference_f = float(request.form.get('interference_f', 15200))
            interference_amplitude = float(request.form.get('interference_amplitude', 1.8))
            
            # FFT parameters
            fft_size = int(request.form.get('fft_size', 2048))
            window_size = int(request.form.get('window_size', 2048))
            window_type = request.form.get('window_type', 'hann')
            overlap_percent = float(request.form.get('overlap_percent', 50))
            
            # Filter parameters
            filter_type = request.form.get('filter_type', 'butter')
            order = int(request.form.get('order', 8))
            cutoff = float(request.form.get('cutoff', 5000))
            ripple = float(request.form.get('ripple', 1))
            attenuation = float(request.form.get('attenuation', 40))
            
            # Check if file was uploaded
            if 'audio_file' not in request.files:
                return render_template('index.html', error="No audio file provided")
            
            audio_file = request.files['audio_file']
            if audio_file.filename == '':
                return render_template('index.html', error="No audio file selected")
            
            # Save the uploaded file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_file.filename)
            audio_file.save(file_path)
            
            # Print for debugging
            print(f"File saved to: {file_path}")
            print(f"File exists: {os.path.exists(file_path)}")
            
            # Process the audio file and generate results
            results = process_audio(file_path, sr, interference_f, interference_amplitude, 
                                   fft_size, window_size, window_type, overlap_percent,
                                   filter_type, order, cutoff, ripple, attenuation)
            
            return render_template('index.html', results=results)
            
        except Exception as e:
            import traceback
            error_msg = f"Error processing audio: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)
            return render_template('index.html', error=error_msg)
    
    return render_template('index.html')

def plot_to_base64(plt):
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    plt.close()
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode('utf-8')

def audio_to_base64(audio_data, sr):
    import tempfile
    import soundfile as sf
    
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
        sf.write(temp_file.name, audio_data, sr)
        
    with open(temp_file.name, 'rb') as f:
        audio_base64 = base64.b64encode(f.read()).decode('utf-8')
    
    os.unlink(temp_file.name)
    return audio_base64

def process_audio(file_path, sr, interference_f, interference_amplitude, 
                 fft_size, window_size, window_type, overlap_percent,
                 filter_type, order, cutoff, ripple, attenuation):
    # Verify file exists before proceeding
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found at: {file_path}")
    
    print(f"Loading audio file: {file_path}")
    # Load audio file with specified sampling rate
    data, fs = librosa.load(file_path, sr=sr)
    
    # Extract segment from middle of audio
    middle_index = len(data) // 2
    samples = int(3 * fs)
    start_index = middle_index - samples // 2
    end_index = start_index + samples
    
    # Ensure we don't go out of bounds
    if end_index > len(data):
        end_index = len(data)
        start_index = max(0, end_index - samples)
    
    segment = data[start_index:end_index]
    
    # Ensure segment is 1D
    if len(segment.shape) > 1:
        segment = segment[:,0]
    
    # Generate time array
    time = np.arange(len(segment)) / fs
    
    # Plot original segment
    plt.figure()
    plt.plot(time, segment)
    plt.title("Original Audio Segment")
    plt.xlabel("Time (Seconds)")
    plt.ylabel("Amplitude")
    orig_segment_plot = plot_to_base64(plt)
    
    # Create interference signal
    interference = interference_amplitude * np.sin(2 * np.pi * interference_f * time)
    
    # Plot interference
    plt.figure()
    plt.plot(time, interference)
    plt.title("Interference Signal")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.xlim(0, min(3, time[-1]))
    plt.ylim(-2, 2)
    interference_plot = plot_to_base64(plt)
    
    # Add interference to segment
    new_segment = segment + interference
    
    # Plot original vs with interference
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(time, segment)
    plt.title('Original Audio Signal')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    
    plt.subplot(2, 1, 2)
    plt.plot(time, new_segment)
    plt.title('Audio Signal with Interference')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.tight_layout()
    comparison_plot = plot_to_base64(plt)
    
    # Plot Welch spectrum
    welch_plot, psd, detected_interference = plot_welch_spectrum(
        new_segment, fs, fft_size, window_size, window_type, overlap_percent)
    
    # Design and evaluate filters
    nyquist_freq = fs / 2
    filter_metrics, filter_plot = design_filter(
        filter_type, fs, order, cutoff, ripple, attenuation, interference_f)
    
    # Apply the filter
    b, a = filter_metrics['b'], filter_metrics['a']
    filtered_audio = signal.filtfilt(b, a, new_segment)
    
    # Plot before and after filtering
    plt.figure(figsize=(12, 8))
    plt.subplot(3, 1, 1)
    plt.plot(time, segment)
    plt.title('Original Audio Signal')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    
    plt.subplot(3, 1, 2)
    plt.plot(time, new_segment)
    plt.title('Audio with Interference')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    
    plt.subplot(3, 1, 3)
    plt.plot(time, filtered_audio)
    plt.title('Filtered Audio Signal')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    
    plt.tight_layout()
    filtered_comparison_plot = plot_to_base64(plt)
    
    # Convert audio segments to base64 for playback
    orig_audio_b64 = audio_to_base64(segment, fs)
    noisy_audio_b64 = audio_to_base64(new_segment, fs)
    filtered_audio_b64 = audio_to_base64(filtered_audio, fs)
    
    # Return all results
    return {
        'fs': fs,
        'segment_length': len(segment) / fs,
        'interference_f': interference_f,
        'detected_interference': detected_interference,
        'window_type': window_type,
        'filter_type': filter_type,
        'filter_order': order,
        'orig_segment_plot': orig_segment_plot,
        'interference_plot': interference_plot,
        'comparison_plot': comparison_plot,
        'welch_plot': welch_plot,  
        'filter_plot': filter_plot,
        'filtered_comparison_plot': filtered_comparison_plot,
        'orig_audio': orig_audio_b64,
        'noisy_audio': noisy_audio_b64,
        'filtered_audio': filtered_audio_b64,
        'filter_metrics': filter_metrics
    }

def plot_welch_spectrum(data, fs, fft_size, window_size, window_type='hann', overlap_percent=50):
    """Plot the single-sided power spectrum using Welch's method and detect interference frequency."""
    # Calculate overlap in samples
    overlap = int(window_size * overlap_percent / 100)

    # Define window functions
    window_types = {
        'hann': np.hanning(window_size),
        'hamming': np.hamming(window_size),
        'blackman': np.blackman(window_size),
        'rectangular': np.ones(window_size)
    }

    window = window_types.get(window_type.lower())
    if window is None:
        print(f"Window type '{window_type}' not recognized. Using Hann window instead.")
        window = np.hanning(window_size)

    # Compute Welch PSD
    freqs, psd = signal.welch(data, fs=fs, window=window, nperseg=window_size,
                              noverlap=overlap, nfft=fft_size, return_onesided=True)
   
    # Convert to dB scale
    psd_db = 10 * np.log10(psd + 1e-12)  
    peak_index = np.argmax(psd)
    interference_freq = freqs[peak_index]
    interference_power = psd_db[peak_index]

    # Plot the PSD
    plt.figure(figsize=(12, 6))
    plt.plot(freqs, psd_db, label='Power Spectrum')
    plt.axvline(interference_freq, color='r', linestyle='--', linewidth=1.5, 
                label=f'Interference ≈ {interference_freq:.2f} Hz')
    plt.title(f'Power Spectrum using Welch Method\nWindow: {window_type}, Size: {window_size}, '
              f'Overlap: {overlap_percent}%, FFT: {fft_size}')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power Spectral Density (dB/Hz)')
    plt.grid(True)
    plt.legend()
    plt.xlim(0, fs/2)
    plt.tight_layout()
    
    welch_plot = plot_to_base64(plt)
    
    return welch_plot, psd, interference_freq

def design_filter(filter_type, fs, order, cutoff, ripple, attenuation, interference_f):
    """Design and plot filter response based on user parameters."""
    nyquist_freq = fs / 2
    
    # Normalizing frequency to Nyquist
    if isinstance(cutoff, (list, tuple)):
        normalized_cutoff = [freq / nyquist_freq for freq in cutoff]
    else:
        normalized_cutoff = cutoff / nyquist_freq

    # Filter design
    if filter_type == 'butter':
        b, a = signal.butter(order, normalized_cutoff, btype='low')
        title = f"Butterworth Filter (Order {order})"
    elif filter_type == 'cheby1':
        b, a = signal.cheby1(order, ripple, normalized_cutoff, btype='low')
        title = f"Chebyshev Type I Filter (Order {order}, Ripple {ripple} dB)"
    elif filter_type == 'cheby2':
        b, a = signal.cheby2(order, attenuation, normalized_cutoff, btype='low')
        title = f"Chebyshev Type II Filter (Order {order}, Attenuation {attenuation} dB)"
    elif filter_type == 'ellip':
        b, a = signal.ellip(order, ripple, attenuation, normalized_cutoff, btype='low')
        title = f"Elliptic Filter (Order {order}, Ripple {ripple} dB, Attenuation {attenuation} dB)"
    elif filter_type == 'fir':
        b = signal.firwin(order + 1, normalized_cutoff, window='hamming')
        a = [1.0]
        title = f"FIR Filter (Order {order}, Hamming window)"
    else:
        raise ValueError(f"Unknown filter type: {filter_type}")

    # Frequency response
    w, h = signal.freqz(b, a, worN=8000)
    w_hz = w * fs / (2 * np.pi)

    # Group delay
    w_gd, gd = signal.group_delay((b, a), w=8000)
    w_gd_hz = w_gd * fs / (2 * np.pi)
    avg_delay_samples = np.mean(gd)
    avg_delay_ms = (avg_delay_samples / fs) * 1000

    # Plotting
    plt.figure(figsize=(14, 10))

    # Magnitude response
    plt.subplot(3, 1, 1)
    plt.plot(w_hz, 20 * np.log10(abs(h)))
    plt.axvline(x=cutoff, color='g', linestyle='--', label=f'Cutoff: {cutoff} Hz')
    plt.axvline(x=interference_f, color='m', linestyle='--', label=f'Interference: {interference_f} Hz')
    plt.title(title)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude (dB)')
    plt.grid(True)
    plt.legend(loc='lower left')
    plt.xlim(0, fs / 2)
    plt.ylim(-80, 5)

    # Passband detail
    plt.subplot(3, 1, 2)
    plt.plot(w_hz, 20 * np.log10(abs(h)))
    plt.axvline(x=cutoff, color='g', linestyle='--')
    plt.title(f'Passband Detail - {title}')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude (dB)')
    plt.grid(True)
    plt.xlim(0, cutoff * 1.2)
    plt.ylim(-3, 1)

    # Group delay plot
    plt.subplot(3, 1, 3)
    plt.plot(w_gd_hz, gd)
    plt.axvline(x=cutoff, color='g', linestyle='--')
    plt.title(f'Group Delay - Avg: {avg_delay_samples:.2f} samples ({avg_delay_ms:.2f} ms)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Group delay (samples)')
    plt.grid(True)
    plt.xlim(0, fs / 2)

    plt.tight_layout()
    filter_plot = plot_to_base64(plt)

    # Calculate metrics
    stopband_vals = 20 * np.log10(abs(h[w_hz > interference_f]))
    stopband_rejection = -np.min(stopband_vals) if stopband_vals.size > 0 else 0

    metrics = {
        'type': filter_type,
        'order': order,
        'avg_delay_ms': avg_delay_ms,
        'passband_deviation': np.max(np.abs(20 * np.log10(abs(h[w_hz < cutoff])))),
        'stopband_rejection': stopband_rejection,
        'num_coefficients': len(b) + len(a) - 1,
        'b': b,
        'a': a
    }

    return metrics, filter_plot


if __name__ == '__main__':
   
    app.run(debug=True)