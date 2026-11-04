from .core import sample
for base, result in sample().items():
    print(f'base {base}: {result.integer}.{result.prefix}({result.repetend}) period={len(result.repetend)}')
