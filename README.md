# plycut

crop point cloud .ply data.

needs python3 

## Example

```
./plycut.py src.ply -o out.ply --min -1 -1 -1 --max 1 1 1 

```
crop (-1,-1,-1)-(1,1,1)


## usage

```
usage: plycut.py [-h] [-o O] [--min MIN MIN MIN] [--max MAX MAX MAX] [--center CENTER CENTER CENTER] [--random RANDOM] src

positional arguments:
  src                   ply file

options:
  -h, --help            show this help message and exit
  -o O                  dest file
  --min MIN MIN MIN     min axis
  --max MAX MAX MAX     max axis
  --center CENTER CENTER CENTER
                        center axis
  --random RANDOM       mabiki
```