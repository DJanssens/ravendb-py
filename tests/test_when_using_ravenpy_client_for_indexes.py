import ravenpy
import unittest
from ravenpy import client as rdb


class test_when_using_ravenpy_client_for_indexes(unittest.TestCase):

    def setUp(self):
        self.client = rdb('localhost', 'test', 8080)
        pass

    def tearDown(self):
        pass

    def test_it_is_possible_to_create_a_new_index(self):

        index = {'Map': 'from doc in docs\r\nselect new { doc.title }'}
        indexId = None
        indexId = self.client.createIndex(index, 'documentsByTitle')

        self.assertEqual(indexId, 'documentsByTitle')
        self.client.deleteIndex('documentsByTitle')

    def test_it_is_possible_to_delete_an_index(self):

        index = {'Map': 'from doc in docs\r\nselect new { doc.title }'}
        indexId = None
        indexId = self.client.createIndex(index, 'documentsByTitle')

        result = self.client.deleteIndex('documentsByTitle')
        self.assertEqual(True, result)

    def test_it_is_possible_to_query_an_index(self):

        docId1 = self.client.store({
            "title": "test document",
            "deleted": True
        })

        docId2 = self.client.store({
            "title": "test document",
            "deleted": False
        })

        docId3 = self.client.store({
            "title": "test document",
            "deleted": False
        })

        index = {'Map': 'from doc in docs\r\n select new { doc.deleted }'}
        self.client.createIndex(index, 'documentsByState')
        results = self.client.query('documentsByState', "deleted:false")

        self.client.delete(docId1)
        self.client.delete(docId2)
        self.client.delete(docId3)

        self.assertTrue("Results" in results)
        self.assertEqual(len(results["Results"]), 2)
