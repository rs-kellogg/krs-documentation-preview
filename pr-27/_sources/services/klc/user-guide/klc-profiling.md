# Monitoring and Managing Jobs

## Overall Node Usage

You can find updated stats on memory and CPU usage per KLC node on our official KLC site here: 

https://www.kellogg.northwestern.edu/academics-research/research-support/computing/kellogg-linux-cluster.aspx  

This information is updated every 10 minutes.

You can also determine how much memory is still available on a specific KLC node with: 

  ```bash
  free -h
  ```


## Your Process Status 

To check what’s running or consuming resources:

* List **most** of your running processes:

  ```bash
  ps -u <your net ID>
  ```

* List **ALL** your running processes (including those launched in cronjobs):

  ```bash
  ps aux | grep <your net ID> | grep -v grep
  ```


* Detailed view with process IDs:

  ```bash
  top
  ```

* **Kill** a job/process (use with caution):

  ```bash
  kill [PID]
  ```

## Check Memory

A quick way to determine the memory and CPU consumed by each of your individual KLC processes is with: 

* **CPU and Memory by Process**:

  ```bash
  ps -u <your net ID> -o pid,cmd,%mem,%cpu 
  ```

To obtain a summary of cumulative memory used by all of your processes on a specific KLC node use: 

* **Total Memory Usage**:


  ```bash
  ps -u <your net ID> -o vsz= | awk '{sum+=$1} END {print sum/1024/1024 " GB"}'
  ```

## 💡 Detour: Making Aliases

Since the these commands are quite long, you can save them as permanent aliases in your `bashrc`. 
This allows you to type a short, memorable word instead of the entire line.

1. **Define an Alias**

    Open shell configuration file (e.g., nano ~/.bashrc) 
    ```bash
    nano ~/.bashrc
    ```
    Then add the following to set an alias for these commands.

    ```bash
    alias myprocs='ps -u <your net ID> -o pid,cmd,%mem,%cpu'
    ```

    ```bash
    alias memsum='ps -u <your net ID> -o vsz= | awk "{sum+=\$1} END {print sum/1024/1024 \" GB\"}"'
    ```

2. **Apply these Changes**

    After saving and closing the file, you need to tell your current terminal session to load the new aliases.
    ```bash
    source ~/.bashrc
    ```

3. **Usage**

    Now, you can use the short aliases instead of the full commands.

    ```bash
    myprocs
    ```

    ```bash
    memsum
    ```

## Check Memory with `glances`

You can also check your CPU and memory usage with `glances`.  The `glances` utility is easy-to-read, real-time dashboard that shows your system's CPU, memory, and running processes all at once.
To use this tool on KLC, load the shared environment.

```bash
module load mamba
source activate /kellogg/software/envs/glances_env
glances
```

## Memory Use Notifications

The Research Support team has a `glances` server running on each KLC node at all times.  We can utilize this server to help monitor memory usage in real-time by sending an email notification if either 
- the cumulative memory **your own** processes use OR 
- the total memory consumed by **all** users on a specific node 

hit a threshold we set.

Using a `tmux` command (described in detail [here](./klc-tmux.md)), you can run a `memory_monitor.py` script on any KLC node to monitor your jobs.  
This script requires three input fields: 

1. A total memory threshold

    ```
    -- node_thresold
    ```

    If the total memory on a KLC node falls **BELOW** the node_threshold, the script will send you an email notification

2. A personal memory threshold for all your jobs

    ```
    -- user_thresold
    ```

    If the cumulative memory consumed by all your processes on a node **EXCEEDS** the user_threshold, the script will send you an email notification.

3. Your email

    ```
    -- email
    ```

    An automated email will be sent to and from the personal Kellogg email account you provide here.  These emails will be sent every 10 minutes until you modify the jobs you have running on this node.


[View the full memory monitoring script here](./code/memory_monitor.py)

To launch this memory monitor script, type the following in a new `tmux` session

```bash
# launch a new tmux session
tmux new -s <session name>
tmux new -s memory_monitor
```

```bash
# inside the tmux session
module load mamba
source activate /kellogg/software/envs/glances_env
python memory_monitor.py --email <your email> --user-threshold <amount you select> --node-threshold <amount you select>
python memory_monitor.py --email rs@kellogg.northwestern.edu --user-threshold 400.0 --node-threshold 200.0
```

Detach from `tmux` with:

```
Ctrl + b, then press d
```
