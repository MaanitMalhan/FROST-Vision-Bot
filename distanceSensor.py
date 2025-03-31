from gpiozero import DistanceSensor
def DistanceSensor():
    ultrasonic = DistanceSensor(echo=17, trigger=4)
    while True:
        print(ultrasonic.distance)
    