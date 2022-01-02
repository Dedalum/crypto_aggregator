# Crypto aggregator


## Table of contents

- [Tools & CI/CD](#tools-&-ci/cd)
- [Usage](#usage)
- [Development](#development)
- [TODO](#todo)

## Usage

`python main.py` 

### Configuration 
The configuration is defined in the `.env` file and is loaded using the `dotenv` 
module:
```
INPUT="BINANCE" # load data from Binance, other platforms are to be further handled
API_KEY=""      # API key
API_SECRET=""   # API key secret
```

## Development

```
app/        # application, core 
inputs/     # input modules (Binance, other platforms)
model/      # data model
outputs/    # output modules (MQTT, etc.)
```

### Input modules
Input modules are used for gathering data (from crypto coins stockexchanges,
where a wallet is to be expected, etc.): 
- Binance module: uses the wrapper <https://github.com/binance/binance-connector-python>

## TODO
- input modules:
    - Binance: gather further data
    - handle further stock exchanges (and wallets)
- make a output module for a full chain POC (MQTT ?)
- which data model to follow: 1 crypto asset = 1 account or 1 investment ?
- dockerize and kubernitize (ofc)
