import docker


class DockerManager:
    def __init__(self, image, environment=None):

        #must be changed to local
        base_url = "unix://var/run/docker.sock"
        self.client = docker.DockerClient(base_url=base_url)
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

    def stop_container(self, container_ids):
        try:
            if container_ids:
                for id in container_ids:
                    container = self.client.containers.get(id)
                    container.stop()
                    print(f"CONTAINER {container_ids} STOPPED.")
                else:
                    print("No containers running")
        except docker.errors.NotFound as e:
            print(f"Container not found: {e}")
        except docker.errors.APIError as e:
            print(f"Error stopping container: {e}")

    def remove_container(self, container_ids):
        try:
            if container_ids:
                for id in container_ids:
                    container = self.client.containers.get(id)
                    container.remove()
                print(f"CONTAINER {container_ids} REMOVED.")
            else:
                print("No containers running")
        except docker.errors.NotFound as e:
            print(f"Container not found: {e}")
        except docker.errors.APIError as e:
            print(f"Error removing container: {e}")


    def get_nicehash_running_containers(self, image="dockerhubnh/nicehash:latest"):
        try:
            containers = self.client.containers.list()
            # Filter containers by the specified image tag
            containers = [container for container in containers if any(tag == image for tag in container.image.tags)]
            container_ids = [container.id for container in containers]
            return container_ids
        except docker.errors.APIError as e:
            print(f"Error listing containers: {e}")
            return []




