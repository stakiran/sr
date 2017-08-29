# sr
A soundrecorder.exe wrapper for instant voice recording.

<!-- toc -->
- [sr](#sr)
  - [Demo](#demo)
  - [Requirement](#requirement)
  - [FAQ](#faq)
    - [Q: Where recorded files are stored?](#q-where-recorded-files-are-stored)
    - [Q: Is it possible to open the mic property dialog quickly?](#q-is-it-possible-to-open-the-mic-property-dialog-quickly)
    - [Q: Is it possible to collect information about an existing recording process?](#q-is-it-possible-to-collect-information-about-an-existing-recording-process)
    - [Q: Is it possible to execute multiply?](#q-is-it-possible-to-execute-multiply)
  - [License](#license)
  - [Author](#author)

## Demo
Record for 5 seconds.

```terminal
$ python sr.py -s 5

$ dir
2017/08/08  13:43            76,813 170808_134347_5s.wma
```

Record for 1 hour 15 minutes.

```
$ python sr.py -m 15 --hour 1
```

Use `.wav` format.

```terminal
$ python sr.py -s 5 --wav

$ dir
2017/08/08  13:47           882,046 170808_134734_5s.wav
```

Use the comment function.

```terminal
$ python sr.py -s 5 --wav MyFirstUse

$ dir
2017/08/08  14:06           882,046 170808_140623_5s_MyFirstUse.wav
```

Show the commandline. (No command execution)

```
$ python sr.py -s 5 --wav --test
soundrecorder /FILE 170808_134833_5s.wav /DURATION 0000:00:05
```

## Requirement
- Windows 7+
- Python 2.7
- A Mic device for recording.

## FAQ

### Q: Where recorded files are stored?
All of files are saved in the same directory of `sr.py`.

### Q: Is it possible to open the mic property dialog quickly?
Ans: Yes.

Use `-d` option.

```
$ python sr.py -d
```

### Q: Is it possible to collect information about an existing recording process?
Ans: Yes.

Use `--ps` option.

```
$ python sr.py --ps
from 20170808_134502
```

This means that a soundrecorder.exe process exists from 2017/08/08 13:45:02.

For more information about a process, you can use `taskmgr.exe` or [Process Explorer](https://docs.microsoft.com/en-us/sysinternals/downloads/process-explorer) and check `soundrecorder.exe` entry.

By the way, an existing soundrecorder.exe is also shown on the system tray, but no context menu and not operational.

### Q: Is it possible to execute multiply?
Ans: No.

The soundrecorder.exe can be as a single instance only, not multiple execution. The 2nd execution is not ran.

If you want to record with a new one, you have to terminate an old soundrecorder.exe process.

The sample of terminating an old one with `--ps` option and `taskkill` command like this:

```
$ python sr.py --ps
from 20170808_134502

$ taskkill /f /im soundrecorder.exe
成功: プロセス "SoundRecorder.exe" (PID 3484) は強制終了されました。

$ python sr.py --ps
利用できるインスタンスがありません。
```

## License
[MIT License](LICENSE)

## Author
[stakiran](https://github.com/stakiran)
