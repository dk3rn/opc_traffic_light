import tkinter as tk
from data_exchange import Traffic_Light_Container
tlc = None;

class TrafficLightApp(tk.Tk):
    def __init__(self):
        super().__init__()

        tlc = Traffic_Light_Container()

        self.title("Traffic Light Control")
        self.geometry("300x550")

        # Initial state of the traffic light
        self.state = 'RED'
        self.is_running_cycle = False

        # Traffic light bulbs
        self.red_light = tk.Label(self, text="", width=10, height=5, bg="red")
        self.red_light.pack(pady=(30, 5))

        self.yellow_light = tk.Label(self, text="", width=10, height=5, bg="gray")
        self.yellow_light.pack(pady=(5, 5))

        self.green_light = tk.Label(self, text="", width=10, height=5, bg="gray")
        self.green_light.pack(pady=(5, 30))

        # Countdown label for green phase
        self.green_timer_label = tk.Label(self, text="", font=("Helvetica", 16))
        self.green_timer_label.pack(pady=(0, 20))

        # Request button
        self.button = tk.Button(self, text="Request", command=self.request)
        self.button.pack(pady=(10, 10))

    def request(self):
        """Called when the request button is pressed."""
        if not self.is_running_cycle:
            self.is_running_cycle = True
            self.state = 'RED_YELLOW'
            self.update_lights()
            print("Starting cycle from RED to RED_YELLOW!")

    def request_opc(self):
        """Called when the request opc request activated"""
        if not self.is_running_cycle:
            self.is_running_cycle = True
            self.state = 'RED_YELLOW'
            self.update_lights()
            print("Starting cycle from RED to RED_YELLOW!")

    def update_lights(self):
        """Updates the UI based on the current state."""
        tlc = Traffic_Light_Container()
        if self.state == 'GREEN':
            self.red_light.config(bg="gray")
            tlc.red = 0
            self.yellow_light.config(bg="gray")
            tlc.yellow = 0
            self.green_light.config(bg="green")
            tlc.green = 1
            self.start_green_countdown(10)  # 10 seconds green phase
            tlc.green = 1
        elif self.state == 'RED_YELLOW':
            self.red_light.config(bg="red")
            tlc.red = 1
            self.yellow_light.config(bg="yellow")
            tlc.yellow = 1
            self.green_light.config(bg="gray")
            tlc.green = 0
            self.after(2000, self.set_light, 'GREEN')  # 2 seconds for red-yellow
        elif self.state == 'YELLOW':
            self.red_light.config(bg="gray")
            tlc.red= 0
            self.yellow_light.config(bg="yellow")
            tlc.yellow = 1
            self.green_light.config(bg="gray")
            tlc.green = 0
            self.after(2000, self.set_light, 'RED')  # 2 seconds for yellow
        else:  # RED state
            self.red_light.config(bg="red")
            tlc.red = 1
            self.yellow_light.config(bg="gray")
            tlc.yellow = 0
            self.green_light.config(bg="gray")
            tlc.green = 0
            self.is_running_cycle = False
            print("Cycle complete, waiting for request...")

    def set_light(self, state):
        """Sets the state of the traffic light and updates the bulbs."""
        self.state = state
        self.update_lights()

    def start_green_countdown(self, duration):
        """Starts the countdown for the green phase."""
        tlc = Traffic_Light_Container()
        self.green_timer_label.config(text=f"Green for: {duration} sec.")
        tlc.green_time_left = duration
        if duration > 0:
            self.after(1000, self.start_green_countdown, duration - 1)
        else:
            self.set_light('YELLOW')


if __name__ == "__main__":
    app = TrafficLightApp()
    app.mainloop()