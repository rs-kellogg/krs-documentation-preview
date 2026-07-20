# Organizing Directories

```{seealso}
For more detail on Quest storage — permissions, scratch space, filesystem quotas, and storage best practices — see the [Quest Filesystems documentation](https://rcdsdocs.it.northwestern.edu/systems/quest/user-guide/filesystem/filesystem.html).
```

## File System on KLC
- Home directory
  - `/home/your_netid/`
  - 80 GB
    ```bash
    # Quick check of home directory usage
    homedu
    ```
  - **Note**: 
    The 80 GB quota is a strict limit. Many common issues with logging into KLC or running software are caused by running out of space in your home directory. We strongly recommend storing only essential scripts in your home directory and using the project directory (described below) for research-related work.

- Project directory 
  - `/kellogg/proj/netid/`
  - Each KLC project directory will have a strict capacity limit, or "quota". The default quota for each directory is 2 TB. 
  - The current price for additional storage is $195 per TB for up to 5 year of access
  - Email Kellogg Research Support (rs@kellogg.northwestern.edu) if you want to create a project directory or share directory with collaborators

- Check usage of space at current folder
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
cp original_file destination_file

# Move or rename a file
mv original_file destination_file

# Delete a file
rm file_name
```
