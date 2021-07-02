# Binja-RPyc

Author: **@hugsy**

Headless Binary Ninja!



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
>>> bv = c.root.bv
>>> binaryninja = c.root.binaryninja
# and then go crazy
>>> bv.arch
<arch: x86_64>
>>> bv.file.original_filename
'//ph0ny/Temp/ls'
>>> bv.get_functions_by_name("main")
[<func: x86_64@0x4df0>]
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
