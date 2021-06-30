#!/usr/bin/env python
# coding: utf-8

import numpy as np
import random
import math
import matplotlib.pyplot as plt
from balance_sim_module import *


## Finding the optimal ranks to use based on fight length ##

# https://seventyupgrades.com/set/dfNkfvvAM87CBLvJfmuATC
stat_arc = {
    'base mana':2090,
    'hit':114,
    'crit':206,
    'int':368,
    'spi':194,
    'Mp5':11,
    'haste':0,
    'arcane':1109+36+80+23,
    'nature':887+36+80+23
}
arc_settings = settings()
arc_settings[1]['spellfire'] = True
arc_settings[1]['SF idol'] = True

data = np.zeros((300,13,8,13,8))
for MFrank in range(0,13):
    for SFrank in range(1,9):
        for MFrank2 in range(0,MFrank+1):
            for SFrank2 in range(1,SFrank+1):
                for T in range(1,301):
                    if MFrank!=0:
                        rot1 = ['MF','SF']; ranks1 = [MFrank,SFrank]
                    else:
                        rot1 = ['SF']; ranks1 = [SFrank]
                    if MFrank2!=0:
                        rot2 = ['MF','SF']; ranks2 = [MFrank2,SFrank2]
                    else:
                        rot2 = ['SF']; ranks2 = [SFrank]
                    data[T-1,MFrank,SFrank-1,MFrank2,SFrank2-1] = encounter(T,arc_settings,rot1,ranks1,rot2,ranks2)
initial_max = np.amax(data[1])
optimal_ranks = np.zeros((300,4))
Ts=np.linspace(1,300,300)
for T in Ts:
    T = int(T)
    maximum = np.amax(data[T-1])
    where = np.where(data[T-1]==maximum)
    mf1 = where[0][0]
    sf1 = where[1][0]+1
    if len(where[0])!=1:
        mf2 = -10
        sf2 = -10
    else:
        mf2 = where[2][0]
        sf2 = where[3][0]+1
    optimal_ranks[T-1,:] = [mf1,sf1,mf2,sf2]
plt.scatter(Ts,optimal_ranks[:,0],s=0.5,label='Moonfire')
plt.scatter(Ts,optimal_ranks[:,1],s=0.5,label='Starfire')
plt.ylabel('Rank')
plt.xlabel('Fight length (s)')
plt.ylim(-0.5,12.5)
plt.title('Optimal rank for burn rotation')
plt.legend()
plt.show()
plt.scatter(Ts,optimal_ranks[:,2],s=0.5,label='Moonfire')
plt.scatter(Ts,optimal_ranks[:,3],s=0.5,label='Starfire')
plt.ylabel('Rank')
plt.xlabel('Fight length (s)')
plt.ylim(-0.5,12.5)
plt.title('Optimal rank for regen rotation')
plt.legend()
plt.show()


## plotting the stat weights ##

names = ['hit','crit','int','spi','mp5','haste','arcane','nature']
for n,stat in enumerate(get_stat_weights([['SF'],[-1],['SF'],[1]])[0]):
    plt.plot(stat,label=names[n])
plt.ylabel('spellpower equivalent')
plt.xlabel('Fight length (s)')
plt.legend()
plt.show()


## Comparing wrath and starfire rotation in respective BiS ##

# Examing both the case of having and not having curse of elements
for elements in [True,False]:
    # https://seventyupgrades.com/set/dfNkfvvAM87CBLvJfmuATC
    stats_arcane = {
        'base mana':2090,
        'hit':114,
        'crit':206,
        'int':368,
        'spi':194,
        'Mp5':11,
        'haste':0,
        'arcane':1109+36+80+23,
        'nature':887+36+80+23
    }
    arcane_settings = settings() # initialize
    arcane_settings[3] = stats_arcane # updating stats with the above
    arcane_settings[1]['spellfire'] = True # changing setting from default
    arcane_settings[1]['SF idol'] = True # starfire rotation
    arcane_settings[1]['elements'] = elements

    # https://seventyupgrades.com/set/wHj3URGBDfDBcy4tLaoz44
    stats_nature = {
        'base mana':2090,
        'hit':114,
        'crit':201,
        'int':411,
        'spi':247,
        'Mp5':19,
        'haste':0,
        'arcane':1014+36+80+23,
        'nature':1014+36+80+23
    }
    nature_settings = settings() # initialize
    nature_settings[3] = stats_nature # updating stats with the above
    nature_settings[1]['W idol'] = True # wrath rotation
    nature_settings[1]['elements'] = elements

    arcane_settings2 = settings() # initialize
    arcane_settings2[3] = stats_nature # using the general set rather than spellfire
    arcane_settings2[1]['SF idol'] = True # still starfire idol
    arcane_settings2[1]['elements'] = elements

    mfsfDPS,sfDPS,mfsf2DPS,sf2DPS,mfwDPS,wDPS = [],[],[],[],[],[]
    # iterate over fight lengths
    for T in range(10,360):
        mfsfDPS.append(encounter(T,arcane_settings,burn_rot=['MF','SF'],burn_ranks=[12,8],regen_rot=['SF'],regen_ranks=[1]))
        sfDPS.append(encounter(T,arcane_settings,burn_rot=['SF'],burn_ranks=[8],regen_rot=['SF'],regen_ranks=[1]))
        mfsf2DPS.append(encounter(T,arcane_settings2,burn_rot=['MF','SF'],burn_ranks=[12,8],regen_rot=['SF'],regen_ranks=[1]))
        sf2DPS.append(encounter(T,arcane_settings2,burn_rot=['SF'],burn_ranks=[8],regen_rot=['SF'],regen_ranks=[1]))
        mfwDPS.append(encounter(T,nature_settings,burn_rot=['MF','W'],burn_ranks=[-1,-1,],regen_rot=['W'],regen_ranks=[1]))
        wDPS.append(encounter(T,nature_settings,burn_rot=['W'],burn_ranks=[-1],regen_rot=['W'],regen_ranks=[1]))
    plt.plot(mfsfDPS,label='moonfire+starfire, arcane BiS')
    plt.plot(sfDPS,label='starfire, arcane BiS')
    plt.plot(mfsf2DPS,label='moonfire+starfire')
    plt.plot(sf2DPS,label='starfire')
    plt.plot(mfwDPS,label='moonfire+wrath')
    plt.plot(wDPS,label='wrath')
    plt.title('CoE = '+str(elements))
    plt.ylabel('DPS')
    plt.xlabel('Fight length (s)')
    plt.legend()
    plt.show()

