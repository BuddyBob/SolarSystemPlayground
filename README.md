# Earth Orbiting Sun Simulation

This project is a simple simulation built using Python and Pygame that shows the Earth orbiting the Sun. It’s based on real physics formulas (like Newton's law of gravitation)
However I simplified this to fit in the simulation and the realm of my knowledge

Disclaimer: Sun and Earth ratios innacurate for sake of display

## Overview

- **What It Does:**  
  The simulation shows the Earth moving around the Sun using the gravitational force formula:  
  \[
  F = G \times \frac{M_{\text{sun}} \times M_{\text{earth}}}{r^2}
  \]
  Then, Earth’s acceleration is calculated by \( a = \frac{F}{M_{\text{earth}}} \).  
  In this simulation, the Sun is fixed in the center, which means even if you change Earth's mass, the orbit time (about 365 days in sim-time) stays the same.

- **Main Tool**
  You can adjust various parameters (like gravitational constant, Sun mass, Earth mass, time step, and Earth’s velocity) in real-time and see how they affect the orbit.
