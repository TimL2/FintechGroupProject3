# import subprocess allows python interaction with json files
import subprocess
import sys
import json
from copy import deepcopy

img_path = '.\images\business_NFT.png'
print('img_path: ', img_path)

node_path = ".\Program Files\\nodejs\\node.exe"

def pin_img_to_pinata(img_path):
    ipfs_hash = subprocess.check_output([f'{node_path}', './_pinImgToPinata.js', img_path])
    print('IPFS_HASH: ', ipfs_hash)

pin_img_to_pinata(img_path)

