import unittest
import stores

class TestStores(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load up all the store information from 'stores.json'
        cls.harness = stores.Stores()
        # Ensure all stores have their location appended
        cls.harness.populate_location_info()

    def test_stores(self):
        # Ensure all 95 stores are loaded from stores.json
        self.assertEqual(len(self.harness.stores), 95)

    def test_alphabetical_sort(self):
        stores = self.harness.sort_by_name()
        # Ensure we still have 95 stores
        self.assertEqual(len(stores), 95)
        # Check that the first and last names match watch we expect
        self.assertEqual(stores[0]['name'],'Alton')
        self.assertEqual(stores[-1]['name'],'Worthing')

    def test_stores_near_postcode(self):
        # Check for stores 30km around Ashford
        stores = self.harness.stores_around_postcode('TN24 8LF',30000)
        # Ensure we still have 6 stores
        self.assertEqual(len(stores), 6)
        # Check that the first and last names match watch we expect
        self.assertEqual(stores[0]['name'],'Sittingbourne')
        self.assertEqual(stores[-1]['name'],'Folkestone')
