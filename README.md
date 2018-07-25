
---

### 1. 要解决的问题

传key自动化，密码去TM

### 2. 环境要求

```

pip install plumbum

pip install paramiko

pip install subprocess

```

### 3. 使用

首先引入公钥存放的路径PUBKEY_PATH `export PUBKEY_PATH=/Users/vonhng/.ssh/id_rsa.pub`

```

➜ ~ transfer_pubkey -h

transfer_pubkey 1.0.0



Usage:

    transfer_pubkey [SWITCHES]



Meta-switches:

    -h, --help Prints this help message and quits

    --help-all Print help messages of all subcommands and quit

    -v, --version Prints the program's version and quits



Switches:

    -i, --ip IPS:str remote ips,use '/' to split  # 可以一次传输到多个节点，节点ip以'/'隔开

    -p, --password PWD:str password  # 远端用户密码，可以不填，默认为cljslrl0620

    -u, --user USER:str user  # 远端用户账号，可以不填，默认为root

```

### 4. Example

- 使用默认账号密码

```

➜ ~ transfer_pubkey -i 10.10.100.5/10.10.100.6

transfer pubkey --> 10.10.100.5

transfer pubkey --> 10.10.100.6

```

- 使用指定账号密码

```

➜ ~ transfer_pubkey -i 192.168.1.105 -u root -p xxxxxxxx

[ ERROR ] Authentication failed.

```

### 5. TODO

#### 谢绝依赖

1). 基于第一点完成后制作成二进制文件

2). GO语言重建

