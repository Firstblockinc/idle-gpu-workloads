from utils.ssh_command import execute_ssh_command


class GPUManager:
          
    def count_gpus(self, ip, username, password):
        command = "nvidia-smi --list-gpus | wc -l"
        output = execute_ssh_command(ip, username, password, command)
        
        if output:
            return int(output.strip())
        return 0

    def get_idle_gpus(self, host, username, password):
        command = "nvidia-smi --query-compute-apps=gpu_uuid --format=csv,noheader,nounits"  # Check for any processes running
        try:
            output = execute_ssh_command(host, username, password, command)
            command_list_uuid = "nvidia-smi --query-gpu=gpu_uuid --format=csv,noheader,nounits"  # Get the GPU UUIDs
            all_gpus_output = execute_ssh_command(host, username, password, command_list_uuid)
            
            if not output.strip():  # If output is empty, no processes are running
                return all_gpus_output.strip().split('\n')
            
            running_gpu_uuids = set(output.strip().split('\n'))
            all_gpu_uuids = all_gpus_output.strip().split('\n')
            
            idle_gpus = []
            for gpu_uuid in all_gpu_uuids:
                if gpu_uuid not in running_gpu_uuids:
                    idle_gpus.append(gpu_uuid)
            
            return idle_gpus
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def get_running_gpus(self, host, username, password):
        try:
            # Command to get the UUIDs of GPUs currently running processes
            command = "nvidia-smi --query-compute-apps=gpu_uuid --format=csv,noheader,nounits"
            
            # Execute the command
            output = execute_ssh_command(host, username, password, command)
            
            # Process the output
            if output.strip():  # If there is output, process it
                running_gpu_uuids = set(output.strip().split('\n'))
            else:  # If output is empty, no GPUs are running processes
                running_gpu_uuids = set()
            
            return list(running_gpu_uuids)
        except Exception as e:
            print(f"An error occurred while retrieving running GPUs: {e}")
            return []

    def get_gpus_with_multiple_processes(self, host, username, password):
        try:
            # Command to get detailed information about processes using GPUs
            command = "nvidia-smi --query-compute-apps=gpu_uuid --format=csv,noheader,nounits"
            output = execute_ssh_command(host, username, password, command)
            
            if not output.strip():
                return []  # No processes running
            
            # Split the output into lines
            gpu_uuids = output.strip().split('\n')
            # Count the number of processes per GPU
            gpu_process_count = {}
            for gpu_uuid in gpu_uuids:
                if gpu_uuid in gpu_process_count:
                    gpu_process_count[gpu_uuid] += 1
                else:
                    gpu_process_count[gpu_uuid] = 1
            
            # Filter GPUs with 2 or more processes
            gpus_with_multiple_processes = [gpu_uuid for gpu_uuid, count in gpu_process_count.items() if count >= 2]
            
            return gpus_with_multiple_processes
        except Exception as e:
            print(f"An error occurred while retrieving GPUs with multiple processes: {e}")
            return []
