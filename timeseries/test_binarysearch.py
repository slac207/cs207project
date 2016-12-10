from binarysearch import binary_search

import unittest
import numpy as np

class MyTest(unittest.TestCase):
    
    def setUp(self):
        self.inputt = range(10)
        
    def tearDown(self):
        del self.inputt
    
    #test showing that sorted array is necessary- 3 is present but returns -1
    def test_sorted(self):
        self.assertEqual(binary_search([2,1,5,3,6],3),(1, 2))
    
    #test for searching in an empty array
    def test_empty(self):
        self.assertEqual(binary_search([], 1), (-1,0))   
        
    #test for passing in non-array 
    def test_not_array(self):
        with self.assertRaises(TypeError):
            binary_search(1,2)     
            
    #test for passing in strings
    def test_non_numeric_str(self):
        with self.assertRaises(TypeError):
            binary_search(['l','ol'],2)  
            
    def test_chr(self):
        self.assertEqual(binary_search(['a','b','c','d'],'c'),(2,'FOUND'))         
    
    #test for whether NaN is valid input in array      
    def test_non_numeric_nan(self):
        self.assertEqual(binary_search([1,2,float('NaN'),float('NaN')],2),(1,'FOUND'))
    
    #test for whether inf is valid input in array         
    def test_non_numeric_inf(self):
        self.assertEqual(binary_search([1,2,np.inf],np.inf),(2,'FOUND')) 
     
  