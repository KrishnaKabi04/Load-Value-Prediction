import sys
import numpy as np
import configparser

class PredOutcomeHistory:
    def __init__(self, lvpt_sizebits, hist_bits, ce_bits, thresh, penalty):
        self.lvpt_sizebits= lvpt_sizebits
        self.p_out_ht= np.zeros(2**lvpt_sizebits * 2).reshape(2**lvpt_sizebits,2)     #direct mapped
        self.hist_bits=  (1<<hist_bits)-1
        self.ce= [0] * (2**hist_bits)
        self.ce_bits= (1<<ce_bits)-1  ##saturating counter
        self.threshold= thresh
        self.penalty= penalty
        self.np_incorr =0
        self.np_corr= 0
        self.p_corr =0
        self.p_incorr= 0

    def fetch_instruction(self,line):
        self.PC_address= line[0][:-1]
        self.oper= line[1]
        self.mem_add= line[2][:-1]
        self.actual_v= int(line[3], 16)

    def value_prediction(self, file_name):

        with open(file_name, 'r') as file:
            content = file.readlines()
            for line in content:
                if "#eof" not in line:
                    self.fetch_instruction(line.strip().split())

                    p_out_ht_index= int(self.PC_address, 16) & ((1<<self.lvpt_sizebits)-1)
                    #print('LVPT index: {} LCT index: {}'.format(p_out_ht_index, lct_index))
                    pred_value=  self.p_out_ht[p_out_ht_index][1]
                    ce_index= int(self.p_out_ht[p_out_ht_index][0])
                    confidence= self.ce[ce_index]
                    if confidence > self.threshold:
                        if pred_value == self.actual_v:
                            #predicted right
                            #increase confidence by 1
                            self.ce[ce_index]= min(self.ce_bits, self.ce[ce_index]+1)

                            #shift the history table with 1 since PV==AV
                            self.p_out_ht[p_out_ht_index][0] = ((int(self.p_out_ht[p_out_ht_index][0]) << 1) |1) & self.hist_bits
                            self.p_corr= self.p_corr+1
                        else:

                            #decrease confidence by penalty
                            self.ce[ce_index]= max(0, self.ce[ce_index]- self.penalty)

                            #shift the history table with 0 since PV!=AV
                            self.p_out_ht[p_out_ht_index][0] = (int(self.p_out_ht[p_out_ht_index][0]) << 1) & self.hist_bits
                            self.p_incorr= self.p_incorr+1
                    else:
                        if pred_value == self.actual_v:
                            #predicted wrong
                            #increase confidence by 1
                            self.ce[ce_index]= min(self.ce_bits, self.ce[ce_index]+1)
                            #shift the history table with 1 since PV==AV
                            self.p_out_ht[p_out_ht_index][0] = ((int(self.p_out_ht[p_out_ht_index][0]) << 1) |1) & self.hist_bits
                            self.np_incorr= self.np_incorr+1
                        else:
                            self.np_corr= self.np_corr+1
                            #decrease confidence by penalty since we were right to not predict
                            self.ce[ce_index]= max(0, self.ce[ce_index]- self.penalty)

                            #shift the history table with 0 since PV!=AV
                            self.p_out_ht[p_out_ht_index][0] = (int(self.p_out_ht[p_out_ht_index][0]) << 1) & self.hist_bits

                    self.p_out_ht[p_out_ht_index][1] = self.actual_v

        return self.p_corr,self.p_incorr,self.np_corr,self.np_incorr





