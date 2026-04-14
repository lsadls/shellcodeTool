def shellcode_to_ips(shellcode_bytes, ipv6=False):
    """
    将shellcode字节转换为IP地址列表

    Args:
        shellcode_bytes: shellcode字节数据
        ipv6: 是否使用IPv6格式，默认为False（使用IPv4）

    Returns:
        IP地址字符串列表，每个IP地址用引号包裹

    Note:
        - IPv4模式: 每4个字节转换为一个IP地址，格式为 "x.x.x.x"
        - IPv6模式: 每16个字节转换为一个IP地址，格式为 "xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx"
        - 如果最后一块数据不足，用0x00填充
    """
    ips = []
    if ipv6:
        for i in range(0, len(shellcode_bytes), 16):
            chunk = shellcode_bytes[i : i + 16]
            if len(chunk) == 16:
                ip = ":".join(f"{b:02x}" for b in chunk)
                ips.append(f'"{ip}"')
            else:
                padded = chunk + b"\x00" * (16 - len(chunk))
                ip = ":".join(f"{b:02x}" for b in padded)
                ips.append(f'"{ip}"')
    else:
        for i in range(0, len(shellcode_bytes), 4):
            chunk = shellcode_bytes[i : i + 4]
            if len(chunk) == 4:
                ip = ".".join(str(b) for b in chunk)
                ips.append(f'"{ip}"')
            else:
                padded = chunk + b"\x00" * (4 - len(chunk))
                ip = ".".join(str(b) for b in padded)
                ips.append(f'"{ip}"')
    return ips


def shellcode_to_macs(shellcode_bytes):
    """
    将shellcode字节转换为MAC地址列表

    Args:
        shellcode_bytes: shellcode字节数据

    Returns:
        MAC地址字符串列表，每个MAC地址用引号包裹

    Note:
        - 每6个字节转换为一个MAC地址，格式为 "xx:xx:xx:xx:xx:xx"
        - 如果最后一块数据不足，用0x00填充
    """
    macs = []
    for i in range(0, len(shellcode_bytes), 6):
        chunk = shellcode_bytes[i : i + 6]
        if len(chunk) == 6:
            mac = ":".join(f"{b:02x}" for b in chunk)
            macs.append(f'"{mac}"')
        else:
            padded = chunk + b"\x00" * (6 - len(chunk))
            mac = ":".join(f"{b:02x}" for b in padded)
            macs.append(f'"{mac}"')
    return macs


def shellcode_to_uuids(shellcode_bytes):
    """
    将shellcode字节转换为UUID列表

    Args:
        shellcode_bytes: shellcode字节数据

    Returns:
        UUID字符串列表，每个UUID用引号包裹

    Note:
        - 每16个字节转换为一个UUID，格式为 "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        - 如果最后一块数据不足，用0x00填充
    """
    uuids = []
    for i in range(0, len(shellcode_bytes), 16):
        chunk = shellcode_bytes[i : i + 16]
        if len(chunk) == 16:
            uuid = (
                f"{chunk[0]:02x}{chunk[1]:02x}{chunk[2]:02x}{chunk[3]:02x}"
                f"-{chunk[4]:02x}{chunk[5]:02x}"
                f"-{chunk[6]:02x}{chunk[7]:02x}"
                f"-{chunk[8]:02x}{chunk[9]:02x}"
                f"-{chunk[10]:02x}{chunk[11]:02x}{chunk[12]:02x}{chunk[13]:02x}{chunk[14]:02x}{chunk[15]:02x}"
            )
            uuids.append(f'"{uuid}"')
        else:
            padded = chunk + b"\x00" * (16 - len(chunk))
            uuid = (
                f"{padded[0]:02x}{padded[1]:02x}{padded[2]:02x}{padded[3]:02x}"
                f"-{padded[4]:02x}{padded[5]:02x}"
                f"-{padded[6]:02x}{padded[7]:02x}"
                f"-{padded[8]:02x}{padded[9]:02x}"
                f"-{padded[10]:02x}{padded[11]:02x}{padded[12]:02x}{padded[13]:02x}{padded[14]:02x}{padded[15]:02x}"
            )
            uuids.append(f'"{uuid}"')
    return uuids
