import unittest
import gc
import sys
import random
from unittest.mock import patch, Mock

from API.resource_manager import ResourceManager


class TestResourceManager(unittest.TestCase):

    @patch('gc.collect')
    def test_reload_model(self, mock_gc_collect):

        mock_embeddings_model = Mock()

        resource_manager = ResourceManager()
        resource_manager.load_model = Mock(return_value=mock_embeddings_model)

        # Simulate an increase in memory usage
        self.simulate_high_memory_usage()

        # Call reload_model
        resource_manager.reload_model()

        # Assert that load_model was called
        resource_manager.load_model.assert_called_once()

        # Assert that the model attribute was updated
        self.assertIsNotNone(resource_manager.model)

    def simulate_high_memory_usage(self):
        large_list = [random.randint(1, 100) for _ in range(10**6)]
        print(f"Memory usage before collecting: {sys.getsizeof(large_list)} bytes")
        del large_list  # Release the reference to the large list

        # Trigger garbage collection
        gc.collect()

        # Print memory usage after collecting
        print(f"Memory usage after collecting: {sys.getsizeof(gc.garbage)} bytes")

