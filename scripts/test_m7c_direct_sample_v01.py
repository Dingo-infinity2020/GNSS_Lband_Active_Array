from __future__ import print_function
import copy
import json
import unittest
from pathlib import Path
from m7c_direct_sample_contract_v01 import (FREQUENCIES,require_direct_config,classify,
                                          native_frequencies,native_deltas,exact_index)

ROOT=Path(__file__).resolve().parents[1]


class DirectSampleTests(unittest.TestCase):
    def test_installed_configuration_is_direct_and_exact(self):
        require_direct_config((ROOT/"source/cst/M7C_DIRECT_SAMPLE_CONFIG_V01.mcr").read_text())

    def test_resampled_broadband_is_rejected(self):
        t=(ROOT/"source/cst/M7C_DIRECT_SAMPLE_CONFIG_V01.mcr").read_text()
        with self.assertRaises(RuntimeError):
            require_direct_config(t.replace('Discrete samples only','General purpose'))

    def test_missing_direct_frequency_is_rejected(self):
        t=(ROOT/"source/cst/M7C_DIRECT_SAMPLE_CONFIG_V01.mcr").read_text()
        t=t.replace('        .AddSampleInterval "1.2096", "1.2096", "1", "Single", "False"','')
        with self.assertRaises(RuntimeError):require_direct_config(t)

    def test_unregistered_precision_change_is_rejected(self):
        t=(ROOT/"source/cst/M7C_DIRECT_SAMPLE_CONFIG_V01.mcr").read_text()
        with self.assertRaises(RuntimeError):require_direct_config(t+'\n.AccuracyTet "1e-8"')

    def test_native_parser_real_fixture(self):
        p=ROOT/"evidence/M7C_OFFLINE_REVIEW_20261027_V01/M7C_native_output.txt"
        t=p.read_text()
        self.assertEqual(len(native_frequencies(t)),10)
        self.assertIn(1.2144,native_frequencies(t))
        self.assertNotIn(1.2096,native_frequencies(t))
        self.assertAlmostEqual(native_deltas(t)[-1],.0149349)

    def test_exact_sample_never_interpolates(self):
        with self.assertRaises(RuntimeError):exact_index([1.2088,1.2104],1.2096)

    def test_pre_registered_outcomes_and_numerical_hold(self):
        old={(2,5):[8e-5]*15,(5,2):[8e-6]*15}
        direct={(2,5):[8e-6]*15,(5,2):[8e-6]*15}
        self.assertEqual(classify(FREQUENCIES,direct,FREQUENCIES,old,True)['status'],'H_NUM_SUPPORTED_M7C_DIRECT_SAMPLE')
        direct={(2,5):[7e-5]*15,(5,2):[7e-5]*15}
        self.assertEqual(classify(FREQUENCIES,direct,FREQUENCIES,old,True)['status'],'FEATURE_REPRODUCED_M7C_DIRECT_SAMPLE')
        direct[(5,2)]=[5e-5]*15
        self.assertEqual(classify(FREQUENCIES,direct,FREQUENCIES,old,True)['status'],'INCONCLUSIVE_HOLD_M7C_DIRECT_SAMPLE')
        self.assertEqual(classify(FREQUENCIES,direct,FREQUENCIES,old,False)['status'],'HOLD_M7C_DIRECT_NUMERICAL_OR_PROVENANCE')


if __name__=='__main__':unittest.main()
