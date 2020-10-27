import os
import subprocess

def apktool_decompile(apk_fp, out_dir):
    print(f'Decompiling {(apk_fp)}...')

    command = subprocess.run([
        'apktool', 'd',     # decode
        apk_fp,             # apk filename
        '-o', out_dir,      # out dir path
        '-f',               # overwrite out path
        '--no-res'          # do not decode resources
    ], capture_output=True)

    print(command.stdout.decode(), end="")
    if command.stderr != b'':
        print(command.stderr.decode())
