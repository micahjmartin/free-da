"""
Sourced from the patch files at https://github.com/hluwa/Patchs

Condensed into one script. This tool needs updated once we get the build working
"""
try:
    import lief
except:
    pass
import sys
import random
import os

if __name__ == "__main__":
    input_file = sys.argv[1]
    print(f"[*] Patch frida-agent: {input_file}")
    random_name = "".join(random.sample("ABCDEFGHIJKLMNO", 5))
    print(f"[*] Patch `frida` to `{random_name}``")

    binary = lief.parse(input_file)

    if not binary:
        exit()

    for symbol in binary.symbols:
        if symbol.name == "frida_agent_main":
            symbol.name = "main"
        
        if "frida" in symbol.name:
            symbol.name = symbol.name.replace("frida", random_name)

        if "FRIDA" in symbol.name:
            symbol.name = symbol.name.replace("FRIDA", random_name)

    binary.write(input_file)

    # gum-js-loop thread
    random_name = "".join(random.sample("abcdefghijklmnpqrstuv", 11))
    print(f"[*] Patch `gum-js-loop` to `{random_name}`")
    os.system(f"sed -b -i s/gum-js-loop/{random_name}/g {input_file}")


    # gmain thread
    random_name = "".join(random.sample("abcdefghijklmn", 5))
    print(f"[*] Patch `gmain` to `{random_name}`")
    os.system(f"sed -b -i s/gmain/{random_name}/g {input_file}")
