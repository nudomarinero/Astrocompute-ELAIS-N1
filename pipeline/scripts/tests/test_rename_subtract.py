from __future__ import print_function
import sys
import unittest
import traceback
import os
import shutil
import tempfile

# Append the path of the module to the syspath
sys.path.append('..')
from rename_subtract import get_name, rename_directory, rename_ms

input_names = [
 "L229673_SAP000_SB000_uv.MS_12487D6BAt_115MHz.pre-cal.ms.tar",
 "L229673_SAP000_SB000_uv.MS_12487D6BAt_117MHz.pre-cal.ms.tar",
 "L229673_SAP000_SB000_uv.MS_12487D6BAt_119MHz.pre-cal.ms.tar",
 "L229673_SAP000_SB000_uv.MS_12487D6BAt_121MHz.pre-cal.ms.tar",
 "L229673_SAP000_SB040_uv.MS_12487D6BAt_123MHz.pre-cal.ms.tar",
 "L229673_SAP000_SB040_uv.MS_12487D6BAt_125MHz.pre-cal.ms.tar",
 "L229673_SAP000_SB040_uv.MS_12487D6BAt_127MHz.pre-cal.ms.tar",
 "L229673_SAP000_SB040_uv.MS_12487D6BAt_129MHz.pre-cal.ms.tar",
 "L229673_SAP000_SB080_uv.MS_12487D6BAt_131MHz.pre-cal.ms.tar",
 "L229673_SAP000_SB080_uv.MS_12487D6BAt_133MHz.pre-cal.ms.tar",
 "L229673_SAP000_SB080_uv.MS_12487D6BAt_135MHz.pre-cal.ms.tar",
 "L229673_SAP000_SB080_uv.MS_12487D6BAt_137MHz.pre-cal.ms.tar",
 "L229673_SAP000_SB120_uv.MS_12487D6BAt_139MHz.pre-cal.ms.tar",
 "L229673_SAP000_SB120_uv.MS_12487D6BAt_141MHz.pre-cal.ms.tar",
 "L229673_SAP000_SB120_uv.MS_12487D6BAt_143MHz.pre-cal.ms.tar",
 "L229673_SAP000_SB120_uv.MS_12487D6BAt_145MHz.pre-cal.ms.tar",
 "L229673_SAP000_SB160_uv.MS_12487D6BAt_147MHz.pre-cal.ms.tar",
 "L229673_SAP000_SB160_uv.MS_12487D6BAt_149MHz.pre-cal.ms.tar",
 "L229673_SAP000_SB160_uv.MS_12487D6BAt_151MHz.pre-cal.ms.tar",
 "L229673_SAP000_SB160_uv.MS_12487D6BAt_153MHz.pre-cal.ms.tar",
 "L229673_SAP000_SB200_uv.MS_12487D6BAt_154MHz.pre-cal.ms.tar",
 "L229673_SAP000_SB200_uv.MS_12487D6BAt_156MHz.pre-cal.ms.tar",
 "L229673_SAP000_SB200_uv.MS_12487D6BAt_158MHz.pre-cal.ms.tar",
 "L229673_SAP000_SB200_uv.MS_12487D6BAt_160MHz.pre-cal.ms.tar",
 "L229673_SAP000_SB240_uv.MS_12487D6BAt_162MHz.pre-cal.ms.tar",
 "L229673_SAP000_SB240_uv.MS_12487D6BAt_164MHz.pre-cal.ms.tar",
 "L229673_SAP000_SB240_uv.MS_12487D6BAt_166MHz.pre-cal.ms.tar",
 "L229673_SAP000_SB240_uv.MS_12487D6BAt_168MHz.pre-cal.ms.tar",
 "L229673_SAP000_SB281_uv.MS_12487D6BAt_170MHz.pre-cal.ms.tar",
 "L229673_SAP000_SB281_uv.MS_12487D6BAt_172MHz.pre-cal.ms.tar",
 "L229673_SAP000_SB281_uv.MS_12487D6BAt_174MHz.pre-cal.ms.tar",
 "L229673_SAP000_SB281_uv.MS_12487D6BAt_176MHz.pre-cal.ms.tar",
 "L229673_SAP000_SB321_uv.MS_12487D6BAt_180MHz.pre-cal.ms.tar",
 "L229673_SAP000_SB321_uv.MS_12487D6BAt_184MHz.pre-cal.ms.tar",
 "L229673_SAP000_SB321_uv.MS_12487D6BAt_186MHz.pre-cal.ms.tar"]

output_names_template = "L229673_SBgr{:03d}-10_uv.MS.pre-cal.ms.tar"
out_group = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,
  20,21,22,23,24,25,26,27,28,29,30,31,32,34,35]

output_names = [output_names_template.format(a) for a in out_group]

class TestRenameSubtract(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        for f in input_names:
            open(os.path.join(self.tmp_dir, f), "a").close()
        self.tmp_dir_one = tempfile.mkdtemp()
        f1 = "L000000_SAP000_SB000_uv.MS_12487D6BAt_182MHz.pre-cal.ms.tar"
        self.fileone = os.path.join(self.tmp_dir_one, f1)
        open(self.fileone, "a").close()
        self.tmp_dir_two = tempfile.mkdtemp()
        f2 = "L000000_SAP000_SB000_uv.MS_12487D6BAt_182MHz.pre-cal.ms"
        self.filetwo = os.path.join(self.tmp_dir_two, f2)
        open(self.filetwo, "a").close()
        
    
    def test_get_name1(self):
        self.assertEqual(get_name(input_names[0]), output_names[0])
    
    def test_get_name_no_tar(self):
        self.assertEqual(get_name("L000000_SAP000_SB321_uv.MS_12487D6BAt_182MHz.pre-cal.ms"), 
                         "L000000_SBgr033-10_uv.MS.pre-cal.ms")

            
    def test_get_name_all(self):
        for i, input_name in enumerate(input_names):
            self.assertEqual(get_name(input_name), output_names[i])
    
    def test_move_all(self):
        rename_directory(self.tmp_dir, verbose=True)
        final_names = os.listdir(self.tmp_dir)
        #print(final_names)
        for final_name in final_names:
            self.assertIn(final_name, output_names)
            
    def test_move_one(self):
        rename_ms(self.fileone, verbose=False)
        final_names = os.listdir(self.tmp_dir_one)
        #print(final_names)
        self.assertEqual(final_names[0], "L000000_SBgr033-10_uv.MS.pre-cal.ms.tar")
    
    def test_move_two(self):
        rename_ms(self.filetwo, verbose=False)
        final_names = os.listdir(self.tmp_dir_two)
        #print(final_names)
        self.assertEqual(final_names[0], "L000000_SBgr033-10_uv.MS.pre-cal.ms")
    
    def tearDown(self):
        shutil.rmtree(self.tmp_dir)
        shutil.rmtree(self.tmp_dir_one)

      
if __name__ == '__main__':
    unittest.main()   
    