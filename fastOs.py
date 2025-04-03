import os
import time
import threading
import tkinter as tk
from tkinter import scrolledtext
from concurrent.futures import ThreadPoolExecutor

# OS Configuration
OS_CONFIG = {
    "name": "PyFastOS",
    "version": "1.1",
    "services": ["Filesystem", "Networking", "User Interface", "Applications", "Security", "Background Tasks"]
}

class FastBootOS:
    """Simulates a fast boot OS with parallel processing for service management."""

    def __init__(self, config=None):
        self.config = config or OS_CONFIG
        self.status = "idle"
        self.services = {service: "stopped" for service in self.config["services"]}

    def boot(self, log_callback):
        """Boots the OS by starting services in parallel."""
        self.status = "booting"
        start_time = time.time()

        with ThreadPoolExecutor(max_workers=len(self.services)) as executor:
            for service in self.services.keys():
                executor.submit(self._start_service, service, log_callback)

        self.status = "running"
        boot_time = time.time() - start_time
        log_callback(f"OS Booted in {boot_time:.2f} seconds")

    def shutdown(self, log_callback):
        """Shuts down all services in parallel."""
        self.status = "shutting down"
        log_callback("Shutting down services...")

        with ThreadPoolExecutor(max_workers=len(self.services)) as executor:
            for service in self.services.keys():
                executor.submit(self._stop_service, service, log_callback)

        self.status = "stopped"
        log_callback("OS Shutdown complete.")

    def _start_service(self, service, log_callback):
        """Simulates starting a service."""
        time.sleep(1)  # Simulated boot time
        self.services[service] = "running"
        log_callback(f"{service} started.")

    def _stop_service(self, service, log_callback):
        """Simulates stopping a service."""
        time.sleep(0.5)  # Simulated shutdown time
        self.services[service] = "stopped"
        log_callback(f"{service} stopped.")

    def run_command(self, command):
        """Executes a dummy command in the OS."""
        if self.status != "running":
            return "Cannot execute command. OS is not running."
        return f"Executed: {command}"

class OS_GUI:
    """Graphical interface for PyFastOS with parallel boot & shutdown."""

    def __init__(self, root):
        self.root = root
        self.root.title("PyFastOS GUI")
        self.os_instance = FastBootOS(OS_CONFIG)

        # UI Elements
        self.start_button = tk.Button(root, text="Boot OS", command=self.start_os)
        self.start_button.pack(pady=5)

        self.shutdown_button = tk.Button(root, text="Shutdown OS", state=tk.DISABLED, command=self.shutdown_os)
        self.shutdown_button.pack(pady=5)

        self.log_display = scrolledtext.ScrolledText(root, height=15, width=60, state='disabled')
        self.log_display.pack(pady=5)

        self.command_entry = tk.Entry(root, width=40)
        self.command_entry.pack(pady=5)
        self.command_entry.bind("<Return>", self.execute_command)

        self.execute_button = tk.Button(root, text="Execute Command", command=self.execute_command)
        self.execute_button.pack(pady=5)

    def log_message(self, message):
        """Logs messages in the GUI."""
        self.log_display.config(state='normal')
        self.log_display.insert(tk.END, message + "\n")
        self.log_display.config(state='disabled')
        self.log_display.yview(tk.END)

    def start_os(self):
        """Starts the OS boot process in a separate thread."""
        self.log_message("Booting PyFastOS...")
        self.start_button.config(state=tk.DISABLED)
        threading.Thread(target=self.boot_process, daemon=True).start()

    def boot_process(self):
        """Handles the OS boot process with parallel service startup."""
        self.os_instance.boot(self.log_message)
        self.shutdown_button.config(state=tk.NORMAL)

    def shutdown_os(self):
        """Starts the OS shutdown process in a separate thread."""
        self.log_message("Shutting down...")
        self.shutdown_button.config(state=tk.DISABLED)
        threading.Thread(target=self.shutdown_process, daemon=True).start()

    def shutdown_process(self):
        """Handles the OS shutdown process with parallel service shutdown."""
        self.os_instance.shutdown(self.log_message)
        self.start_button.config(state=tk.NORMAL)

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
