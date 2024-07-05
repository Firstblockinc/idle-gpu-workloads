from services.gpus.gpu_manager import GPUManager
from services.containers.docker_manager import DockerManager
from config.docker.images import nicehash_idle_image
from utils.network import get_local_ip
import time

def scan():
    gpu_manager = GPUManager()
    uuids = gpu_manager.get_idle_gpus("172.17.0.185", "unix", "password")
    string_of_uuids = ', '.join(uuids)
    environment={
        "MINING_ADDRESS": "NHbEoHxbUrsQmGxA9mbtDVTkKWDxwvCQa936",
        "MINING_WORKER_NAME": f"rig-{get_local_ip()}",
        "NVIDIA_VISIBLE_DEVICES": string_of_uuids,
    }

    docker_manager = DockerManager(nicehash_idle_image, environment=environment)
    if(len(uuids) > 0):
        docker_manager.run_container()

    multiple_processes_list = gpu_manager.get_gpus_with_multiple_processes("172.17.0.185", "unix", "password")
    if (len(multiple_processes_list) > 0):
            running_nicehash_containers = docker_manager.get_nicehash_running_containers() #all the running containers on nicehash image only
            docker_manager.stop_container(running_nicehash_containers)
            docker_manager.remove_container(running_nicehash_containers)

if __name__ == "__main__":
    while True:
     print("Running idle check")
     scan()
     time.sleep(20)



