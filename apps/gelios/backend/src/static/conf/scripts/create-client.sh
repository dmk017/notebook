#!/bin/bash

function newClient() {
  CLIENT={client}
  PASS={pass}
	PASSWORD={password}

	CLIENTEXISTS=$(tail -n +2 /etc/openvpn/easy-rsa/pki/index.txt | grep -c -E "/CN=$CLIENT\$")
	if [[ $CLIENTEXISTS == '1' ]]; then
		echo ""
		echo "The specified client CN was already found in easy-rsa, please choose another name."
		
		
		exit
	else
		cd /etc/openvpn/easy-rsa/ || return
		case $PASS in
		1)
			./easyrsa --batch build-client-full "$CLIENT" nopass
			;;
		2)
    	/usr/bin/expect <<EOF
spawn ./easyrsa --batch build-client-full "$CLIENT"
exp_internal 1
expect "Enter PEM pass phrase:" {
    send "$PASSWORD\r"
    exp_continue
}
expect "Verifying - Enter PEM pass phrase:" {
    send "$PASSWORD\r"
    exp_continue
}
expect eof
EOF
    ;;
		esac
		echo "Client $CLIENT added."
	fi

	if [ -e "/home/${CLIENT}" ]; then
		homeDir="/home/${CLIENT}"
	elif [ "${SUDO_USER}" ]; then
		if [ "${SUDO_USER}" == "root" ]; then
			homeDir="/root"
		else
			homeDir="/home/${SUDO_USER}"
		fi
	else
		homeDir="/root"
	fi

	TLS_SIG="1"

	# Generates the custom client.ovpn
	cp /etc/openvpn/client-template.txt "$homeDir/$CLIENT.ovpn"
	{
		echo "<ca>"
		cat "/etc/openvpn/easy-rsa/pki/ca.crt"
		echo "</ca>"

		echo "<cert>"
		awk '/BEGIN/,/END CERTIFICATE/' "/etc/openvpn/easy-rsa/pki/issued/$CLIENT.crt"
		echo "</cert>"

		echo "<key>"
		cat "/etc/openvpn/easy-rsa/pki/private/$CLIENT.key"
		echo "</key>"

		echo "<tls-crypt>"
		cat /etc/openvpn/tls-crypt.key
		echo "</tls-crypt>"
	} >>"$homeDir/$CLIENT.ovpn"

	echo ""
	echo "The configuration file has been written to $homeDir/$CLIENT.ovpn."
	echo "Download the .ovpn file and import it in your OpenVPN client."

	exit 0
}


newClient
