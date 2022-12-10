# icon-cli

icon-cli is a command line interface for interacting with the ICON blockchain network. At this time, icon-cli is in active development, so we don't recommend using it for mission-critical tasks for now.

## Commands

### config

* `icon config network`: Change the default network in config.yml.
* `icon config purge`: Empty icon-cli's internal trash bin.
* `icon config view`: View the current config.yml file.
* `icon config keystore add`: Import an existing keystore into icon-cli.
* `icon config keystore list`: List all imported keystores.
* `icon config keystore set`: Set the default keystore for interacting with the ICON blockchain.

### query

* `icon query abi`: View the ABI of a SCORE on the ICON blockchain.
* `icon query block`: View information about an ICON block.
* `icon query tx`: View information about an ICX transaction.
* `icon query tx-result`: View information about the result of an ICX transaction.

### tx

* `icon tx send`: Send an ICX transaction.