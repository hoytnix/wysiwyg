Dictionary
==========



"List"

When sensible, a list must have the following properties:

+ Slicable
+ Searchable

```
class Foo:
    def __init__(self):
        self.bar = ['apple_orange', 'apple_grape', 'grape_orange', 'orange_apple']

    @property
    def search(self, key):
        return [item for item in self.bar if key in item]
```
