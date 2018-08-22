## Welcome

This repository provides you with a simple interface to interact with the PythonAnywhere API.

All you need to do is:
 - Get an API token from [here](https://help.pythonanywhere.com/pages/API/)
 - Then use the module :)
 - Feel free to extend or modify it as you would like to!

## Example

```python
from anywherepython import *
API = AnywherePython(username='youuser', apikey = 'yourapikey')
API.get_consoles()
```

```python
from anywherepython import *
API = AnywherePython(username='youuser', apikey = 'yourapikey')
API.get_consoles()
API.get_console_output(<idofconsole>)
API.send_console_input(<idofconsole>, <tobesent>)
```

```python
from anywherepython import *
API = AnywherePython(username='youuser', apikey = 'yourapikey')
API.get_webapps()
API.reload_webapps()
```
