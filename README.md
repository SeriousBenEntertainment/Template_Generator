# ❄️ Template Generator

Template Generator.

## Local Installation

Download the [Package](https://github.com/SeriousBenEntertainment/Template_Generator/archive/refs/tags/v0.1.0.zip) and install the needed libraries with

### Python Environment

To create a local Python environment with [Miniconda](https://docs.anaconda.com/miniconda/), use the following commands

```bash
conda create --name myenv python=3.10
conda activate myenv
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

# or local MinIO Server
brew install minio/stable/minio
```

###  MinIO Client

Install the MinIO Client with

```bash
# MinIO Client
brew install minio/stable/mc
mc alias set myminio/ http://127.0.0.1:9000 minioadmin minioadmin

# Info about the MinIO server
mc --insecure admin info myminio
```

### Web Interface

[Minio Web Interface](http://127.0.0.1:9001/browser).