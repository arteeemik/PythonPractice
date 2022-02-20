import argparse
import venv
import tempfile
import subprocess
import shutil

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get date with some format and font using pyfiglet.')
    parser.add_argument('format', nargs='?', type=str, default='%Y %d %b, %A', help='format date for strftime.')
    parser.add_argument('font', nargs='?', type=str, default='graceful', help='font stype for pyfiglet.')

    args = parser.parse_args()

    temp_dir_name = tempfile.mkdtemp()
    venv.create(temp_dir_name, clear=True, with_pip=True)

    pip_path = temp_dir_name + '/bin/pip'
    subprocess.run([pip_path, 'install', 'pyfiglet'])

    py3_path = temp_dir_name + '/bin/python3'
    subprocess.run([py3_path, '-m', 'figdate', args.format, args.font])

    shutil.rmtree(temp_dir_name)
