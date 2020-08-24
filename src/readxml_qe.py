#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 12:21:20 2020

@author: nicholas
"""

import xml.etree.ElementTree as et
import numpy as np

def read_pw_data(xml,needInput=True):
    
    """reads xml file for pwscf input/output data"""
    
    # prepare xml file
    tree = et.parse(xml) # abs path
    root = tree.getroot()
    
    '''input: n-atoms, n-types, atom names, atom positions'''
    
    ntyp = root[2][1].attrib['ntyp'] # number of species
    nat = root[2][2].attrib['nat'] # number of atoms
    atoms = [o.attrib['name'] for o in root[2][2][0]] # atoms & their indices
    positions = []
    for o in root[2][2][0]: # atom positions
        r = [float(i) for i in o.text.split()] # str -> float
        positions.append(r)
    
    '''output: total energy & force'''
    
    etot = round(float(root[3][8][0].text), 4) # total energy
    
    # compute total force
    fstr = root[3][10].text.split()
    fmat = np.array([ sum(float(i) for i in fstr[:3]), # component force magnitudes
                      sum(float(j) for j in fstr[3:6]),
                      sum(float(k) for k in fstr[6:]) ])
    ftot = round(np.linalg.norm(fmat), 4)
    
    '''return all data if needInput = True'''
    
    if needInput:
        return int(ntyp), int(nat), atoms, positions, etot, ftot
    else:
        return positions, etot, ftot
    
# def main():


if __name__ == "__main__":
    main()