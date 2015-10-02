
# How to update reveal.js

Add the remote if necessary

```sh
git remote add -f reveal.js https://github.com/hakimel/reveal.js.git
```

Execute this command to get the master code
```sh
git subtree pull --prefix reveal.js reveal.js master --squash
```

Alternatively use of the dev branch may be justified
```sh
git subtree pull --prefix reveal.js reveal.js dev --squash
```
