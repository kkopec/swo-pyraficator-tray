# swo-pyraficator-tray
Systray GUI for Pyraficator API

### Usage
There are several option to use the app:
 - use the binary attached to the most recent release
 - build the binary yourself ;)
 - call the script directly:
```bash
python pyraficator-tray.py
```

### Dependencies
Building / running the script locally requires installing dependencies:
```bash
pip install PyQt5 requests
```

### Customization
Pyraficator behavior can be customized via `userconfig.json` file. In order for it to work place the config file in the same directory as the program's binary/script.

Available options:

| property | description |
| --- | --- |
| refreshInterval |  interval between subsequent data fetches [ms] |
| notificationTime |  notification visibility time [ms] |
| notificationStatuses |  statuses that should trigger notification |
| notificationRegex |  regex that is tested against statusDetails items. only matching items will trigger notification|

Example:
```js
{
  "refreshInterval": 10000
  "notificationTime": 5000,
  "notificationStatuses": ["Success", "InProgress", "Failure"],
  "notificationRegex": "\\[SHELL\\]"
}
```
