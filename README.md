# binja-headless

Author: **@hugsy**

Headless Binary Ninja (sort of!)



## Description

Allows to use Binary Ninja headlessly and remotely by creating an RPyc service for it.
It works just like [IDA-RPyc](https://github.com/hugsy/stuff/blob/master/ida_scripts/ida_rpyc_server.py) but for Binja.

Install the files in the Binary Ninja plugin directory, and start it.

From a remote Python terminal, you can now access binja!

```python
>>> import rpyc
>>> c = rpyc.connect("192.168.57.2", 18812)
>>> c.root.bv
<BinaryView: '//ph0ny/Temp/ls', len 0x248e8>

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
```

## Minimum Version

This plugin requires the following minimum version of Binary Ninja:

 * 1200



## Required Dependencies

The following dependencies are required for this plugin:

 * rpyc >= 5.0.0



## License

This plugin is released under a MIT license.


## Metadata Version

2
