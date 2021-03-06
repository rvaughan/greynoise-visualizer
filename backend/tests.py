import os, json
import unittest
import app
from unittest.mock import patch, Mock
 
class TestApi(unittest.TestCase):
 
    ############################
    #### setup ####
    ############################
 
    # executed prior to each test
    def setUp(self):
        self.app = app.app.test_client()
 
    # executed after each test
    def tearDown(self):
        pass
 
 
###############
#### tests ####
###############
    
    @patch('app.requests.get')
    def test_api_get_only_tag_names(self, mock_get): 
        """test api call to get only tag names"""       
        names =  {
              "status": "ok",
              "tags": [
                "VNC_SCANNER_HIGH",
                "PING_SCANNER_LOW"
                ]}
        finalNames = {
                      "tags": [
                        {
                          "name": "VNC_SCANNER_HIGH"
                        }, 
                        {
                          "name": "PING_SCANNER_LOW"
                        }
                      ]
                    }
        mock_get.return_value = Mock()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = names

        response = self.app.get("/api/tagnames")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), finalNames)

    @patch('app.getTags')
    def test_api_get_tags(self, mock_get_tags):
        """test api call to get tags (category, intention, name, confidence)"""
        tags = [
                    {
                      "category": "search_engine",
                      "confidence": "high",
                      "intention": "Null",
                      "name": "YANDEX_SEARCH_ENGINE"
                    }]
        finalTagData = { 
                      "tags": [
                          {
                          "category": "search_engine",
                          "confidence": "high",
                          "intention": "Null",
                          "name": "YANDEX_SEARCH_ENGINE"
                        }
                        ]
                      }

        mock_get_tags.return_value = Mock()
        mock_get_tags.return_value = tags

        tagDataResponse = self.app.get("/api/tags")
        self.assertEqual(tagDataResponse.status_code, 200)
        self.assertEqual(json.loads(tagDataResponse.data), finalTagData)

    @patch('app.getTagData')
    def test_api_get_tagData(self, mock_get_tag_data):
        """test api call to get tag data (instances)"""
        tagData = [
                      {
                        "category": "search_engine", 
                        "confidence": "high", 
                        "first_seen": "2018-01-03T22:47:16.556Z", 
                        "intention": "Null", 
                        "ip": "37.9.113.90",
                        "last_updated": "2018-01-03T22:47:16.556Z", 
                        "name": "YANDEX_SEARCH_ENGINE"
                      }
                  ]
        finalTagData = { 
                      "records": [
                        {
                            "category": "search_engine", 
                            "confidence": "high", 
                            "first_seen": "2018-01-03T22:47:16.556Z", 
                            "intention": "Null", 
                            "ip": "37.9.113.90",
                            "last_updated": "2018-01-03T22:47:16.556Z", 
                            "name": "YANDEX_SEARCH_ENGINE"
                        }]
                      }

        mock_get_tag_data.return_value = Mock()
        mock_get_tag_data.return_value = tagData

        response = self.app.post("/api/tags/YANDEX_SEARCH_ENGINE")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), finalTagData)


    @patch('app.getTags')
    def test_api_get_stats_counts(self, mock_get_tags):
        """test api call to get category and intention counts"""
        tags = [
                    {
                      "category": "search_engine",
                      "confidence": "high",
                      "intention": "Null",
                      "name": "YANDEX_SEARCH_ENGINE"
                    }]
        finalTagData = { 
                  "counts": {
                    "category": [
                      {
                        "count": 1, 
                        "name": "search_engine"
                      }],
                      "intention": [
                      {
                        "count": 1, 
                        "name": "Null"
                      }]
                    }
                  }

        mock_get_tags.return_value = Mock()
        mock_get_tags.return_value = tags

        tagDataResponse = self.app.get("/api/stats/counts")
        self.assertEqual(tagDataResponse.status_code, 200)
        self.assertEqual(json.loads(tagDataResponse.data), finalTagData)


    @patch('app.requests.post')
    def test_getTagData(self, mock_post):
        """test getTagData function"""
        tagData = {
              "tag": "YANDEX_SEARCH_ENGINE",
              "status": "ok",
              "returned_count": 131,
              "records": [
                {
                  "ip": "37.9.113.90",
                  "name": "YANDEX_SEARCH_ENGINE",
                  "first_seen": "2018-01-03T22:47:16.556Z",
                  "last_updated": "2018-01-03T22:47:16.556Z",
                  "confidence": "high",
                  "intention": "",
                  "category": "search_engine",
                  "metadata": {
                    "org": "YANDEX LLC",
                    "rdns": "37-9-113-90.spider.yandex.com",
                    "rdns_parent": "yandex.com",
                    "datacenter": "",
                    "asn": "AS13238",
                    "os": "Linux 2.2-3.x",
                    "link": "generic tunnel or VPN",
                    "tor": "false"
                  }
                }
            ]
        }
        finalTagData = [
                      {
                        "category": "search_engine", 
                        "confidence": "high", 
                        "first_seen": "2018-01-03T22:47:16.556Z", 
                        "intention": "Null", 
                        "ip": "37.9.113.90",
                        "last_updated": "2018-01-03T22:47:16.556Z", 
                        "name": "YANDEX_SEARCH_ENGINE"
                      }
                  ]

        mock_post.return_value = Mock()
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = tagData

        response = app.getTagData("YANDEX_SEARCH_ENGINE")

        self.assertEqual(response, finalTagData)

    @patch('app.requests.get')
    def test_getTags(self, mock_get):
        """test getTags function"""
        names =  {
              "status": "ok",
              "tags": [
                "YANDEX_SEARCH_ENGINE"
                ]}
        finalTagData =  [
                    {
                      "category": "search_engine",
                      "confidence": "high",
                      "intention": "Null",
                      "name": "YANDEX_SEARCH_ENGINE"
                    }]

        mock_get.return_value = Mock()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = names

        response = app.getTags()

        self.assertEqual(response, finalTagData)

    def test_counter_of_things(self):
        """Test counter function"""
        test_response = [{
                          "category": "activity",
                          "confidence": "high",
                          "intention": "Null",
                          "name": "TEST1"
                        },
                        {
                          "category": "activity",
                          "confidence": "high",
                          "intention": "benign",
                          "name": "TEST2"
                        },
                        {
                          "category": "actor",
                          "confidence": "high",
                          "intention": "benign",
                          "name": "TEST3"
                        }]

        counts = app.counter_of_things(test_response)

        for item in counts['intention']:
            if (item['name'] == "Null"):
                assert item['count'] == 1
            if (item['name'] == "benign"):
                assert item['count'] == 2

        for item in counts['category']:
            if (item['name'] == "activity"):
                assert item['count'] == 2
            if (item['name'] == "actor"):
                assert item['count'] == 1

    @patch('app.getTagData')
    def test_get_time_series_data(self, mock_get_tag_data):
        """test get_time_series_data function"""
        tagData = [
                      {
                        "category": "search_engine", 
                        "confidence": "high", 
                        "first_seen": "2017-11-21T07:00:00.000Z", 
                        "intention": "Null", 
                        "ip": "37.9.113.90",
                        "last_updated": "2018-01-03T22:47:16.556Z", 
                        "name": "YANDEX_SEARCH_ENGINE"
                      },
                      {
                        "category": "search_engine", 
                        "confidence": "high", 
                        "first_seen": "2017-11-21T07:00:00.000Z", 
                        "intention": "Null", 
                        "ip": "37.9.113.90",
                        "last_updated": "2018-01-03T22:47:16.556Z", 
                        "name": "YANDEX_SEARCH_ENGINE"
                      }
                  ]
        finalTagData = [
                        {
                        "timestamp": 1511222400000,
                        "hits": 2
                        }]

        mock_get_tag_data.return_value = Mock()
        mock_get_tag_data.return_value = tagData

        tagDataResponse = self.app.post("/api/stats/YANDEX_SEARCH_ENGINE")
        self.assertEqual(tagDataResponse.status_code, 200)
        self.assertEqual(json.loads(tagDataResponse.data), finalTagData)

    @patch('app.getTagData')
    def test_getTagIpGeo(self, mock_get_tag_data):
        """test getTagIpGeo function"""
        tagData = [
                      {
                        "category": "search_engine", 
                        "confidence": "high", 
                        "first_seen": "2017-11-21T07:00:00.000Z", 
                        "intention": "Null", 
                        "ip": "66.249.80.1",
                        "last_updated": "2018-01-03T22:47:16.556Z", 
                        "name": "YANDEX_SEARCH_ENGINE"
                      },
                      {
                        "category": "search_engine", 
                        "confidence": "high", 
                        "first_seen": "2017-11-21T07:00:00.000Z", 
                        "intention": "Null", 
                        "ip": "66.102.6.191",
                        "last_updated": "2018-01-03T22:47:16.556Z", 
                        "name": "YANDEX_SEARCH_ENGINE"
                      }
                  ]
        finalTagData = [
                {
                  "ip": "66.249.80.1",
                  "lat": 32.7787,
                  "long": -96.8217
                },
                {
                  "ip": "66.102.6.191",
                  "lat": 37.419200000000004,
                  "long": -122.0574
                }
              ]

        mock_get_tag_data.return_value = Mock()
        mock_get_tag_data.return_value = tagData

        data = app.getTagIpGeo("GOOGLEBOT")
        self.assertEqual(data, finalTagData)

    @patch('app.getTagIpGeo')
    def test_api_get_tag_geo(self, mock_get_tag_data):
        """test api call to get IP locations"""
        tagData = [
                {
                  "ip": "66.249.80.1",
                  "lat": 32.7787,
                  "long": -96.8217
                },
                {
                  "ip": "66.102.6.191",
                  "lat": 37.419200000000004,
                  "long": -122.0574
                }
              ]
        finalTagData = {
                    "record": [
                      {
                        "ip": "66.249.80.1",
                        "lat": 32.7787,
                        "long": -96.8217
                      },
                      {
                        "ip": "66.102.6.191",
                        "lat": 37.419200000000004,
                        "long": -122.0574
                      }
                    ]
                  }

        mock_get_tag_data.return_value = Mock()
        mock_get_tag_data.return_value = tagData

        tagDataResponse = self.app.post("/api/geo/GOOGLEBOT")
        self.assertEqual(tagDataResponse.status_code, 200)
        self.assertEqual(json.loads(tagDataResponse.data), finalTagData)

if __name__ == "__main__":
    unittest.main()
