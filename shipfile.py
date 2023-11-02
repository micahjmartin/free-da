"""
A Shipyard class that implements the patches located at https://github.com/hluwa/Patchs

These patches make frida most resistant to detection
"""
import os
import re
import shutil

from shipyard import CodePatch, EZ

class Shipfile:
    Name = "frida-core"
    Url = "https://github.com/frida/frida-core"
    source_directory = "frida-core"

    @CodePatch(r".*/base/rpc\.vala")
    def rpc(file):
        """
        0001-strongR-frida-string_frida_rpc.patch
        """
        with EZ(file) as f:
            # Replace both these strings
            f.replace_all({
                r'"\"frida:rpc\""': '(string) GLib.Base64.decode("ImZyaWRhOnJwYyI=")',
                '"frida:rpc"': '(string) GLib.Base64.decode("ZnJpZGE6cnBj=")'
            }, err=True)

    @CodePatch(r".*/server/server\.vala")
    def server(file):
        """
        0002-strongR-frida-io_re_frida_server.patch
        """
        with EZ(file) as f:
            f.replace('"re.frida.server"', "null", err=True)
            f.reinsert(
                r"\s+Environment.init\s*\(\);",
                "\n		DEFAULT_DIRECTORY = GLib.Uuid.string_random();",
                before=True,
                err="hunk #2 failed. regex not found {regex}"
            )

    @CodePatch(r".*/binjector-glue\.c")
    def binjector(file):
        """
        0003-strongR-frida-pipe_linjector.patch
        """
        with EZ(file) as f:
            f.replace(
                re.compile(r'\(.+binjector.+self..temp_path..self..id\)'),
                '("%s/%p%u", self->temp_path, self, self->id)',
                err=True
            )

    @CodePatch(r".*/linux-host-session.vala")
    def agent(file):
        """
        0004-strongR-frida-io_frida_agent_so.patch
        """
        with EZ(file) as f:
            f.reinsert(
                r"\s+agent = new AgentDescriptor.*frida-agent-<arch>",
                "\n\t\t\tvar random_prefix = GLib.Uuid.string_random();",
                before=True,
                err=True
            )
            f.replace(
                '"frida-agent-',
                'random_prefix + "-',
                err=True
            )

    @CodePatch(r".*\.vala")
    def agent_main(file):
        """
        0005-strongR-frida-symbol_frida_agent_main.patch
        """
        with EZ(file) as f:
            f.replace('"frida_agent_main"', '"main"')

    @CodePatch(r".*/embed-agent\.sh")
    def inject_anti_anti_frida(file):
        """
        0005-strongR-frida-symbol_frida_agent_main.patch
        0006-strongR-frida-thread_gum_js_loop.patch
        0007-strongR-frida-thread_gmain.patch

        Implement the parts of these patch files that create the anti-anti-frida.py script
        """
        with EZ(file) as f:
            lines = [
                '',
                '  if [ -f "$custom_script" ]; then',
                '    python3 "$custom_script" "$embedded_agent"',
                '  fi'
            ]
            f.reinsert(r'\s+embedded_agents\+=\("\$embedded_agent"\)', lines, before=True, err=True)
            f.reinsert(r'\s+exec.+--toolchain=gnu -c ".resource_config" -o ".output_dir/frida-data-agent" ".embedded_agent"', lines, before=True, err=True)
            f.reinsert(r"#!.*bash", 'custom_script="$output_dir/../../../../frida-core/src/anti-anti-frida.py"', err=True)
        # Add the file to the source dir
        dst = os.path.join(Shipfile.source_directory, "src", "anti-anti-frida.py")
        src, _ = os.path.split(__file__)
        src = os.path.join(src, "anti-anti-frida.py")
        shutil.copy(src, dst)

    @CodePatch(r".*/droidy/droidy-client\.vala")
    def droidy(file):
        """
        0008-strongR-frida-protocol_unexpected_command.patch
        """
        with EZ(file) as f:
            s = 'throw new Error.PROTOCOL ("Unexpected command");'
            f.replace(s, "break; // " + s, err=True)

