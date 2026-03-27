#!/usr/bin/env python3
"""
Shellcode转换工具 - 主程序

功能:
    - 将shellcode文件转换为不同语言的代码格式（C/Go/Rust/Zig）
    - 支持多种混淆方式（IP地址、MAC地址、UUID）
    - 支持多种加密算法（ROT、RC4、XOR、AES）
    - 支持自定义段放置（.data/.rdata/.text/.rsrc/自定义）

使用方法:
    python main.py <文件> [选项]

示例:
    python main.py shellcode.bin -l rust -f code -e xor -k "secret"
    python main.py shellcode.bin -l go -f ip -4 -e rc4 -k "key123"
    python main.py shellcode.bin -l c -f code -s .rdata -e aes -k "mykey"
"""

import sys
import argparse
from converters import shellcode_to_ips, shellcode_to_macs, shellcode_to_uuids
from encryption import rot_encrypt, rc4_encrypt, xor_encrypt, aes_encrypt
from formatters import (
    to_go_byte_slice,
    to_rust_byte_slice,
    to_zig_byte_slice,
    to_c_byte_array,
)


def main():
    """
    主函数：解析命令行参数并执行相应的转换操作

    处理流程:
        1. 解析命令行参数
        2. 读取输入文件
        3. 根据参数进行加密处理
        4. 根据功能类型进行转换
        5. 根据目标语言输出结果
    """
    parser = argparse.ArgumentParser(description="Shellcode转换工具")
    parser.add_argument("file", help="输入文件路径")
    parser.add_argument(
        "-l",
        "--language",
        choices=["c", "go", "rust", "zig"],
        default="rust",
        help="输出语言: c, go, rust, zig",
    )
    parser.add_argument(
        "-f",
        "--func",
        choices=["code", "ip", "mac", "uuid"],
        default="code",
        help="功能类型: code(转成代码), ip(转成IP地址), mac(转成MAC地址), uuid(转成UUID), 默认code",
    )
    parser.add_argument(
        "-s",
        "--section",
        type=str,
        default=".data",
        help="段名称: .data, .rdata, .text, .rsrc 或自定义段名，默认.data (C语言会生成段定义，其他语言仅作注释)",
    )
    parser.add_argument(
        "-n",
        "--name",
        type=str,
        default="shellcode",
        help="数组名称，默认shellcode",
    )
    parser.add_argument(
        "-e",
        "--encrypt",
        choices=["none", "rot", "rc4", "xor", "aes"],
        default="none",
        help="加密方式: none(不加密), rot(ROT加密), rc4(RC4加密), xor(XOR加密), aes(AES加密), 默认none",
    )
    parser.add_argument(
        "-k",
        "--key",
        type=str,
        default="",
        help="加密密钥 (ROT为数字, 其他为字符串)",
    )
    parser.add_argument(
        "-4", "--ipv4", action="store_true", help="使用IPv4格式 (仅ip模式)"
    )
    parser.add_argument(
        "-6", "--ipv6", action="store_true", help="使用IPv6格式 (仅ip模式)"
    )
    args = parser.parse_args()

    try:
        with open(args.file, "rb") as f:
            shellcode = f.read()
    except FileNotFoundError:
        print(f"错误: 文件不存在: {args.file}")
        sys.exit(1)
    except Exception as e:
        print(f"错误: 读取文件失败: {e}")
        sys.exit(1)

    if args.encrypt == "rot":
        if not args.key:
            print("错误: ROT加密需要指定密钥 (-k 参数)")
            sys.exit(1)
        try:
            key = int(args.key)
        except ValueError:
            print("错误: ROT密钥必须是数字")
            sys.exit(1)
        shellcode = rot_encrypt(shellcode, key)
    elif args.encrypt == "rc4":
        if not args.key:
            print("错误: RC4加密需要指定密钥 (-k 参数)")
            sys.exit(1)
        shellcode = rc4_encrypt(shellcode, args.key)
    elif args.encrypt == "xor":
        if not args.key:
            print("错误: XOR加密需要指定密钥 (-k 参数)")
            sys.exit(1)
        shellcode = xor_encrypt(shellcode, args.key)
    elif args.encrypt == "aes":
        if not args.key:
            print("错误: AES加密需要指定密钥 (-k 参数)")
            sys.exit(1)
        shellcode = aes_encrypt(shellcode, args.key)

    if args.func == "ip":
        ipv6 = args.ipv6
        ips = shellcode_to_ips(shellcode, ipv6)
        ip_type = "IPv6" if ipv6 else "IPv4"
        encrypt_info = f" (加密: {args.encrypt})" if args.encrypt != "none" else ""
        print(f"\n// Shellcode size: {len(shellcode)} bytes{encrypt_info}")
        print(f"// {ip_type} count: {len(ips)}")
        if args.language == "go":
            print("\nvar OBFUSCATED_IPS = []string{")
            for ip in ips:
                print(f"    {ip},")
            print("}")
        elif args.language == "rust":
            print("\nstatic OBFUSCATED_IPS: &[&str] = &[")
            for ip in ips:
                print(f"    {ip},")
            print("];")
        elif args.language == "zig":
            print("\nconst OBFUSCATED_IPS = [_][]const u8{")
            for ip in ips:
                print(f"    {ip},")
            print("};")
    elif args.func == "mac":
        macs = shellcode_to_macs(shellcode)
        encrypt_info = f" (加密: {args.encrypt})" if args.encrypt != "none" else ""
        print(f"\n// Shellcode size: {len(shellcode)} bytes{encrypt_info}")
        print(f"// MAC count: {len(macs)}")
        if args.language == "go":
            print("\nvar OBFUSCATED_MACS = []string{")
            for mac in macs:
                print(f"    {mac},")
            print("}")
        elif args.language == "rust":
            print("\nstatic OBFUSCATED_MACS: &[&str] = &[")
            for mac in macs:
                print(f"    {mac},")
            print("];")
        elif args.language == "zig":
            print("\nconst OBFUSCATED_MACS = [_][]const u8{")
            for mac in macs:
                print(f"    {mac},")
            print("};")
    elif args.func == "uuid":
        uuids = shellcode_to_uuids(shellcode)
        encrypt_info = f" (加密: {args.encrypt})" if args.encrypt != "none" else ""
        print(f"\n// Shellcode size: {len(shellcode)} bytes{encrypt_info}")
        print(f"// UUID count: {len(uuids)}")
        if args.language == "go":
            print("\nvar OBFUSCATED_UUIDS = []string{")
            for uuid in uuids:
                print(f"    {uuid},")
            print("}")
        elif args.language == "rust":
            print("\nstatic OBFUSCATED_UUIDS: &[&str] = &[")
            for uuid in uuids:
                print(f"    {uuid},")
            print("];")
        elif args.language == "zig":
            print("\nconst OBFUSCATED_UUIDS = [_][]const u8{")
            for uuid in uuids:
                print(f"    {uuid},")
            print("};")
    elif args.func == "code":
        encrypt_info = f" (加密: {args.encrypt})" if args.encrypt != "none" else ""
        print(f"// Shellcode size: {len(shellcode)} bytes{encrypt_info}")
        if args.language == "c":
            result = to_c_byte_array(shellcode, args.section, args.name)
            print(result)
        elif args.language == "go":
            result = to_go_byte_slice(shellcode, args.section, args.name)
            print(result)
        elif args.language == "rust":
            result = to_rust_byte_slice(shellcode, args.section, args.name)
            print(result)
        elif args.language == "zig":
            result = to_zig_byte_slice(shellcode, args.section, args.name)
            print(result)


if __name__ == "__main__":
    main()
