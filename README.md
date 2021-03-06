# xiaoniu-tr-free [![PyPI version](https://badge.fury.io/py/xiaoniu-tr-free.svg)](https://badge.fury.io/py/xiaoniu-tr-free)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

xiaoniu translate for free -- local cache plus throttling (1.5 calls/s from 201st call on). Let's hope it lasts.

### Update

version 0.0.3, fix query=50980349 and source="text", resort to use requests.get

### Installation
``` pip install -U xiaoniu-tr-free```

or
* Install (pip or whatever) necessary requirements, e.g. ```
pip install requests_cache langid``` or ```
pip install -r requirements.txt```
* Drop the file xiaoniu_tr.py in any folder in your PYTHONPATH (check with import sys; print(sys.path)
* or clone the repo (e.g., ```git clone https://github.com/ffreemt/xiaoniu-tr-free.git``` or download https://github.com/ffreemt/xiaoniu-tr-free/archive/master.zip and unzip) and change to the xiaoniu-tr-free folder and do a ```
python setup.py develop``` or `pip install -e .`

### Usage

```
from xiaoniu_tr import xiaoniu_tr
print(xiaoniu_tr('hello world'))  # -> '你好世界'
print(xiaoniu_tr('Good morning', to_lang='de'))  # ->'Guten Morgen, wow'
print(xiaoniu_tr('hello world', to_lang='fr'))  # ->'Bonjour le monde'
print(xiaoniu_tr('hello world', to_lang='ja'))  # ->'こんにちは世界'
```

### Acknowledgments

* Thanks to everyone whose code was used
