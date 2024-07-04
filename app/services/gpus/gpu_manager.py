from utils.ssh_command import execute_ssh_command


class GPUManager:
          
    def count_gpus(self, ip, username, password):
        command = "nvidia-smi --list-gpus | wc -l"
        output = execute_ssh_command(ip, username, password, command)
        
        if output:
            return int(output.strip())
        return 0

    def check_gpu_process(self, host, username, password):
        command = "nvidia-smi --query-compute-apps=gpu_uuid --format=csv,noheader,nounits"  # Check for any processes running
        try:
            output = execute_ssh_command(host, username, password, command)
            if not output.strip():  # If output is empty, no processes are running
                command_list_uuid = "nvidia-smi --query-gpu=gpu_uuid --format=csv,noheader,nounits"  # Get the GPU UUIDs
                all_gpus_output = execute_ssh_command(host, username, password, command_list_uuid)
                return all_gpus_output.strip().split('\n')
            
            running_gpu_uuids = set(output.strip().split('\n'))
            command_list_uuid = "nvidia-smi --query-gpu=gpu_uuid --format=csv,noheader,nounits"  # Get the GPU UUIDs
            all_gpus_output = execute_ssh_command(host, username, password, command_list_uuid)
            all_gpu_uuids = all_gpus_output.strip().split('\n')
            
            idle_gpus = []
            for gpu_uuid in all_gpu_uuids:
                if gpu_uuid not in running_gpu_uuids:
                    idle_gpus.append(gpu_uuid)
            
            return idle_gpus
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
