# binja-headless

Author: **@hugsy**

Headless Binary Ninja (sort of!)

_Note_: A Snippet version can be copy/pasted from [here](https://gist.github.com/hugsy/714e0038d5d0b1deb7fad1907928252f)

## Description

This plugin allows you to use Binary Ninja headlessly and remotely to script and control Binja remotely without the need of an entreprise license. This makes it convenient for creating scripts, or live reversing using Jupyter for instance. It works internally by simply creating an RPyc service within the Python environment, and expose it on a TCP socket. Note that this plugin is Binary Ninja specific: an equivalent for IDA was created in the repository [IDA-Headless](https://github.com/hugsy/ida-headless).

**Important note**: this plugin exposes entirely the targeted Python VM over a TCP socket, in cleartext without authentication. Therefore *anyone* able to connect to it will be able to execute command on the remote system; so this plugin should never be used on a host that receive untrusted connections.

This plugin requires the installation of the [`rpyc`](https://rpyc.readthedocs.io/en/latest) package, but the service is only opened on demand. It was tested and works well under Windows and Linux but is expected to work the same on MacOS.

## Installation

Install the files in the Binary Ninja plugin directory:

```bash
# linux/osx
git clone --depth 1 https://github.com/hugsy/binja-headless "~/.config/Binary Ninja/plugins/binja-headless"
# windows
git clone --depth 1 https://github.com/hugsy/binja-headless "$env:AppData/Binary Ninja/plugins/binja-headless"
```

Then start Binary Ninja and check in the logs the plugin is correctly loaded.
```text
Loaded python3 plugin 'binja-headless'
```

## Settings

Settings can be configured to specify a different host and port (default 0.0.0.0:18812) to listen to by RPyC.
You can also enable the plugin autostart, allowing it to launch immediately in background when Binary Ninja starts.

![image](https://github.com/user-attachments/assets/bb3e30d7-cded-4bb9-b897-a07dfdff402f)


## Start / Stop the service manually

You can now start the service (Palette -> `Binja-RPyc - Start RPyc Service`). A popup will confirm the service is running, or show the error in the logs on failure.

## Usage

From a remote Python terminal, you can now import the `rpyc` module and access your remote Binary Ninja.

```python
>>> import rpyc
>>> c = rpyc.connect("192.168.57.2", 18812)
>>> c.root.bv
<BinaryView: '//DESKTOP-SD4TH5/Temp/ls', len 0x248e8>

>>> dir(c.root.binaryninja)
['ActionType',
 'ActiveAnalysisInfo',
 'AddressField',
 'AddressRange',
 'AdvancedFunctionAnalysisDataRequestor',
 'AnalysisCompletionEvent',
 [...]
```

And then you can create some aliases to make as if you were using it locally:
```python
>>> bv = c.root.bv ;  bn = c.root.binaryninja

# and then go crazy
>>> bn.core_version()
'3.4.4189-dev Personal'

>>> bv.file
<FileMetadata: Y:/IDBs/windows/kernel32/10.0.18362.329/kernel32.bndb>

>>> bv.arch
<arch: x86_64>

>>> bv.file.original_filename
'Y:/IDBs/windows/kernel32/10.0.18362.329/kernel32.dll'

>>> bv.get_functions_by_name("CreateFileMappingW")
[<func: x86_64@0x18001c250>]

>>> for f in bv.functions:
    print(f"{f.name} -> {f.start:#x}")
RtlVirtualUnwindStub -> 0x180001010
GetNumberFormatWStub -> 0x180001060
GetTimeZoneInformationForYearStub -> 0x180001070
IdnToAsciiStub -> 0x180001080
CreateWaitableTimerW -> 0x180001090
[...]

>>> for block in bv.get_functions_by_name("GlobalUnlock")[0]:
      for insn in block:
        print(insn)
(['mov', '     ', 'qword ', '[', 'rsp', '+', '0x8', ']', ', ', 'rbx'], 5)
(['mov', '     ', 'qword ', '[', 'rsp', '+', '0x10', ']', ', ', 'rsi'], 5)
(['push', '    ', 'rdi'], 1)
[...]
```

## Demo

[![binja-headless](https://i.imgur.com/1dUevj7.png)](https://youtu.be/wvQyXbYV92c)


## Minimum Version

This plugin requires the following minimum version of Binary Ninja:

 * 3164



## Required Dependencies

The required dependencies can be found in the `requirements.txt` file.


## License

This plugin is released under a MIT license. See the `LICENSE` file for complete details.


## Metadata Version

2
