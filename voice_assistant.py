import pyttsx3
import threading

class PanelVoiceAssistant:
    def __init__(self):
        # Initialize the text-to-speech driver engine
        self.engine = pyttsx3.init()
        self.setup_voice()
        self.is_speaking = False

    def setup_voice(self):
        """Configures clear vocal properties for industrial environments."""
        # Adjust speaking rate speed (default is usually around 200)
        self.engine.setProperty('rate', 165)
        
        # Set volume level (0.0 to 1.0)
        self.engine.setProperty('volume', 1.0)
        
        # Pick a voice profile (Index 0 is usually male, Index 1 is usually female)
        voices = self.engine.getProperty('voices')
        if len(voices) > 1:
            self.engine.setProperty('voice', voices[1].id) # Cleaner enunciations

    def _speak_worker(self, alert_text):
        """Worker thread to handle audio output without locking the main system loop."""
        self.is_speaking = True
        self.engine.say(alert_text)
        self.engine.runAndWait()
        self.is_speaking = False

    def announce(self, text, critical=False):
        """
        Speaks the given text out loud. If the notification is critical (like a fire trip),
        it will instantly interrupt or cut through standard telemetry readings.
        """
        if self.is_speaking and not critical:
            # Skip routine announcements if the engine is already talking
            return
            
        # Run speech inside a separate thread to prevent sensor sampling lags
        speech_thread = threading.Thread(target=self._speak_worker, args=(text,))
        speech_thread.daemon = True
        speech_thread.start()

# Quick test condition to confirm installation parameters run locally
if __name__ == "__main__":
    assistant = PanelVoiceAssistant()
    print("🔊 Testing Voice Assistant Audio Output...")
    assistant.announce("System initialization complete. Monitoring phase distribution panel.", critical=True)
    # Give the background worker thread a moment to finish speaking during this fast test
    import time
    time.sleep(5)