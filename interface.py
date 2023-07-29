import simulator as s

if __name__ == '__main__':
    # Good size is (620, 520)
    # Create a Simulator object
    sim = s.Simulator((100, 100), 10, 0.001, True)
    sim.start()


