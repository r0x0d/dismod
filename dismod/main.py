import code
import dis 

def read_file(path: str) -> str:
    with open(path, mode='r') as f: 
        return f.read()

def main() -> int: 
    contents = read_file("cases/main.py")
    
    a = dis.Bytecode(contents)
    a = list(a)
    # b = dis.get_instructions(a[0].argval)
    
    print("Disassembly A:")

    for b in a: 
        if b.opcode == 108 or b.opcode == 109:
            print(b)
        # if b.opcode == 108 or b.opcode == 109 or "<code" in b.argval: 
        
    # print("Disassembly B:")
    # [print(c) for c in b]

    return 0 