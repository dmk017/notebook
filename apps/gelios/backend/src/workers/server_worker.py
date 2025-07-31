import os
from src.workers import constants
from src.libs.ssh.SSHRemoteWorker import SSHRemoteWorker
from src.services.server.data.servers_schema import ServerState


async def check_server_alive(ip: str, login: str, password: str) -> ServerState:
    ssh_worker = SSHRemoteWorker(host=ip, username=login, password=password)

    server_status = ServerState.READY
    try:
        await ssh_worker.connect()
    except:
        server_status = ServerState.UNAVAILABLE

    await ssh_worker.close()

    return server_status


async def prepare_server_for_chain(
    ip: str, login: str, password: str, subnet: int
) -> None:
    ssh_worker = SSHRemoteWorker(host=ip, username=login, password=password)

    await ssh_worker.connect()
    await ssh_worker.send_file_to_server(
        local_file_path=os.path.join(
            constants.SCRIPTS_FOLDER_RELATIVE_PATH, constants.UPDATING_PACKAGES
        )
    )
    await ssh_worker.exec_remote_script(script_name=constants.UPDATING_PACKAGES)
    await ssh_worker.remove_remote_files(constants.UPDATING_PACKAGES)
    await ssh_worker.send_file_to_server(
        local_file_path=os.path.join(
            constants.SCRIPTS_FOLDER_RELATIVE_PATH,
            constants.INSTALL_OVPN_SERVER_FILE_NAME,
        )
    )
    await ssh_worker.exec_remote_script(
        script_name=constants.INSTALL_OVPN_SERVER_FILE_NAME
    )
    await ssh_worker.close()
