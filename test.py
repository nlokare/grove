import unittest
from find_store import FindStore

class TestFindStore(unittest.TestCase):

  def test_find_by_address(self):
    find_store = FindStore()
    expected_answer= 'The closest store is located at 2675 Geary Blvd. San Francisco, CA 94118-3400 and is 1.48 mi away'
    target_address = '1770 Union St, San Francisco, CA 94123'
    self.assertEqual(find_store.find_by_address(target_address, 'mi', 'text'), expected_answer)

  def test_find_by_address_km(self):
    find_store = FindStore()
    expected_answer= 'The closest store is located at 2675 Geary Blvd. San Francisco, CA 94118-3400 and is 2.38 km away'
    target_address = '1770 Union St, San Francisco, CA 94123'
    self.assertEqual(find_store.find_by_address(target_address, 'km', 'text'), expected_answer)

  def test_find_by_zip(self):
    find_store = FindStore()
    expected_answer= 'The closest store is located at 2700 Fifth Street. Alameda, CA 94501 and is 4.4 mi away'
    target_zip = '94602'
    self.assertEqual(find_store.find_by_zip(target_zip, 'mi', 'text'), expected_answer)

  def test_find_by_zip_km(self):
    find_store = FindStore()
    expected_answer= 'The closest store is located at 2700 Fifth Street. Alameda, CA 94501 and is 7.08 km away'
    target_zip = '94602'
    self.assertEqual(find_store.find_by_zip(target_zip, 'km', 'text'), expected_answer)

if __name__ == '__main__':
  unittest.main()