import os


def to_go_byte_slice(data, section=None, array_name="shellcode", nop_sled=0):
    """
    将数据转换为 Go 语言的字节数组格式，支持段定义和NOP sled

    Args:
        data: 输入数据，可以是文件路径 (str)、bytes 对象或 list[int]
        section: 段名称，支持 .data, .rdata, .text, .rsrc 或自定义段名
        array_name: 数组名称，默认为 shellcode
        nop_sled: NOP sled长度，在shellcode前面添加的0x90数量，默认为0

    Returns:
        Go 语言字节数组格式的字符串，包含段定义（如果指定）

    Raises:
        FileNotFoundError: 当输入是文件路径但文件不存在时
        TypeError: 当输入类型不支持时
        ValueError: 当列表元素不是 0-255 之间的整数时

    Note:
        - 支持三种输入类型：文件路径、bytes 对象、整数列表
        - 输出格式为 Go 语言的字节数组语法
        - 使用 //go:section 和 //go:linkname 指令实现段放置
        - NOP sled通过在shellcode前面添加0x90指令实现
    """
    byte_list = []
    if isinstance(data, str):
        if not os.path.exists(data):
            raise FileNotFoundError(f"文件不存在：{data}")
        with open(data, "rb") as f:
            file_data = f.read()
            byte_list = list(file_data)
    elif isinstance(data, bytes):
        byte_list = list(data)
    elif isinstance(data, list):
        byte_list = data
    else:
        raise TypeError("输入必须是 文件路径 (str), bytes 对象，或 list[int]")
    if not all(isinstance(b, int) and 0 <= b <= 255 for b in byte_list):
        raise ValueError("列表中的所有元素必须是 0 到 255 之间的整数")

    if nop_sled > 0:
        nop_sled_bytes = [0x90] * nop_sled
        byte_list = nop_sled_bytes + byte_list

    hex_parts = [f"0x{b:02x}" for b in byte_list]
    if not hex_parts:
        return "[]byte{}"

    result = ""
    if section:
        result += f"//go:section {section}\n"
        result += f"//go:linkname {array_name} {section}\n"
    if nop_sled > 0:
        result += f"// NOP sled: {nop_sled} bytes\n"
    result += f"var {array_name} = []byte{{" + ", ".join(hex_parts) + "}"
    return result


def to_rust_byte_slice(data, section=None, array_name="shellcode", nop_sled=0):
    """
    将数据转换为 Rust 语言的字节数组格式，支持段定义和NOP sled

    Args:
        data: 输入数据，可以是文件路径 (str)、bytes 对象或 list[int]
        section: 段名称，支持 .data, .rdata, .text, .rsrc 或自定义段名
        array_name: 数组名称，默认为 shellcode
        nop_sled: NOP sled长度，在shellcode前面添加的0x90数量，默认为0

    Returns:
        Rust 语言字节数组格式的字符串，包含段定义（如果指定）

    Raises:
        FileNotFoundError: 当输入是文件路径但文件不存在时
        TypeError: 当输入类型不支持时
        ValueError: 当列表元素不是 0-255 之间的整数时

    Note:
        - 支持三种输入类型：文件路径、bytes 对象、整数列表
        - 输出格式为 Rust 语言的字节数组语法
        - 使用 #[link_section] 属性实现段放置
        - NOP sled通过在shellcode前面添加0x90指令实现
    """
    byte_list = []
    if isinstance(data, str):
        if not os.path.exists(data):
            raise FileNotFoundError(f"文件不存在：{data}")
        with open(data, "rb") as f:
            file_data = f.read()
            byte_list = list(file_data)
    elif isinstance(data, bytes):
        byte_list = list(data)
    elif isinstance(data, list):
        byte_list = data
    else:
        raise TypeError("输入必须是 文件路径 (str), bytes 对象，或 list[int]")
    if not all(isinstance(b, int) and 0 <= b <= 255 for b in byte_list):
        raise ValueError("列表中的所有元素必须是 0 到 255 之间的整数")

    if nop_sled > 0:
        nop_sled_bytes = [0x90] * nop_sled
        byte_list = nop_sled_bytes + byte_list

    hex_parts = [f"0x{b:02x}" for b in byte_list]
    if not hex_parts:
        return "&[u8]"

    result = ""
    if section:
        result += f'#[link_section = "{section}"]\n'
    if nop_sled > 0:
        result += f"// NOP sled: {nop_sled} bytes\n"
    result += f"static {array_name}: &[u8] = &[" + ", ".join(hex_parts) + "];"
    return result


def to_zig_byte_slice(data, section=None, array_name="shellcode", nop_sled=0):
    """
    将数据转换为 Zig 语言的字节数组格式，支持段定义和NOP sled

    Args:
        data: 输入数据，可以是文件路径 (str)、bytes 对象或 list[int]
        section: 段名称，支持 .data, .rdata, .text, .rsrc 或自定义段名
        array_name: 数组名称，默认为 shellcode
        nop_sled: NOP sled长度，在shellcode前面添加的0x90数量，默认为0

    Returns:
        Zig 语言字节数组格式的字符串，包含段定义（如果指定）

    Raises:
        FileNotFoundError: 当输入是文件路径但文件不存在时
        TypeError: 当输入类型不支持时
        ValueError: 当列表元素不是 0-255 之间的整数时

    Note:
        - 支持三种输入类型：文件路径、bytes 对象、整数列表
        - 输出格式为 Zig 语言的字节数组语法
        - 使用 linksection 实现段放置
        - NOP sled通过在shellcode前面添加0x90指令实现
    """
    byte_list = []
    if isinstance(data, str):
        if not os.path.exists(data):
            raise FileNotFoundError(f"文件不存在：{data}")
        with open(data, "rb") as f:
            file_data = f.read()
            byte_list = list(file_data)
    elif isinstance(data, bytes):
        byte_list = list(data)
    elif isinstance(data, list):
        byte_list = data
    else:
        raise TypeError("输入必须是 文件路径 (str), bytes 对象，或 list[int]")
    if not all(isinstance(b, int) and 0 <= b <= 255 for b in byte_list):
        raise ValueError("列表中的所有元素必须是 0 到 255 之间的整数")

    if nop_sled > 0:
        nop_sled_bytes = [0x90] * nop_sled
        byte_list = nop_sled_bytes + byte_list

    hex_parts = [f"0x{b:02x}" for b in byte_list]
    if not hex_parts:
        return "[_]u8{}"

    result = ""
    if section:
        result += f'comptime {{ @linksection("{section}"); }}\n'
    if nop_sled > 0:
        result += f"// NOP sled: {nop_sled} bytes\n"
    result += f"const {array_name} = [_]u8{{" + ", ".join(hex_parts) + "};"
    return result


def to_c_byte_array(data, section=".data", array_name="shellcode", nop_sled=0):
    """
    将数据转换为 C 语言的字节数组格式，支持指定段和NOP sled

    Args:
        data: 输入数据，可以是文件路径 (str)、bytes 对象或 list[int]
        section: 段名称，支持 .data, .rdata, .text, .rsrc 或自定义段名，默认为 .data
        array_name: 数组名称，默认为 shellcode
        nop_sled: NOP sled长度，在shellcode前面添加的0x90数量，默认为0

    Returns:
        C 语言字节数组格式的字符串，包含段定义和数组声明

    Raises:
        FileNotFoundError: 当输入是文件路径但文件不存在时
        TypeError: 当输入类型不支持时
        ValueError: 当列表元素不是 0-255 之间的整数时

    Note:
        - 支持三种输入类型：文件路径、bytes 对象、整数列表
        - 输出格式为 C 语言的字节数组语法，包含段定义
        - 支持常见的 PE 文件段：.data, .rdata, .text, .rsrc
        - 也支持自定义段名
        - NOP sled通过在shellcode前面添加0x90指令实现
    """
    byte_list = []
    if isinstance(data, str):
        if not os.path.exists(data):
            raise FileNotFoundError(f"文件不存在：{data}")
        with open(data, "rb") as f:
            file_data = f.read()
            byte_list = list(file_data)
    elif isinstance(data, bytes):
        byte_list = list(data)
    elif isinstance(data, list):
        byte_list = data
    else:
        raise TypeError("输入必须是 文件路径 (str), bytes 对象，或 list[int]")
    if not all(isinstance(b, int) and 0 <= b <= 255 for b in byte_list):
        raise ValueError("列表中的所有元素必须是 0 到 255 之间的整数")

    if nop_sled > 0:
        nop_sled_bytes = [0x90] * nop_sled
        byte_list = nop_sled_bytes + byte_list

    hex_parts = [f"0x{b:02x}" for b in byte_list]
    if not hex_parts:
        return ""

    result = f'#pragma section("{section}", read, write)\n'
    result += f'__declspec(allocate("{section}")) unsigned char {array_name}[] = {{\n'

    for i in range(0, len(hex_parts), 16):
        line_parts = hex_parts[i : i + 16]
        result += "    " + ", ".join(line_parts)
        if i + 16 < len(hex_parts):
            result += ","
        result += "\n"

    result += r"}};\n"
    result += f'#pragma comment(linker, "/merge:{section}=.data")\n'
    result += f"unsigned int {array_name}_len = sizeof({array_name});\n"

    return result
