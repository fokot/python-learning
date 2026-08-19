import reactivex as rx
from reactivex import operators as ops

"""
  concat_map	queue it, run in order — nothing lost, order kept
  flat_map	run it immediately, concurrently — order not guaranteed
  concat_map(fn) is literally flat_map(fn, max_concurrent=1).
"""

source = rx.interval(1).pipe(ops.take(100))
# emit incrementing number every second
out = source

# paced to one every 3s (nothing dropped)
# rx.zip(source, rx.interval(3)).subscribe(lambda t: print(t[0]))
# out = source.pipe(ops.concat_map(lambda n: rx.timer(3).pipe(ops.map(lambda _: n))))

def throttle(duration):
    return ops.concat_map(lambda n: rx.timer(duration).pipe(ops.map(lambda _: n)))

# A1, B1, C1, D1, A2, ... — one per tick
letters = ['A', 'B', 'C', 'D']
letters_source = source.pipe(ops.flat_map(lambda n: rx.of(*[f"{l}{n}" for l in letters])))
# out = letters_source

# paced every 3 seconds
# out = source.pipe(ops.flat_map(lambda n: rx.of(*[f"{l}{n}" for l in letters])), throttle(3))

# paced per letter (stream) every 3s (nothing dropped)
# out = letters_source.pipe(ops.group_by(lambda s: s[0]), ops.flat_map(lambda g: g.pipe(throttle(3))))

# batch triples
# out = source.pipe(ops.buffer_with_count(3))

source_5_seconds = rx.timer(0, 5).pipe(ops.map(lambda _: 'x'))
# out = rx.merge(source, source_5_seconds).pipe(ops.buffer_with_time(2))

sub = out.subscribe(print)

print("Press Enter to finish")
input()
sub.dispose()
