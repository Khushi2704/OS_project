import os
import time
import threading
import tkinter as tk
from tkinter import scrolledtext, ttk
from concurrent.futures import ThreadPoolExecutor

# OS Configuration
OS_CONFIG = {
    "name": "PyFastOS",
    "version": "2.1",
    "services": ["Filesystem", "Networking", "User Interface", "Applications", "Security", "Background Tasks"]
}

class FastBootOS:
    """Simulates a fast boot OS with enhanced parallel processing."""
    
    def __init__(self, config=None):
        self.config = config or OS_CONFIG
        self.status = "idle"
        self.services = {service: "stopped" for service in self.config["services"]}
        self.start_time = None
        self.command_history = []
        self.tasks = {}  # Track active tasks
        self.boot_time = 0

    def boot(self, log_callback):
        """Boots the OS by starting services in parallel."""
        self.status = "booting"
        start_time = time.time()
        log_callback("Booting PyFastOS...")
        
        with ThreadPoolExecutor(max_workers=len(self.services)) as executor:
            for service in self.services.keys():
                executor.submit(self._start_service, service, log_callback)
        
        self.status = "running"
        self.boot_time = time.time() - start_time
        log_callback(f"OS Boot Complete in {self.boot_time:.2f} seconds.")
    
    def shutdown(self, log_callback):
        """Shuts down all services in parallel."""
        self.status = "shutting down"
        log_callback("Shutting down PyFastOS...")
        
        with ThreadPoolExecutor(max_workers=len(self.services)) as executor:
            for service in self.services.keys():
                executor.submit(self._stop_service, service, log_callback)
        
        self.status = "stopped"
        log_callback("OS Shutdown complete.")
    
    def _start_service(self, service, log_callback):
        """Simulates starting a service."""
        time.sleep(1)
        self.services[service] = "running"
        log_callback(f"{service} started.")
    
    def _stop_service(self, service, log_callback):
        """Simulates stopping a service."""
        time.sleep(0.5)
        self.services[service] = "stopped"
        log_callback(f"{service} stopped.")
    
    def run_command(self, command):
        """Executes a basic command and returns output."""
        if command.lower() == "status":
            return f"OS Status: {self.status}"
        elif command.lower() == "services":
            return "\n".join([f"{svc}: {sts}" for svc, sts in self.services.items()])
        else:
            return "Unknown command. Try 'status' or 'services'."

class OS_GUI:
    """Graphical interface for PyFastOS with enhanced styling."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("PyFastOS - v2.1")
        self.root.geometry("600x550")
        self.root.config(bg="#2B3A42")  # Coolwarm base background

        self.os_instance = FastBootOS(OS_CONFIG)

        # UI Elements
        self.start_button = tk.Button(root, text="Boot OS", command=self.start_os, bg="#D7263D", fg="white", font=("Arial", 12, "bold"))
        self.start_button.pack(pady=5)

        self.shutdown_button = tk.Button(root, text="Shutdown OS", state=tk.DISABLED, command=self.shutdown_os, bg="#0081A7", fg="white", font=("Arial", 12, "bold"))
        self.shutdown_button.pack(pady=5)

        self.log_display = scrolledtext.ScrolledText(root, height=15, width=70, state='disabled', bg="#1B263B", fg="#F4D35E", font=("Courier", 10))
        self.log_display.pack(pady=5)

        self.command_entry = tk.Entry(root, width=40, font=("Arial", 12))
        self.command_entry.pack(pady=5)
        self.command_entry.bind("<Return>", self.execute_command)

        self.execute_button = tk.Button(root, text="Execute Command", command=self.execute_command, bg="#F4A261", fg="white", font=("Arial", 12, "bold"))
        self.execute_button.pack(pady=5)

        self.status_label = tk.Label(root, text="OS Status: Idle", fg="#E63946", bg="#2B3A42", font=("Arial", 12, "bold"))
        self.status_label.pack(pady=5)

        self.boot_time_label = tk.Label(root, text="Boot Time: N/A", fg="#F4D35E", bg="#2B3A42", font=("Arial", 12, "bold"))
        self.boot_time_label.pack(pady=5)

        self.service_frame = tk.Frame(root, bg="#2B3A42")
        self.service_frame.pack()
        self.service_labels = {}
        for service in OS_CONFIG["services"]:
            label = tk.Label(self.service_frame, text=f"{service}: Stopped", fg="#E63946", bg="#2B3A42", font=("Arial", 10, "bold"))
            label.pack()
            self.service_labels[service] = label

    def log_message(self, message):
        """Logs messages in the GUI."""
        self.log_display.config(state='normal')
        if message == "clear_log":
            self.log_display.delete(1.0, tk.END)  
        else:
            self.log_display.insert(tk.END, message + "\n")
        self.log_display.config(state='disabled')
        self.log_display.yview(tk.END)
    
    def update_service_status(self):
        """Updates service labels in the GUI."""
        for service, status in self.os_instance.services.items():
            color = "#2EC4B6" if status == "running" else "#E63946"
            self.service_labels[service].config(text=f"{service}: {status.capitalize()}", fg=color)

    def start_os(self):
        """Starts the OS boot process."""
        self.start_button.config(state=tk.DISABLED)
        threading.Thread(target=self.boot_process, daemon=True).start()
    
    def boot_process(self):
        """Handles the OS boot process."""
        self.os_instance.boot(self.log_message)
        self.shutdown_button.config(state=tk.NORMAL)
        self.update_service_status()
        self.boot_time_label.config(text=f"Boot Time: {self.os_instance.boot_time:.2f} sec", fg="#F4D35E")
    
    def shutdown_os(self):
        """Starts the OS shutdown process."""
        self.shutdown_button.config(state=tk.DISABLED)
        threading.Thread(target=self.shutdown_process, daemon=True).start()
    
    def shutdown_process(self):
        """Handles the OS shutdown process."""
        self.os_instance.shutdown(self.log_message)
        self.start_button.config(state=tk.NORMAL)
        self.update_service_status()
        self.boot_time_label.config(text="Boot Time: N/A", fg="#F4D35E")
    
    def execute_command(self, event=None):
        """Executes a command in the OS."""
        command = self.command_entry.get()
        if command:
            self.log_message(f"> {command}")
            result = self.os_instance.run_command(command)
            self.log_message(result)
            self.command_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = OS_GUI(root)
    root.mainloop()
