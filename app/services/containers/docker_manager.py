import docker


class DockerManager:
    def __init__(self, image, environment=None):

        base_url = f"tcp://172.17.0.185:2375"  # Default Docker remote API port
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


    def get_running_containers(self):
        try:
            containers = self.client.containers.list()
            container_ids = [container.id for container in containers]
            return container_ids
        except docker.errors.APIError as e:
            print(f"Error listing containers: {e}")
            return []




