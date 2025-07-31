import os
from typing import Optional
from src.workers import constants
from .paths import create_file, read_file, remove_file
from src.libs.ssh.SSHRemoteWorker import SSHRemoteWorker


# TODO: пока что максимальная длина равна 1
# async def get_ovpn_file_from_server(
#     ip: str, login: str, password: str, path_to_save_file: str, name_file: str
# ) -> None:
#     ssh_worker = SSHRemoteWorker(host=ip, username=login, password=password)
#     await ssh_worker.connect()
#     await ssh_worker.get_file_from_server(
#         remote_file_path=OVPN_FILE_PATH,
#         local_file_path=os.path.join(path_to_save_file, name_file),
#     )


# TODO: пока что максимальная длина равна 1
# async def setup_intermediate_server(
#     ip: str, login: str, password: str, prev_id: str
# ) -> None:
#     ssh_worker = SSHRemoteWorker(host=ip, username=login, password=password)
#     await ssh_worker.connect()
#     prev_file_vpn_path = os.path.join(
#         TEMP_FOLDER_RELATIVE_PATH, f"connection-to-vpn{prev_id}.ovpn"
#     )
#     await ssh_worker.send_file_to_server(os.path.join(prev_file_vpn_path))
#     remove_file(prev_file_vpn_path)
#     await ssh_worker.send_file_to_server(
#         os.path.join(SCRIPTS_FOLDER_RELATIVE_PATH, IPTABLES_RULE_FILE_NAME)
#     )
#     await ssh_worker.exec_remote_script(IPTABLES_RULE_FILE_NAME)
#     await ssh_worker.create_connection(
#         f"openvpn --config connection-to-vpn{prev_id}.ovpn"
#     )
#     await ssh_worker.close()

#     await ssh_worker.connect()
#     await ssh_worker.send_file_to_server(
#         os.path.join(SCRIPTS_FOLDER_RELATIVE_PATH, CHAIN_RULE_FILE_NAME)
#     )

#     await ssh_worker.exec_remote_script(CHAIN_RULE_FILE_NAME)
#     await ssh_worker.close()


# TODO: пока что максимальная длина равна 1
# async def remove_chain_rule(ip: int, login: str, password: str, file_name: str) -> None:
#     ssh_worker = SSHRemoteWorker(host=ip, username=login, password=password)
#     await ssh_worker.connect()

#     await ssh_worker.send_file_to_server(
#         os.path.join(SCRIPTS_FOLDER_RELATIVE_PATH, REMOVE_CHAIN_FILE_NAME)
#     )
#     await ssh_worker.exec_remote_script(REMOVE_CHAIN_FILE_NAME)
#     await ssh_worker.remove_remote_files(
#         REMOVE_CHAIN_FILE_NAME,
#         IPTABLES_RULE_FILE_NAME,
#         CHAIN_RULE_FILE_NAME,
#         file_name,
#     )
#     await ssh_worker.close()


async def remove_vpn_settings(ip: int, login: str, password: str) -> None:
    ssh_worker = SSHRemoteWorker(host=ip, username=login, password=password)
    await ssh_worker.connect()
    await ssh_worker.send_file_to_server(
        os.path.join(
            constants.SCRIPTS_FOLDER_RELATIVE_PATH,
            constants.REMOVE_OVPN_SERVER_FILE_NAME,
        )
    )
    await ssh_worker.exec_remote_script(constants.REMOVE_OVPN_SERVER_FILE_NAME)
    await ssh_worker.remove_remote_files(
        constants.REMOVE_OVPN_SERVER_FILE_NAME, constants.INSTALL_OVPN_SERVER_FILE_NAME
    )
    await ssh_worker.close()


async def create_chain_client(
    ip: int, login: str, password: str, client_name: str, client_password: Optional[str]
):
    ssh_worker = SSHRemoteWorker(host=ip, username=login, password=password)

    content = read_file(
        path=os.path.join(
            constants.SCRIPTS_FOLDER_RELATIVE_PATH, constants.CREATE_CLIENT
        )
    )
    client_sh_file_name = create_client_sh_filename(client_name=client_name)
    content = (
        content.replace("{client}", client_name)
        .replace("{pass}", "2" if client_password is not None else "1")
        .replace(
            "{password}", client_password if client_password is not None else "None"
        )
    )
    create_client_temp_path = os.path.join(
        constants.TEMP_FOLDER_RELATIVE_PATH, client_sh_file_name
    )
    create_file(path=create_client_temp_path, content=content)
    await ssh_worker.connect()
    await ssh_worker.send_file_to_server(create_client_temp_path)
    remove_file(file_path=create_client_temp_path)
    await ssh_worker.exec_remote_script(client_sh_file_name)
    await ssh_worker.remove_remote_files(client_sh_file_name)

    client_ovpn_filename = create_client_ovpn_filename(client_name=client_name)
    await ssh_worker.get_file_from_server(
        remote_file_path=client_ovpn_filename,
        local_file_path=os.path.join(
            constants.DATA_FOLDER_RELATIVE_PATH, client_ovpn_filename
        ),
    )
    await ssh_worker.close()


async def delete_chain_client(ip: int, login: str, password: str, client_name: str):
    ssh_worker = SSHRemoteWorker(host=ip, username=login, password=password)

    content = read_file(
        path=os.path.join(
            constants.SCRIPTS_FOLDER_RELATIVE_PATH, constants.REVOKE_CLIENT
        )
    )
    delete_client_sh_file_name = delete_client_sh_filename(client_name=client_name)
    content = content.replace("{client}", client_name)
    delete_client_temp_path = os.path.join(
        constants.TEMP_FOLDER_RELATIVE_PATH, delete_client_sh_file_name
    )
    create_file(path=delete_client_temp_path, content=content)
    await ssh_worker.connect()
    await ssh_worker.send_file_to_server(delete_client_temp_path)
    remove_file(file_path=delete_client_temp_path)
    await ssh_worker.exec_remote_script(delete_client_sh_file_name)
    await ssh_worker.remove_remote_files(delete_client_sh_file_name)
    remove_file(
        os.path.join(
            constants.DATA_FOLDER_RELATIVE_PATH,
            create_client_ovpn_filename(client_name=client_name),
        )
    )
    await ssh_worker.close()


def create_client_name(username: str, timestamp: float):
    return f"{username}_{timestamp}"


def create_client_ovpn_filename(client_name: str):
    return f"{client_name}.ovpn"


def create_client_sh_filename(client_name: str):
    return f"{client_name}.sh"


def delete_client_sh_filename(client_name: str):
    return f"delete_{client_name}.sh"
