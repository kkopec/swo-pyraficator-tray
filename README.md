# swo-pyraficator-tray
Systray GUI for Pyraficator API

### Usage
There are several option to use the app:
 - use the binary attached to the most recent release
 - build the binary yourself ;)
 - call the script directly:
```json
python pyraficator-tray.py
```

### Customization
Pyraficator behavior can be customized via `userconfig.json` file. In order for it to work place the config file in the same directory as the program's binary.

Available options:
```js
{
  "refreshInterval": 10000, // interval between subsequent data fetches [ms]
  "notificationTime": 5000, // notification visibility time [ms]
  "notificationStatuses": ["Success", "InProgress", "Failure"], // statuses that should trigger notification
  "notificationRegex": "\\[SHELL\\]" // regex that is tested against statusDetails items. only matching items will trigger notification
}
```
