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

    def boot(self, log_callback):
        """Boots the OS by starting services in parallel."""
        self.status = "booting"
        self.start_time = time.time()
        log_callback("Booting PyFastOS...")
        
        with ThreadPoolExecutor(max_workers=len(self.services)) as executor:
            for service in self.services.keys():
                executor.submit(self._start_service, service, log_callback)
        
        self.status = "running"
        log_callback(f"OS Boot Complete.")
    
    def shutdown(self, log_callback):
        """Shuts down all services in parallel."""
        self.status = "shutting down"
        log_callback("Shutting down PyFastOS...")
        
        with ThreadPoolExecutor(max_workers=len(self.services)) as executor:
            for service in self.services.keys():
                executor.submit(self._stop_service, service, log_callback)
        
        self.status = "stopped"
        log_callback("OS Shutdown complete.")
    
    def restart(self, log_callback):
        """Restarts the OS."""
        self.shutdown(log_callback)
        self.boot(log_callback)
    
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
        """Executes a system-like command in PyFastOS."""
        if self.status != "running":
            return "Cannot execute command. OS is not running."

        command = command.lower().strip()
        self.command_history.append(command)

        if command.startswith("add_task "):
            task_name = command[9:]
            return self.add_task(task_name)
        elif command.startswith("kill_task "):
            try:
                task_id = int(command[10:])
                return self.kill_task(task_id)
            except ValueError:
                return "Invalid task ID."
        elif command.startswith("prioritize_task "):
            try:
                parts = command.split()
                task_id = int(parts[1])
                priority = parts[2]
                return self.prioritize_task(task_id, priority)
            except (IndexError, ValueError):
                return "Usage: prioritize_task <task_id> <priority>"
        elif command == "list_tasks":
            return self.list_tasks()
        elif command == "status":
            return f"OS Status: {self.status.capitalize()}"
        elif command == "uptime":
            if self.start_time:
                return f"Uptime: {time.time() - self.start_time:.2f} seconds"
            return "OS is not running."
        elif command == "services":
            running_services = [s for s, status in self.services.items() if status == "running"]
            return f"Running Services: {', '.join(running_services) if running_services else 'None'}"
        elif command.startswith("echo "):
            return command[5:]  
        elif command == "date":
            return time.strftime("Current Date & Time: %Y-%m-%d %H:%M:%S")
        elif command == "clear":
            return "clear_log"  
        elif command == "help":
            return (
                "Available Commands:\n"
                " - status: Show OS status\n"
                " - uptime: Display system uptime\n"
                " - services: List active services\n"
                " - echo <message>: Print a message\n"
                " - date: Show current date/time\n"
                " - clear: Clear the log\n"
                " - help: Show this help message\n"
                " - memory: Show detailed memory usage\n"
                " - cpu: Show detailed CPU usage\n"
                " - disk: Show detailed disk usage\n"
                " - network: Show detailed network statistics\n"
                " - log: Show last 10 logs\n"
                " - add_task <name>: Add a new task\n"
                " - kill_task <id>: Kill a task by ID\n"
                " - prioritize_task <id> <priority>: Set task priority\n"
                " - list_tasks: List all active tasks\n"
            )
        elif command == "memory":
            memory_usage = {
                "Total": "8 GB",
                "Used": "3.2 GB",
                "Free": "4.8 GB",
                "Cached": "1.2 GB",
                "Buffers": "0.5 GB"
            }
            return (
                "Memory Usage:\n"
                f" - Total: {memory_usage['Total']}\n"
                f" - Used: {memory_usage['Used']}\n"
                f" - Free: {memory_usage['Free']}\n"
                f" - Cached: {memory_usage['Cached']}\n"
                f" - Buffers: {memory_usage['Buffers']}"
            )
        elif command == "cpu":
            cpu_usage = {
                "Cores": 4,
                "Usage": "45%",
                "Clock Speed": "3.2 GHz",
                "Temperature": "65°C"
            }
            return (
                "CPU Usage:\n"
                f" - Cores: {cpu_usage['Cores']}\n"
                f" - Usage: {cpu_usage['Usage']}\n"
                f" - Clock Speed: {cpu_usage['Clock Speed']}\n"
                f" - Temperature: {cpu_usage['Temperature']}"
            )
        elif command == "disk":
            disk_usage = {
                "Total": "500 GB",
                "Used": "320 GB",
                "Free": "180 GB",
                "Read Speed": "120 MB/s",
                "Write Speed": "100 MB/s"
            }
            return (
                "Disk Usage:\n"
                f" - Total: {disk_usage['Total']}\n"
                f" - Used: {disk_usage['Used']}\n"
                f" - Free: {disk_usage['Free']}\n"
                f" - Read Speed: {disk_usage['Read Speed']}\n"
                f" - Write Speed: {disk_usage['Write Speed']}"
            )
        elif command == "network":
            network_stats = {
                "Download Speed": "50 Mbps",
                "Upload Speed": "20 Mbps",
                "Packets Sent": "1,200",
                "Packets Received": "1,500",
                "Latency": "15 ms"
            }
            return (
                "Network Statistics:\n"
                f" - Download Speed: {network_stats['Download Speed']}\n"
                f" - Upload Speed: {network_stats['Upload Speed']}\n"
                f" - Packets Sent: {network_stats['Packets Sent']}\n"
                f" - Packets Received: {network_stats['Packets Received']}\n"
                f" - Latency: {network_stats['Latency']}"
            )
        elif command == "log":
            return "Last 10 Logs:\n" + "\n".join(self.command_history[-10:])
        elif command in ["exit", "quit"]:
            self.shutdown(lambda msg: None)
            return "Goodbye!"
        else:
            return f"Unknown command: {command}"

    def add_task(self, task_name):
        """Simulates adding a task."""
        task_id = len(self.tasks) + 1
        self.tasks[task_id] = {"name": task_name, "status": "running", "priority": "normal"}
        return f"Task '{task_name}' added with ID {task_id}."

    def kill_task(self, task_id):
        """Simulates killing a task."""
        if task_id in self.tasks:
            self.tasks[task_id]["status"] = "terminated"
            return f"Task ID {task_id} ('{self.tasks[task_id]['name']}') terminated."
        return f"Task ID {task_id} not found."

    def prioritize_task(self, task_id, priority):
        """Simulates prioritizing a task."""
        if task_id in self.tasks:
            self.tasks[task_id]["priority"] = priority
            return f"Task ID {task_id} ('{self.tasks[task_id]['name']}') priority set to {priority}."
        return f"Task ID {task_id} not found."

    def list_tasks(self):
        """Lists all active tasks."""
        if not self.tasks:
            return "No active tasks."
        task_list = "Active Tasks:\n"
        for task_id, task_info in self.tasks.items():
            task_list += (
                f" - ID: {task_id}, Name: {task_info['name']}, "
                f"Status: {task_info['status']}, Priority: {task_info['priority']}\n"
            )
        return task_list

    def run_background_task(self, task_name, duration, log_callback):
        """Simulates a background task."""
        task_id = len(self.tasks) + 1
        self.tasks[task_id] = {"name": task_name, "status": "running", "priority": "background"}
        log_callback(f"Background task '{task_name}' started with ID {task_id}.")
        time.sleep(duration)
        self.tasks[task_id]["status"] = "completed"
        log_callback(f"Background task '{task_name}' completed.")

class OS_GUI:
    """Graphical interface for PyFastOS with additional features."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("PyFastOS - v2.1")
        self.root.geometry("600x500")
        self.dark_mode = False  

        self.os_instance = FastBootOS(OS_CONFIG)
        self.command_history = []

        # UI Elements
        self.start_button = tk.Button(root, text="Boot OS", command=self.start_os, bg="green", fg="white")
        self.start_button.pack(pady=5)

        self.shutdown_button = tk.Button(root, text="Shutdown OS", state=tk.DISABLED, command=self.shutdown_os, bg="red", fg="white")
        self.shutdown_button.pack(pady=5)

        self.log_display = scrolledtext.ScrolledText(root, height=15, width=70, state='disabled', bg="black", fg="lime")
        self.log_display.pack(pady=5)

        self.command_entry = tk.Entry(root, width=40)
        self.command_entry.pack(pady=5)
        self.command_entry.bind("<Return>", self.execute_command)

        self.execute_button = tk.Button(root, text="Execute Command", command=self.execute_command, bg="blue", fg="white")
        self.execute_button.pack(pady=5)

        self.toggle_theme_button = tk.Button(root, text="Toggle Dark Mode", command=self.toggle_dark_mode, bg="gray", fg="black")
        self.toggle_theme_button.pack(pady=5)

        self.status_label = tk.Label(root, text="OS Status: Idle", fg="black")
        self.status_label.pack(pady=5)

        self.service_frame = tk.Frame(root)
        self.service_frame.pack()
        self.service_labels = {}
        for service in OS_CONFIG["services"]:
            label = tk.Label(self.service_frame, text=f"{service}: Stopped", fg="red")
            label.pack()
            self.service_labels[service] = label

        self.task_frame = tk.Frame(root)
        self.task_frame.pack(pady=10)

        self.add_task_button = tk.Button(self.task_frame, text="Add Task", command=self.add_task_gui, bg="blue", fg="white")
        self.add_task_button.pack(side=tk.LEFT, padx=5)

        self.kill_task_button = tk.Button(self.task_frame, text="Kill Task", command=self.kill_task_gui, bg="red", fg="white")
        self.kill_task_button.pack(side=tk.LEFT, padx=5)

        self.prioritize_task_button = tk.Button(self.task_frame, text="Prioritize Task", command=self.prioritize_task_gui, bg="orange", fg="white")
        self.prioritize_task_button.pack(side=tk.LEFT, padx=5)

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
            color = "green" if status == "running" else "red"
            self.service_labels[service].config(text=f"{service}: {status.capitalize()}", fg=color)
    
    def start_os(self):
        """Starts the OS boot process in a separate thread."""
        self.start_button.config(state=tk.DISABLED)
        threading.Thread(target=self.boot_process, daemon=True).start()
    
    def boot_process(self):
        """Handles the OS boot process."""
        self.os_instance.boot(self.log_message)
        self.shutdown_button.config(state=tk.NORMAL)
        self.update_service_status()
    
    def shutdown_os(self):
        """Starts the OS shutdown process."""
        self.shutdown_button.config(state=tk.DISABLED)
        threading.Thread(target=self.shutdown_process, daemon=True).start()
    
    def shutdown_process(self):
        """Handles the OS shutdown process."""
        self.os_instance.shutdown(self.log_message)
        self.start_button.config(state=tk.NORMAL)
        self.update_service_status()
    
    def execute_command(self, event=None):
        """Executes a command in the OS."""
        command = self.command_entry.get()
        if command:
            self.command_history.append(command)  # Track command history
            self.log_message(f"> {command}")
            result = self.os_instance.run_command(command)
            if command in ["memory", "cpu", "disk", "network"]:
                self.log_message("Detailed Data:\n" + result)
            elif command == "clear":
                self.log_message("Log cleared.")
            else:
                self.log_message(result)
            self.command_entry.delete(0, tk.END)

    def toggle_dark_mode(self):
        """Toggles between dark and light mode."""
        if self.dark_mode:
            self.root.config(bg="white")
            self.status_label.config(fg="black")
            self.toggle_theme_button.config(bg="gray", fg="black")
        else:
            self.root.config(bg="black")
            self.status_label.config(fg="white")
            self.toggle_theme_button.config(bg="black", fg="white")

        self.dark_mode = not self.dark_mode

    def add_task_gui(self):
        """Adds a task via the GUI."""
        task_name = self.command_entry.get()
        if task_name:
            result = self.os_instance.add_task(task_name)
            self.log_message(result)
            self.command_entry.delete(0, tk.END)

    def kill_task_gui(self):
        """Kills a task via the GUI."""
        task_id = self.command_entry.get()
        if task_id.isdigit():
            result = self.os_instance.kill_task(int(task_id))
            self.log_message(result)
            self.command_entry.delete(0, tk.END)
        else:
            self.log_message("Invalid task ID.")

    def prioritize_task_gui(self):
        """Prioritizes a task via the GUI."""
        parts = self.command_entry.get().split()
        if len(parts) == 2 and parts[0].isdigit():
            task_id = int(parts[0])
            priority = parts[1]
            result = self.os_instance.prioritize_task(task_id, priority)
            self.log_message(result)
            self.command_entry.delete(0, tk.END)
        else:
            self.log_message("Usage: <task_id> <priority>")

if __name__ == "__main__":
    root = tk.Tk()
    app = OS_GUI(root)
    root.mainloop()
