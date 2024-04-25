# my simple 6502 assembler
# 2022 by thomasg
# Version 0.0.1

import argparse

def asmfile(filename):
    instlist = [['NOP\n', 0xEA, 1], 
                ['LDA',  0xA9, 2], 
                ['LDAA', 0xAD, 3], 
                ['STA', 0x8D, 3], 
                ['JMP', 0x4C, 3], 
                ['ADC', 0x69, 2], 
                ['SBC', 0xE9, 2], 
                ['TAX\n', 0xAA, 1], 
                ['TAY\n', 0xA8, 1], 
                ['DEX\n', 0xCA, 1], 
                ['INX\n', 0xE8, 1],
                ['LDX', 0xA2, 2],  
                ['CPX', 0xE0, 2], 
                ['BNE', 0xD0, 2] 
                ]
    
    
    lbllist = {}
    prgcnt = 0x800
    
    prg = bytearray([])
    instr = ''

    inf = open(filename, 'r')
    lines = inf.readlines()
   
  
    # parsing
    print("parsing...")
    for line in lines:
        print(hex(prgcnt),  ": ",  line)
        try:
            instr, data = line.split(' ')
            d = data
            instr = instr.upper()
        except:
            instr = line
            
        if instr == 'LBL':
            lbllist[data] = prgcnt
            print("Declare Label: ",  data,  " at ",  hex(prgcnt))
        for ins in instlist:
            if instr == ins[0]:
                prgcnt += ins[2]
                print(prgcnt, ins)
                
    #print(lbllist)
    


    prgcnt = 0x800
    print("assembling...")
    for line in lines:
        print(hex(prgcnt),  ": ",  line)
        try:
            instr, data = line.split(' ')
            #d = data
            instr = instr.upper()
        except:
            instr = line
                
        if instr == 'JMP':
            prg.append(0x4C)
            adr = lbllist[data]
            adrhex = adr.to_bytes(2, byteorder='little')
            print("JMP to ",  hex(adr))
            prg = prg + adrhex
            prgcnt += 3
        elif instr == 'BNE':
            prg.append(0xD0)
            prgcnt += 1
            adr = lbllist[data]
            lbladr = prgcnt - adr
            if lbladr < prgcnt:
                val = 0xFF - lbladr
            else:
                val = lbladr
            
            valbin = val.to_bytes(2, byteorder='little')
            print("Backw: ", str(lbladr), "val: ", str(val))
            prg = prg + valbin[0].to_bytes(1, byteorder='little')
            prgcnt += 1
        else:
            for ins in instlist:
                if instr == ins[0]:
                    prg.append(ins[1])
                    if ins[2] == 1: #  1 byte
                        prgcnt += 1
                    if ins[2] == 2: # 2 bytes
                        val = bytearray.fromhex(data[0:2])
                        prg = prg + val
                        prgcnt += 2
                    if ins[2] == 3: # 3bytes
                        valH = bytearray.fromhex(data[0:2])
                        valL = bytearray.fromhex(data[2:4])
                        prg = prg + valL
                        prg = prg + valH
                        prgcnt += 3
            
            print(ins)
   
    print("prglen: ",  prgcnt)
    inf.close()
    
    print("Asm finished!")
    
    print(prg)
    
    rom = prg + bytearray([0xea] * (8192 - len(prg)))

    rom[0x1ffc] = 0x00
    rom[0x1ffd] = 0x80
    
    print("writing file..")
    try:
        f = open(filename + '.bin', 'wb')
        f.write(bytes(rom))
        f.close()
        print("Success")
    except:
        print("Error writing binary!")
    
  
        
#asmfile("test1.asm")
asmfile("branchtest1.asm")
#asmfile("test2.asm")
    
#parser = argparse.ArgumentParser()
#parser.add_argument('-asmfile', help='Assembly File')
#parser.add_argument('-cpuload', help='Load CPU with Bin File')
#parser.add_argument('-cpuport', help='COM Port for Load')
#args = parser.parse_args()

#if args.asmfile is not None:
#    try:
#        asmfile(args.asmfile)
#        print("Success!")
#    except:
#        print("asmfile Error!")
