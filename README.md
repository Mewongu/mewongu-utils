# Utils for python

Examples:

Timed context:
```python
>>> from time import sleep
>>> from utils import timed_ctx
>>>
>>> with timed_ctx(msg='It took:'):
...     sleep(1.5)
...
It took: 1.5052039623260498
```

Timed function:
```python
>>> from time import sleep
>>> from utils import timed
>>>
>>> @timed(msg='Call took:')
... def my_fn():
...     sleep(1.5)
...
>>> my_fn()
Call took: 1.5051820278167725
```



