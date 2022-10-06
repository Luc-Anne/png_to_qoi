#!/bin/python3.10.4

import unittest

from png_to_qoi import *

### Possible results/Chunks of tests
QOI_OP_RUN_run_of_1 = int('11000000', 2).to_bytes(1, 'big')
QOI_OP_RUN_run_of_2 = int('11000001', 2).to_bytes(1, 'big')
QOI_OP_RUN_run_of_62 = int('11111101', 2).to_bytes(1, 'big')

QOI_OP_RGBA_128_129_130_131 = \
    int('11111111', 2).to_bytes(1, 'big') + \
    int('10000000', 2).to_bytes(1, 'big') + \
    int('10000001', 2).to_bytes(1, 'big') + \
    int('10000010', 2).to_bytes(1, 'big') + \
    int('10000011', 2).to_bytes(1, 'big')

QOI_OP_RGB_128_129_130 = \
    int('11111110', 2).to_bytes(1, 'big') + \
    int('10000000', 2).to_bytes(1, 'big') + \
    int('10000001', 2).to_bytes(1, 'big') + \
    int('10000010', 2).to_bytes(1, 'big')

QOI_OP_DIFF_without_diff = int('01101010', 2).to_bytes(1, 'big')
QOI_OP_DIFF_without_diff_with_dr_minus_2 = int('01001010', 2).to_bytes(1, 'big')
QOI_OP_DIFF_without_diff_with_dr_plus_1  = int('01111010', 2).to_bytes(1, 'big')
QOI_OP_DIFF_without_diff_with_dg_minus_2 = int('01100010', 2).to_bytes(1, 'big')
QOI_OP_DIFF_without_diff_with_dg_plus_1  = int('01101110', 2).to_bytes(1, 'big')
QOI_OP_DIFF_without_diff_with_db_minus_2 = int('01101000', 2).to_bytes(1, 'big')
QOI_OP_DIFF_without_diff_with_db_plus_1  = int('01101011', 2).to_bytes(1, 'big')

QOI_OP_LUMA_31_31_31 =  \
    int('10111111', 2).to_bytes(1, 'big') + \
    int('10001000', 2).to_bytes(1, 'big')
QOI_OP_LUMA_224_224_224 =  \
    int('10000000', 2).to_bytes(1, 'big') + \
    int('10001000', 2).to_bytes(1, 'big')
    
QOI_OP_LUMA_7_0_0 =  \
    int('10100000', 2).to_bytes(1, 'big') + \
    int('11111000', 2).to_bytes(1, 'big')
QOI_OP_LUMA_248_0_0 =  \
    int('10100000', 2).to_bytes(1, 'big') + \
    int('00001000', 2).to_bytes(1, 'big')
QOI_OP_LUMA_0_0_7 =  \
    int('10100000', 2).to_bytes(1, 'big') + \
    int('10001111', 2).to_bytes(1, 'big')
QOI_OP_LUMA_0_0_248 =  \
    int('10100000', 2).to_bytes(1, 'big') + \
    int('10000000', 2).to_bytes(1, 'big')
    
QOI_OP_LUMA_23_16_16 =  \
    int('10110000', 2).to_bytes(1, 'big') + \
    int('11111000', 2).to_bytes(1, 'big')
QOI_OP_LUMA_8_16_16 =  \
    int('10110000', 2).to_bytes(1, 'big') + \
    int('00001000', 2).to_bytes(1, 'big')
QOI_OP_LUMA_16_16_23 =  \
    int('10110000', 2).to_bytes(1, 'big') + \
    int('10001111', 2).to_bytes(1, 'big')
QOI_OP_LUMA_16_16_8 =  \
    int('10110000', 2).to_bytes(1, 'big') + \
    int('10000000', 2).to_bytes(1, 'big')

QOI_OP_INDEX_53 = int('00110101', 2).to_bytes(1, 'big')

first_4_bands = QOI_OP_RUN_run_of_1
first_3_bands = QOI_OP_DIFF_without_diff

class Test_qoi_encode_pixel(unittest.TestCase):
    '''
    Tests of qoi_encode_pixel
    
    Due to a difference of first pixel dependings on 3 or 4 bands,
    every test is supposed to start at second pixel for 3 bands except the first test
    
    For convienience, first pixel will be (0, 0, 0) for 3 bands
    '''
    
    ### First pixel, special behavior ##################################
    def test_1(self):
        with self.subTest(4):
            self.assertEqual(encode_qoi_pixels([(0, 0, 0, 255)] , 4),
                QOI_OP_RUN_run_of_1,
                'QOI_OP_RUN_run_of_1')
        with self.subTest(3):
            self.assertEqual(encode_qoi_pixels( [(0, 0, 0)] , 3),
                QOI_OP_DIFF_without_diff,
                'QOI_OP_DIFF_without_diff')
    
    ### CHUNK QOI_OP_RUN ###############################################
    
    ### Run of 1
    def test_2(self):
        with self.subTest(4):
            self.assertEqual(encode_qoi_pixels( [(0, 0, 0, 255), (0, 0, 0, 255)] , 4),
                QOI_OP_RUN_run_of_2,
                'QOI_OP_RUN_run_of_2')
        with self.subTest(3):
            self.assertEqual(encode_qoi_pixels( [(0, 0, 0), (0, 0, 0)] , 3),
                first_3_bands + QOI_OP_RUN_run_of_1,
                'first_3_bands + QOI_OP_RUN_run_of_1')
    
    ### Run of 62
    def test_3(self):
        with self.subTest(4):
            pixel_list = list()
            for i in range(62):
                pixel_list.append((0, 0, 0, 255))
            self.assertEqual(encode_qoi_pixels( pixel_list , 4),
                QOI_OP_RUN_run_of_62,
                'QOI_OP_RUN_run_of_62')
        with self.subTest(3):
            pixel_list = [(0, 0, 0)]
            for i in range(62):
                pixel_list.append((0, 0, 0))
            self.assertEqual(encode_qoi_pixels( pixel_list , 3),
                first_3_bands + QOI_OP_RUN_run_of_62,
                'first_3_bands + QOI_OP_RUN_run_of_62')
    
    ### Run of 62 + 1 to test limit of run
    def test_4(self):
        with self.subTest(4):
            pixel_list = list()
            for i in range(62 + 1):
                pixel_list.append((0, 0, 0, 255))
            self.assertEqual(encode_qoi_pixels( pixel_list , 4),
                QOI_OP_RUN_run_of_62 + QOI_OP_RUN_run_of_1,
                'QOI_OP_RUN_run_of_62 + QOI_OP_RUN_run_of_1')
        with self.subTest(3):
            pixel_list = [(0, 0, 0)]
            for i in range(62 + 1):
                pixel_list.append((0, 0, 0))
            self.assertEqual(encode_qoi_pixels( pixel_list , 3),
                first_3_bands + QOI_OP_RUN_run_of_62 + QOI_OP_RUN_run_of_1,
                'first_3_bands + QOI_OP_RUN_run_of_62 + QOI_OP_RUN_run_of_1')

    ### CHUNK QOI_OP_RGBA ##############################################
    
    def test_5(self):
        with self.subTest(4):
            pixel_list = [(0, 0, 0, 255), (128,129,130,131)]
            self.assertEqual(encode_qoi_pixels( pixel_list , 4),
                first_4_bands + QOI_OP_RGBA_128_129_130_131,
                'first_4_bands + QOI_OP_RGBA_128_129_130_131')
        with self.subTest(3):
            pixel_list = [(0, 0, 0), (128,129,130)]
            self.assertEqual(encode_qoi_pixels( pixel_list , 3),
                first_3_bands + QOI_OP_RGB_128_129_130,
                'first_3_bands + QOI_OP_RGB_128_129_130')

    ### CHUNK QOI_OP_RGB ###############################################
    
    def test_6(self):
        with self.subTest(4):
            pixel_list = [(0, 0, 0, 255), (128,129,130,255)]
            self.assertEqual(encode_qoi_pixels( pixel_list , 4),
                first_4_bands + QOI_OP_RGB_128_129_130,
                'first_4_bands + QOI_OP_RGB_128_129_130')
        with self.subTest(3):
            pixel_list = [(0, 0, 0), (128,129,130)]
            self.assertEqual(encode_qoi_pixels( pixel_list , 3),
                first_3_bands + QOI_OP_RGB_128_129_130,
                'first_3_bands + QOI_OP_RGB_128_129_130')

    ### CHUNK QOI_OP_DIFF ##############################################
    
    ### dr
    def test_7(self):
        with self.subTest(4):
            pixel_list = [(0, 0, 0, 255), (254,0,0,255)]
            r = 'first_4_bands + QOI_OP_DIFF_without_diff_with_dr_minus_2'
            self.assertEqual(encode_qoi_pixels( pixel_list , 4), eval(r),r)
        with self.subTest(3):
            pixel_list = [(0, 0, 0), (254,0,0)]
            r = 'first_3_bands + QOI_OP_DIFF_without_diff_with_dr_minus_2'
            self.assertEqual(encode_qoi_pixels( pixel_list , 3), eval(r),r)

    def test_8(self):
        with self.subTest(4):
            pixel_list = [(0, 0, 0, 255), (1,0,0,255)]
            r = 'first_4_bands + QOI_OP_DIFF_without_diff_with_dr_plus_1'
            self.assertEqual(encode_qoi_pixels( pixel_list , 4), eval(r),r)
        with self.subTest(3):
            pixel_list = [(0, 0, 0), (1,0,0)]
            r = 'first_3_bands + QOI_OP_DIFF_without_diff_with_dr_plus_1'
            self.assertEqual(encode_qoi_pixels( pixel_list , 3), eval(r),r)
    
    ### dg
    def test_9(self):
        with self.subTest(4):
            pixel_list = [(0, 0, 0, 255), (0,254,0,255)]
            r = 'first_4_bands + QOI_OP_DIFF_without_diff_with_dg_minus_2'
            self.assertEqual(encode_qoi_pixels( pixel_list , 4), eval(r),r)
        with self.subTest(3):
            pixel_list = [(0, 0, 0), (0,254,0)]
            r = 'first_3_bands + QOI_OP_DIFF_without_diff_with_dg_minus_2'
            self.assertEqual(encode_qoi_pixels( pixel_list , 3), eval(r),r)
    
    def test_10(self):
        with self.subTest(4):
            pixel_list = [(0, 0, 0, 255), (0,1,0,255)]
            r = 'first_4_bands + QOI_OP_DIFF_without_diff_with_dg_plus_1'
            self.assertEqual(encode_qoi_pixels( pixel_list , 4), eval(r),r)
        with self.subTest(3):
            pixel_list = [(0, 0, 0), (0,1,0)]
            r = 'first_3_bands + QOI_OP_DIFF_without_diff_with_dg_plus_1'
            self.assertEqual(encode_qoi_pixels( pixel_list , 3), eval(r),r)
    
    ### db
    def test_11(self):
        with self.subTest(4):
            pixel_list = [(0, 0, 0, 255), (0,0,254,255)]
            r = 'first_4_bands + QOI_OP_DIFF_without_diff_with_db_minus_2'
            self.assertEqual(encode_qoi_pixels( pixel_list , 4), eval(r),r)
        with self.subTest(3):
            pixel_list = [(0, 0, 0), (0,0,254)]
            r = 'first_3_bands + QOI_OP_DIFF_without_diff_with_db_minus_2'
            self.assertEqual(encode_qoi_pixels( pixel_list , 3), eval(r),r)
                
    def test_12(self):
        with self.subTest(4):
            pixel_list = [(0, 0, 0, 255), (0,0,1,255)]
            r = 'first_4_bands + QOI_OP_DIFF_without_diff_with_db_plus_1'
            self.assertEqual(encode_qoi_pixels( pixel_list , 4), eval(r),r)
        with self.subTest(3):
            pixel_list = [(0, 0, 0), (0,0,1)]
            r = 'first_3_bands + QOI_OP_DIFF_without_diff_with_db_plus_1'
            self.assertEqual(encode_qoi_pixels( pixel_list , 3), eval(r),r)

    ### CHUNK QOI_OP_LUMA ##############################################
    
    ### dg
    def test_13(self):
        with self.subTest(4):
            pixel_list = [(0, 0, 0, 255), (31,31,31,255)]
            self.assertEqual(encode_qoi_pixels( pixel_list , 4),
                first_4_bands + QOI_OP_LUMA_31_31_31,
                'first_4_bands + QOI_OP_LUMA_31_31_31')
        with self.subTest(3):
            pixel_list = [(0, 0, 0), (31,31,31)]
            self.assertEqual(encode_qoi_pixels( pixel_list , 3),
                first_3_bands + QOI_OP_LUMA_31_31_31,
                'first_3_bands + QOI_OP_LUMA_31_31_31')
    
    def test_14(self):
        with self.subTest(4):
            pixel_list = [(0, 0, 0, 255), (224,224,224,255)]
            self.assertEqual(encode_qoi_pixels( pixel_list , 4),
                first_4_bands + QOI_OP_LUMA_224_224_224,
                'first_4_bands + QOI_OP_LUMA_224_224_224')
        with self.subTest(3):
            pixel_list = [(0, 0, 0), (224,224,224)]
            self.assertEqual(encode_qoi_pixels( pixel_list , 3),
                first_3_bands + QOI_OP_LUMA_224_224_224,
                'first_3_bands + QOI_OP_LUMA_224_224_224')

    ### dr
    def test_15(self):
        with self.subTest(4):
            pixel_list = [(0, 0, 0, 255), (7,0,0,255)]
            self.assertEqual(encode_qoi_pixels( pixel_list , 4),
                first_4_bands + QOI_OP_LUMA_7_0_0,
                'first_4_bands + QOI_OP_LUMA_7_0_0')
        with self.subTest(3):
            pixel_list = [(0, 0, 0), (7,0,0)]
            self.assertEqual(encode_qoi_pixels( pixel_list , 3),
                first_3_bands + QOI_OP_LUMA_7_0_0,
                'first_3_bands + QOI_OP_LUMA_7_0_0')
    
    def test_16(self):
        with self.subTest(4):
            pixel_list = [(0, 0, 0, 255), (248,0,0,255)]
            self.assertEqual(encode_qoi_pixels( pixel_list , 4),
                first_4_bands + QOI_OP_LUMA_248_0_0,
                'first_4_bands + QOI_OP_LUMA_248_0_0')
        with self.subTest(3):
            pixel_list = [(0, 0, 0), (248,0,0)]
            self.assertEqual(encode_qoi_pixels( pixel_list , 3),
                first_3_bands + QOI_OP_LUMA_248_0_0,
                'first_3_bands + QOI_OP_LUMA_248_0_0')

    ### db
    def test_17(self):
        with self.subTest(4):
            pixel_list = [(0, 0, 0, 255), (0,0,7,255)]
            self.assertEqual(encode_qoi_pixels( pixel_list , 4),
                first_4_bands + QOI_OP_LUMA_0_0_7,
                'first_4_bands + QOI_OP_LUMA_0_0_7')
        with self.subTest(3):
            pixel_list = [(0, 0, 0), (0,0,7)]
            self.assertEqual(encode_qoi_pixels( pixel_list , 3),
                first_3_bands + QOI_OP_LUMA_0_0_7,
                'first_3_bands + QOI_OP_LUMA_0_0_7')
    
    def test_18(self):
        with self.subTest(4):
            pixel_list = [(0, 0, 0, 255), (0,0,248,255)]
            self.assertEqual(encode_qoi_pixels( pixel_list , 4),
                first_4_bands + QOI_OP_LUMA_0_0_248,
                'first_4_bands + QOI_OP_LUMA_0_0_248')
        with self.subTest(3):
            pixel_list = [(0, 0, 0), (0,0,248)]
            self.assertEqual(encode_qoi_pixels( pixel_list , 3),
                first_3_bands + QOI_OP_LUMA_0_0_248,
                'first_3_bands + QOI_OP_LUMA_0_0_248')
                
    ### dr - dg
    def test_19(self):
        with self.subTest(4):
            pixel_list = [(0, 0, 0, 255), (23,16,16,255)]
            self.assertEqual(encode_qoi_pixels( pixel_list , 4),
                first_4_bands + QOI_OP_LUMA_23_16_16,
                'first_4_bands + QOI_OP_LUMA_23_16_16')
        with self.subTest(3):
            pixel_list = [(0, 0, 0), (23,16,16)]
            self.assertEqual(encode_qoi_pixels( pixel_list , 3),
                first_3_bands + QOI_OP_LUMA_23_16_16,
                'first_3_bands + QOI_OP_LUMA_23_16_16')
    
    def test_20(self):
        with self.subTest(4):
            pixel_list = [(0, 0, 0, 255), (8,16,16,255)]
            self.assertEqual(encode_qoi_pixels( pixel_list , 4),
                first_4_bands + QOI_OP_LUMA_8_16_16,
                'first_4_bands + QOI_OP_LUMA_8_16_16')
        with self.subTest(3):
            pixel_list = [(0, 0, 0), (8,16,16)]
            self.assertEqual(encode_qoi_pixels( pixel_list , 3),
                first_3_bands + QOI_OP_LUMA_8_16_16,
                'first_3_bands + QOI_OP_LUMA_8_16_16')

    ### db - dg
    def test_21(self):
        with self.subTest(4):
            pixel_list = [(0, 0, 0, 255), (16,16,23,255)]
            self.assertEqual(encode_qoi_pixels( pixel_list , 4),
                first_4_bands + QOI_OP_LUMA_16_16_23,
                'first_4_bands + QOI_OP_LUMA_16_16_23')
        with self.subTest(3):
            pixel_list = [(0, 0, 0), (16,16,23)]
            self.assertEqual(encode_qoi_pixels( pixel_list , 3),
                first_3_bands + QOI_OP_LUMA_16_16_23,
                'first_3_bands + QOI_OP_LUMA_16_16_23')
    
    def test_22(self):
        with self.subTest(4):
            pixel_list = [(0, 0, 0, 255), (16,16,8,255)]
            self.assertEqual(encode_qoi_pixels( pixel_list , 4),
                first_4_bands + QOI_OP_LUMA_16_16_8,
                'first_4_bands + QOI_OP_LUMA_16_16_8')
        with self.subTest(3):
            pixel_list = [(0, 0, 0), (16,16,8)]
            self.assertEqual(encode_qoi_pixels( pixel_list , 3),
                first_3_bands + QOI_OP_LUMA_16_16_8,
                'first_3_bands + QOI_OP_LUMA_16_16_8')

    ### CHUNK QOI_OP_INDEX #############################################
    
    def test_23(self):
        with self.subTest(4):
            pixel_list = [(0, 0, 0, 255), (128,129,130,255), (0, 0, 0, 255)]
            self.assertEqual(encode_qoi_pixels( pixel_list , 4),
                first_4_bands + QOI_OP_RGB_128_129_130 + QOI_OP_INDEX_53,
                'first_4_bands + QOI_OP_RGB_128_129_130 + QOI_OP_INDEX_53')
        with self.subTest(3):
            pixel_list = [(0, 0, 0), (128,129,130), (0, 0, 0)]
            self.assertEqual(encode_qoi_pixels( pixel_list , 3),
                first_3_bands + QOI_OP_RGB_128_129_130 + QOI_OP_INDEX_53,
                'first_3_bands + QOI_OP_RGB_128_129_130 + QOI_OP_INDEX_53')

if __name__ == "__main__":
    unittest.main()
