import os


CONFIG_FOLDER_RELATIVE_PATH = "src/static/conf"
OVPN_FILE_PATH = "/etc/openvpn/client.ovpn"
SCRIPTS_FOLDER_RELATIVE_PATH = os.path.join(CONFIG_FOLDER_RELATIVE_PATH, "scripts")
TEMP_FOLDER_RELATIVE_PATH = os.path.join(CONFIG_FOLDER_RELATIVE_PATH, "temp")
DATA_FOLDER_RELATIVE_PATH = os.path.join(CONFIG_FOLDER_RELATIVE_PATH, "data")

CONFIG_FILE_NAME = "config.json"
INSTALL_OVPN_SERVER_FILE_NAME = "install-ovpn.sh"
IPTABLES_RULE_FILE_NAME = "setup-iptables-rule.sh"
CHAIN_RULE_FILE_NAME = "setup-chain-rules.sh"
REMOVE_CHAIN_FILE_NAME = "remove-chain-rules.sh"
REMOVE_OVPN_SERVER_FILE_NAME = "remove-ovpn.sh"
UPDATING_PACKAGES = "updating-packages.sh"
CREATE_CLIENT = "create-client.sh"
REVOKE_CLIENT = "revoke-client.sh"
