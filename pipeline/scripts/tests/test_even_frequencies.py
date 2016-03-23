from __future__ import print_function
import sys
import unittest
import traceback
import os
import numpy as np
import numpy.testing as npt

# Append the path of the module to the syspath
sys.path.append('..')
from even_frequencies import check_assertion, get_even_frequencies


class TestEvenFrequencies(unittest.TestCase):
    def setUp(self):
        self.freq_array_arrange = np.arange(10)
        self.freq_array_1edge_2groups = np.array([2.,3.,6.,7.])
        self.f5 =  np.array(
          [  1.16917419e+08,   1.16954041e+08,   1.16990662e+08,
          1.17027283e+08,   1.17063904e+08,   1.17112732e+08,
          1.17149353e+08,   1.17185974e+08,   1.17222595e+08,
          1.17259216e+08,   1.17308044e+08,   1.17344666e+08,
          1.17381287e+08,   1.17417908e+08,   1.17454529e+08,
          1.17503357e+08,   1.17539978e+08,   1.17576599e+08,
          1.17613220e+08,   1.17649841e+08,   1.17698669e+08,
          1.17735291e+08,   1.17771912e+08,   1.17808533e+08,
          1.17845154e+08,   1.17893982e+08,   1.17930603e+08,
          1.17967224e+08,   1.18003845e+08,   1.18040466e+08,
          1.18089294e+08,   1.18125916e+08,   1.18162537e+08,
          1.18199158e+08,   1.18235779e+08,   1.18284607e+08,
          1.18321228e+08,   1.18357849e+08,   1.18394470e+08,
          1.18431091e+08,   1.18479919e+08,   1.18516541e+08,
          1.18553162e+08,   1.18589783e+08,   1.18626404e+08,
          1.18675232e+08,   1.18711853e+08,   1.18748474e+08,
          1.18785095e+08,   1.18821716e+08])
        self.f3 = np.array(
          [  1.55992126e+08,   1.56053162e+08,   1.56114197e+08,
          1.56187439e+08,   1.56248474e+08,   1.56309509e+08,
          1.56382751e+08,   1.56443787e+08,   1.56504822e+08,
          1.56578064e+08,   1.56639099e+08,   1.56700134e+08,
          1.56773376e+08,   1.56834412e+08,   1.56895447e+08,
          1.56968689e+08,   1.57029724e+08,   1.57090759e+08,
          1.57164001e+08,   1.57225037e+08,   1.57286072e+08,
          1.57359314e+08,   1.57420349e+08,   1.57481384e+08,
          1.57554626e+08,   1.57615662e+08,   1.57676697e+08,
          1.57749939e+08,   1.57810974e+08,   1.57872009e+08])
    
    def test_assertion_array_arrange(self):
        self.assertTrue(check_assertion(self.freq_array_arrange))
        
    def test_assertion_1edge_2groups(self):
        self.assertFalse(check_assertion(self.freq_array_1edge_2groups))
    
    def test_even_1edge_2groups_plain(self):
        expected = np.array([ 2.,  3.66666667,  5.33333333,  7.])
        obtained = get_even_frequencies(self.freq_array_1edge_2groups, edge_up=0, edge_down=0)
        npt.assert_array_almost_equal(obtained, expected, decimal=7)

    def test_even_1edge_2groups_plain(self):
        expected = np.array([ 1.,  3.33333333,  5.66666667,  8.])
        obtained = get_even_frequencies(self.freq_array_1edge_2groups, 
                                        group=2, 
                                        edge_up=1, 
                                        edge_down=1,
                                        ch_per_sb=4)
        npt.assert_array_almost_equal(obtained, expected, decimal=7)
    
    def test_even_f3(self):
        even = get_even_frequencies(self.f3, group=3)
        npt.assert_approx_equal(even[0], 1.559862051e+08, significant=10)
        npt.assert_approx_equal(even[-1], 1.5787792989e+08, significant=10)
    
    def test_even_f5(self):
        even = get_even_frequencies(self.f5)
        npt.assert_approx_equal(even[0], 1.1691142121e+08, significant=10)
        npt.assert_approx_equal(even[-1], 1.18827713785e+08, significant=10)

if __name__ == '__main__':
    unittest.main()