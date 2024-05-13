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
usage: plycut.py [-h] [-o O] 
  [--min minx miny minz] [--max maxx maxy maxz] 
  [--center centerx centery centerz] 
  [--rot roty ]
  [--random RANDOM] src

positional arguments:
  src                   ply file

options:
  -h, --help            show this help message and exit
  -o O                  dest file
  --min x y z     min axis
  --max x y z     max axis
  --center x y z
                  center axis
  --rot deg       rotatino Y
  --random ratio  mabiki
```