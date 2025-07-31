import asyncssh
import asyncio
import os
import time


class SSHRemoteWorker:
    def __init__(self, host: str, username: str, password: str, port: int = 22) -> None:
        self._host = host
        self._username = username
        self._password = password
        self._port = port
        self._connection = None
        self.__exec_delay = 3

    async def close(self):
        if self._connection:
            self._connection.close()
            await self._connection.wait_closed()

    async def connect(self):
        self._connection = await asyncssh.connect(
            self._host,
            username=self._username,
            password=self._password,
            port=self._port,
            known_hosts=None,
        )

    async def send_file_to_server(self, local_file_path: str):
        async with self._connection.start_sftp_client() as sftp:
            file_name = os.path.basename(local_file_path)
            await sftp.put(local_file_path, file_name)

    async def get_file_from_server(self, remote_file_path: str, local_file_path: str):
        async with self._connection.start_sftp_client() as sftp:
            await sftp.get(remote_file_path, local_file_path)

    async def exec_remote_script(self, script_name: str):
        await self.exec_remote_command(f"sed -i -e 's/\r$//' {script_name}")
        await self.exec_remote_command(f"chmod +x {script_name}")
        await self.exec_remote_command(f"./{script_name}")

    async def remove_remote_files(self, *file_paths: tuple):
        await self.exec_remote_command(f'rm -f {" ".join(file_paths)}')

    async def exec_remote_command(self, command: str):
        await self._connection.run(command, check=True)
