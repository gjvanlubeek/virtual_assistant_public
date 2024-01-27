from connectors.openai_connector import DigitalBrain
from connectors.gmail_connector import PostReceiver, PostSender
from connectors.list_maker import create_list

import RPi.GPIO as GPIO
import time
import board
import neopixel

import os
from dotenv import load_dotenv

# Check if the mode has already been set
if GPIO.getmode() is None:
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

# Set up the button
button_pin = 15
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# NeoPixels must be connected to D10, D12, D18, or D21 to work.
pixel_pin = 18 

# The number of NeoPixels
num_pixels = 6

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=1, auto_write=False, pixel_order=ORDER
)

load_dotenv()

PRIVATE_EMAIL = EMAIL = os.getenv('PRIVATE_EMAIL')

def pulsate(color, speed_up, speed_down, led_sleep):
    pixels.fill(color)
    for brightness in range(0, 255, speed_up):  # Increase brightness
        pixels.brightness = brightness / 255.0
        pixels.show()
        time.sleep(0.01)

    time.sleep(led_sleep)

    for brightness in range(255, 0, -speed_down):  # Decrease brightness
        pixels.brightness = brightness / 255.0
        pixels.show()
        time.sleep(0.01)
      
    pixels.brightness = 0
    pixels.show()

def rotate(color, speed):
    pixels.brightness = 255
    for i in range(num_pixels):
        pixels.fill((0, 0, 0))  # Turn off all pixels
        pixels[i] = color
        pixels.show()
        time.sleep(speed)
        if GPIO.input(button_pin) == GPIO.HIGH:
            ### script to run ###
            pulsate((255, 0, 255), 5, 5, 0.5)  # Change the color and parameters as needed
            
            pixels.fill((0, 0, 0))  # Turn off all pixels
            pixels.brightness = 255
            pixels[0] = (255, 0, 255)
            pixels.show()

            print("Button pushed, mail is being summarized")        

            va = DigitalBrain("Act as a virtual assistant named Dorothy, tasked with reviewing emails and \
                            summarizing specific details within the email. Additionally, you excel at \
                            crafting concise and playful responses to emails. Always use the native \
                            language from the sender's email")

            mail = PostReceiver()
            
            pixels[1] = (255, 0, 255)
            pixels.show()

            check_mail = mail.retreive_messages('seen')

            pixels[2] = (255, 0, 255)
            pixels.show()

            mail_list = create_list(check_mail)

            if not mail_list:
                print('no messages')

                pixels[3] = (255, 0, 255)
                pixels[4] = (255, 0, 255)
                pixels[5] = (255, 0, 255)
                pixels.show()

            else:
                response = []
                pixels[3] = (255, 0, 255)
                pixels.show()
                for mail in mail_list:
                    va.insert_data(mail)
                    response.append(va.generate_response("Summarize the provided email message in bullet points, using the \
                                                        native language from the sender's email. Descibe specific and detailed \
                                                        information always start by senders emailadres, the name of the sender date and \
                                                        than the content. Additionally, create a short draft email response use \
                                                        a cheecky tone of voice. Always end the draft email with 'Groeten \
                                                        Dorothy, \n Virtual assistant van Gert-Jan van Lubeek.'"))
                
                dashed_line = "-" * 50  # Create a dashed line with 30 dashes
                message = f"\n\n{dashed_line}\n\n".join(response)
                pixels[4] = (255, 0, 255)
                pixels.show()
                reply = PostSender()
                
                print("I've summarized " + str(len(mail_list)) + " messages")
                reply.add_message(PRIVATE_EMAIL, 'overview of ' + str(len(mail_list)) + ' messages', message)
                pixels[5] = (255, 0, 255)
                pixels.show()
                reply.send_message()

try:
    while True:
        rotate((0, 0, 255), 0.1)

except KeyboardInterrupt:
    print("Cleaning up GPIO")
    pixels.brightness = 0
    pixels.show()
    GPIO.cleanup()

finally:
    pixels.fill((0, 0, 0))
    pixels.show()



-----------------------------------

import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin for the button
button_pin = 15  # GPIO15, corresponds to pin 10 on the Raspberry Pi Zero 2W

# Set up the button as an input with a pull-up resistor
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    print("Press the button (Ctrl+C to exit)")

    while True:
        # Check if the button is pressed
        if GPIO.input(button_pin) == GPIO.LOW:
            print("Button pressed!")

        # Add a small delay to avoid button bouncing
        time.sleep(0.1)

except KeyboardInterrupt:
    # Clean up GPIO on Ctrl+C exit
    GPIO.cleanup()
