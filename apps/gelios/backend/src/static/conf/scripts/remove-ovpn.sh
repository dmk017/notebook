#!/bin/bash


function isRoot() {
	if [ "$EUID" -ne 0 ]; then
		return 1
	fi
}


function tunAvailable() {
	if [ ! -e /dev/net/tun ]; then
		return 1
	fi
}


function checkOS() {
	if [[ -e /etc/debian_version ]]; then
		OS="debian"
		source /etc/os-release

		if [[ $ID == "debian" || $ID == "raspbian" ]]; then
			if [[ $VERSION_ID -lt 9 ]]; then
				echo "⚠️ Your version of Debian is not supported."
				echo ""
				echo "However, if you're using Debian >= 9 or unstable/testing then you can continue, at your own risk."
				echo ""
			fi
		elif [[ $ID == "ubuntu" ]]; then
			OS="ubuntu"
			MAJOR_UBUNTU_VERSION=$(echo "$VERSION_ID" | cut -d '.' -f1)
			if [[ $MAJOR_UBUNTU_VERSION -lt 16 ]]; then
				echo "⚠️ Your version of Ubuntu is not supported."
				echo ""
				echo "However, if you're using Ubuntu >= 16.04 or beta, then you can continue, at your own risk."
				echo ""
			fi
		fi
	elif [[ -e /etc/system-release ]]; then
		source /etc/os-release
		if [[ $ID == "fedora" || $ID_LIKE == "fedora" ]]; then
			OS="fedora"
		fi
		if [[ $ID == "centos" || $ID == "rocky" || $ID == "almalinux" ]]; then
			OS="centos"
			if [[ ${VERSION_ID%.*} -lt 7 ]]; then
				echo "⚠️ Your version of CentOS is not supported."
				echo ""
				echo "The script only support CentOS 7 and CentOS 8."
				echo ""
				exit 1
			fi
		fi
		if [[ $ID == "ol" ]]; then
			OS="oracle"
			if [[ ! $VERSION_ID =~ (8) ]]; then
				echo "Your version of Oracle Linux is not supported."
				echo ""
				echo "The script only support Oracle Linux 8."
				exit 1
			fi
		fi
		if [[ $ID == "amzn" ]]; then
			OS="amzn"
			if [[ $VERSION_ID != "2" ]]; then
				echo "⚠️ Your version of Amazon Linux is not supported."
				echo ""
				echo "The script only support Amazon Linux 2."
				echo ""
				exit 1
			fi
		fi
	elif [[ -e /etc/arch-release ]]; then
		OS=arch
	else
		echo "Looks like you aren't running this installer on a Debian, Ubuntu, Fedora, CentOS, Amazon Linux 2, Oracle Linux 8 or Arch Linux system"
		exit 1
	fi
}


function initialCheck() {
	if ! isRoot; then
		echo "Sorry, you need to run this as root"
		exit 1
	fi
	if ! tunAvailable; then
		echo "TUN is not available"
		exit 1
	fi
	checkOS
}



function removeOpenVPN() {
	PORT=$(grep '^port ' /etc/openvpn/server.conf | cut -d " " -f 2)
	PROTOCOL=$(grep '^proto ' /etc/openvpn/server.conf | cut -d " " -f 2)
	echo "$PORT"
	echo "$PROTOCOL"

	# Stop OpenVPN
	if [[ $OS =~ (fedora|arch|centos|oracle) ]]; then
		systemctl disable openvpn-server@server
		systemctl stop openvpn-server@server
		# Remove customised service
		rm /etc/systemd/system/openvpn-server@.service
	elif [[ $OS == "ubuntu" ]] && [[ $VERSION_ID == "16.04" ]]; then
		systemctl disable openvpn
		systemctl stop openvpn
	else
		systemctl disable openvpn@server
		systemctl stop openvpn@server
		# Remove customised service
		rm /etc/systemd/system/openvpn\@.service
	fi

	# Remove the iptables rules related to the script
	systemctl stop iptables-openvpn
	# Cleanup
	systemctl disable iptables-openvpn
	rm /etc/systemd/system/iptables-openvpn.service
	systemctl daemon-reload
	rm /etc/iptables/add-openvpn-rules.sh
	rm /etc/iptables/rm-openvpn-rules.sh

	# SELinux
	if hash sestatus 2>/dev/null; then
		if sestatus | grep "Current mode" | grep -qs "enforcing"; then
			if [[ $PORT != '1194' ]]; then
				semanage port -d -t openvpn_port_t -p "$PROTOCOL" "$PORT"
			fi
		fi
	fi

	if [[ $OS =~ (debian|ubuntu) ]]; then
		apt-get remove --purge -y openvpn
		if [[ -e /etc/apt/sources.list.d/openvpn.list ]]; then
			rm /etc/apt/sources.list.d/openvpn.list
			apt-get update
		fi
	elif [[ $OS == 'arch' ]]; then
		pacman --noconfirm -R openvpn
	elif [[ $OS =~ (centos|amzn|oracle) ]]; then
		yum remove -y openvpn
	elif [[ $OS == 'fedora' ]]; then
		dnf remove -y openvpn
	fi

	# Cleanup
	find /home/ -maxdepth 2 -name "*.ovpn" -delete
	find /root/ -maxdepth 1 -name "*.ovpn" -delete
	rm -rf /etc/openvpn
	rm -rf /usr/share/doc/openvpn*
	rm -f /etc/sysctl.d/99-openvpn.conf
	rm -rf /var/log/openvpn

	echo ""
	echo "OpenVPN removed!"
}


initialCheck
removeOpenVPN