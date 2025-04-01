import tkinter as tk
from tkinter import scrolledtext
import sys
from io import StringIO
import pyttsx3
import speech_recognition as sr
from lex import lexer
from yacc import parser
from semantic import SemanticAnalyzer
from interpreter import Interpreter

class TicketLangIDE:
    def __init__(self, root):
        self.root = root
        root.title("Ticket Booking Language IDE")

        self.code_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Courier New", 12))
        self.code_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.run_button = tk.Button(root, text="Run", command=self.run_code)
        self.run_button.pack(pady=5)
        
        self.tts_toggle_button = tk.Button(root, text="Toggle TTS", command=self.toggle_tts)
        self.tts_toggle_button.pack(pady=5)
        
        self.stt_button = tk.Button(root, text="Speech to Text", command=self.speech_to_text)
        self.stt_button.pack(pady=5)

        self.output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Courier New", 12), state=tk.DISABLED, height=10)
        self.output_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        self.lexer = lexer
        self.parser = parser
        self.semantic_analyzer = SemanticAnalyzer()
        self.interpreter = Interpreter(self.semantic_analyzer)
        
        self.tts_engine = pyttsx3.init()
        self.tts_enabled = True
        self.recognizer = sr.Recognizer()

    def run_code(self):
        code = self.code_text.get("1.0", tk.END)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)

        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        syntax_error = False
        semantic_error = False

        try:
            result = self.parser.parse(code, lexer=self.lexer)
            if result:
                semantic_errors = self.semantic_analyzer.analyze(result)
                if semantic_errors:
                    semantic_error = True
                    output_message = "Semantic Analysis Errors:\n" + "\n".join([f"  Semantic Error: {error}" for error in semantic_errors])
                    self.output_text.insert(tk.END, output_message + "\n")
                else:
                    self.interpreter.interpret(result)
            else:
                syntax_error = True
                self.output_text.insert(tk.END, "Syntax Error.\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"An unexpected error occurred:\n{e}\n")
        finally:
            sys.stdout = old_stdout
            output_value = captured_output.getvalue()
            if output_value:
                self.output_text.insert(tk.END, output_value)
                if self.tts_enabled:
                    self.speak_output(output_value)

        if syntax_error or semantic_error:
            self.root.title("Ticket Booking Language IDE - Errors Found")
        else:
            self.root.title("Ticket Booking Language IDE - Run Successful")

        self.output_text.config(state=tk.DISABLED)

    def speak_output(self, text):
        if self.tts_enabled:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
    
    def toggle_tts(self):
        self.tts_enabled = not self.tts_enabled
        status = "ON" if self.tts_enabled else "OFF"
        self.tts_toggle_button.config(text=f"TTS: {status}")
    
    def speech_to_text(self):
        with sr.Microphone() as source:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, "Listening for input...\n")
            self.output_text.config(state=tk.DISABLED)
            try:
                audio = self.recognizer.listen(source)
                text = self.recognizer.recognize_google(audio)
                self.code_text.insert(tk.END, text + "\n")
            except sr.UnknownValueError:
                self.output_text.config(state=tk.NORMAL)
                self.output_text.insert(tk.END, "Could not understand audio\n")
                self.output_text.config(state=tk.DISABLED)
            except sr.RequestError:
                self.output_text.config(state=tk.NORMAL)
                self.output_text.insert(tk.END, "Speech recognition service unavailable\n")
                self.output_text.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    ide = TicketLangIDE(root)
    root.mainloop()

if __name__ == "__main__":
    main()
import tkinter as tk
from tkinter import scrolledtext
import sys
from io import StringIO
import pyttsx3
import speech_recognition as sr 
from lex import lexer
from yacc import parser
from semantic import SemanticAnalyzer
from interpreter import Interpreter

class TicketLangIDE:
    def __init__(self, root):
        self.root = root
        root.title("Ticket Booking Language IDE")

        self.code_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Courier New", 12))
        self.code_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.run_button = tk.Button(root, text="Run", command=self.run_code)
        self.run_button.pack(pady=5)
        
        self.tts_toggle_button = tk.Button(root, text="Toggle TTS", command=self.toggle_tts)
        self.tts_toggle_button.pack(pady=5)
        
        self.stt_button = tk.Button(root, text="Speech to Text", command=self.speech_to_text)
        self.stt_button.pack(pady=5)

        self.output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Courier New", 12), state=tk.DISABLED, height=10)
        self.output_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        self.lexer = lexer
        self.parser = parser
        self.semantic_analyzer = SemanticAnalyzer()
        self.interpreter = Interpreter(self.semantic_analyzer)
        
        self.tts_engine = pyttsx3.init()
        self.tts_enabled = True
        self.recognizer = sr.Recognizer()

    def run_code(self):
        code = self.code_text.get("1.0", tk.END)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)

        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        syntax_error = False
        semantic_error = False

        try:
            result = self.parser.parse(code, lexer=self.lexer)
            if result:
                semantic_errors = self.semantic_analyzer.analyze(result)
                if semantic_errors:
                    semantic_error = True
                    output_message = "Semantic Analysis Errors:\n" + "\n".join([f"  Semantic Error: {error}" for error in semantic_errors])
                    self.output_text.insert(tk.END, output_message + "\n")
                else:
                    self.interpreter.interpret(result)
            else:
                syntax_error = True
                self.output_text.insert(tk.END, "Syntax Error.\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"An unexpected error occurred:\n{e}\n")
        finally:
            sys.stdout = old_stdout
            output_value = captured_output.getvalue()
            if output_value:
                self.output_text.insert(tk.END, output_value)
                if self.tts_enabled:
                    self.speak_output(output_value)

        if syntax_error or semantic_error:
            self.root.title("Ticket Booking Language IDE - Errors Found")
        else:
            self.root.title("Ticket Booking Language IDE - Run Successful")

        self.output_text.config(state=tk.DISABLED)

    def speak_output(self, text):
        if self.tts_enabled:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
    
    def toggle_tts(self):
        self.tts_enabled = not self.tts_enabled
        status = "ON" if self.tts_enabled else "OFF"
        self.tts_toggle_button.config(text=f"TTS: {status}")
    
    def speech_to_text(self):
        with sr.Microphone() as source:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, "Listening for input...\n")
            self.output_text.config(state=tk.DISABLED)
            try:
                audio = self.recognizer.listen(source)
                text = self.recognizer.recognize_google(audio)
                self.code_text.insert(tk.END, text + "\n")
            except sr.UnknownValueError:
                self.output_text.config(state=tk.NORMAL)
                self.output_text.insert(tk.END, "Could not understand audio\n")
                self.output_text.config(state=tk.DISABLED)
            except sr.RequestError:
                self.output_text.config(state=tk.NORMAL)
                self.output_text.insert(tk.END, "Speech recognition service unavailable\n")
                self.output_text.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    ide = TicketLangIDE(root)
    root.mainloop()

if __name__ == "__main__":
    main()
