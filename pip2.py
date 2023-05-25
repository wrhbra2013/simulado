try:
    from pip._internal.operations import freeze
except ImportError:  # pip < 10.0
    from pip.operations import freeze

x = freeze.freeze()
for p in x:
    print(p)
