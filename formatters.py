import os


def to_go_byte_slice(data, section=None, array_name="shellcode"):
    """
    将数据转换为Go语言的字节数组格式

    Args:
        data: 输入数据，可以是文件路径(str)、bytes对象或list[int]
        section: 段名称（可选），仅用于注释说明
        array_name: 数组名称，默认为 shellcode

    Returns:
        Go语言字节数组格式的字符串，例如: []byte{0x90, 0x90, 0x90}

    Raises:
        FileNotFoundError: 当输入是文件路径但文件不存在时
        TypeError: 当输入类型不支持时
        ValueError: 当列表元素不是0-255之间的整数时

    Note:
        - 支持三种输入类型：文件路径、bytes对象、整数列表
        - 输出格式为Go语言的字节数组语法
    """
    byte_list = []
    if isinstance(data, str):
        if not os.path.exists(data):
            raise FileNotFoundError(f"文件不存在: {data}")
        with open(data, "rb") as f:
            file_data = f.read()
            byte_list = list(file_data)
    elif isinstance(data, bytes):
        byte_list = list(data)
    elif isinstance(data, list):
        byte_list = data
    else:
        raise TypeError("输入必须是 文件路径(str), bytes 对象, 或 list[int]")
    if not all(isinstance(b, int) and 0 <= b <= 255 for b in byte_list):
        raise ValueError("列表中的所有元素必须是 0 到 255 之间的整数")
    hex_parts = [f"0x{b:02x}" for b in byte_list]
    if not hex_parts:
        return "[]byte{}"
    
    result = ""
    if section:
        result += f"// Section: {section}\n"
    result += f"var {array_name} = []byte{{" + ", ".join(hex_parts) + "}"
    return result


def to_rust_byte_slice(data, section=None, array_name="shellcode"):
    """
    将数据转换为Rust语言的字节数组格式

    Args:
        data: 输入数据，可以是文件路径(str)、bytes对象或list[int]
        section: 段名称（可选），仅用于注释说明
        array_name: 数组名称，默认为 shellcode

    Returns:
        Rust语言字节数组格式的字符串，例如: &[u8] = &[0x90, 0x90, 0x90]

    Raises:
        FileNotFoundError: 当输入是文件路径但文件不存在时
        TypeError: 当输入类型不支持时
        ValueError: 当列表元素不是0-255之间的整数时

    Note:
        - 支持三种输入类型：文件路径、bytes对象、整数列表
        - 输出格式为Rust语言的字节数组语法
    """
    byte_list = []
    if isinstance(data, str):
        if not os.path.exists(data):
            raise FileNotFoundError(f"文件不存在: {data}")
        with open(data, "rb") as f:
            file_data = f.read()
            byte_list = list(file_data)
    elif isinstance(data, bytes):
        byte_list = list(data)
    elif isinstance(data, list):
        byte_list = data
    else:
        raise TypeError("输入必须是 文件路径(str), bytes 对象, 或 list[int]")
    if not all(isinstance(b, int) and 0 <= b <= 255 for b in byte_list):
        raise ValueError("列表中的所有元素必须是 0 到 255 之间的整数")
    hex_parts = [f"0x{b:02x}" for b in byte_list]
    if not hex_parts:
        return "&[u8]"
    
    result = ""
    if section:
        result += f"// Section: {section}\n"
    result += f"static {array_name}: &[u8] = &[" + ", ".join(hex_parts) + "];"
    return result


def to_zig_byte_slice(data, section=None, array_name="shellcode"):
    """
    将数据转换为Zig语言的字节数组格式

    Args:
        data: 输入数据，可以是文件路径(str)、bytes对象或list[int]
        section: 段名称（可选），仅用于注释说明
        array_name: 数组名称，默认为 shellcode

    Returns:
        Zig语言字节数组格式的字符串，例如: [_]u8{0x90, 0x90, 0x90}

    Raises:
        FileNotFoundError: 当输入是文件路径但文件不存在时
        TypeError: 当输入类型不支持时
        ValueError: 当列表元素不是0-255之间的整数时

    Note:
        - 支持三种输入类型：文件路径、bytes对象、整数列表
        - 输出格式为Zig语言的字节数组语法
    """
    byte_list = []
    if isinstance(data, str):
        if not os.path.exists(data):
            raise FileNotFoundError(f"文件不存在: {data}")
        with open(data, "rb") as f:
            file_data = f.read()
            byte_list = list(file_data)
    elif isinstance(data, bytes):
        byte_list = list(data)
    elif isinstance(data, list):
        byte_list = data
    else:
        raise TypeError("输入必须是 文件路径(str), bytes 对象, 或 list[int]")
    if not all(isinstance(b, int) and 0 <= b <= 255 for b in byte_list):
        raise ValueError("列表中的所有元素必须是 0 到 255 之间的整数")
    hex_parts = [f"0x{b:02x}" for b in byte_list]
    if not hex_parts:
        return "[_]u8{}"
    
    result = ""
    if section:
        result += f"// Section: {section}\n"
    result += f"const {array_name} = [_]u8{{" + ", ".join(hex_parts) + "};"
    return result


def to_c_byte_array(data, section=".data", array_name="shellcode"):
    """
    将数据转换为C语言的字节数组格式，支持指定段

    Args:
        data: 输入数据，可以是文件路径(str)、bytes对象或list[int]
        section: 段名称，支持 .data, .rdata, .text, .rsrc 或自定义段名，默认为 .data
        array_name: 数组名称，默认为 shellcode

    Returns:
        C语言字节数组格式的字符串，包含段定义和数组声明

    Raises:
        FileNotFoundError: 当输入是文件路径但文件不存在时
        TypeError: 当输入类型不支持时
        ValueError: 当列表元素不是0-255之间的整数时

    Note:
        - 支持三种输入类型：文件路径、bytes对象、整数列表
        - 输出格式为C语言的字节数组语法，包含段定义
        - 支持常见的PE文件段：.data, .rdata, .text, .rsrc
        - 也支持自定义段名
    """
    byte_list = []
    if isinstance(data, str):
        if not os.path.exists(data):
            raise FileNotFoundError(f"文件不存在: {data}")
        with open(data, "rb") as f:
            file_data = f.read()
            byte_list = list(file_data)
    elif isinstance(data, bytes):
        byte_list = list(data)
    elif isinstance(data, list):
        byte_list = data
    else:
        raise TypeError("输入必须是 文件路径(str), bytes 对象, 或 list[int]")
    if not all(isinstance(b, int) and 0 <= b <= 255 for b in byte_list):
        raise ValueError("列表中的所有元素必须是 0 到 255 之间的整数")
    
    hex_parts = [f"0x{b:02x}" for b in byte_list]
    if not hex_parts:
        return ""
    
    result = f'#pragma section("{section}", read, write)\n'
    result += f'__declspec(allocate("{section}")) unsigned char {array_name}[] = {{\n'
    
    for i in range(0, len(hex_parts), 16):
        line_parts = hex_parts[i:i+16]
        result += "    " + ", ".join(line_parts)
        if i + 16 < len(hex_parts):
            result += ","
        result += "\n"
    
    result += f"}};\n"
    result += f'#pragma comment(linker, "/merge:{section}=.data")\n'
    result += f'unsigned int {array_name}_len = sizeof({array_name});\n'
    
    return result
