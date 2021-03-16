#!/usr/bin/env python3

import os
import time
import random as rand

class Unit:
    
    def __init__(self):
        self.celldm1 = -1
        self.nat = -1
        self.ntyp = -1
        self.etot = -1
        self.symbols = []
        self.positions = []
        self.f_components = []

    def read_input(self, txt):
        
        '''reads pw input txt file for unit cell data'''
        
        with open(txt) as f:
            
            for line in f:
                
                strlist = line.strip().split() # break string into list
                
                if strlist == []: continue # skip empty lines
                elif strlist[0] == 'celldm(1)': self.celldm1 = float(strlist[-1])
                elif strlist[0] == 'nat': self.nat = int(strlist[-1])
                elif strlist[0] == 'ntyp': self.ntyp = int(strlist[-1])
                elif 'ATOMIC_POSITIONS' in strlist: # find position block
                    for i in range(nat): # record position data
                        strlist = f.readline().strip().split() # make new string list
                        self.positions.append([ float(k) for k in strlist[-3:] ])
                        self.symbols.append( strlist[0] )
                        
        return
        
    def read_output(self, txt, atoms_moved, move_directions): # ATOMS_MOVED, MOVE_DIRECTIONS UNACCOUNTED FOR
    
        '''reads pw output for total energy & total force'''

        force_components = ['n/a' for i in range(self.nat)]

        with open(txt) as f:
            
            for line in f:
                
                strlist = line.strip().split()

                if strlist == []: continue # skip empty lines
                elif ' '.join(strlist[1:3]) == 'total energy' and strlist[-1] == 'Ry':
                    self.etot = float( strlist[-2] ) # record total energy
                elif ' '.join(strlist[:2]) == 'Forces acting': # find block with forces acting on atoms
                    
                    f.readline()
                    for v in range(self.nat): # WORKING

                        blocklinelist = f.readline().strip().split()
                        if int(blocklinelist[1]) in atoms_moved: # if atom index is in list of atoms to be moved
                            atom_sysindex = int(blocklinelist[1]) # atom index in system from 1 to nat
                            for w in range(len(atoms_moved)):
                                if int(atoms_moved[w]) == atom_sysindex:
                                    atom_listindex = int(atoms_moved[w]) - 1 # index in system -> index in list
                                else: continue
                                self.f_components[ atom_listindex ] = float( blocklinelist[ move_directions[w] - 3 ])
                        else:
                            continue

        return

    def translate(self, pwx): # NEED PROMPT FOR INPUT
    
        axes = ['x','y','z']
        read_input('pw.in')
        
        #translation prompt
        
        os.system(f'{pwx} < pw.in > pw.out')
        read_output('pw.out')
        
        return

def main():
    
    
