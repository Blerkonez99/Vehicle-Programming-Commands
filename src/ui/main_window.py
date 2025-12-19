import customtkinter as ctk
from tkinter import ttk, messagebox
from .vehicle_frame import VehicleFrame
from .command_frame import CommandFrame
from .status_frame import StatusFrame


class MainWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app

        # Create main container with less bottom padding
        self.container = ctk.CTkFrame(master)
        self.container.pack(fill="both", expand=True, padx=10, pady=(10, 2))

        # Create header
        self.create_header()

        # Create main content area with less bottom padding
        self.create_content()

        # Create status bar
        self.create_status_bar()

    def create_header(self):
        """Create the header with connection controls"""
        header = ctk.CTkFrame(self.container)
        header.pack(fill="x", padx=5, pady=5)

        # Connection button
        self.conn_btn = ctk.CTkButton(
            header,
            text="Connect Device",
            command=self.toggle_connection
        )
        self.conn_btn.pack(side="left", padx=5)

        # Port selection
        port_label = ctk.CTkLabel(header, text="Port:")
        port_label.pack(side="left", padx=5)

        self.port_var = ctk.StringVar(value=self.app.config.get("device_port", "COM3"))
        self.port_entry = ctk.CTkEntry(
            header,
            textvariable=self.port_var,
            width=100
        )
        self.port_entry.pack(side="left", padx=5)

        # Baud rate selection
        baud_label = ctk.CTkLabel(header, text="Baud:")
        baud_label.pack(side="left", padx=5)

        baud_default = str(self.app.config.get("device_baudrate", 115200))
        self.baud_var = ctk.StringVar(value=baud_default)
        self.baud_entry = ctk.CTkEntry(
            header,
            textvariable=self.baud_var,
            width=100
        )
        self.baud_entry.pack(side="left", padx=5)

    def create_content(self):
        """Create the main content area"""
        content = ctk.CTkFrame(self.container)
        content.pack(fill="both", expand=True, padx=5, pady=(5, 2))

        # Create left side (vehicle selection)
        self.vehicle_frame = VehicleFrame(content, self.app)
        self.vehicle_frame.pack(side="left", fill="y", padx=(0, 5))

        # Create right side (commands)
        self.command_frame = CommandFrame(content, self.app)
        self.command_frame.pack(side="left", fill="both", expand=True)

    def create_status_bar(self):
        """Create the status bar"""
        # Main status frame with border and different background
        status_frame = ctk.CTkFrame(self.container)
        status_frame.pack(side="bottom", fill="x", padx=5, pady=5, anchor="s")

        # Left side - Connection status
        status_left = ctk.CTkFrame(status_frame, fg_color="transparent")
        status_left.pack(side="left", fill="x", expand=True)

        self.status_label = ctk.CTkLabel(
            status_left,
            text="Not Connected",
            font=("Helvetica", 12),
            text_color="red"
        )
        self.status_label.pack(side="left", padx=10, pady=5)

        # Add separator
        separator = ttk.Separator(status_frame, orient="vertical")
        separator.pack(side="left", fill="y", padx=10, pady=5)

        # Right side - Developer caption
        status_right = ctk.CTkFrame(status_frame, fg_color="transparent")
        status_right.pack(side="right")

        developer_label = ctk.CTkLabel(
            status_right,
            text="Developed by M Khanfar 2025",
            font=("Helvetica", 12, "bold"),
            text_color="#666666"
        )
        developer_label.pack(side="right", padx=10, pady=5)

    def toggle_connection(self):
        """Toggle device connection"""
        if not self.app.device:
            # Update port and baud from entries
            self.app.config.set("device_port", self.port_var.get())
            try:
                baudrate = int(self.baud_var.get())
            except ValueError:
                messagebox.showerror("Error", "Invalid baud rate value")
                return

            self.app.config.set("device_baudrate", baudrate)

            if self.app.connect_device():
                self.conn_btn.configure(text="Disconnect")
                self.port_entry.configure(state="disabled")
                self.baud_entry.configure(state="disabled")
                self.status_label.configure(text="Connected to OBDLink EX", text_color="green")
                self.command_frame.update_connection_state(True)
        else:
            self.app.disconnect_device()
            self.conn_btn.configure(text="Connect Device")
            self.port_entry.configure(state="normal")
            self.baud_entry.configure(state="normal")
            self.status_label.configure(text="Disconnected", text_color="red")
            self.command_frame.update_connection_state(False)
