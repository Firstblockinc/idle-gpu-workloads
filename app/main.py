from services.gpus.gpu_manager import GPUManager
from services.containers.docker_manager import DockerManager
from config.docker.images import nicehash_idle_image
from utils.network import get_local_ip
import time
import logging
import threading

ip_address = get_local_ip()
last_three_chars = ip_address[-3:]
logging.basicConfig(level=logging.INFO)

scan_interval = 720  
short_interval = 30 
multiple_process_check_interval = 8 

def scan():
    while True:
        gpu_manager = GPUManager()
        uuids = gpu_manager.get_idle_gpus(ip_address, "unix", "password")
        string_of_uuids = ', '.join(uuids)
        logging.info(f"{len(uuids)} idle GPUs found")
        logging.info(f"(UUIDs: {uuids})")
        environment = {
            "MINING_ADDRESS": "NHbP3AQgHwLAbP266U2UKcppmgTK2ouUCLkV",
            "MINING_WORKER_NAME": f"AI-Rig-{last_three_chars}",
            "NVIDIA_VISIBLE_DEVICES": string_of_uuids,
        }
        print(f"Idle UUIDs: {uuids}")
        docker_manager = DockerManager(nicehash_idle_image, environment=environment)
        
        if len(uuids) > 0:
            logging.info("Running new container")
            container = docker_manager.run_container()
            logging.info(container)
            time_to_sleep = scan_interval
        else:

            time_to_sleep = short_interval
        
        logging.info(f"Sleeping for {time_to_sleep} seconds")
        time.sleep(time_to_sleep)

def check_multiple_processes():
    while True:
        gpu_manager = GPUManager()
        docker_manager = DockerManager(nicehash_idle_image)
        multiple_processes_list = gpu_manager.get_gpus_with_multiple_processes(ip_address, "unix", "password")
        logging.info(f"Multiple process GPUs: {multiple_processes_list}")
        if len(multiple_processes_list) > 0:
            running_nicehash_containers = docker_manager.get_nicehash_running_containers()  
            docker_manager.stop_container(running_nicehash_containers)
            docker_manager.remove_container(running_nicehash_containers)
        logging.info(f"Sleeping for {multiple_process_check_interval} seconds")
        time.sleep(multiple_process_check_interval)

if __name__ == "__main__":
    scan_thread = threading.Thread(target=scan)
    check_thread = threading.Thread(target=check_multiple_processes)
    
    scan_thread.start()
    check_thread.start()
    
    scan_thread.join()
    check_thread.join()
