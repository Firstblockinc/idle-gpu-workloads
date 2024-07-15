from services.gpus.gpu_manager import GPUManager
from services.containers.docker_manager import DockerManager
from config.docker.images import nicehash_idle_image
from utils.network import get_local_ip
from config.mining_addresses import gez_nicehash_address
from config.nicehash.nicehash_config import make_signed_request
import time
import logging

ip_address = get_local_ip()
logging.basicConfig(level=logging.INFO)

def scan():
    gpu_manager = GPUManager()
    uuids = gpu_manager.get_idle_gpus(ip_address, "unix", "password")
    string_of_uuids = ', '.join(uuids)
    logging.info(f" {len(uuids)} idle gpus found")
    logging.info(f"(uuids : {uuids})")
    environment={
        "MINING_ADDRESS": "NHbP3AQgHwLAbP266U2UKcppmgTK2ouUCLkV",
        "MINING_WORKER_NAME": f"rig-{get_local_ip()}",
        "NVIDIA_VISIBLE_DEVICES": string_of_uuids,
    }
    print(f"Idle uuids : {uuids}")
    docker_manager = DockerManager(nicehash_idle_image, environment=environment)
    if(len(uuids) > 0):
        logging.info("Running new container")
        container = docker_manager.run_container()
        logging.info(container)

    multiple_processes_list = gpu_manager.get_gpus_with_multiple_processes(ip_address, "unix", "password")
    logging.info(f"Multiple process gpu : {multiple_processes_list}")
    if (len(multiple_processes_list) > 0):
            running_nicehash_containers = docker_manager.get_nicehash_running_containers() #all the running containers on nicehash image only
            docker_manager.stop_container(running_nicehash_containers)
            docker_manager.remove_container(running_nicehash_containers)

if __name__ == "__main__":
    first_run = True
    while True:
        if first_run:
            logging.info(f"Running idle check on ip : {ip_address} after initial delay")
            scan()
            time.sleep(720)  # Sleep for 12 minutes
            first_run = False
        else:
            logging.info(f"Running idle check on ip : {ip_address}")
            scan()
            time.sleep(30)  # Sleep for 20 seconds

