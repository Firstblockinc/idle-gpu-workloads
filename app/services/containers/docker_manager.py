import docker
import logging
logging.basicConfig(level=logging.INFO)


class DockerManager:
    def __init__(self, image, environment=None):

        #base_url = "unix://var/run/docker.sock"
        #self.client = docker.DockerClient(base_url=base_url)
        base_url = f"tcp://10.0.1.185:2375"  # Default Docker remote API port
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
            logging.info(container)
            container_details = self.client.containers.get(container.id).attrs
            
            env_vars = container_details['Config']['Env']
            devices = self.get_nvidia_visible_devices(env_vars)
            print("Yooo")
            print(devices)
            return container
        except docker.errors.APIError as e:
            logging.error(f"Error running container: {e}")
            return None

    def stop_container(self, container_ids):
        try:
            if container_ids:
                for id in container_ids:
                    container = self.client.containers.get(id)
                    container.stop()
                    logging.info(f"CONTAINER {container_ids} STOPPED.")
                else:
                    logging.info("No containers running")
        except docker.errors.NotFound as e:
            logging.error(f"Container not found: {e}")
        except docker.errors.APIError as e:
            logging.error(f"Error stopping container: {e}")

    def remove_container(self, container_ids):
        try:
            if container_ids:
                for id in container_ids:
                    container = self.client.containers.get(id)
                    container.remove()
                logging.info(f"CONTAINER {container_ids} REMOVED.")
            else:
                logging.info("No containers running")
        except docker.errors.NotFound as e:
            logging.error(f"Container not found: {e}")
        except docker.errors.APIError as e:
            logging.error(f"Error removing container: {e}")

    def get_nicehash_running_containers(self, image="dockerhubnh/nicehash:latest"):
        try:
            containers = self.client.containers.list()
            # Filter containers by the specified image tag
            containers = [container for container in containers if any(tag == image for tag in container.image.tags)]
            container_ids = [container.id for container in containers]
            return container_ids
        except docker.errors.APIError as e:
            logging.error(f"Error listing containers: {e}")
            return []

    def get_nvidia_visible_devices(self, env_vars):
        for env in env_vars:
            if env.startswith('NVIDIA_VISIBLE_DEVICES='):
                return env.split('=', 1)[1]
        return None
