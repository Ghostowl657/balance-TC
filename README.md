# Analytical TBC Balance Sim: Burn-Regen model
The current sim is written in Python2 (cause that's what I happened to have) and in Jupyter notebook. 
This allows easy editing and running subcomponents, but there is also a standard .py file which can be run in any python IDE or command line.

## How to use
See the example.py for a quick explanation of the correct way to run the sim, as you desire.

## Model explanation
As the name suggests, the model assumes there are two distinct dps "phases": a burn phase, and a regen phase. The burn phase is characterized by 
a high dps, high mana usage rotation (e.g. max moonfire + max starfire). The regen phase is the opposite: a low dps, low mana usage rotation (e.g. rank 6 starfire)
intended to regenerate your mana so you can begin burning once again.
A full fight is expected to be a combination of these two phases where you begin at full mana at the start and end the fight with exactly zero mana.
