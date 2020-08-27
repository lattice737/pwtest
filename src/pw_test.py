#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 09:20:03 2020

@author: nicholas
"""

import os
import random as rand

def launch_prompt():
    
    '''prompts user about program running and default settings; user can change settings'''
    
    # 85 picked arbitrarily
    print(85 * '-')
    print('PW TEST'.center(85))
    print(85 * '-')
    
    pwd = os.getcwd().split('/')
    path = '/Users/nicholas/Desktop/qe/bin/pw.x'
    ftype = 'txt'
    step = '0.01'
    
    '''prompt user about default settings'''
    
    if len(pwd[1:]) >= 5:
        print('\nCURRENT WORKING DIRECTORY:', f"/{pwd[1]}/{pwd[2]}/ ... /{pwd[-2]}/{pwd[-1]}") # attempt grep?
    else:
        print("\nCURRENT WORKING DIRECTORY:", '/'.join(pwd))
    print('DEFAULT LOCATION OF PW.X:', path) # attempt grep?
    print('INPUT/OUTPUT FILE TYPE:', ftype)
    
    # add receipt/log option for temporary runs

    try:
        okay = input('\nSETTINGS OKAY? (y/n): ')
        if okay.lower() != 'y' and okay.lower() != 'n':
            print('\nINVALID RESPONSE. DEFAULT SETTINGS WILL BE USED')
    except:
        print('\nSOMETHING WENT WRONG. DEFAULT SETTINGS WILL BE USED')
        okay = 'y'
    
    while okay == 'n': # menu block
        
        print('\n1 : CWD')
        print('2 : PW.X PATH')
        print('3 : I/O TYPE')
        print('4 : STEP SIZE')
        
        try:
            selection = input('ENTER NUMBER TO CHANGE A SETTING: ')
        except:
            print('\nINVALID SELECTION')
            okay = 'n'
        
        if selection == '1': # pwd path block
            
            try:
                
                print('\nCURRENT WORKING DIRECTORY:', f"/{pwd[1]}/{pwd[2]}/ ... /{pwd[-2]}/{pwd[-1]}")
                os.getcwd( input('ENTER ABSOLUTE PATH OF WORKING DIRECTORY (NO ALIASES): ') )
                print('\nNEW WORKING DIRECTORY:', f"/{pwd[1]}/{pwd[2]}/ ... /{pwd[-2]}/{pwd[-1]}")
                
            except:
                print('\nSOMETHING WENT WRONG. CWD NOT CHANGED')
            
        elif selection == '2': # pw.x path block
            
            try:
                
                print('\nCURRENT LOCATION OF PW.X:', path)
                path = input('ENTER ABSOLUTE PATH OF PW.X LOCATION: ')
                print('NEW LOCATION OF PW.X:', path)
                
            except:
                print('\nSOMETHING WENT WRONG. PATH NOT CHANGED')
                
        elif selection == '3': # i/o file type block
            
            try:
                
                print('\nCURRENT INPUT/OUTPUT FILE TYPE:', ftype)
                xml = input('USE XML? (y/n): ')
                
                if xml == 'y': ftype = 'xml'
                else: ftype = 'txt'
                
                print('NEW INPUT/OUTPUT FILE TYPE:', ftype)
                
            except:
                print('\nSOMETHING WENT WRONG. FILETYPE NOT CHANGED')
        
        print('\nCURRENT WORKING DIRECTORY:', f"/{pwd[1]}/{pwd[2]}/ ... /{pwd[-2]}/{pwd[-1]}")
        print('DEFAULT LOCATION OF PW.X:', path) # attempt grep?
        print('INPUT/OUTPUT FILE TYPE:', ftype)
        print('DEFAULT STEP SIZE:', step)
        
        try:
            okay = input('SETTINGS OKAY? (y/n): ')
            if okay.lower() != 'y': raise Exception
        
        except:
            okay = 'n'
        
    #os.chdir('/Users/nicholas/gitwork/pwtest/test') # developer machine
    ftype = 'txt' # xml reading not enabled yet
        
    return path, ftype

def read_input(txt):
    
    '''reads pw input txt file; returns celldm(1), nat, ntyp, atom symbols, & atom positions'''
        
    with open(txt) as f:
        
        celldm1 = 0
        nat = 0
        ntyp = 0
        
        for line in f:
            
            strlist = line.strip().split() # break string into list
            
            if strlist == []: continue # skip empty lines
        
            elif strlist[0] == 'celldm(1)': celldm1 = float(strlist[-1])
            elif strlist[0] == 'nat': nat = int(strlist[-1])
            elif strlist[0] == 'ntyp': ntyp = int(strlist[-1]) 
            
            elif 'ATOMIC_POSITIONS' in strlist: # find position block
                
                positions = []
                symbols = []
                
                for i in range(nat): # record position data
                    
                    strlist = f.readline().strip().split() # make new string list
                    positions.append([ float(k) for k in strlist[-3:] ])
                    symbols.append( strlist[0] )
                    
    return celldm1, nat, ntyp, symbols, positions

def read_output(txt):
    
    '''reads pw output; returns total energy & total force'''

    with open(txt) as f:
        
        for line in f:
            
            strlist = line.strip().split()

            if strlist == []: continue # skip empty lines
                
            elif ' '.join(strlist[1:3]) == 'total energy' and strlist[-1] == 'Ry': etot = float( strlist[-2] ) # record total energy
            elif ' '.join(strlist[:2]) == 'Total force': ftot = float( strlist[3] ) # record total force
    
    try:
        return etot, ftot
    
    except:
        print('\n!!! PW ERROR -- VALUES NOT FOUND IN OUTPUT !!!')
        return -1, -1

def translation_prompt(): # INCOMPLETE

    '''translation prompt'''

    print(f"\nTHERE ARE {nat} ATOMS\n")
    
    for k in range(nat): # display atoms in system
        print(f"{k+1} : {symbols[k]}")

    nat_moved = 1 # number of atoms moved
    atom = rand.randint(0,nat-1) # random atom to translate -- move to translate()
    nsteps = 3 # number of translations
    rhat = rand.randint(0,2) # random direction -- 0 : x, 1 : y, 2 : z
    axes = ['x','y','z']    
    step = 0.01

    '''prompt user about default translation settings'''

    print(f"\n# OF ATOM(S) TRANSLATED: {nat_moved}")
    print(f"NUMBER OF STEPS: {nsteps}")
    print(f"STEP DIRECTION: {axes[rhat]}")
    print(f"STEP SIZE: {step}")

    okay = input("\nDEFAULT SETTINGS OKAY? (y/n): ")

    while okay == 'n':

        print('\n1 : # OF ATOMS TO TRANSLATE')
        print('2 : NUMBER OF STEPS')
        print('3 : STEP DIRECTION')
        print('4 : STEP SIZE')

        # add try/except block later
        selection = input('\nENTER A NUMBER TO CHANGE A SETTING: ')

        if selection == '1': # number of translated atoms block

            try:
                print('\nCURRENT # OF ATOMS TO TRANSLATE:', nat_moved)
                nat_moved = input(f"NUMBER OF ATOMS TO TRANSLATE (MAX {nat}): ")
                
                if 0 < nat_moved <= nat:
                    print(f"NEW ATOM(S) TRANSLATED: {nat_moved}")
                    atoms_moved = []

                    '''n-random-atoms translated'''
                    for i in range(nat_moved): # loop picks atoms to translate
                        n = rand.choice(range(len(symbols))) # random index between 0 and nat
                        if n not in atoms_moved: # do not repeat indices
                            atoms_moved.append()

                    '''n-selected-atoms translated'''
                    """
                    print(f"\nTRANSLATED ATOMS MARKED BY ASTERISK (*)")
                    for k in range(nat): # display translated atoms
                        if k in atoms_moved:
                            print(f"{k+1} : {symbols[k]} *")
                        else:
                            print(f"{k+1} : {symbols[k]}")

                    another = input("CHOOSE ATOMS TO TRANSLATE? (y/n): ")
                    while another.lower() == 'y':

                        index = input("ENTER A NUMBER TO CHOOSE AN ATOM: ")
                        if index not in atoms_moved:
                            atoms_moved.append(index)

                        print(f"\nTRANSLATED ATOMS MARKED BY ASTERISK (*)")
                        for k in range(nat): # display atoms in system
                            if k in atoms_moved:
                                print(f"{k+1} : {symbols[k]} *")
                            else:
                                print(f"{k+1} : {symbols[k]}")

                        another = input("\nCHOOSE ANOTHER ATOM? (y/n): ")
                    """

                else:
                    print(f"ATOM(S) TRANSLATED CANNOT BE {nat_moved}")
                    print("ATOM(S) TRANSLATED NOT CHANGED")
                    nat_moved = 1

            except:
                print(f"\nINVALID RESPONSE. # OF ATOM(S) TRANSLATED NOT CHANGED")






        elif selection == '2': # number of steps block
            
            try:
                
                print('\nCURRENT NUMBER OF STEPS:', nsteps)
                nsteps = input('ENTER NUMBER OF STEPS TO TAKE: ')
                if 0 < nsteps <= 20:
                    print('NEW NUMBER OF STEPS:', nsteps)
                elif nsteps > 20:
                    print('WARNING: NEW NUMBER OF STEPS IS LARGE')
                
            except:
                print('\nSOMETHING WENT WRONG. NUMBER OF STEPS NOT CHANGED')
                
        elif selection == '3': # step direction block
            
            try:
                
                print('\nCURRENT STEP DIRECTION:', axes[rhat])
                rhat = input("ENTER NEW STEP DIRECTION (x,y,z): ")
                
                if rhat.lower() in axes:
                    print('NEW STEP DIRECTION:', rhat) # rhat is a char
                    rhat = axes.find(rhat) # assign index to rhat; rhat is an int
                
            except:
                print('\nSOMETHING WENT WRONG. STEP DIRECTION NOT CHANGED')
                
        elif selection == '4': # step size block
            
            try:
                print('\nCURRENT STEP SIZE:', step)
                random = input('USE RANDOM? (y/n): ')
                
                if random == 'y': step = round(rand.uniform(-0.01,0.01), 4) # one small random step size to use for all difference calculations
                else: step = '0.01'
                
                print('\nNEW STEP SIZE:', step)
                
            except:
                print('\nSOMETHING WENT WRONG. STEP SIZE NOT CHANGED')

        '''confirm settings'''

        print(f"\nATOM(S) TRANSLATED: {nat_moved}")
        print(f"NUMBER OF STEPS: {n}")
        print(f"STEP DIRECTION: {axes[rhat]}")
        print(f"STEP SIZE: {step}")

        try:
            okay = input('SETTINGS OKAY? (y/n): ')
            if okay.lower() != 'y': raise Exception
        
        except:
            okay = 'n'

        return 

def translate(pwx, nat, symbols, positions, energies, forces):

    #step = translation_prompt()

    # settings block -- delete when translation prompt complete
    atom = rand.randint(0,nat-1) # random atom to translate
    n = 3 # number of translations
    rhat = rand.randint(0,2) # random direction -- 0 : x, 1 : y, 2 : z
    axes = ['x','y','z']    
    step = 0.01

    '''translation routine -- uses variables n (# of steps), atom (translated), rhat (step direction), axes (axis strings)'''

    for i in range(1,n+1): # multiple pw runs
        
        print(f'\nRUNNING TEST ITERATION {i}')
        
        positions[atom][rhat] += step # increment position
        
        if i == 1: readfile = 'pw.in' # to read initial input file
        else: readfile = 'test.in' + str(i-1) # to read last input file

        test_input = open(f'test.in{i}','w') # temporary input file creation -- manual open

        with open(readfile) as f: # write new input file
            
            for line in f:
                
                if line.strip() == 'ATOMIC_POSITIONS (bohr)': # find position block
                    
                    test_input.write(line) # copy block title
                    for n in range(nat): # write new position set
                        test_input.write(f"{symbols[n]}   {positions[n][0]}   {positions[n][1]}   {positions[n][2]}\n")
                        f.readline()
                
                else:
                    
                    test_input.write(line) # copy everything else
        
        test_input.close() # manual close; opened outside with-statement
        
        os.system(f'{pwx} < test.in{i} > test.out{i}') # run new pw calculation; proceeds after calculation
        
        #coordinates, newE, newF = read_pw_data(pwxml, needInput=False) # uses read_pw_data function -- moved to module
        pwE, pwF = read_output(f'test.out{i}')
        
        energies.append(pwE)
        forces.append(pwF)
        
        print(f'COMPLETED TEST ITERATION {i}')
    
    print()
    print(32 * '~', 'PW TESTING COMPLETE', 32 * '~')
    
    print('\nTRANSLATION DETAILS:')
    print(f"ATOM (INDEX): '{symbols[atom]}' ({atom+1})")
    print(f'\u0394r({axes[rhat]}) = {step}\n')
        
    return step # may need to return more

def main():
    """read initial pw results & evaluate pw results at new positions"""
    
    # do not use
    # pwxml = 'pwscf.xml' # pw xml file name
    # ntypes, natoms, names, coordinates, e0, f0 = read_pw_data(pwxml) # after running pw ; uses read_pw_data function -- moved to module
    
    # present default settings and prompt user for changes
    makepw, ftype = launch_prompt()
    
    print()
    print(38 * '~', 'RUNNING', 38 * '~')
    
    # run initial input for initial output
    celldim, natoms, ntypes, names, coordinates = read_input('pw.in')
    print('\nRUNNING INITIAL INPUT')
    os.system(f'{makepw} < pw.in > pw.out')
    print('COMPLETED INITIAL PW CALCULATION')
    E0, F0 = read_output('pw.out')
    
    # initialize lists
    pwEnergies, pwForces = [E0], [F0]
    calcforces = []
    errors = []
    
    # run tests
    dr = translate( makepw, natoms, names, coordinates, pwEnergies, pwForces ) # returns step size & number of translations
    
    # remove test files
    try:
        delete = input('PERMANENTLY REMOVE TEMPORARY FILES? (y/n): ')
        
        if delete.lower() == 'y':
            for i in range(1,natoms+1): os.remove(f'test.in{i}')
            for i in range(1,natoms+1): os.remove(f'test.out{i}')

        else:
            print('\nNO APPROVAL: FILES NOT REMOVED')

    except:
        print('\nSOMETHING WENT WRONG. FILES NOT REMOVED')
    
    """NEED STEP SIZE BELOW"""

    '''interpolate and compare'''
    
    # compute forces
    #for i in range(len(pwEnergies)):
    #    
    #    calcforces.append( round( (pwEnergies[i] - pwEnergies[i-1]) / (20 * dr), 6 ) ) # (E2 - E1) / (r2 - r1); 20 * dr = bohr = au
    #    errors.append( round(pwForces[i] - calcforces[i], 6) )
    #
    # evaluate finite differences [ F(x - dx) - F(x + dx) ] / [ 2dx ]
    
    for f in range(1, len(pwEnergies) - 1):
        
         calcforces.append( round( np.linalg.norm((pwEnergies[f-1] - pwEnergies[f+1]) / (2 * dr), 6) )
         errors.append( round(pwForces[f] - calcforces[f]) )
    
    '''display results'''
    
    #print('\npwEnergies (Ry):', pwEnergies)
    #print('pwForces (Ry/au):', pwForces)
    #print('calcForces (dE/dr):', calcforces)
    #print('difference (F - dE/dr):', errors)
    #print('finite differences (Ry/au):', finiteforces) # will be shorter than other arrays

    # plot pw forces v. finite differences ?
    
    print()

    from pandas import DataFrame
    print(DataFrame( { 'Output Forces' : pwForces ,
                       '\u0394E/\u0394r' : ['n/a'] + calcforces + ['n/a'],
                       'Error' :  } ))

    #print(f"Output Forces : {pwForces}")
    #print(f"Difference : {calcforces}")
    #print(f"Finite Differences : {['n/a'] + finiteforces + ['n/a']}")
    #print(f"Error : {errors}")

main()

# read pw.in text files rather than xml -- by default ***DONE***
# add input options, maybe exception handling ***DONE***
# compare (E(x - dx) - E(x + dx)) / (2 * dx) against F component of particle ***DONE***
# evaluate difference between finite difference and pw output (error) ***DONE***
# future task: displace the other atoms in a random direction ***IN PROGRESS***

# force value to use from output should be from the atom changed in the direction changed
# manage temporary files differently
# use a file to store user settings