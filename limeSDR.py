import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time
from scipy.signal import butter, lfilter, freqz # Importar scipy.signal para DSP

# Importar la librería para LimeSDR
try:
    import pylimesdr
    LIME_SDR_AVAILABLE = True
except ImportError:
    print("Advertencia: La librería 'pylimesdr' no está instalada. La aplicación funcionará en modo simulación básica (sin interacción real con SDR).")
    LIME_SDR_AVAILABLE = False
except Exception as e:
    print(f"Error al cargar pylimesdr: {e}. La aplicación funcionará en modo simulación básica (sin interacción real con SDR).")
    LIME_SDR_AVAILABLE = False

class NBFMInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Transmisor-Receptor NBFM (Hardware Real)")
        self.root.geometry("1000x750") # Tamaño inicial de la ventana
        self.root.resizable(True, True) # Permitir redimensionar la ventana

        # Configuración de estilos para una apariencia más moderna
        style = ttk.Style()
        style.theme_use('clam') # 'clam', 'alt', 'default', 'classic'
        style.configure('TFrame', background='#e0e0e0', borderwidth=2, relief='groove')
        style.configure('TLabelframe', background='#e0e0e0', borderwidth=2, relief='ridge')
        style.configure('TLabel', background='#e0e0e0', font=('Inter', 10))
        style.configure('TButton', font=('Inter', 10, 'bold'))
        style.configure('TRadiobutton', background='#e0e0e0', font=('Inter', 10))
        style.configure('TScale', background='#e0e0e0')
        style.configure('TNotebook.Tab', font=('Inter', 10, 'bold')) # Estilo para las pestañas

        # Variables de estado del LimeSDR
        self.sdr = None
        self.rx_stream_active = False
        self.tx_stream_active = False
        self.stop_threads = threading.Event() # Evento para detener los hilos de RX/TX
        self.rx_thread = None
        self.tx_thread = None
        self.current_rx_samples_iq = np.array([]) # Almacena las muestras IQ recibidas del SDR
        self.current_rx_samples_audio = np.array([]) # Almacena las muestras de audio demoduladas

        # Parámetros DSP
        self.audio_sample_rate = 48000 # Frecuencia de muestreo de audio, como en GNU Radio
        self.sdr_sample_rate = 5e6 # Frecuencia de muestreo del SDR (muestras IQ)
        self.max_freq_deviation = 5000 # Hz, DeltaF = 5kHz como en el documento
        self.kf = 2 * np.pi * self.max_freq_deviation / (self.audio_sample_rate / 2) # Constante de desviación de frecuencia para FM
        self.preemphasis_tau = 75e-6 # 75 us como en el documento
        self.audio_lowpass_cutoff = 5000 # Hz, ancho de banda de audio 5 kHz
        self.squelch_threshold_db = -45 # dB, umbral de squelch como en el documento

        # Contenedor principal
        main_frame = ttk.Frame(root, padding="10 10 10 10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Sección de Control General (Rojo en el documento) ---
        control_frame = ttk.LabelFrame(main_frame, text="CONTROL", padding="10 10 10 10")
        control_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.operation_mode = tk.StringVar(value="Full Duplex")
        ttk.Radiobutton(control_frame, text="Full Duplex", variable=self.operation_mode, value="Full Duplex", command=self.update_interface).grid(row=0, column=0, padx=10, pady=5)
        ttk.Radiobutton(control_frame, text="Push to Talk", variable=self.operation_mode, value="Push to Talk", command=self.update_interface).grid(row=0, column=1, padx=10, pady=5)
        ttk.Radiobutton(control_frame, text="Test", variable=self.operation_mode, value="Test", command=self.update_interface).grid(row=0, column=2, padx=10, pady=5)

        ttk.Label(control_frame, text="Frec. Test:").grid(row=0, column=3, padx=10, pady=5)
        self.test_freq_var = tk.StringVar(value="1000 Hz")
        self.test_freq_options = ["400 Hz", "1000 Hz", "3000 Hz"]
        # Al cambiar la frecuencia de test, se debe reiniciar la transmisión en modo Test
        self.test_freq_menu = ttk.OptionMenu(control_frame, self.test_freq_var, self.test_freq_var.get(), *self.test_freq_options, command=lambda x: self.start_tx_if_test())
        self.test_freq_menu.grid(row=0, column=4, padx=10, pady=5)

        # --- Sección de Control Push to Talk (Naranja en el documento) ---
        ptt_frame = ttk.LabelFrame(main_frame, text="CONTROL PUSH TO TALK", padding="10 10 10 10")
        ptt_frame.grid(row=0, column=2, columnspan=2, padx=5, pady=5, sticky="ew")
        self.ptt_status = tk.StringVar(value="Desactivado")
        self.ptt_button = ttk.Button(ptt_frame, text="Push to Talk", command=self.toggle_ptt)
        self.ptt_button.grid(row=0, column=0, padx=10, pady=5)
        self.ptt_label = ttk.Label(ptt_frame, textvariable=self.ptt_status)
        self.ptt_label.grid(row=0, column=1, padx=10, pady=5)

        # --- Controles de Transmisor y Receptor (Verde y Azul) ---
        tx_rx_frame = ttk.Frame(main_frame)
        tx_rx_frame.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky="ew")
        tx_rx_frame.grid_columnconfigure(0, weight=1)
        tx_rx_frame.grid_columnconfigure(1, weight=1)

        # Control de Transmisor (Verde)
        tx_frame = ttk.LabelFrame(tx_rx_frame, text="CONTROL DE TRANSMISOR", padding="10 10 10 10")
        tx_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        ttk.Label(tx_frame, text="Ganancia de transmisor (dB):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.tx_gain = tk.DoubleVar(value=45.0)
        # Al mover el slider, se aplican las configuraciones al SDR
        ttk.Scale(tx_frame, from_=0.0, to=100.0, orient=tk.HORIZONTAL, variable=self.tx_gain, command=self.apply_sdr_settings).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Entry(tx_frame, textvariable=self.tx_gain, width=5).grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(tx_frame, text="Frecuencia RF transmisor [MHz]:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.tx_freq = tk.DoubleVar(value=916.000)
        # Al cambiar la frecuencia, se aplican las configuraciones al SDR
        ttk.Entry(tx_frame, textvariable=self.tx_freq, width=10).grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        self.tx_freq.trace_add("write", lambda *args: self.apply_sdr_settings()) # Detectar cambios manuales en la entrada

        ttk.Label(tx_frame, text="Ganancia de MIC (dB):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.mic_gain = tk.DoubleVar(value=1.0)
        # Esta ganancia afectará la amplitud de la señal generada para TX
        ttk.Scale(tx_frame, from_=0.0, to=10.0, orient=tk.HORIZONTAL, variable=self.mic_gain, command=self.start_tx_if_test).grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        ttk.Entry(tx_frame, textvariable=self.mic_gain, width=5).grid(row=2, column=2, padx=5, pady=5)


        # Control de Receptor (Azul)
        rx_frame = ttk.LabelFrame(tx_rx_frame, text="CONTROL DE RECEPTOR", padding="10 10 10 10")
        rx_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        ttk.Label(rx_frame, text="Ganancia de receptor (dB):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.rx_gain = tk.DoubleVar(value=30.0)
        # Al mover el slider, se aplican las configuraciones al SDR
        ttk.Scale(rx_frame, from_=0.0, to=100.0, orient=tk.HORIZONTAL, variable=self.rx_gain, command=self.apply_sdr_settings).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Entry(rx_frame, textvariable=self.rx_gain, width=5).grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(rx_frame, text="Frecuencia RF receptor [MHz]:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.rx_freq = tk.DoubleVar(value=917.000)
        # Al cambiar la frecuencia, se aplican las configuraciones al SDR
        ttk.Entry(rx_frame, textvariable=self.rx_freq, width=10).grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        self.rx_freq.trace_add("write", lambda *args: self.apply_sdr_settings()) # Detectar cambios manuales en la entrada

        ttk.Label(rx_frame, text="Volumen de audio:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.audio_volume = tk.DoubleVar(value=0.5)
        # Este control es para la simulación de audio o para una futura implementación de audio
        ttk.Scale(rx_frame, from_=0.0, to=1.0, orient=tk.HORIZONTAL, variable=self.audio_volume, command=self.update_measurements_display).grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        ttk.Entry(rx_frame, textvariable=self.audio_volume, width=5).grid(row=2, column=2, padx=5, pady=5)

        # --- Sección de Mediciones (Violeta) ---
        measurements_frame = ttk.LabelFrame(main_frame, text="MEDICIONES", padding="10 10 10 10")
        measurements_frame.grid(row=2, column=0, columnspan=4, padx=5, pady=5, sticky="ew")
        measurements_frame.grid_columnconfigure(0, weight=1)
        measurements_frame.grid_columnconfigure(1, weight=1)

        # Mediciones SNR
        snr_frame = ttk.LabelFrame(measurements_frame, text="MEDICION SNR", padding="5 5 5 5")
        snr_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.snr_val = tk.StringVar(value="SNR: N/A")
        self.snr_signal = tk.StringVar(value="Señal: N/A")
        self.snr_noise_distortion = tk.StringVar(value="Ruido + Distorsión: N/A")
        ttk.Label(snr_frame, textvariable=self.snr_val).pack(anchor="w")
        ttk.Label(snr_frame, textvariable=self.snr_signal).pack(anchor="w")
        ttk.Label(snr_frame, textvariable=self.snr_noise_distortion).pack(anchor="w")

        # Mediciones SINAD
        sinad_frame = ttk.LabelFrame(measurements_frame, text="MEDICION SINAD", padding="5 5 5 5")
        sinad_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.sinad_val = tk.StringVar(value="SINAD: N/A")
        self.sinad_signal_noise_distortion = tk.StringVar(value="Señal + Ruido + Distorsión: N/A")
        self.sinad_noise_distortion = tk.StringVar(value="Ruido + Distorsión: N/A")
        ttk.Label(sinad_frame, textvariable=self.sinad_val).pack(anchor="w")
        ttk.Label(sinad_frame, textvariable=self.sinad_signal_noise_distortion).pack(anchor="w")
        ttk.Label(sinad_frame, textvariable=self.sinad_noise_distortion).pack(anchor="w")

        # --- Sección de Visualización de Gráficos (Marrón) con Notebook ---
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=3, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
        main_frame.grid_rowconfigure(3, weight=1) # Permite que el notebook se expanda verticalmente

        # Crear frames para cada pestaña
        self.tab_demodulated_signal = ttk.Frame(self.notebook, padding="10 10 10 10")
        self.tab_filtered_tone = ttk.Frame(self.notebook, padding="10 10 10 10")
        self.tab_noise_floor = ttk.Frame(self.notebook, padding="10 10 10 10")

        self.notebook.add(self.tab_demodulated_signal, text="SEÑAL DEMODULADA")
        self.notebook.add(self.tab_filtered_tone, text="TONO FILTRADO")
        self.notebook.add(self.tab_noise_floor, text="PISO DE RUIDO")

        # Variables para controlar el modo de visualización de cada pestaña
        self.demod_signal_display_mode = tk.StringVar(value="Frecuencia")
        self.filtered_tone_display_mode = tk.StringVar(value="Frecuencia")
        self.noise_floor_display_mode = tk.StringVar(value="Frecuencia")

        # Añadir controles de visualización a cada pestaña
        self._add_display_mode_controls(self.tab_demodulated_signal, self.demod_signal_display_mode)
        self._add_display_mode_controls(self.tab_filtered_tone, self.filtered_tone_display_mode)
        self._add_display_mode_controls(self.tab_noise_floor, self.noise_floor_display_mode)

        # Configurar el gráfico de Matplotlib en la primera pestaña inicialmente
        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.tab_demodulated_signal)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        # Vincular el evento de cambio de pestaña para actualizar el gráfico
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)


        # Inicializar LimeSDR al inicio de la aplicación
        self.initialize_sdr()

        # Configurar el cierre de la ventana para liberar recursos del SDR
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Actualizar la interfaz y las mediciones/espectro iniciales
        self.update_interface()
        self.update_measurements_display()

    # --- Funciones Auxiliares para la GUI ---
    def _add_display_mode_controls(self, parent_frame, mode_var):
        """Añade los botones de radio para seleccionar el modo de visualización (Tiempo/Frecuencia)."""
        control_frame = ttk.Frame(parent_frame)
        control_frame.pack(side=tk.TOP, fill=tk.X, pady=5)
        
        ttk.Label(control_frame, text="Modo de Visualización:").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(control_frame, text="Tiempo", variable=mode_var, value="Tiempo", command=self.update_measurements_display).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(control_frame, text="Frecuencia", variable=mode_var, value="Frecuencia", command=self.update_measurements_display).pack(side=tk.LEFT, padx=5)

    # --- Funciones de Procesamiento de Señales (DSP) ---

    def _design_butter_filter(self, cutoff_freq, fs, order, btype='low', rp=None, rs=None):
        """
        Diseña un filtro Butterworth.
        cutoff_freq: Frecuencia de corte (o banda para bandpass) en Hz.
        fs: Frecuencia de muestreo en Hz.
        order: Orden del filtro.
        btype: Tipo de filtro ('low', 'high', 'bandpass', 'bandstop').
        rp, rs: Parámetros para filtros Chebyshev/Elliptic (no usados en Butterworth aquí).
        """
        nyquist = 0.5 * fs
        normal_cutoff = np.array(cutoff_freq) / nyquist
        b, a = butter(order, normal_cutoff, btype=btype, analog=False)
        return b, a

    def _preemphasis_filter(self, signal, fs, tau):
        """
        Aplica un filtro de pre-énfasis a la señal de audio.
        signal: Señal de audio de entrada.
        fs: Frecuencia de muestreo.
        tau: Constante de tiempo (ej. 75e-6 para 75 us).
        """
        # Filtro de primer orden: H(s) = (1 + s*tau) / (1 + s*tau_dc)
        # Para pre-énfasis, se amplifican las altas frecuencias.
        # Implementación simple como un filtro IIR de primer orden
        # H(z) = (1 + a1*z^-1) / (1 + b1*z^-1)
        # Para un filtro RC de pre-énfasis, la constante de tiempo tau = R*C
        # La frecuencia de corte es fc = 1 / (2 * pi * tau)
        # En el dominio discreto, un filtro de pre-énfasis simple es y[n] = x[n] - alpha * x[n-1]
        # O un IIR: y[n] = x[n] + alpha * y[n-1]
        # Una implementación común es un filtro de primer orden:
        # b = [1, -np.exp(-1/(fs*tau))]
        # a = [1, -np.exp(-1/(fs*tau_dc))] (donde tau_dc es mucho mayor para DC)
        # Para simplificar y seguir la idea de GNU Radio (que es un filtro de paso alto de primer orden):
        alpha = tau * fs / (1 + tau * fs) # Coeficiente para filtro de primer orden
        b = [1, -0.95] # Numerador (aproximación, real sería 1 y 0)
        a = [1, -alpha] # Denominador (polo en -alpha)
        # Esto es una aproximación. Un pre-énfasis real es un filtro de paso alto con una ganancia de 1 a baja frecuencia
        # y una pendiente de +6dB/octava. Se implementa como un filtro IIR de primer orden.
        # H(s) = (1 + s/w0) / (1 + s/(w0*K)) donde w0 = 1/tau
        # Para un pre-énfasis simple de primer orden:
        b = [1, -np.exp(-1.0 / (fs * tau))]
        a = [1] # Sin polo en el denominador para un filtro FIR de pre-énfasis simple
        # Sin embargo, la implementación de GNU Radio para pre-énfasis es un filtro IIR de primer orden:
        # H(z) = (1 + a*z^-1) / (1 + b*z^-1)
        # donde a = -exp(-1/(fs*tau)) y b = -exp(-1/(fs*tau_dc))
        # Para simplificar, usaremos una aproximación común para pre-énfasis:
        # y[n] = x[n] + alpha * (x[n] - x[n-1]) donde alpha es un factor de ganancia.
        # O un filtro de paso alto de primer orden:
        RC = tau
        alpha = RC / (RC + 1.0/fs)
        b = [1, -1] # Numerador para derivador (aproximación de altas frecuencias)
        a = [1, -(1 - 1.0/(fs*tau))] # Denominador para paso alto
        return lfilter(b, a, signal)


    def _fm_modulate(self, audio_signal, fs_audio, fs_sdr, kf):
        """
        Realiza la modulación FM de banda angosta (NBFM).
        audio_signal: Señal de audio de entrada.
        fs_audio: Frecuencia de muestreo del audio.
        fs_sdr: Frecuencia de muestreo del SDR (para las muestras IQ de salida).
        kf: Constante de desviación de frecuencia (rad/s por unidad de amplitud de audio).
        """
        # Integrar la señal de audio para obtener la fase instantánea
        integrated_audio = kf * np.cumsum(audio_signal) / fs_audio

        # Resamplear la fase integrada a la frecuencia de muestreo del SDR
        num_samples_sdr = int(len(integrated_audio) * fs_sdr / fs_audio)
        # Interpolación lineal para resamplear la fase
        integrated_audio_resampled = np.interp(
            np.linspace(0, len(integrated_audio) - 1, num_samples_sdr),
            np.arange(len(integrated_audio)),
            integrated_audio
        )

        # Generar las muestras IQ moduladas
        # I = cos(fase_instantanea), Q = sin(fase_instantanea)
        # La señal compleja es I + jQ
        modulated_iq = np.exp(1j * integrated_audio_resampled)
        return modulated_iq.astype(np.complex64)

    def _fm_demodulate(self, iq_signal, fs_sdr, kf):
        """
        Realiza la demodulación FM de banda angosta (NBFM).
        iq_signal: Señal IQ recibida del SDR.
        fs_sdr: Frecuencia de muestreo del SDR.
        kf: Constante de desviación de frecuencia (rad/s por unidad de amplitud de audio).
        """
        # Calcular la fase instantánea
        # Diferencia de fase entre muestras consecutivas
        phase_diff = np.diff(np.unwrap(np.angle(iq_signal)))

        # Demodulación: la señal de audio es proporcional a la derivada de la fase
        demodulated_audio = phase_diff * fs_sdr / kf

        # Asegurarse de que la longitud de la señal demodulada sea consistente
        # np.diff reduce la longitud en 1, así que ajustamos
        if len(demodulated_audio) < len(iq_signal):
            demodulated_audio = np.pad(demodulated_audio, (0, len(iq_signal) - len(demodulated_audio)), 'edge')

        return demodulated_audio

    def _deemphasis_filter(self, signal, fs, tau):
        """
        Aplica un filtro de de-énfasis a la señal de audio.
        signal: Señal de audio de entrada.
        fs: Frecuencia de muestreo.
        tau: Constante de tiempo (ej. 75e-6 para 75 us).
        """
        # Filtro de de-énfasis es el inverso del pre-énfasis.
        # Es un filtro de paso bajo de primer orden.
        # H(s) = 1 / (1 + s*tau)
        # En el dominio discreto: y[n] = alpha * x[n] + (1 - alpha) * y[n-1]
        # donde alpha = 1 / (1 + 2*pi*fc*tau)
        # O más directamente:
        RC = tau
        alpha = 1.0 / (RC * fs + 1)
        b = [alpha]
        a = [1, -(1 - alpha)]
        return lfilter(b, a, signal)

    def _squelch_audio(self, audio_signal, threshold_db, fs):
        """
        Aplica un squelch (silenciador) a la señal de audio.
        audio_signal: Señal de audio de entrada.
        threshold_db: Umbral de squelch en dB.
        fs: Frecuencia de muestreo.
        """
        # Calcular la potencia de la señal en ventanas cortas
        window_size = int(0.01 * fs) # Ventana de 10 ms
        if window_size == 0: window_size = 1 # Asegurar que no sea cero
        num_windows = len(audio_signal) // window_size
        
        squelched_signal = np.copy(audio_signal)

        for i in range(num_windows):
            start = i * window_size
            end = start + window_size
            window = audio_signal[start:end]
            
            # Calcular la potencia RMS en dB
            if len(window) > 0:
                rms_power_db = 10 * np.log10(np.mean(window**2) + 1e-12) # Añadir un pequeño valor para evitar log(0)
            else:
                rms_power_db = -np.inf

            if rms_power_db < threshold_db:
                squelched_signal[start:end] = 0 # Silenciar la ventana
        
        return squelched_signal

    # --- Métodos de la Interfaz y Control del SDR ---

    def initialize_sdr(self):
        """Intenta inicializar el dispositivo LimeSDR."""
        global LIME_SDR_AVAILABLE # Necesario para modificar la variable global
        if LIME_SDR_AVAILABLE:
            try:
                # Encontrar el primer dispositivo LimeSDR
                self.sdr = pylimesdr.find(index=0)
                if self.sdr:
                    print("LimeSDR encontrado e inicializado.")
                    # Configuración inicial de la tasa de muestreo (ej. 5 MSPS)
                    self.sdr.sample_rate = self.sdr_sample_rate
                    # Calibrar RX y TX (puede tomar unos segundos)
                    self.sdr.calibrar(1, 1) # Calibrar RX (1) y TX (1)
                    self.apply_sdr_settings() # Aplicar configuración inicial de UI al SDR
                    self.start_rx_stream() # Iniciar la recepción al inicio
                else:
                    print("No se encontró ningún dispositivo LimeSDR. Funcionando en modo simulación básica.")
                    LIME_SDR_AVAILABLE = False # Deshabilitar si no se encuentra
            except Exception as e:
                print(f"Error al inicializar LimeSDR: {e}. Asegúrate de que los drivers de SoapySDR estén instalados y el dispositivo conectado. Funcionando en modo simulación básica.")
                self.sdr = None
                LIME_SDR_AVAILABLE = False
        else:
            print("pylimesdr no está disponible. Funcionando en modo simulación básica.")

    def apply_sdr_settings(self, *args):
        """Aplica la configuración de TX/RX (frecuencia, ganancia) al LimeSDR."""
        if self.sdr and LIME_SDR_AVAILABLE:
            try:
                tx_freq_hz = self.tx_freq.get() * 1e6
                rx_freq_hz = self.rx_freq.get() * 1e6

                # Configurar TX
                self.sdr.tx_freq = tx_freq_hz
                self.sdr.tx_gain = self.tx_gain.get()

                # Configurar RX
                self.sdr.rx_freq = rx_freq_hz
                self.sdr.rx_gain = self.rx_gain.get()

                print(f"Configuración SDR aplicada: TX Freq={tx_freq_hz/1e6} MHz, TX Gain={self.tx_gain.get()} dB, "
                      f"RX Freq={rx_freq_hz/1e6} MHz, RX Gain={self.rx_gain.get()} dB")
            except Exception as e:
                print(f"Error al aplicar configuración SDR: {e}")
        self.update_measurements_display() # Actualizar la visualización incluso si es simulación

    def start_rx_stream(self):
        """Inicia el hilo de recepción del LimeSDR."""
        if self.sdr and LIME_SDR_AVAILABLE and not self.rx_stream_active:
            self.stop_threads.clear() # Limpiar el evento de parada
            self.rx_thread = threading.Thread(target=self._rx_loop)
            self.rx_thread.daemon = True # Permite que el hilo termine con la aplicación principal
            self.rx_thread.start()
            self.rx_stream_active = True
            print("Hilo de recepción SDR iniciado.")

    def stop_rx_stream(self):
        """Detiene el hilo de recepción del LimeSDR."""
        if self.rx_stream_active:
            self.stop_threads.set() # Establecer el evento de parada
            if self.rx_thread and self.rx_thread.is_alive():
                self.rx_thread.join(timeout=1) # Esperar a que el hilo termine
            self.rx_stream_active = False
            print("Hilo de recepción SDR detenido.")

    def _rx_loop(self):
        """Bucle de recepción de muestras del LimeSDR y procesamiento DSP."""
        stream_args = pylimesdr.StreamArgs()
        stream_args.channels = [0] # Canal 0 para RX
        stream_args.buffersize = 1024 * 16 # Tamaño del buffer para recibir
        stream_args.format = pylimesdr.LMS_FMT_F32 # Formato de flotante de 32 bits (IQ complejo)

        # Diseño del filtro pasa bajas para la señal IQ antes de demodular (ancho de banda de 10 KHz)
        b_lp_iq, a_lp_iq = self._design_butter_filter(10000, self.sdr_sample_rate, 5, btype='low')

        try:
            self.sdr.start_stream(stream_args, pylimesdr.LMS_CH_RX)
            print("Stream RX de LimeSDR iniciado.")
            while not self.stop_threads.is_set():
                samples_iq = self.sdr.recv_stream(stream_args, stream_args.buffersize, timeout_ms=100)
                if samples_iq is not None and len(samples_iq) > 0:
                    raw_iq_samples = samples_iq[0] # Muestras IQ crudas

                    # --- Procesamiento DSP de Recepción ---
                    # 1. Filtrado pasa bajas de las muestras IQ
                    filtered_iq = lfilter(b_lp_iq, a_lp_iq, raw_iq_samples)

                    # 2. Demodulación FM
                    demodulated_audio = self._fm_demodulate(filtered_iq, self.sdr_sample_rate, self.kf)

                    # 3. De-énfasis
                    deemphasized_audio = self._deemphasis_filter(demodulated_audio, self.sdr_sample_rate, self.preemphasis_tau)
                    
                    # 4. Resamplear audio a la frecuencia de muestreo de audio deseada
                    num_audio_samples = int(len(deemphasized_audio) * self.audio_sample_rate / self.sdr_sample_rate)
                    # Usar np.interp para resamplear
                    resampled_audio = np.interp(
                        np.linspace(0, len(deemphasized_audio) - 1, num_audio_samples),
                        np.arange(len(deemphasized_audio)),
                        deemphasized_audio
                    )

                    # 5. Aplicar Squelch
                    final_audio = self._squelch_audio(resampled_audio, self.squelch_threshold_db, self.audio_sample_rate)
                    
                    # Almacenar las muestras para la visualización
                    self.current_rx_samples_iq = raw_iq_samples # Guardar IQ crudas también para "señal demodulada"
                    self.current_rx_samples_audio = final_audio # Guardar audio procesado

                    # Actualizar la GUI desde el hilo principal de Tkinter
                    self.root.after(10, self.update_measurements_display)
                else:
                    time.sleep(0.01) # Pequeña pausa para no saturar la CPU si no hay muestras
        except Exception as e:
            print(f"Error en el bucle de recepción SDR: {e}")
        finally:
            if self.sdr and self.sdr.is_stream_active(pylimesdr.LMS_CH_RX):
                try:
                    self.sdr.stop_stream(pylimesdr.LMS_CH_RX)
                    print("Stream RX de LimeSDR detenido.")
                except Exception as e:
                    print(f"Error al detener stream RX: {e}")

    def start_tx_stream(self, signal_data_iq):
        """Inicia el hilo de transmisión del LimeSDR con la señal IQ proporcionada."""
        if self.sdr and LIME_SDR_AVAILABLE and not self.tx_stream_active:
            self.stop_threads.clear() # Limpiar el evento de parada para el hilo TX
            self.tx_thread = threading.Thread(target=self._tx_loop, args=(signal_data_iq,))
            self.tx_thread.daemon = True # Permite que el hilo termine con la aplicación principal
            self.tx_thread.start()
            self.tx_stream_active = True
            print("Hilo de transmisión SDR iniciado.")

    def stop_tx_stream(self):
        """Detiene el hilo de transmisión del LimeSDR."""
        if self.tx_stream_active:
            self.stop_threads.set() # Establecer el evento de parada
            if self.tx_thread and self.tx_thread.is_alive():
                self.tx_thread.join(timeout=1) # Esperar a que el hilo termine
            self.tx_stream_active = False
            print("Hilo de transmisión SDR detenido.")

    def _tx_loop(self, signal_data_iq):
        """Bucle de transmisión de muestras IQ al LimeSDR."""
        stream_args = pylimesdr.StreamArgs()
        stream_args.channels = [0] # Canal 0 para TX
        stream_args.buffersize = 1024 * 16 # Tamaño del buffer para enviar
        stream_args.format = pylimesdr.LMS_FMT_F32 # Formato de flotante de 32 bits (IQ complejo)

        try:
            self.sdr.start_stream(stream_args, pylimesdr.LMS_CH_TX)
            print("Stream TX de LimeSDR iniciado.")
            # Repetir la señal indefinidamente
            while not self.stop_threads.is_set():
                self.sdr.send_stream(stream_args, signal_data_iq, len(signal_data_iq), timeout_ms=100)
                time.sleep(0.01) # Pequeña pausa para no saturar la CPU
        except Exception as e:
            print(f"Error en el bucle de transmisión SDR: {e}")
        finally:
            if self.sdr and self.sdr.is_stream_active(pylimesdr.LMS_CH_TX):
                try:
                    self.sdr.stop_stream(pylimesdr.LMS_CH_TX)
                    print("Stream TX de LimeSDR detenido.")
                except Exception as e:
                    print(f"Error al detener stream TX: {e}")

    def toggle_ptt(self):
        """Alterna el estado del botón Push to Talk y controla la transmisión."""
        if self.operation_mode.get() != "Push to Talk":
            return # Solo el modo Push to Talk puede usar este botón

        if self.ptt_status.get() == "Desactivado":
            self.ptt_status.set("Activado")
            self.ptt_button.config(text="Soltar PTT")
            # Generar señal de audio para TX
            test_freq = float(self.test_freq_var.get().split(' ')[0]) # Frecuencia del tono de prueba
            t_audio = np.linspace(0, 1, self.audio_sample_rate, endpoint=False) # 1 segundo de audio
            audio_signal = np.sin(2 * np.pi * test_freq * t_audio) * (self.mic_gain.get() / 10.0)

            # --- Procesamiento DSP de Transmisión ---
            # 1. Pre-énfasis
            preemphasized_audio = self._preemphasis_filter(audio_signal, self.audio_sample_rate, self.preemphasis_tau)

            # 2. Modulación FM (genera muestras IQ)
            modulated_iq = self._fm_modulate(preemphasized_audio, self.audio_sample_rate, self.sdr_sample_rate, self.kf)
            
            self.start_tx_stream(modulated_iq)
        else:
            self.ptt_status.set("Desactivado")
            self.ptt_button.config(text="Push to Talk")
            self.stop_tx_stream()
        self.update_measurements_display() # Actualizar la visualización

    def start_tx_if_test(self, *args):
        """Inicia la transmisión si el modo es 'Test' y se cambian parámetros relevantes."""
        if self.operation_mode.get() == "Test":
            self.stop_tx_stream() # Detener cualquier TX anterior para aplicar nueva configuración
            if self.sdr and LIME_SDR_AVAILABLE:
                test_freq = float(self.test_freq_var.get().split(' ')[0])
                t_audio = np.linspace(0, 1, self.audio_sample_rate, endpoint=False)
                audio_signal = np.sin(2 * np.pi * test_freq * t_audio) * (self.mic_gain.get() / 10.0)

                # --- Procesamiento DSP de Transmisión ---
                # 1. Pre-énfasis
                preemphasized_audio = self._preemphasis_filter(audio_signal, self.audio_sample_rate, self.preemphasis_tau)

                # 2. Modulación FM (genera muestras IQ)
                modulated_iq = self._fm_modulate(preemphasized_audio, self.audio_sample_rate, self.sdr_sample_rate, self.kf)
                
                self.start_tx_stream(modulated_iq)
            else:
                print("LimeSDR no disponible para transmitir en modo Test.")
        else:
            self.stop_tx_stream() # Asegurarse de detener TX si no estamos en modo Test

    def update_interface(self, *args):
        """Actualiza la visibilidad y el estado de los controles según el modo de operación."""
        mode = self.operation_mode.get()

        if mode == "Test":
            self.test_freq_menu.config(state="normal")
            self.start_tx_if_test() # Iniciar TX inmediatamente en modo Test
        else:
            self.test_freq_menu.config(state="disabled")
            self.stop_tx_stream() # Detener TX si salimos del modo Test

        if mode == "Push to Talk":
            self.ptt_button.config(state="normal")
        else:
            self.ptt_button.config(state="disabled")
            self.ptt_status.set("Desactivado") # Asegurarse de que PTT esté desactivado
            self.ptt_button.config(text="Push to Talk")
            self.stop_tx_stream() # Asegurarse de que TX esté detenido si no es PTT

        self.update_measurements_display()

    def on_tab_change(self, event):
        """Se llama cuando la pestaña del Notebook cambia."""
        # Re-empaquetar el canvas en la nueva pestaña
        selected_tab = self.notebook.tab(self.notebook.select(), "text")
        if selected_tab == "SEÑAL DEMODULADA":
            self.canvas_widget.pack_forget()
            self.canvas_widget.pack(fill=tk.BOTH, expand=True, in_=self.tab_demodulated_signal)
        elif selected_tab == "TONO FILTRADO":
            self.canvas_widget.pack_forget()
            self.canvas_widget.pack(fill=tk.BOTH, expand=True, in_=self.tab_filtered_tone)
        elif selected_tab == "PISO DE RUIDO":
            self.canvas_widget.pack_forget()
            self.canvas_widget.pack(fill=tk.BOTH, expand=True, in_=self.tab_noise_floor)

        self.update_measurements_display() # Actualizar el gráfico para la nueva pestaña

    def update_measurements_display(self, *args):
        """Actualiza los valores de SNR, SINAD y el espectro/tiempo en la GUI."""
        # Las mediciones ahora se basan en self.current_rx_samples_audio (audio demodulado)
        if self.current_rx_samples_audio is not None and len(self.current_rx_samples_audio) > 0:
            # Calcular la potencia de la señal de audio demodulada
            signal_power_audio = np.mean(self.current_rx_samples_audio**2)

            # Para SNR/SINAD realistas, necesitaríamos separar la señal del ruido/distorsión.
            # Esto es complejo sin una señal de referencia conocida o técnicas avanzadas.
            # Por ahora, haremos una estimación más "realista" basada en la potencia del audio.
            # Si hay una señal fuerte, el ruido relativo es menor.
            # Asumiremos que el "ruido" es lo que queda después de un filtro de tono si estamos en modo test
            # o un nivel base si no hay señal.

            noise_power_audio_simulated = 1e-6 # Nivel de ruido base muy bajo
            if self.operation_mode.get() == "Test":
                test_freq = float(self.test_freq_var.get().split(' ')[0])
                # Intentar aislar el tono y el ruido para una mejor estimación
                b_bp_tone, a_bp_tone = self._design_butter_filter(
                    [test_freq - 50, test_freq + 50], self.audio_sample_rate, 4, btype='bandpass'
                )
                tone_component = lfilter(b_bp_tone, a_bp_tone, self.current_rx_samples_audio)
                signal_power_audio = np.mean(tone_component**2)
                
                noise_and_distortion_component = self.current_rx_samples_audio - tone_component
                noise_power_audio_simulated = np.mean(noise_and_distortion_component**2) + 1e-12
            else:
                # Para modos no-test, el ruido es más general
                noise_power_audio_simulated = max(1e-9, signal_power_audio * (1 - (self.rx_gain.get() / 100.0)) * 0.5)
                if self.operation_mode.get() == "Push to Talk" and self.ptt_status.get() == "Desactivado":
                    noise_power_audio_simulated *= 10 # Mucho más ruido si PTT no está activo

            # SNR (Signal-to-Noise Ratio) en dB
            snr_val_db = 10 * np.log10(signal_power_audio / noise_power_audio_simulated) if noise_power_audio_simulated > 0 else 999
            self.snr_val.set(f"SNR: {snr_val_db:.2f} dB")
            self.snr_signal.set(f"Señal: {signal_power_audio:.4f} mW")
            self.snr_noise_distortion.set(f"Ruido + Distorsión: {noise_power_audio_simulated:.4f} mW")

            # SINAD (Signal-to-Noise and Distortion) en dB
            sinad_val_db = 10 * np.log10(signal_power_audio / noise_power_audio_simulated) if noise_power_audio_simulated > 0 else 999
            self.sinad_val.set(f"SINAD: {sinad_val_db:.2f} dB")
            self.sinad_signal_noise_distortion.set(f"Señal + Ruido + Distorsión: {signal_power_audio + noise_power_audio_simulated:.4f} mW")
            self.sinad_noise_distortion.set(f"Ruido + Distorsión: {noise_power_audio_simulated:.4f} mW")

            # --- Visualización del Espectro/Tiempo ---
            self.ax.clear()
            
            current_tab_text = self.notebook.tab(self.notebook.select(), "text")
            
            plot_data = None
            fs_plot = None
            plot_title = ""
            display_mode = ""

            if current_tab_text == "SEÑAL DEMODULADA":
                plot_data = self.current_rx_samples_iq
                fs_plot = self.sdr_sample_rate
                plot_title = "Señal IQ Cruda (Hardware Real)"
                display_mode = self.demod_signal_display_mode.get()
            elif current_tab_text == "TONO FILTRADO":
                plot_data = self.current_rx_samples_audio
                fs_plot = self.audio_sample_rate
                plot_title = "Tono Filtrado (Simulado)"
                display_mode = self.filtered_tone_display_mode.get()
                if self.operation_mode.get() == "Test":
                    test_freq = float(self.test_freq_var.get().split(' ')[0])
                    b_bp_tone, a_bp_tone = self._design_butter_filter(
                        [test_freq - 100, test_freq + 100], self.audio_sample_rate, 4, btype='bandpass'
                    )
                    plot_data = lfilter(b_bp_tone, a_bp_tone, self.current_rx_samples_audio)
            elif current_tab_text == "PISO DE RUIDO":
                plot_data = self.current_rx_samples_audio
                fs_plot = self.audio_sample_rate
                plot_title = "Piso de Ruido (Hardware Real)"
                display_mode = self.noise_floor_display_mode.get()

            if plot_data is not None and len(plot_data) > 0:
                if display_mode == "Frecuencia":
                    N = len(plot_data)
                    yf = np.fft.fft(plot_data)
                    xf = np.fft.fftfreq(N, 1 / fs_plot)

                    magnitudes_db = 20 * np.log10(np.abs(yf[:N//2]) + 1e-9)
                    frequencies_khz = xf[:N//2] / 1000

                    self.ax.plot(frequencies_khz, magnitudes_db)
                    self.ax.set_xlabel("Frecuencia (kHz)")
                    self.ax.set_ylabel("Ganancia Relativa (dB)")
                    self.ax.set_title(f"Espectro de {plot_title}")
                    max_freq_khz = (fs_plot / 2) / 1000
                    self.ax.set_xlim(-max_freq_khz, max_freq_khz)
                    self.ax.set_ylim(-140, 0)
                else: # Dominio del Tiempo
                    # Limitar el número de puntos para evitar gráficos demasiado densos
                    max_points = 2000
                    if len(plot_data) > max_points:
                        step = len(plot_data) // max_points
                        plot_data_time = plot_data[::step]
                        t_plot = np.linspace(0, len(plot_data_time) / fs_plot, len(plot_data_time), endpoint=False)
                    else:
                        plot_data_time = plot_data
                        t_plot = np.linspace(0, len(plot_data_time) / fs_plot, len(plot_data_time), endpoint=False)

                    # Para IQ, podemos mostrar la magnitud o la parte real/imaginaria
                    if current_tab_text == "SEÑAL DEMODULADA":
                        self.ax.plot(t_plot, np.abs(plot_data_time), label='Magnitud IQ')
                        # self.ax.plot(t_plot, np.real(plot_data_time), label='Parte Real IQ')
                        # self.ax.plot(t_plot, np.imag(plot_data_time), label='Parte Imaginaria IQ')
                        self.ax.set_ylabel("Amplitud")
                    else:
                        self.ax.plot(t_plot, plot_data_time)
                        self.ax.set_ylabel("Amplitud")

                    self.ax.set_xlabel("Tiempo (s)")
                    self.ax.set_title(f"Forma de Onda de {plot_title}")
                    self.ax.set_xlim(0, t_plot[-1] if len(t_plot) > 0 else 1)
                    self.ax.grid(True)
                    self.ax.legend() if current_tab_text == "SEÑAL DEMODULADA" else None # Mostrar leyenda solo si hay múltiples líneas

            self.canvas.draw()
        else:
            # Si no hay muestras del SDR, mostrar un mensaje y resetear mediciones
            self.ax.clear()
            self.ax.text(0.5, 0.5, "No hay datos del SDR (¿LimeSDR conectado y pylimesdr instalado?)", horizontalalignment='center', verticalalignment='center', transform=self.ax.transAxes, fontsize=12)
            self.ax.set_title("Espectro/Tiempo de Señal (Hardware Real)")
            self.ax.set_xlabel("Frecuencia (kHz) / Tiempo (s)")
            self.ax.set_ylabel("Ganancia Relativa (dB) / Amplitud")
            self.ax.set_xlim(-6, 6)
            self.ax.set_ylim(-140, 0)
            self.ax.grid(True)
            self.canvas.draw()

            # Resetear las mediciones a N/A
            self.snr_val.set("SNR: N/A")
            self.snr_signal.set("Señal: N/A")
            self.snr_noise_distortion.set("Ruido + Distorsión: N/A")
            self.sinad_val.set("SINAD: N/A")
            self.sinad_signal_noise_distortion.set("Señal + Ruido + Distorsión: N/A")
            self.sinad_noise_distortion.set("Ruido + Distorsión: N/A")


    def on_closing(self):
        """Maneja el cierre de la aplicación, deteniendo streams y cerrando el SDR."""
        print("Cerrando aplicación...")
        self.stop_threads.set() # Señal para detener todos los hilos
        # Esperar a que los hilos terminen
        if self.rx_thread and self.rx_thread.is_alive():
            self.rx_thread.join(timeout=2)
        if self.tx_thread and self.tx_thread.is_alive():
            self.tx_thread.join(timeout=2)

        if self.sdr and LIME_SDR_AVAILABLE:
            try:
                self.sdr.close() # Cerrar el dispositivo LimeSDR
                print("LimeSDR cerrado correctamente.")
            except Exception as e:
                print(f"Error al cerrar LimeSDR: {e}")
        self.root.destroy() # Destruir la ventana de Tkinter

if __name__ == "__main__":
    root = tk.Tk()
    app = NBFMInterface(root)
    root.mainloop()
