/**
 * IMPORTANT
 *
 * These functions have been taken from https://github.com/nvie/itertools.js
 */

const SENTINEL = Symbol();
type Primitive = string | number | boolean;

export function* flatten<T>(
  iterableOfIterables: Iterable<Iterable<T>>
): Iterable<T> {
  for (const iterable of iterableOfIterables) {
    for (const item of iterable) {
      yield item;
    }
  }
}

export function chain<T>(...iterables: Array<Iterable<T>>): Iterable<T> {
  return flatten(iterables);
}

function primitiveIdentity(x: any): Primitive {
  /* istanbul ignore if */
  if (
    typeof x !== "string" &&
    typeof x !== "number" &&
    typeof x !== "boolean"
  ) {
    throw new Error(
      "Please provide a key function that can establish object identity"
    );
  }
  return x;
}

function iter<T>(iterable: Iterable<T>): Iterator<T> {
  return iterable[Symbol.iterator]();
}

export function* groupby<T>(
  iterable: Iterable<T>,
  keyFn: (arg0: T) => Primitive = primitiveIdentity
): Iterable<[Primitive, Iterable<T>]> {
  const it = iter(iterable);

  let currentValue: T;
  // @ts-ignore
  let currentKey: Primitive = SENTINEL;
  let targetKey = currentKey;

  const grouper = function* grouper(tgtKey: Primitive) {
    while (currentKey === tgtKey) {
      yield currentValue;

      const nextVal = it.next();
      if (nextVal.done) return;
      currentValue = nextVal.value;
      currentKey = keyFn(currentValue);
    }
  };

  for (;;) {
    while (currentKey === targetKey) {
      const nextVal = it.next();
      if (nextVal.done) {
        // @ts-ignore
        currentKey = SENTINEL;
        return;
      }
      currentValue = nextVal.value;
      currentKey = keyFn(currentValue);
    }

    targetKey = currentKey;
    yield [currentKey, grouper(targetKey)];
  }
}
