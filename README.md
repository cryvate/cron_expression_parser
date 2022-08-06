cron_expression_parser
=====================

Meta note: I have used `IMP:` as meta-comments on things I would change depending on circumstances/if this was not an
exercise.

How to run as CLI
-----------------
- Install Python 3.10+ due to typing annotations used and some dubious pattern matching, 
  recommend [pyenv](https://github.com/pyenv/pyenv)
- Enable this Python to be accessible using `python3` and it might in theory be possible you need to upgrade `pip`:
```bash
pip3 install pip==22.0.4
```
IMP: this is not necessary with the proper packaged version, as those are backwards compatible much older versions
pip, but I am using `pep-517` build system which is not available in all `pip`s (but probably in all that run on 3.10+
but I have not checked)
- Install using
```bash
pip3 install git@github.com:cryvate/cron_expression_parser.git
```
- You should now be able to run whenever this `python3` environment stays enabled, try it using:
```bash
cron_expression_parser "*/15 0 1,15 * 1-5 /usr/bin/find"
```
and you will get output like this:
```
minute 0 15 30 45
hour 0
day of month 1 15
month 1 2 3 4 5 6 7 8 9 10 11 12
day of week 1 2 3 4 5
command /usr/bin/find
```

Run tests & hooks
---------
- Checkout the repo
```bash
git clone git@github.com:cryvate/cron_expression_parser.git
```
- Install and enable a `python3.10+` environment
- Install `pytest` and `pre-commit`
```bash
pip3 install pytest pre-commit
```
- Run `pytest` and `pre-commit`:
```bash
pytest
pre-commit run --all-files
```
