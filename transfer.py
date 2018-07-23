#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@version: 2.7.10
@author: vonhng
@contact: vonhng@qq.com
@file: transfer.py
@time: 2018/7/13
"""
import subprocess
import paramiko
from plumbum import cli, colors


class SSHError(Exception):
    pass


class SSHClient(paramiko.SSHClient):
    max_read_size = 102400

    def exec_command(self, command, bufsize=-1, timeout=None, get_pty=False):
        stdin, stdout, stderr = super(SSHClient, self).exec_command(command, bufsize, timeout, get_pty)
        stdin.close()
        stdin.flush()

        err = stderr.read()
        output = stdout.read()
        if err:
            raise SSHError(err)
        else:
            return output


class SSH(object):
    def __init__(self, host, username, password,  port=22):
        self.host = host
        self.ssh = SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(host, port, username, password, timeout=2)

    def exec_command(self, command, bufsize=-1, timeout=None, get_pty=False):
        return self.ssh.exec_command(command, bufsize, timeout, get_pty)

    def close(self):
        self.ssh.close()


def run_cmd(cmd):
    try:
        output = subprocess.check_output(cmd, shell=False)
    except Exception as e:
        raise Exception(
            "Run cmd %s failed: %s" % (" ".join(cmd), e))
    return output


class Transfer(cli.Application):
    VERSION = colors.bold | "1.0.0"
    COLOR_GROUPS = {"Meta-switches": colors.bold & colors.yellow, "Switches": colors.bold & colors.yellow}

    _user, _pwd = ("root", "xxxxxxx")  # 这里修改默认用户和密码

    @cli.switch(["-i", "-ip"], str, help="remote ips,use '/' to split")
    def ips(self, ips):
        self._ips = ips

    @cli.switch(["-u", "--user"], str, help="user")
    def user(self, user):
        self._user = user

    @cli.switch(["-p", "--password"], str, help="password")
    def pwd(self, pwd):
        self._pwd = pwd

    def main(self):
        pubkey = run_cmd(["cat", "/Users/vonhng/.ssh/id_rsa.pub"])  # 修改这个路径
        cmd = "echo '{}' >> /root/.ssh/authorized_keys".format(pubkey)
        remote_ips = self._ips.split("/")
        for remote_ip in remote_ips:
            try:
                ssh = SSH(remote_ip, self._user, password=self._pwd, port=22)
                ssh.exec_command(cmd)
                ssh.close()
            except Exception as e:
                print colors.red | "[ ERROR ] {}".format(e)
            else:
                print colors.green | "[ OK ] transfer pubkey --> {}".format(remote_ip)


if __name__ == '__main__':
    Transfer.run()
