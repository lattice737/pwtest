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
    
    workdir = os.getcwd().split('/')
    pwx = pwstr = '/Users/nicholas/Desktop/qe/bin/pw.x' # pwx: not to be changed, pwstr: to be manipulated
    ftype = 'txt'
    
    '''prompt user about default settings'''

    try:
        with open('./paths.txt') as f:
            for line in f:
                strlist = line.strip().split()
                if strlist == []: continue
                elif strlist[0] == 'workdir':
                    os.chdir(strlist[-1])
                    workdir = strlist[-1].split('/')
                    if len(workdir) >= 6: 
                        workdir = f"/{workdir[1]}/{workdir[2]}/ ... /{workdir[-2]}/{workdir[-1]}" # attempt grep?
                    else:
                        workdir = '/'.join(workdir)
                elif strlist[0] == 'pwx':
                    pwx = strlist[-1]
                    pwlist = strlist[-1].split('/')
                    if len(pwlist) >= 6:
                        pwstr = f"/{pwlist[1]}/{pwlist[2]}/ ... /{pwlist[-2]}/{pwlist[-1]}" # attempt grep?
                    else:
                        pwstr = '/'.join(pwlist)
            
            print("\nCURRENT WORKING DIRECTORY:", workdir)
            print("CURRENT LOCATION OF PW.X:", pwstr)

    except:
        workdir = '/'.join(workdir)
        print("\nCURRENT WORKING DIRECTORY:", workdir)
        print("CURRENT LOCATION OF PW.X:", pwx)
    
    print('INPUT/OUTPUT FILE TYPE:', ftype)
    
    # add receipt/log option for temporary runs

    try:
        okay = input('\nFILE SETTINGS OKAY? (y/n): ')
        if okay.lower() != 'y' and okay.lower() != 'n':
            print('\nINVALID RESPONSE. CURRENT SETTINGS WILL BE USED')
    except KeyboardInterrupt: # end program when input is CTRL + C
        print('\nEXITING PROGRAM. GOODBYE')
        exit()
    except:
        print('\nSOMETHING WENT WRONG. CURRENT SETTINGS WILL BE USED')
        okay = 'y'
    
    while okay.lower() == 'n': # menu block
        
        print('\n1 : WORKING DIR')
        print('2 : PW.X PATH')
        print('3 : I/O TYPE')
        
        try:
            selection = input('\nENTER NUMBER TO CHANGE A SETTING: ')
        except:
            print('\nINVALID SELECTION')
            okay = 'n'
        
        if selection == '1': # working directory path block
            
            try:
                
                print('\nCURRENT WORKING DIRECTORY:', workdir)
                newdir = input('ENTER ABSOLUTE PATH OF WORKING DIRECTORY: ').split('/')
                if len(newdir) >= 6:
                    print('\nNEW WORKING DIRECTORY:', f"/{newdir[1]}/{newdir[2]}/ ... /{newdir[-2]}/{newdir[-1]}")
                    workdir = '/'.join(newdir)
                else:
                    workdir = '/'.join(newdir)

                with open('paths.txt','w') as f: # store new directory path
                    f.write("'''paths of user working directory & pw.x'''\n\n")
                    f.write(f"workdir = {workdir}\n")
                    f.write(f"pwx = {pwx}\n")

                os.chdir(workdir)

            except:
                print('\nSOMETHING WENT WRONG. WORKING DIRECTORY NOT CHANGED')

        elif selection == '2': # pw.x path block
            
            try:
                
                print('\nCURRENT LOCATION OF PW.X:', pwstr)
                pwx = input('ENTER ABSOLUTE PATH OF PW.X LOCATION: ')
                print('NEW LOCATION OF PW.X:', pwx)

                with open('paths.txt','w') as f: # store new pw.x path
                    f.write("'''paths of user working directory & pw.x'''\n\n")
                    f.write(f"workdir = {workdir}\n")
                    f.write(f"pwx = {pwx}\n")
                
            except:
                print('\nSOMETHING WENT WRONG. PW.X PATH NOT CHANGED')
                
        elif selection == '3': # i/o file type block
            
            try:
                
                print('\nCURRENT INPUT/OUTPUT FILE TYPE:', ftype)
                xml = input('USE XML? (y/n): ')
                
                if xml == 'y': ftype = 'xml'
                else: ftype = 'txt'
                
                print('NEW INPUT/OUTPUT FILE TYPE:', ftype)
                
            except:
                print('\nSOMETHING WENT WRONG. FILE TYPE NOT CHANGED')
        
        print('\nCURRENT WORKING DIRECTORY:', workdir)
        print('LOCATION OF PW.X:', pwx) # attempt grep?
        print('INPUT/OUTPUT FILE TYPE:', ftype)
        
        try:
            okay = input('\nFILE SETTINGS OKAY? (y/n): ')
            if okay.lower() != 'y': raise Exception
        
        except:
            okay = 'n'
        
    #os.chdir('/Users/nicholas/gitwork/pwtest/test') # developer machine
    ftype = 'txt' # xml reading not enabled yet
        
    return pwx, ftype

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

def read_output(txt, nat, atoms_moved, move_directions):
    
    '''reads pw output; returns total energy & total force'''

    force_components = ['n/a' for i in range(nat)]

    with open(txt) as f:
        
        for line in f:
            
            strlist = line.strip().split()

            if strlist == []: continue # skip empty lines
                
            elif ' '.join(strlist[1:3]) == 'total energy' and strlist[-1] == 'Ry':
                etot = float( strlist[-2] ) # record total energy

            elif ' '.join(strlist[:2]) == 'Forces acting': # find block with forces acting on atoms
                
                f.readline()
                for v in range(nat): # WORKING

                    blocklinelist = f.readline().strip().split()

                    if int(blocklinelist[1]) in atoms_moved: # if atom index is in list of atoms to be moved
                        
                        atom_sysindex = int(blocklinelist[1]) # atom index in system from 1 to nat
                        for w in range(len(atoms_moved)):

                            if int(atoms_moved[w]) == atom_sysindex: # 
                                atom_listindex = int(atoms_moved[w]) - 1 # index in system -> index in list
                            else: continue

                            force_components[ atom_listindex ] = float( blocklinelist[ move_directions[w] - 3 ])
                            
                    else:
                        continue

    try:
        return etot, force_components
    
    except:
        print('\n!!! ERROR -- VALUES NOT FOUND IN OUTPUT !!!')
        return -1, -1

def translation_prompt(nat, symbols, n_steps, axislist):
    
    '''translation prompt'''

    # initial values -- len(atoms_moved) should always equal len(move_directions) should always equal nat_moved
    nat_moved = 1
    atoms_moved = [rand.randint(1,nat)] # system indices 1 to nat
    move_directions = [rand.randint(0,2)] # x:0, y:1, z:2
    stepsize = 0.01

    # display atoms in system
    print(f"\nTHIS SYSTEM HAS {nat} ATOM(S):")
    for k in range(nat):
        print(f"{k+1} : {symbols[k]}")

    '''prompt user about default translation settings'''

    print("\nATOM(S) TO TRANSLATE:")
    for i in range(nat_moved):
        print(f"{atoms_moved[i]} : {symbols[ atoms_moved[i]-1 ]} \u0394{axislist[ move_directions[i] ]}") # n-atom : symbol delta(x or y or z)
    print("\nNUMBER OF STEPS:", n_steps)
    print("STEP SIZE:", stepsize)

    try:
        okay = input("\nTRANSLATION SETTINGS OKAY? (y/n): ")
        if okay.lower() != 'y' and okay.lower() != 'n':
            print('\nINVALID RESPONSE. CURRENT SETTINGS WILL BE USED')
    except KeyboardInterrupt:
        print('\nEXITING PROGRAM. GOODBYE')
        exit()
    except:
        print('\nSOMETHING WENT WRONG. CURRENT SETTINGS WILL BE USED')
        okay = 'y'

    while okay.lower() == 'n':

        print('\n1 : ATOM(S) TO TRANSLATE')
        print('2 : NUMBER OF STEPS')
        print('3 : STEP DIRECTION(S)')
        print('4 : STEP SIZE')

        try:
            selection = int(input('\nENTER A NUMBER TO CHANGE A SETTING: '))
            if not 0 < selection < 5:
                print('\nINVALID RESPONSE. CURRENT SETTINGS WILL BE USED')
                okay = 'y'
        except:
            print('\nSOMETHING WENT WRONG. CURRENT SETTINGS WILL BE USED')
            okay = 'y'

        if selection == 1: # number of translated atoms block

            try:
                # shows atoms to be translated
                print("\nASTERISKED ATOMS WILL BE TRANSLATED:\n")
                for k in range(nat):
                    if k+1 in atoms_moved:
                        print(f"{k+1} : {symbols[k]} *")
                    else:
                        print(f"{k+1} : {symbols[k]}")

                atom = int(input("\nENTER A NUMBER TO MARK AN ATOM FOR TRANSLATION: "))

                # value cannot be zero or larger than number of atoms in system
                if 0 < atom <= nat:

                    if atom in atoms_moved:
                        print('\nTHIS ATOM IS ALREADY BEING TRANSLATED')
                    
                    elif atom not in atoms_moved:
                        atoms_moved.append(atom)
                        direction = input("\nWHICH DIRECTION? (x,y,z): ")
                        if direction.lower() in axislist:
                            move_directions.append(axislist.index(direction))
                            nat_moved += 1
                        else:
                            print('\nINVALID RESPONSE. NO CHANGES MADE')
                            atoms_moved.remove(atom)

                else:
                    print("\nINVALID RESPONSE. ATOM(S) TRANSLATED NOT CHANGED")
                    nat_moved = 1 # translate only 1 atom if input is bad

            except:
                print(f"\nSOMETHING WENT WRONG. ATOM(S) TRANSLATED NOT CHANGED")
                atoms_moved.remove(atom)

        elif selection == 2: # number of steps block
            
            try:
                
                print('\nCURRENT NUMBER OF STEPS:', n_steps)
                n_steps = int(input('ENTER NUMBER OF STEPS TO TAKE: '))
                if 0 < n_steps <= 20:
                    print('NEW NUMBER OF STEPS:', n_steps)
                elif n_steps > 20:
                    print('\nWARNING: NEW NUMBER OF STEPS IS LARGE (GREATER THAN 20)')
                    print('NEW NUMBER OF STEPS:', n_steps)
                
            except Exception as e:
                print(f'\nSOMETHING WENT WRONG: {e} -- NUMBER OF STEPS NOT CHANGED')
                n_steps = 3 # default chosen arbitrarily
                
        elif selection == 3: # step direction block
            
            try:
                
                print("\nASTERISKED ATOM(S) WILL BE TRANSLATED:\n")
                for k in range(nat):
                    if k+1 in atoms_moved:
                        print(f"{k+1} : {symbols[k]} *")
                    else:
                        print(f"{k+1} : {symbols[k]}")

                atom = int(input("\nENTER A NUMBER TO CHANGE AN ATOM'S TRANSLATION DIRECTION: "))

                if 0 < atom <= nat: # selection must be nonzero and not greater than the total number of particles

                    if atom in atoms_moved: # selection must already be tagged for translation
                        
                        print(f"\nCURRENT DIRECTION TO TRANSLATE ATOM {atom} : {axislist[ move_directions[ int(atoms_moved.index(atom)) ] ]}")
                        direction = input("ENTER NEW STEP DIRECTION (x,y,z): ")
                    
                        if direction.lower() in axislist:
                            print('\nNEW STEP DIRECTION:', direction) # rhat is a char
                            move_directions[ int(atoms_moved.index(atom)) ] = axislist.index(direction) # replace direction index
                        else:
                            print(f'DIRECTION CANNOT BE {direction}. DIRECTION NOT CHANGED')

                    else:
                        print("\nTHAT ATOM IS NOT BEING TRANSLATED. STEP DIRECTION NOT CHANGED")

                else:
                    print("\nINVALID RESPONSE. STEP DIRECTION NOT CHANGED")

            except:
                print('\nSOMETHING WENT WRONG. STEP DIRECTION NOT CHANGED')
                
        elif selection == 4: # step size block
            
            try:
                print('\nCURRENT STEP SIZE:', stepsize)
                random = input('USE RANDOM? (y/n): ')
                
                if random.lower() == 'y':
                    stepsize = round(rand.uniform(-0.01,0.01), 4) # one small random step size to use for all difference calculations
                elif random == 'n':
                    other = input('\nUSE YOUR OWN VALUE? (y/n): ')
                    if other.lower() == 'y':
                        stepsize = float(input('ENTER A VALUE: '))
                    else:
                        print('\nINVALID RESPONSE. STEP SIZE NOT CHANGED')
                else:
                    step = 0.01
                
                print('\nNEW STEP SIZE:', stepsize)
                
            except:
                print('\nSOMETHING WENT WRONG. STEP SIZE NOT CHANGED')

        '''confirm settings'''

        print("\nATOM(S) TO TRANSLATE:")
        for i in range(nat_moved):
            print(f"{atoms_moved[i]} : {symbols[ atoms_moved[i]-1 ]} \u0394{axislist[ move_directions[i] ]}") # n-atom : symbol delta(x or y or z)
        print("\nNUMBER OF STEPS:", n_steps)
        print("STEP SIZE:", stepsize)

        try:
            okay = input('\nTRANSLATION SETTINGS OKAY? (y/n): ')
            if okay.lower() != 'y':
                raise Exception
        
        except:
            okay = 'n'

    return atoms_moved, n_steps, move_directions, stepsize # in menu order

def translate(pwx):

    '''initialize translation settings & lists, allow user to change settings, and run translation routine'''

    nsteps = 3 # number of translations, default 3
    axes = ['x','y','z'] # axis string list

    # read input file, but don't run until translation settings confirmed
    celldim, natoms, ntypes, names, coordinates = read_input('pw.in')

    # confirm translation settings
    atoms_to_translate, nsteps, translate_directions, step  = translation_prompt(natoms, names, nsteps, axes)

    print()
    print(38 * '~', 'RUNNING', 38 * '~')

    # run initial input for initial output
    print('\nRUNNING PW WITH INITIAL INPUT')
    os.system(f'{pwx} < pw.in > pw.out')
    print('COMPLETED INITIAL PW CALCULATION')
    E0, F0 = read_output('pw.out', natoms, atoms_to_translate, translate_directions)

    # initialize lists
    energies = [E0]
    forces = [F0]

    '''translation routine -- uses variables n (# of steps), atom (translated), rhat (step direction), axes (axis strings)'''

    for i in range(1,nsteps+1): # multiple pw runs
        
        print(f'\nRUNNING TEST ITERATION {i}')

        for o in range(len(atoms_to_translate)): # change positions of all atoms to be translated
            coordinates[ atoms_to_translate[o] - 1 ][ translate_directions[o] ] += step # increment position

        if i == 1: readfile = 'pw.in' # to read initial input file
        else: readfile = 'test.in' + str(i-1) # to read last input file

        test_input = open(f'test.in{i}','w') # temporary input file creation -- manual open

        with open(readfile) as f: # write new input file
            
            for line in f:
                
                if line.strip() == 'ATOMIC_POSITIONS (bohr)': # find position block

                    test_input.write(line) # copy block title
                    for j in range(natoms): # write new position set
                        test_input.write(f"{names[j]}   {coordinates[j][0]}   {coordinates[j][1]}   {coordinates[j][2]}\n")
                        f.readline()
                
                else:
                    
                    test_input.write(line) # copy everything else
        
        test_input.close() # manual close; opened outside with-statement
        
        os.system(f'{pwx} < test.in{i} > test.out{i}') # run new pw calculation; proceeds after calculation

        #coordinates, newE, newF = read_pw_data(pwxml, needInput=False) # uses read_pw_data function -- moved to module
        pwE, pwF = read_output(f'test.out{i}', natoms, atoms_to_translate, translate_directions)
        energies.append(pwE)
        forces.append(pwF)
        
        print(f'COMPLETED TEST ITERATION {i}')
    
    print()
    print(32 * '~', 'PW TESTING COMPLETE', 32 * '~')
    print()
    
    # at this point, len(atoms_to_translate) = len(translate_directions) = len(forces) where each index has corresponding atomic translation data across lists
    # atoms_to translate[index] : translate_directions[index] : forces[index] -- nth-atom index in system : nth-atom translation direction : nth-atom force component

    return natoms, names, atoms_to_translate, translate_directions, nsteps, step, energies, forces

def main():
    """read initial pw results & evaluate pw results at new positions"""
    
    # do not use
    # pwxml = 'pwscf.xml' # pw xml file name
    # ntypes, natoms, names, coordinates, e0, f0 = read_pw_data(pwxml) # after running pw ; uses read_pw_data function -- moved to module
    
    # present default settings and prompt user for changes
    makepw, ftype = launch_prompt()
    
    # run tests
    natoms, symbols, mvatoms, mvdir, numsteps, stepsize, pwEnergies, pwForces = translate(makepw) # returns nat, moved atoms, move directions, step size, and output energies & forces

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

    '''interpolate and compare'''
    
    calcForcelist = []
    errors = []

    for a in range(1, len(pwEnergies) - 1):
        calcForcelist.append( round( (pwEnergies[a-1] - pwEnergies[a+1]) / (2 * stepsize), 6 ) )
    calcForces = ['n/a'] + calcForcelist + ['n/a']

    print("\nOutput Forces [ atom1, atom2, atom3, etc ]")
    for z in range(len(pwForces)):
        if z == 0:
            print(f"Initial Run: {pwForces[z]}")
        else:
            print(f"Test Run {z}: {pwForces[z]}")

    print("\nFinite Differences")
    for b in calcForces:
        print(b)

    for c in range(len(mvatoms)):

        if mvdir[c] == 0: axis = 'x'
        elif mvdir[c] == 1: axis = 'y'
        elif mvdir[c] == 2: axis = 'z'

        print(f"\n{mvatoms[c]} : {symbols[mvatoms[c]-1]} (\u0394{axis})")

        pwForcelist = []
        for f in pwForces:
            print(f[ mvatoms[c]-1 ])
            pwForcelist.append(f[mvatoms[c]-1])

    print()
    
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy.interpolate import UnivariateSpline

    x = np.arange(0, numsteps * stepsize + stepsize, stepsize)

    # plot pw output and best fit curve
    y1 = np.array(pwForcelist)
    s = UnivariateSpline(x, y1, s=0)
    xs = np.linspace(0, (len(y1)-1) * stepsize, 100)
    ys = s(xs)

    # plot finite difference and interpolation
    y2 = np.array(calcForcelist)
    z = np.polyfit(x[1:-1], y2, 1) # best fit line
    p = np.poly1d(z)

    #print(x)
    #print(y1)
    #print(x[1:-1])
    #print(y2)

    plt.scatter(x, y1, c='r') # scatter method, not plot
    plt.scatter(x[1:-1], y2, c='b')
    plt.plot(x, p(x), "r")
    plt.plot(xs, ys)

    plt.xlabel(f'\u0394{axis}')
    plt.ylabel('Force (N)')

    plt.show()

main()

# read pw.in text files rather than xml -- by default ***DONE***
# add input options, maybe exception handling ***DONE***
# compare (E(x - dx) - E(x + dx)) / (2 * dx) against F component of particle ***DONE***
# evaluate difference between finite difference and pw output (error) ***DONE***
# future task: displace the other atoms in a random direction ***DONE***

# force value to use from output should be from the atom changed in the direction changed ***DONE***
# manage temporary files differently
# use a file to store user settings ***DONE***
