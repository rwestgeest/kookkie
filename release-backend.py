#!/usr/bin/env python
import sys
from qi import *

new_version = sys.argv[1]
old_version = read_file('kookkie-backend/VERSION').replace('\n', '')
if not is_valid_version(new_version): fail_with("invalid new version: {}".format(new_version))

answer = input('are you sure to release from {} to {}: '.format(old_version, new_version))
if answer != 'yes': fail_with('no confirmation')

write_file('kookkie-backend/VERSION', new_version)
patch_file('donstro/docker-compose.yml', lambda c: c.replace('afdop-backend:{}'.format(old_version), 'afdop-backend:{}'.format(new_version)))

run_pipeline(
    task('bash', 'docker-login.sh'),
    chdir('kookkie-backend'),
    task('bash', 'build.sh'),
    task('bash', 'build.sh', 'push'),
    chdir('..'),
    task('donstro_single', 'up'),
    task("git", "pull"),
    task("git", "add", "."),
    task("git", "commit", "-am", "release AFP backend {}".format(new_version)),
    task("git", "tag", "-a", "kookkie-backend-{}".format(new_version), "-m", "release AFP backend {}".format(new_version)),
    task("git", "push", "--follow-tags")
)
