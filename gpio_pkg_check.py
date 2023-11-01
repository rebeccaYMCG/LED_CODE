try: 
    import gpiozero
    print("gpiozero is installed")
except ImportError:
    print("gpiozero is not install. Intall with 'pip install gpiozero'")
try: 
    import pigpio
    print("pigpio is installed")
except ImportError:
    print("gpiozero is not install. Intall with 'pip install pigpio'")

