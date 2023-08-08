<<<<<<< HEAD
import simulator
=======
import simulator as s

if __name__ == '__main__':
    # Good size is (620, 520)
    # Create a Simulator object
    sim = s.Simulator((620, 520), 100)
    sim.start()

>>>>>>> d00fa1e (Stable version that works, minor issue with balls sticking together sometimes.)

# Create the simulator with the canvas size
# Good size is (620, 520)
s = simulator.Simulator((620, 520), 10, 0.00001)
s.start()
