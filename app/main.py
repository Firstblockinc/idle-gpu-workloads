from services.gpus.gpu_manager import GPUManager
from services.containers.docker_manager import DockerManager
from config.docker.images import nicehash_idle_image

gpu_manager = GPUManager()

environment={
    "MINING_ADDRESS": "NHbEoHxbUrsQmGxA9mbtDVTkKWDxwvCQa936",
    "MINING_WORKER_NAME": "idle",
    "NVIDIA_VISIBLE_DEVICES": "all"
}
#error docker and test with join
docker_manager = DockerManager(nicehash_idle_image, environment=environment)

if __name__ == "__main__":
    uuids = gpu_manager.check_gpu_process("172.17.0.185", "unix", "password")
    string_of_uuids = ', '.join(uuids)
    