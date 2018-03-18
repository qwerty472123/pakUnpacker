# pakUnpacker

Chrome pak([Chromium](https://chromium.googlesource.com/) [Grit](https://chromium.googlesource.com/chromium/src/tools/grit/) 生成文件)解包打包工具，用以修改 Chromium 发行版翻译及资源内容。

## 功能信息如下

- `py pakDataUnpack.py [-h] <files...>` 将名称为`{name}.pak`的 pak 文件解包到名称为`{name}-{encoding}-data`的文件夹，其中所有 alias 项使用软连接(`os.symlink`)，您也可以用`-h`指令来使用硬链接。
- `py pakDataPack.py <dirs...>` 将文件夹名称符合格式`{name}-{encoding}-data`的文件夹打包回`{name}.pak`。
- `py pakLangUnpack.py <files...>` 将用于存储翻译信息的 pak 文件解包到对应 json 文件。
- `py pakLangPack.py <files...>` 将 json 文件重新打包回 pak 文件。
- `py pakResLink.py [-f] [-a] [-h] <dirs...>` 将由`pakDataUnpack.py`解压得到的文件夹中的部分内容软链接(`os.symlink`)到名称为`{name}-{encoding}-link`的文件夹，该文件夹中的内容回尝试通过`pakResIds.json`中的`md5 => filename`信息恢复正确命名，找不到的文件不会被链接。
    
    您也可以用`-h`指令来使用硬链接，使用`-f`来链接未知文件到`{name}-{encoding}-link\unknown`文件夹，使用`-a`来链接标识出的文件(已经是**软**链接)和未标识出`filename`信息相同的文件到`{name}-{encoding}-link\alias`和`{name}-{encoding}-link\preAlias`文件夹。这些未知的文件会被尝试识别出扩展名。
- `py pakResAddByDir.py <files...>` 从文件夹中除 unknown/preAlias/alias 三个子文件夹中的文件以外的文件中获取`md5 => filename`并合并入`pakResIds.json`，以新合并入的信息为准。这一文件夹可以是你手工标记过的文件夹，也可以是其他工具生成的文件夹，例如: <https://shuax.com/cpv5> 。
- `py pakResAddByMerge.py <dirs...>` 将文件中的`md5 => filename`与`pakResIds.json`合并，并以新合并入的信息为准。
- `py pakTransformPack.py <files...>` 转换 pak 文件格式的版本。对于名称为`{name}.pak`的pak文件，如果它是 v4 版本，会生成名称为`{name}.v5.pak`的 v5 版本 pak 文件;反之，会生成名称为`{name}.v4.pak`的 v4 版本 pak 文件。

## 提示

所有的 py 文件都依赖于`pakPackLib.py`，且支持读入 v4/v5 版本的 pak 文件。除去`py pakTransformPack.py <files...>`中说明的特殊情况外，生成的 pak 文件都为 v5 版本。

## 其他内容

v4 文件夹下是一套简陋的 v4 版本的解包打包工具。

pakLang 文件夹下是一个支持对 v4 版本语言 pak 文件进行进一步翻译的 GUI 工具。

getResourceByShuaX 文件夹下是复制自 <https://github.com/shuax/ChromePAK/tree/master/resource_ids> (Copyright (c) 2016 舒俊杰) 的`md5 => filename`的信息抓取工具，你可以将得到的`resource_ids.json`文件用`pakResAddByMerge.py`合并入`pakResIds.json`。
