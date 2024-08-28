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
brew tap snowflakedb/snowflake-cli
brew install snowflake-cli
python -m pip install --upgrade --force-reinstall snowflake-cli-labs
```

### Snowflake Native App

Run the [Snowflake native app](https://app.snowflake.com/FFCJEQR/pk52190/#/apps/application/OPENAI_BENJAMINGROSS1).