# ❄️ Template Generator

Template Generator.

## Local Installation

Download the [Package](https://github.com/SeriousBenEntertainment/Template_Generator/archive/refs/tags/v0.1.0.zip) and install the needed libraries with

### Python Environment

To create a local Python environment with [Miniconda](https://docs.anaconda.com/miniconda/), use the following commands

```bash
# Create the environment
conda env create

# Activate the environment
conda activate template-generator

# to remove
conda remove -n template-generator --all
```

### Python Libraries

Install the needed libraries with

```bash
python -m pip install --upgrade -r --force-reinstall requirements.txt
```

### Execution

Run the software with

```bash
python -m streamlit run ❄️_Template_Generator.py
```

## Remote Deployment (Snowflake)

Use the [VS Code Snowflake Extension](https://marketplace.visualstudio.com/items?itemName=snowflake.snowflake-vsc) to deploy the Native App in the Snowflake Badge (`Run (deploy and re-install`). [Python modules in Snowflake](https://repo.anaconda.com/pkgs/snowflake/). To install the needed snowflake-cli, use these commands

```bash
# Mac
brew tap snowflakedb/snowflake-cli
brew install snowflake-cli

# any other System
python -m pip install --upgrade --force-reinstall snowflake-cli-labs
```

### Snowflake Native App

Run the [Snowflake native app](https://app.snowflake.com/FFCJEQR/pk52190/#/apps/application/OPENAI_BENJAMINGROSS1).

### Snowflake Cortex AI

[Quickstart Guide](https://quickstarts.snowflake.com/guide/getting_started_with_synthetic_data_and_distillation_for_llms/#0).

## MinIO Data Lake

To use the [MinIO](https://min.io/download?license=agpl&platform=docker) in Python install the MinIO Client with

```bash
python -m pip install --upgrade --force-reinstall minio
```

### MinIO Server

Install and run the MinIO Podman container with

```bash
# Podman MinIO Server
podman machine init
podman machine start
podman run -p 9000:9000 -p 9001:9001 minio/minio server /data --console-address ":9001"

# Local MinIO Server on Mac
brew install minio/stable/minio
brew services start minio

# or Windows
https://dl.min.io/server/minio/release/windows-amd64/minio.exe
.\db\minio.exe server C:\minio --console-address :9001
```

Configure tls connection with [certgen](https://github.com/minio/certgen)

```bash
# Generate the certificates
certgen -host "localhost,minio-*.example.net"
certgen -client -host "localhost"
```

Put them into `/opt/homebrew/etc/minio/certs` and `/opt/homebrew/etc/minio/certs/CAs` and restart the MinIO server.

```bash
# Restart the MinIO server
brew services restart minio
mc admin service restart myminio
```

###  MinIO Client

Install the MinIO Client with

```bash
# MinIO Client
brew install minio/stable/mc
mc alias set myminio/ http://127.0.0.1:9000 minioadmin minioadmin

# Info about the MinIO server
mc --insecure admin info myminio

# Set the policy for a bucket (to downloadable)
mc anonymous set download myminio/templategenerator
```

### Web Interface

[Minio Web Interface](http://127.0.0.1:9001/browser).