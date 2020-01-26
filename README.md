# docker-hot-reload
Yoba-boba hot-reload(auto sync) util

## Usage

```sh
$ python3 yobareload.py /absolute/local/root --remote /root --container some-container-name
```

`-c/--container` — docker container name or id

`-r/--remote` — remote root directory

It's using [docker cp](https://docs.docker.com/engine/reference/commandline/cp/) to update files in the container.

## Roots
Please note that local root should have the same path segment as the remote root's first one.

**Correct**

local root is `/Users/me/app/static` remote root is `/static`

**Wrong**

local root is `/Users/me/app/scripts/styles` remote root is `/app/styles`

**Correct**

local root is `/Users/me/app/scripts/styles` remote root is `/scripts/styles`
