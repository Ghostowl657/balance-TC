# Analytical TBC Balance Sim: Burn-Regen model
The current sim is written in Python2 (cause that's what I happened to have) and in Jupyter notebook. 
This allows easy editing and running subcomponents, but there is also a standard .py file which can be run in any python IDE or command line.

## How to use
See the example.py for a quick explanation of the correct way to run the sim, as you desire.

## Model explanation
### Overview
As the name suggests, the model assumes there are two distinct dps "phases": a burn phase, and a regen phase. The burn phase is characterized by 
a high dps, high mana usage rotation (e.g. max moonfire + max starfire). The regen phase is the opposite: a low dps, low mana usage rotation (e.g. rank 6 starfire)
intended to regenerate your mana so you can begin burning once again.
A full fight is expected to be a combination of these two phases where you begin at full mana at the start and end the fight with exactly zero mana.

[Assumed mana usage profile for a full encounter](/examplefullfightmanausage.png)

[Smoothing of mana usage/gain](/exampleburnphasemanausage.png)

### Dps calculation
The damage of each spell individually is taken as the average damage done, crit/hit/resist taken into account.
The dps of a phase is calculated over one full "rotation". I.e. if you are casting moonfire+starfire your rotation looks something like
(MF,SF,SF,SF,SF,SF),(MF,SF,SF,SF,SF,SF)...
