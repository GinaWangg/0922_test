import unittest
import json
from typing import Dict, List, Any, Optional
from flask import Flask, Response
from models import Publisher, db, init_db
from routes.publishers import publishers_bp

class TestPublishersRoutes(unittest.TestCase):
    # Test data for publishers
    TEST_DATA: Dict[str, Any] = {
        "publishers": [
            {"name": "DevGames Inc"},
            {"name": "Scrum Masters"},
            {"name": "Another Publisher"}
        ]
    }
    
    # API paths
    PUBLISHERS_API_PATH: str = '/api/publishers'

    def setUp(self) -> None:
        """Set up test database and seed data"""
        # Create a fresh Flask app for testing
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        # Register the publishers blueprint
        self.app.register_blueprint(publishers_bp)
        
        # Initialize database with the app
        with self.app.app_context():
            init_db(self.app)
            db.create_all()
            
            # Seed test data
            self._seed_test_data()
        
        # Create test client
        self.client = self.app.test_client()

    def tearDown(self) -> None:
        """Clean up after each test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()

    def _seed_test_data(self) -> None:
        """Helper method to seed test data"""
        # Create test publishers
        publishers = [
            Publisher(**publisher_data) for publisher_data in self.TEST_DATA["publishers"]
        ]
        db.session.add_all(publishers)
        db.session.commit()

    def _get_response_data(self, response: Response) -> Any:
        """Helper method to get JSON data from response"""
        return json.loads(response.data.decode('utf-8'))

    def test_get_all_publishers_success(self) -> None:
        """Test successful retrieval of all publishers"""
        # Act
        response = self.client.get(self.PUBLISHERS_API_PATH)
        data = self._get_response_data(response)
        
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), len(self.TEST_DATA["publishers"]))
        
        # Check that all publishers have required fields
        for publisher in data:
            self.assertIn('id', publisher)
            self.assertIn('name', publisher)
            self.assertIsInstance(publisher['id'], int)
            self.assertIsInstance(publisher['name'], str)
            # Ensure only id and name are returned (not description or game_count)
            self.assertEqual(len(publisher.keys()), 2)

    def test_get_publishers_structure(self) -> None:
        """Test the response structure for publishers"""
        # Act
        response = self.client.get(self.PUBLISHERS_API_PATH)
        data = self._get_response_data(response)
        
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), len(self.TEST_DATA["publishers"]))
        
        # Check required fields are present
        required_fields = ['id', 'name']
        for field in required_fields:
            self.assertIn(field, data[0])

    def test_get_publishers_names_match(self) -> None:
        """Test that returned publisher names match test data"""
        # Act
        response = self.client.get(self.PUBLISHERS_API_PATH)
        data = self._get_response_data(response)
        
        # Assert
        self.assertEqual(response.status_code, 200)
        
        # Extract names from response
        returned_names = [publisher['name'] for publisher in data]
        expected_names = [publisher['name'] for publisher in self.TEST_DATA["publishers"]]
        
        # Check that all expected names are returned
        for expected_name in expected_names:
            self.assertIn(expected_name, returned_names)

    def test_get_publishers_empty_database(self) -> None:
        """Test behavior when no publishers exist"""
        # Arrange - clear all publishers
        with self.app.app_context():
            db.session.query(Publisher).delete()
            db.session.commit()
        
        # Act
        response = self.client.get(self.PUBLISHERS_API_PATH)
        data = self._get_response_data(response)
        
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0)

if __name__ == '__main__':
    unittest.main()