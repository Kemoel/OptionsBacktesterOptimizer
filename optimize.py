from input.initialization import *
from lib.account_metrics import *
from lib.import_data import *
from lib.indicators import *
from lib.strategy import *
from lib.print_data import *
import time

def main():
    # Start timing code.
    t0 = time.time()

    # Indicator variable values.
    # SMA length.
    sma1_ln_ini = 8
    sma2_ln_ini = 34
    sma3_ln_ini = 200
    # BB sma length, std length, and std multiplier.
    bb_sma_ln_ini = 14
    bb_std_ln_ini = 14
    bb_std_mul_ini = 2
    # KC sma length, atr length, and atr multiplier.
    kc_sma_ln_ini = 3
    kc_atr_ln_ini = 13
    kc_atr_mul_ini = 1.5
    # KC sma length, atr length, and atr multiplier. For strat exit.
    kc_sma_ln_exit = 3
    kc_atr_ln_exit = 14
    kc_atr_mul_exit = 3
    # Momentum length.
    momemtum_ln_ini = 9

    # Get stock data.
    data = get_data()

    # Non iterative values.
    sma1 = sma(data, sma1_ln_ini)
    sma2 = sma(data, sma2_ln_ini)
    sma3 = sma(data, sma3_ln_ini)
    bb_upr = bb(data, 'upr', bb_sma_ln_ini, bb_std_ln_ini, bb_std_mul_ini)
    bb_lwr = bb(data, 'low', bb_sma_ln_ini, bb_std_ln_ini, bb_std_mul_ini)
    kc_upr = kc(data, 'upr', kc_sma_ln_ini, kc_atr_ln_ini, kc_atr_mul_ini)
    kc_lwr = kc(data, 'low', kc_sma_ln_ini, kc_atr_ln_ini, kc_atr_mul_ini)
    momentum = momen(data, momemtum_ln_ini)
    sqz_sig = sqz(data, bb_upr, bb_lwr, kc_upr, kc_lwr)
    bs_sig = bs_rng(data, sma1, sma2)
    trd_data = trade_strat(data, sma1, sma2, momentum, sqz_sig, bs_sig)

    # Optimizing sma1 and sma2 between range.
    def optimizer_loop():
        opt_results = np.zeros((70, 70))
        for tst_1_ln in range(1,20,1):
            for tst_2_ln in range(1,20,1):
                opt_results[tst_1_ln-1][tst_2_ln-1] = back_test_loop(tst_1_ln, tst_2_ln)
                # print(str(sma1_ln_tst)+' '+str(sma2_ln_tst))
        print_all(opt_results)
        print(np.max(opt_results))
        print(np.where(opt_results == np.max(opt_results)))

    # function simulation back test script for iterative testing.
    def back_test_loop(kc_sma_ln_ini, kc_atr_ln_ini):
        kc_upr = kc(data, 'upr', kc_sma_ln_ini, kc_atr_ln_ini, kc_atr_mul_ini)
        kc_lwr = kc(data, 'low', kc_sma_ln_ini, kc_atr_ln_ini, kc_atr_mul_ini)
        sqz_sig = sqz(data, bb_upr, bb_lwr, kc_upr, kc_lwr)
        trd_data = trade_strat(data, sma1, sma2, momentum, sqz_sig, bs_sig)
        # Test if there are trades in range and return account info. If not return 0 for return.
        if(trd_data['trade loc/typ'].loc[strt_dt:end_dt].any()):
            acnt_val_data = acnt_val(data, trd_data)
            acnt_end_val_p = acnt_end_p(acnt_val_data)
        else:
            acnt_end_val_p = 0
        return acnt_end_val_p

    # def multiprocessing_func(kc_sma_ln_ini, kc_atr_ln_ini):
    #     kc_upr = kc(data, 'upr', kc_sma_ln_ini, kc_atr_ln_ini, kc_atr_mul_ini)
    #     kc_lwr = kc(data, 'low', kc_sma_ln_ini, kc_atr_ln_ini, kc_atr_mul_ini)
    #     sqz_sig = sqz(data, bb_upr, bb_lwr, kc_upr, kc_lwr)
    #     trd_data = jfc_trade_strat(data, sma1, sma2, momentum, sqz_sig, bs_sig)
    #     # Test if there are trades in range and return account info. If not return 0 for return.
    #     if(trd_data['trade loc/typ'].loc[strt_dt:end_dt].any()):
    #         acnt_val_data = acnt_val(data, trd_data)
    #         acnt_end_val_p = acnt_end_p(acnt_val_data)
    #     else:
    #         acnt_end_val_p = 0
    #     return acnt_end_val_p

    # if __name__ == '__main__':
    #     opt_results = np.zeros((70, 70))
    #     processes = []
    #     for tst_1_ln in range(1,20,1):
    #         for tst_2_ln in range(1,20,1):
    #             p = multiprocessing.Process(target=multiprocessing_func, args=(tst_1_ln,tst_2_ln,))
    #             processes.append(p)
    #             p.start()
    #     for process in processes:
    #         process.join()
    #     print_all(opt_results)
    #     print(np.max(opt_results))
    #     print(np.where(opt_results == np.max(opt_results)))

    # function simulation back test script for iterative testing.
    optimizer_loop()

    # Print end time.
    print(time.time()-t0)

if __name__ == "__main__":
    main()