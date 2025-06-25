class Traffic_Light_Container:
    _instance = None

    def __new__(cls, *args, **kwargs):
        # Check if an instance of the class already exists
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init_once()
        return cls._instance

    def __init_once(self):
        # Initialize default values (executed only once)
        self.red = False
        self.yellow = False
        self.green = False
        self.request = False
        self.green_time_left = 0

    def __repr__(self):
        return (f"TrafficLightStateSingleton(red={self.red}, yellow={self.yellow}, "
                f"green={self.green}, request={self.request}, green_time_left={self.green_time_left})")

