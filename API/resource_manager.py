import gc
import threading
import time

from InstructorEmbedding import INSTRUCTOR

global model


class ResourceManager:
    """Class symbiotic to the API, manages vital components to the application. In this case, controls the instantiation
    of the embeddings model and its periodic reload"""

    def __init__(self):
        self.model = None
        #self.reload_thread = threading.Thread(target=self.schedule_model_reload, daemon=True)
        #self.reload_thread.start()

    def load_model(self, model_name):
        """Loads the embedding model to use"""
        self.model = INSTRUCTOR(model_name)
        self.model_name = model_name

    def reload_model(self):
        """Calls the garbage collector periodically to clean any remaining objects generated by the model after
        embedding texts"""
        gc.collect()
        # Reload the model
        self.model = self.load_model(self.model_name)
        print("Model reloaded successfully")

    def schedule_model_reload(self):
        while True:
            time.sleep(3600)  # Sleep for one hour (3600 seconds)
            self.reload_model()
