import docker


class DockerManager:
    def __init__(self, image, environment=None):

        self.client = docker.from_env()
        self.image = image
        self.environment = environment if environment is not None else {}

    def run_container(self):
        try:
            container = self.client.containers.run(
                self.image,
                detach=True,
                environment=self.environment,
                runtime="nvidia",
            )
            return container
        except docker.errors.APIError as e:
            print(f"Error running container: {e}")
            return None

    def stop_container(self, container_id):
        try:
            container = self.client.containers.get(container_id)
            container.stop()
            print(f"Container {container_id} stopped.")
        except docker.errors.NotFound as e:
            print(f"Container not found: {e}")
        except docker.errors.APIError as e:
            print(f"Error stopping container: {e}")

    def remove_container(self, container_id):
        try:
            container = self.client.containers.get(container_id)
            container.remove()
            print(f"Container {container_id} removed.")
        except docker.errors.NotFound as e:
            print(f"Container not found: {e}")
        except docker.errors.APIError as e:
            print(f"Error removing container: {e}")



