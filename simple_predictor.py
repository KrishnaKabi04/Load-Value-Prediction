import sys
import numpy as np

np_incorr =0
np_corr= 0
p_corr =0
p_incorr= 0

class ValuePredictor:
    def __init__(self):
        self.lvpt_sizebits= 10
        self.lct_sizebits= 8
        self.lvpt= np.zeros(2**self.lvpt_sizebits)           #direct mapped
        self.lct= np.zeros(2**self.lct_sizebits)             #saturating counter
        self.lct_bits= (1<<2)-1
        #print('self.lct_bits' ,self.lct_bits)

    def fetch_instruction(self,line):
        #print(line)
        self.PC_address= line[0][:-1]
        self.oper= line[1]
        self.mem_add= line[2][:-1]
        self.actual_v= int(line[3], 16)



if __name__ == '__main__':

    vp= ValuePredictor()
    with open(sys.argv[1], 'r') as file:
        content = file.readlines()
        for line in content:

            if "#eof" not in line:
                vp.fetch_instruction(line.strip().split())
                lvpt_index= int(vp.PC_address, 16)  & ((1<<vp.lvpt_sizebits)-1)
                lct_index= int(vp.PC_address, 16) & ((1<<vp.lct_sizebits)-1)
                pred_value=  vp.lvpt[lvpt_index]

                if pred_value == vp.actual_v:
                    if vp.lct[lct_index] ==0:
                        np_incorr= np_incorr+1
                    if vp.lct[lct_index] in (1,2,3):
                        p_corr= p_corr+1
                    vp.lct[lct_index] = min(vp.lct_bits, vp.lct[lct_index] +1)
                else:
                    if vp.lct[lct_index] != 0:
                        p_incorr= p_incorr+1
                    else:
                        np_corr= np_corr+1
                    vp.lct[lct_index]= max(0, vp.lct[lct_index]-1)

                vp.lvpt[lvpt_index] = vp.actual_v

    #check predicability and unpredicability rate
    print("p_corr= {}, p_incorr= {}, np_corr= {}, np_incorr= {} : ".format(p_corr,p_incorr,np_corr,np_incorr))
    potential=  p_corr + np_incorr
    accuracy_p= round(((p_corr )/ ( p_corr + p_incorr) )*100 , 3)
    accuracy_p_np= round(((p_corr + np_corr)/ ( p_corr + p_incorr + np_corr + np_incorr) )*100 , 3)
    coverage= round(((p_corr)/ potential)*100, 3)
    print('accuracy (only considering p_corr): ', accuracy_p)
    print('accuracy (considering p_corr and np_corr): ', accuracy_p_np)
    print('Coverage: ', coverage)




