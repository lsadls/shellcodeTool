# Shellcode转换工具

一个功能强大的shellcode转换工具，支持多种编程语言、混淆方式和加密算法。

## 功能特性

- **多语言支持**: C、Go、Rust、Zig
- **多种混淆方式**:
  - 代码格式（字节数组）
  - IP地址（IPv4/IPv6）
  - MAC地址
  - UUID
- **多种加密算法**:
  - ROT加密（循环移位）
  - RC4流加密
  - XOR加密
  - AES加密（ECB模式）
- **段支持**:
  - 所有语言都支持段定义（.data/.rdata/.text/.rsrc/自定义）
  - 支持自定义数组名称

## 项目结构

```
shellcodeTool/
├── main.py          # 主程序入口
├── converters.py    # 数据转换模块（IP/MAC/UUID）
├── encryption.py    # 加密算法模块
├── formatters.py    # 语言格式化模块
└── README.md        # 项目文档
```

## 安装依赖

```bash
pip install pycryptodome
```

## 使用方法

### 基本语法

```bash
python main.py <文件> [选项]
```

### 参数说明

| 参数         | 简写 | 说明       | 可选值                              | 默认值       |
| ---------- | -- | -------- | -------------------------------- | --------- |
| file       | -  | 输入文件路径   | -                                | 必填        |
| --language | -l | 输出语言     | c, go, rust, zig                 | rust      |
| --func     | -f | 功能类型     | code, ip, mac, uuid              | code      |
| --encrypt  | -e | 加密方式     | none, rot, rc4, xor, aes         | none      |
| --key      | -k | 加密密钥     | -                                | -         |
| --section  | -s | 段名称      | .data, .rdata, .text, .rsrc 或自定义 | .data     |
| --name     | -n | 数组名称     | -                                | shellcode |
| --ipv4     | -4 | 使用IPv4格式 | -                                | false     |
| --ipv6     | -6 | 使用IPv6格式 | -                                | false     |

## 使用示例

### 1. 转换为C语言字节数组（.data段）

```bash
python main.py shellcode.bin -l c -f code -s .data
```

输出示例:

```c
// Shellcode size: 27 bytes
#pragma section(".data", read, write)
__declspec(allocate(".data")) unsigned char shellcode[] = {
    0xfc, 0xe8, 0x82, 0x00, 0x00, 0x00, 0x60, 0x89, 0xe5, 0x31, 0xc0, 0x64, 0x8b, 0x50, 0x30,
    0x8b, 0x52, 0x0c, 0x8b, 0x52, 0x14, 0x8b, 0x72, 0x28, 0x0f, 0xb7, 0x4a, 0x26
};
#pragma comment(linker, "/merge:.data=.data")
unsigned int shellcode_len = sizeof(shellcode);
```

### 2. 转换为C语言字节数组（.rdata段，XOR加密）

```bash
python main.py shellcode.bin -l c -f code -s .rdata -e xor -k "secret"
```

输出示例:

```c
// Shellcode size: 27 bytes (加密: xor)
#pragma section(".rdata", read, write)
__declspec(allocate(".rdata")) unsigned char shellcode[] = {
    0x9e, 0x8c, 0xe8, 0x57, 0x57, 0x57, 0x1c, 0xeb, 0xe9, 0x58, 0xa4, 0x0a, 0xcd, 0x36, 0x56,
    0xcd, 0x34, 0x4a, 0xcd, 0x34, 0x42, 0xcd, 0x1a, 0x4c, 0x69, 0xd4, 0x44
};
#pragma comment(linker, "/merge:.rdata=.data")
unsigned int shellcode_len = sizeof(shellcode);
```

### 3. 转换为C语言字节数组（.text段，自定义名称）

```bash
python main.py shellcode.bin -l c -f code -s .text -n my_payload
```

输出示例:

```c
// Shellcode size: 27 bytes
#pragma section(".text", read, write)
__declspec(allocate(".text")) unsigned char my_payload[] = {
    0xfc, 0xe8, 0x82, 0x00, 0x00, 0x00, 0x60, 0x89, 0xe5, 0x31, 0xc0, 0x64, 0x8b, 0x50, 0x30,
    0x8b, 0x52, 0x0c, 0x8b, 0x52, 0x14, 0x8b, 0x72, 0x28, 0x0f, 0xb7, 0x4a, 0x26
};
#pragma comment(linker, "/merge:.text=.data")
unsigned int my_payload_len = sizeof(my_payload);
```

### 4. 转换为C语言字节数组（自定义段）

```bash
python main.py shellcode.bin -l c -f code -s .mysection -e aes -k "mykey123"
```

输出示例:

```c
// Shellcode size: 32 bytes (加密: aes)
#pragma section(".mysection", read, write)
__declspec(allocate(".mysection")) unsigned char shellcode[] = {
    0x1a, 0x2b, 0x3c, 0x4d, 0x5e, 0x6f, 0x70, 0x81, 0x92, 0xa3, 0xb4, 0xc5, 0xd6, 0xe7, 0xf8,
    0x09, 0x1a, 0x2b, 0x3c, 0x4d, 0x5e, 0x6f, 0x70, 0x81, 0x92, 0xa3, 0xb4, 0xc5, 0xd6, 0xe7,
    0xf8, 0x09
};
#pragma comment(linker, "/merge:.mysection=.data")
unsigned int shellcode_len = sizeof(shellcode);
```

### 5. 转换为Go字节数组（带段注释）

```bash
python main.py shellcode.bin -l go -f code -s .rdata -n my_shellcode
```

输出示例:

```go
// Shellcode size: 27 bytes
// Section: .rdata
var my_shellcode = []byte{0xfc, 0xe8, 0x82, 0x00, 0x00, 0x00, 0x60, 0x89, 0xe5, 0x31, 0xc0, 0x64, 0x8b, 0x50, 0x30, 0x8b, 0x52, 0x0c, 0x8b, 0x52, 0x14, 0x8b, 0x72, 0x28, 0x0f, 0xb7, 0x4a, 0x26}
```

### 6. 转换为Rust字节数组（带段注释，XOR加密）

```bash
python main.py shellcode.bin -l rust -f code -s .text -e xor -k "secret"
```

输出示例:

```rust
// Shellcode size: 27 bytes (加密: xor)
// Section: .text
static shellcode: &[u8] = &[0x9e, 0x8c, 0xe8, 0x57, 0x57, 0x57, 0x1c, 0xeb, 0xe9, 0x58, 0xa4, 0x0a, 0xcd, 0x36, 0x56, 0xcd, 0x34, 0x4a, 0xcd, 0x34, 0x42, 0xcd, 0x1a, 0x4c, 0x69, 0xd4, 0x44];
```

### 7. 转换为Zig字节数组（带段注释，AES加密）

```bash
python main.py shellcode.bin -l zig -f code -s .rsrc -e aes -k "mykey123"
```

输出示例:

```zig
// Shellcode size: 32 bytes (加密: aes)
// Section: .rsrc
const shellcode = [_]u8{0x1a, 0x2b, 0x3c, 0x4d, 0x5e, 0x6f, 0x70, 0x81, 0x92, 0xa3, 0xb4, 0xc5, 0xd6, 0xe7, 0xf8, 0x09, 0x1a, 0x2b, 0x3c, 0x4d, 0x5e, 0x6f, 0x70, 0x81, 0x92, 0xa3, 0xb4, 0xc5, 0xd6, 0xe7, 0xf8, 0x09};
```

### 8. 转换为IPv4地址列表（RC4加密）

```bash
python main.py shellcode.bin -l rust -f ip -4 -e rc4 -k "key123"
```

输出示例:

```rust
// Shellcode size: 27 bytes (加密: rc4)
// IPv4 count: 7

static OBFUSCATED_IPS: &[&str] = &[
    "252.232.130.0",
    "0.96.137.229",
    "49.192.100.139",
    "80.12.139.82",
    "20.139.114.40",
    "15.183.74.38",
    "0.0.0.0",
];
```

### 9. 转换为IPv6地址列表（ROT加密）

```bash
python main.py shellcode.bin -l go -f ip -6 -e rot -k 13
```

输出示例:

```go
// Shellcode size: 27 bytes (加密: rot)
// IPv6 count: 2

var OBFUSCATED_IPS = []string{
    "0b:fb:8f:0d:0d:0d:6d:96:f2:3e:71:77:9c:5f:43:9c",
    "5f:4f:9c:7f:4d:1c:90:c4:b0:87:c1:d2:e3:f4:05:10",
}
```

### 10. 转换为MAC地址列表（无加密）

```bash
python main.py shellcode.bin -l rust -f mac
```

输出示例:

```rust
// Shellcode size: 27 bytes
// MAC count: 5

static OBFUSCATED_MACS: &[&str] = &[
    "fc:e8:82:00:00:00",
    "60:89:e5:31:c0:64",
    "8b:50:30:8b:52:0c",
    "8b:52:14:8b:72:28",
    "0f:b7:4a:26:00:00",
];
```

### 11. 转换为UUID列表（XOR加密）

```bash
python main.py shellcode.bin -l zig -f uuid -e xor -k "obfuscate"
```

输出示例:

```zig
// Shellcode size: 27 bytes (加密: xor)
// UUID count: 2

const OBFUSCATED_UUIDS = [_][]const u8{
    "9e8ce85757571cebe958a408cd3656cd",
    "344acd3442cd1a4c69d4440000000000",
};
```

## 段说明

### PE文件段

本工具支持将shellcode放置在PE文件的不同段中：

| 段名     | 说明    | 特性                  |
| ------ | ----- | ------------------- |
| .data  | 数据段   | 可读可写，默认段            |
| .rdata | 只读数据段 | 可读，通常用于常量           |
| .text  | 代码段   | 可读可执行，通常用于代码        |
| .rsrc  | 资源段   | 可读，用于存储资源           |
| 自定义段   | 用户定义  | 可自定义段名（如.mysection） |

### C 语言段定义

C 语言输出使用以下语法：

```c
#pragma section(".section_name", read, write)
__declspec(allocate(".section_name")) unsigned char array_name[] = {
    // 字节数据
};
#pragma comment(linker, "/merge:.section_name=.data")
unsigned int array_name_len = sizeof(array_name);
```

### Go 语言段定义

Go 语言使用 `//go:section` 和 `//go:linkname` 指令实现段放置：

```go
//go:section .rdata
//go:linkname shellcode .rdata
var shellcode = []byte{0x90, 0x90, 0x90}
```

### Rust 语言段定义

Rust 语言使用 `#[link_section]` 属性实现段放置：

```rust
#[link_section = ".rdata"]
static shellcode: &[u8] = &[0x90, 0x90, 0x90];
```

### Zig 语言段定义

Zig 语言使用 `@linksection` 实现段放置：

```zig
comptime { @linksection(".rdata"); }
const shellcode = [_]u8{ 0x90, 0x90, 0x90 };
```

## 加密算法说明

### ROT加密

- 对每个字节进行循环右移
- 密钥必须是整数（0-255）
- 示例: `-e rot -k 13`

### RC4加密

- 流加密算法
- 密钥可以是字符串或字节数据
- 示例: `-e rc4 -k "mykey"`

### XOR加密

- 对每个字节与密钥进行异或运算
- 密钥循环使用
- 示例: `-e xor -k "secret"`

### AES加密

- 使用AES-ECB模式
- 密钥长度自动调整为16/24/32字节
- 使用PKCS7填充
- 示例: `-e aes -k "mykey123"`

## 模块说明

### converters.py

数据转换模块，提供以下功能:

- `shellcode_to_ips()`: 转换为IP地址列表
- `shellcode_to_macs()`: 转换为MAC地址列表
- `shellcode_to_uuids()`: 转换为UUID列表

### encryption.py

加密算法模块，提供以下功能:

- `rot_encrypt()`: ROT加密
- `rc4_encrypt()`: RC4加密
- `xor_encrypt()`: XOR加密
- `aes_encrypt()`: AES加密

### formatters.py

语言格式化模块，提供以下功能:

- `to_c_byte_array()`: 转换为C语言格式（支持段定义）
- `to_go_byte_slice()`: 转换为Go语言格式
- `to_rust_byte_slice()`: 转换为Rust语言格式
- `to_zig_byte_slice()`: 转换为Zig语言格式

## 注意事项

1. 加密时必须指定密钥（-k 参数）
2. ROT 加密的密钥必须是数字
3. IP 模式需要指定 IPv4 或 IPv6（-4 或 -6 参数）
4. AES 加密会自动填充数据，输出长度可能增加
5. C 语言输出会生成完整的段定义（#pragma section 和\_\_declspec）
6. Go 语言使用 //go:section 和 //go:linkname 指令实现段放置
7. Rust 语言使用 #\[link\_section] 属性实现段放置
8. Zig 语言使用 @linksection 实现段放置
9. 自定义段名可以用于特殊的 PE 文件段（如.rsrc、.pdata 等）
10. 数组名称参数（-n）可用于所有语言，方便代码集成

## 许可证

本项目仅供学习和研究使用。
