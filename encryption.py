from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


def rot_encrypt(data, key):
    """
    ROT加密（循环移位加密）

    Args:
        data: 要加密的字节数据
        key: 旋转密钥（整数，0-255）

    Returns:
        加密后的字节数据

    Note:
        - 对每个字节进行循环右移，使用模256确保结果在0-255范围内
        - key必须是整数类型
    """
    result = bytearray()
    for byte in data:
        result.append((byte + key) % 256)
    return bytes(result)


def rc4_encrypt(data, key):
    """
    RC4流加密算法

    Args:
        data: 要加密的字节数据
        key: 加密密钥（字符串或字节数据）

    Returns:
        加密后的字节数据

    Note:
        - RC4是一种流加密算法，使用密钥调度算法（KSA）和伪随机生成算法（PRGA）
        - 密钥可以是字符串或字节数据
    """
    s = list(range(256))
    j = 0
    key_bytes = key if isinstance(key, bytes) else key.encode()
    key_len = len(key_bytes)
    for i in range(256):
        j = (j + s[i] + key_bytes[i % key_len]) % 256
        s[i], s[j] = s[j], s[i]
    result = bytearray()
    i = j = 0
    for byte in data:
        i = (i + 1) % 256
        j = (j + s[i]) % 256
        s[i], s[j] = s[j], s[i]
        result.append(byte ^ s[(s[i] + s[j]) % 256])
    return bytes(result)


def xor_encrypt(data, key):
    """
    XOR加密算法

    Args:
        data: 要加密的字节数据
        key: 加密密钥（字符串或字节数据）

    Returns:
        加密后的字节数据

    Note:
        - 对每个字节与密钥进行异或运算
        - 密钥循环使用，如果数据长度超过密钥长度则重复使用密钥
        - XOR加密是对称加密，再次使用相同密钥解密即可还原
    """
    key_bytes = key if isinstance(key, bytes) else key.encode()
    key_len = len(key_bytes)
    result = bytearray()
    for i, byte in enumerate(data):
        result.append(byte ^ key_bytes[i % key_len])
    return bytes(result)


def aes_encrypt(data, key):
    """
    AES加密算法（ECB模式）

    Args:
        data: 要加密的字节数据
        key: 加密密钥（字符串或字节数据）

    Returns:
        加密后的字节数据

    Note:
        - 使用AES-ECB模式进行加密
        - 密钥长度必须是16、24或32字节（AES-128、AES-192、AES-256）
        - 如果密钥长度不符合要求，会自动填充到32字节
        - 使用PKCS7填充方式处理数据块对齐
    """
    key_bytes = key if isinstance(key, bytes) else key.encode()
    if len(key_bytes) not in [16, 24, 32]:
        key_bytes = key_bytes[:32].ljust(32, b"\x00")
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    padded_data = pad(data, AES.block_size)
    encrypted = cipher.encrypt(padded_data)
    return encrypted
