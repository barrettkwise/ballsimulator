import simulator as s

if __name__ == '__main__':
    # Good size is (620, 520)
    # Create a Simulator object
    sim = s.Simulator((500, 500), 100)
    sim.start()
