import serial
import time


class OBDLinkEX:
    def __init__(self, port, baudrate=115200, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.connection = None

    def connect(self):
        """Connect to OBDLink EX device"""
        try:
            self.connection = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout,
                write_timeout=self.timeout,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                rtscts=True,
                dsrdtr=True,
            )

            # Ensure clean buffers before we start sending commands
            self.connection.reset_input_buffer()
            self.connection.reset_output_buffer()

            identity = self.identify_adapter()
            if identity and "EX" not in identity.upper():
                raise RuntimeError(
                    f"Incompatible adapter detected: '{identity}'. Please connect an OBDLink EX."
                )

            self.initialize_adapter()
            return True

        except Exception as e:
            print(f"Connection error: {e}")
            self.disconnect()
            return False

    def identify_adapter(self):
        """Return adapter identity string."""
        try:
            response = self.send_command("ATI", timeout=5)
            return response
        except Exception:
            return ""

    def initialize_adapter(self):
        """Send the recommended initialization sequence for OBDLink EX."""
        # Reset device and allow it to reboot
        self.send_command("ATZ", timeout=10)
        time.sleep(1)

        # Basic configuration for stable CAN work
        self.send_command("ATE0")  # Disable echo
        self.send_command("ATL0")  # Disable linefeeds
        self.send_command("ATS1")  # Keep spaces for readability
        self.send_command("ATH1")  # Show headers

        # Set protocol to ISO 15765-4 CAN (11 bit ID, 500 kbaud)
        self.send_command("ATSP6")

    def disconnect(self):
        """Disconnect from device"""
        if self.connection and self.connection.is_open:
            self.connection.close()

    def send_command(self, command, timeout=5):
        """Send command to device and get response"""
        if not self.connection or not self.connection.is_open:
            raise Exception("Device not connected")

        # Clear input buffer
        self.connection.reset_input_buffer()

        # Send command
        self.connection.write(f"{command}\r".encode())

        # Read response
        response = ""
        start_time = time.time()

        while time.time() - start_time < timeout:
            if self.connection.in_waiting:
                char = self.connection.read().decode(errors="ignore")
                if char == '>':  # End of response
                    break
                response += char

        return response.strip()

    def send_can_command(self, id, data):
        """Send CAN command with specific ID and data"""
        command = f"{id:03X}#{data}"
        return self.send_command(command)

    def enter_diagnostic_session(self, session_type):
        """Enter diagnostic session"""
        return self.send_command(f"1003{session_type:02X}")

    def security_access(self, level):
        """Request security access"""
        # Request seed
        response = self.send_command(f"2701{level:02X}")
        if not response.startswith("6701"):
            raise Exception("Failed to get security seed")

        # Calculate key (implementation depends on manufacturer)
        seed = int(response[4:], 16)
        key = self.calculate_security_key(seed)

        # Send key
        response = self.send_command(f"2702{key:08X}")
        if not response.startswith("6702"):
            raise Exception("Security access denied")

        return True

    def calculate_security_key(self, seed):
        """Calculate security key from seed (example implementation)"""
        # This should be implemented according to manufacturer specifications
        return seed ^ 0xFFFFFFFF
