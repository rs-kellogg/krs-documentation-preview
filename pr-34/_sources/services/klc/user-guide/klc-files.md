# Organizing Directories

```{seealso}
For more detail on Quest storage — permissions, scratch space, filesystem quotas, and storage best practices — see the [Quest Filesystems documentation](https://rcdsdocs.it.northwestern.edu/systems/quest/user-guide/filesystem/filesystem.html).
```

## File System on KLC
- Home directory
  - `/home/your_netid/`
  - Your home directory has an 80 GB limit.
    ```bash
    # To quickly check your home directory size, use: 
    homedu
    ```
  - **Note**: 
    The 80 GB quota is a strict limit. Many common issues with logging into KLC or running software are caused by running out of space in your home directory. We strongly recommend storing only essential scripts in your home directory and using the project directory (described below) for research-related work.

- Project directory 
  - `/kellogg/proj/your_netid/`
  - Each KLC project directory will have a strict capacity limit, or "quota". The default quota for each directory is 2 TB. 
  - The current price for additional storage is $195 per TB for up to 5 year of access
  - Email Kellogg Research Support (rs@kellogg.northwestern.edu) if you want to create a project directory or share directory with collaborators

- To check storage consumed on any KLC folder, navigate to the folder and use: 
    ```bash
    module load dust
    dust
    ```


## Common Linux Commands for File Management
### Working with directory
```bash
# List files in the current directory
ls

# Change to a specified directory
cd directory_name

# Print the current working directory
pwd

# Create a new directory
mkdir new_directory_name
```

### Working with files
```bash
# Copy a file to a new location
cp origin_file destination_file

# Move or rename a file
mv origin_file destination_file

# Delete a file
rm file_name
```
