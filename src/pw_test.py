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
        print('exception raised')
        workdir = '/'.join(workdir)
        print("\nCURRENT WORKING DIRECTORY:", workdir)
        print("CURRENT LOCATION OF PW.X:", pwx)
    
    print('INPUT/OUTPUT FILE TYPE:', ftype)
    
    # add receipt/log option for temporary runs

    try:
        okay = input('\nSETTINGS OKAY? (y/n): ')
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
            okay = input('\nSETTINGS OKAY? (y/n): ')
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

def read_output(txt):
    
    '''reads pw output; returns total energy & total force'''

    with open(txt) as f:
        
        for line in f:
            
            strlist = line.strip().split()

            if strlist == []: continue # skip empty lines
                
            elif ' '.join(strlist[1:3]) == 'total energy' and strlist[-1] == 'Ry': etot = float( strlist[-2] ) # record total energy
            df = -1 # dummy value until following routine completed
 
            # need atom moved & translation direction
            #elif strlist[0] == 'atom' and strlist[1] == atom: # atom = translated atom index
            #    fdir = rdir - 3 # rdir = translation direction
            #    df = strlist[fdir]

    try:
        return etot, df
    
    except:
        print('\n!!! PW ERROR -- VALUES NOT FOUND IN OUTPUT !!!')
        return -1, -1

def translation_prompt(nat, symbols, nat_moved, nsteps, axes): # INCOMPLETE
    '''translation prompt'''

    # initialize translation direction

    print(f"\nTHERE ARE {nat} ATOMS\n")
    
    for k in range(nat): # display atoms in system
        print(f"{k+1} : {symbols[k]}")

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
                # show atoms and their indices
                print('\nCURRENT # OF ATOMS TO TRANSLATE:', nat_moved)
                nat_moved = input(f"NUMBER OF ATOMS TO TRANSLATE (MAX {nat}): ")
                
                # value cannot be zero or larger than number of atoms in system
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
                    nat_moved = 1 # translate only 1 atom if input is bad

            except:
                print(f"\nINVALID RESPONSE. # OF ATOM(S) TRANSLATED NOT CHANGED")
                nat_moved = 1 # translate 1 atom if input is bad






        elif selection == '2': # number of steps block
            
            try:
                
                print('\nCURRENT NUMBER OF STEPS:', nsteps)
                nsteps = input('ENTER NUMBER OF STEPS TO TAKE: ')
                if 0 < nsteps <= 20:
                    print('NEW NUMBER OF STEPS:', nsteps)
                elif nsteps > 20:
                    print('WARNING: NEW NUMBER OF STEPS IS LARGE (GREATER THAN 20)')
                
            except:
                print('\nSOMETHING WENT WRONG. NUMBER OF STEPS NOT CHANGED')
                nsteps
                
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

def translate(pwx):

    '''initialize translation lists & settings, allow user to change settings, and run translation routine'''

    # run initial input for initial output
    celldim, natoms, ntypes, names, coordinates = read_input('pw.in')
    print('\nRUNNING INITIAL INPUT')
    os.system(f'{makepw} < pw.in > pw.out')
    print('COMPLETED INITIAL PW CALCULATION')
    E0, F0 = read_output('pw.out')

    # initialize lists
    pwEnergies = [E0]
    pwForces = [F0]
    calcForces = ['n/a']
    errors = ['n/a']

    # initialize translation values
    #atom = rand.randint(0,nat-1) # random atom to translate -- move to translate()
    nat_moved = 1 # number of atoms moved
    nsteps = 3 # number of translations
    #rhat = rand.randint(0,2) # random direction -- 0 : x, 1 : y, 2 : z
    axes = ['x','y','z']    
    #step = 0.01

    # UNPACK TRANSLATION SETTINGS = translation_prompt(natoms, names, nat_moved, nsteps, axes)

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
    
    # need to specify atom and direction to be changed here
    # translate_prompt()
    # translate(makepw)

    # run initial input for initial output
    #celldim, natoms, ntypes, names, coordinates = read_input('pw.in')
    #print('\nRUNNING INITIAL INPUT')
    #os.system(f'{makepw} < pw.in > pw.out')
    #print('COMPLETED INITIAL PW CALCULATION')
    #E0, F0 = read_output('pw.out')
    
    # initialize lists
    #pwEnergies, pwForces = [E0], [F0]
    #calcforces = []
    #errors = []
    
    # run tests
    translate(makepw) # returns step size & number of translations
    
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
    
    for f in range(1, len(pwEnergies) - 1):
        
         calcForces.append( -1 * round( (pwEnergies[f-1] - pwEnergies[f+1]) / (2 * dr), 6 ) )
         errors.append( round(pwForces[f] - calcForces[f-1], 6) )
    
    '''display results'''

    print(f"\nOutput Energies : {pwEnergies}")
    print(f"Output Forces : {pwForces}")
    print(f"Differences : {calcForces + ['n/a']}")
    print(f"Error : {errors + ['n/a']}")
    print()

    # display results graphically?

main()

# read pw.in text files rather than xml -- by default ***DONE***
# add input options, maybe exception handling ***DONE***
# compare (E(x - dx) - E(x + dx)) / (2 * dx) against F component of particle ***DONE***
# evaluate difference between finite difference and pw output (error) ***DONE***
# future task: displace the other atoms in a random direction ***IN PROGRESS***

# force value to use from output should be from the atom changed in the direction changed
# manage temporary files differently
# use a file to store user settings