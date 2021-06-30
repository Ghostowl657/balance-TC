# Analytical TBC Balance Sim: Burn-Regen model
The current sim is written in Python2 (cause that's what I happened to have) and in Jupyter notebook. 
This allows easy editing and running subcomponents, but there is also a standard .py file which can be run in any python IDE or command line.

## How to use
Intialize the stats with the "settings()" function, make any necessary tweaks to the default, then run "encounter" with fight length, settings, and rotation choice as inputs.
It will output only dps by default, or more info if chosen.

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
The dps of a phase is calculated over one full "rotation". I.e. if you are casting moonfire+starfire your full fight looks something like
(MF,SF,SF,SF,SF,SF),(MF,SF,SF,SF,SF,SF)...(MF,SF,SF,SF,SF,SF). A "rotation" is simply one chain of (MF,SF,SF,SF,SF,SF). We can calculate the 
damage done over a single rotation, the mana used, and the time spent doing it. Using damage and time, we calculate the phase dps. Using max mana pool, 
mana consumption/gain, and rotation time, we can calculate the total time spent in a phase. Add up the damage done in each phase and you can get the total DPS.
