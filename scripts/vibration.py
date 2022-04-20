import RPi.GPIO as GPIO

class Vibration:
    def __init__(self, pinNb):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pinNb, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin's mode to input, and pull up to high
        GPIO.add_event_detect(pinNb, GPIO.FALLING, callback=self.callback_vibration)

    def callback_vibration(channel):
        print("vibration detected!")
