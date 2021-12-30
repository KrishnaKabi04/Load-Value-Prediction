import configparser
import numpy as np
import pandas as pd
from datetime import datetime
from PredOutcomeHistory import PredOutcomeHistory

t1= datetime.now()
if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('./config.cfg')
    filename = eval(config.get('DEFAULT', 'tracefile_name'))
    f_name= filename.split('/')[-1].split('.')[0]
    LVPT_index= eval(config.get('ParameterList', 'LVPT_index'))
    LVPT_hist_bit= eval(config.get('ParameterList', 'LVPT_hist_bit'))
    Counter_bit= eval(config.get('ParameterList', 'Counter_bit'))
    threshold= eval(config.get('ParameterList', 'threshold'))
    penalty= eval(config.get('ParameterList', 'Penalty'))

    rows= len(LVPT_index)*len(LVPT_hist_bit)*len(threshold)
    res_mat= np.zeros((rows *11)).reshape(-1,11)
    print('Running for {} different configurations....grab some popcorn!!'.format(res_mat.shape[0]))
    ctr=0
    for i in LVPT_index:
        for hist_bit in LVPT_hist_bit:
            for thresh in threshold:
                pred_hist_obj= PredOutcomeHistory(i, hist_bit, Counter_bit, thresh, penalty)
                p_corr,p_incorr,np_corr,np_incorr = pred_hist_obj.value_prediction(filename)

                if (ctr+1)%10 ==0:
                    print((ctr+1),'configuration completed!')
                #check predicability and unpredicability rate
                potential=  p_corr + np_incorr
                if(p_corr == 0 & p_incorr == 0):
                    accuracy_p= 0
                else:
                    accuracy_p= round(((p_corr )/ ( p_corr + p_incorr) )*100 , 3)
                accuracy_p_np= round(((p_corr + np_corr)/ ( p_corr + p_incorr + np_corr + np_incorr) )*100 , 3)
                coverage= round(((p_corr)/ potential)*100, 3)

                res_mat[ctr]= [i, hist_bit, Counter_bit, thresh, p_corr, p_incorr, np_corr, np_incorr, accuracy_p, accuracy_p_np, coverage]
                ctr= ctr+1

    max_accuracy= np.max(res_mat, axis=0)[8]
    index_max= np.argmax(res_mat, axis=0)[8]
    print('Maximum accuracy considering only correct prediction when PV=AV is:  {},  found for: {} LVPT row, {} hist bits and {} threshold'.format(max_accuracy, res_mat[index_max][0], res_mat[index_max][1], res_mat[index_max][3]))
    #print("LVPT row: {}, LVPT_hist_bit: {}, Counter_bits: {}, Threshold: {}, p_corr: {}, p_incorr: {},np_corr: {}, np_incorr: {}, accuracy_p: {}, accuracy_p_np: {}, coverage : {}".format(res_mat[0][0], res_mat[0][1], res_mat[0][2], res_mat[0][3], res_mat[0][4], res_mat[0][5], res_mat[0][6], res_mat[0][7], res_mat[0][8], res_mat[0][9], res_mat[0][10]))
    df = pd.DataFrame(data=res_mat, columns=["LVPT row", "LVPT_hist_bit", "Counter_bits", "Threshold", 'p_corr', 'p_incorr','np_corr','np_incorr', 'accuracy_p', 'accuracy_p_np', 'coverage'])
    if penalty>1:
        f_name= f_name+'_with_penalty_'+str(penalty)
    excel_filename= './Report/output_for_'+f_name+datetime.now().strftime("_%m_%d_%y_%H%M%S")+'.xlsx'
    writer = pd.ExcelWriter(excel_filename, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    print('Report is available at {}'.format(excel_filename))
    writer.save()
t2= datetime.now()
print("Time taken for execution: {} seconds".format((t2-t1).seconds))
