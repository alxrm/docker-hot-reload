import argparse
import hashlib
from os import walk
import time
from subprocess import call


def md5_checksum(file_name):
    hash_md5 = hashlib.md5()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def find_diff(prev_map, target_dir):
    diff = {}

    for (dir_path, dir_names, file_names) in walk(target_dir, topdown=False):
        for path in map(lambda n: dir_path + '/' + n, filter(lambda p: '.DS_Store' not in p, file_names)):
            file_hash = md5_checksum(path)

            if path not in prev_map or file_hash != prev_map[path]:
                diff[path] = file_hash

    return diff


def observe_directory(target_dir, on_changed, interval_sec=5):
    current_map = find_diff({}, target_dir)

    while True:
        time.sleep(interval_sec)
        next_diff = find_diff(current_map, target_dir)

        if len(next_diff) == 0:
            continue

        for (affected_path, new_hash) in next_diff.items():
            on_changed(affected_path)
            current_map[affected_path] = new_hash


def sync_with_docker(local, remote, container, path):
    start_index = local.find(remote)
    remote_path = path[start_index:]

    print('Updating: {}'.format(path))
    print(['docker', 'cp', path, '{}:{}'.format(container, remote_path)])
    # call(['docker', 'cp', path, '{}:{}'.format(container, remote_path)])


parser = argparse.ArgumentParser(description='Auto-sync files from given root with docker container remote directory')
parser.add_argument('root', help='Root directory to observe')
parser.add_argument('-r', '--remote', dest='remote_root', required=True, help='Remote root to upload into')
parser.add_argument('-c', '--container', dest='container_name', required=True,
                    help='Docker container name, use `docker ps` to find the your container name')

args = parser.parse_args()
root = args.root
remote_root = args.remote_root
container_name = args.container_name

print(root, remote_root, container_name)

if root.find(remote_root) == -1:
    print('Local root must observe the same directory as the remote')
    exit(1)

# file deletion is not supported
observe_directory(root, on_changed=lambda updated_file_path: sync_with_docker(
    root, remote_root, container_name, updated_file_path
))
