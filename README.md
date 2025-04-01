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


## Functionality


- **Time Step (TS):**
- **UP Arrow:** Increase TS by 60 seconds.
- **DOWN Arrow:** Decrease TS by 60 seconds (minimum 60 seconds).

- **Earth's Initial Velocity:**
- **RIGHT Arrow:** Increase velocity by 100 m/s.
- **LEFT Arrow:** Decrease velocity by 100 m/s.

- **Reset Simulation:**
- **R Key:** Reset the simulation with the updated values.
- **SPACE Bar:** Hard reset the simulation.

- **Gravitational and Mass Controls:**
- **G (Gravitational Constant):**
 - **Z Key:** Increase G by 10%.
 - **X Key:** Decrease G by 10%.
- **Sun's Mass:**
 - **C Key:** Increase Sun mass by 10%.
 - **V Key:** Decrease Sun mass by 10%.
- **Earth's Mass:**
 - **B Key:** Increase Earth mass by 10%.
 - **N Key:** Decrease Earth mass by 10%.

## ISSUES

- Since the Sun doesn’t move, adjusting Earth’s mass won’t change the orbit time. For a more realistic simulation, both the Earth and the Sun should be allowed to move.
- I understand rbits are far more complicated and deal with different forced other than gravity, velocity mass and acc. 
