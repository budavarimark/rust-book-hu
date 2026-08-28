## Kommentek

Minden programozó igyekszik könnyen érthetővé tenni a kódját, de néha
szükség van némi extra magyarázatra. Ilyenkor a programozók _kommenteket_
hagynak a forráskódban, amelyeket a fordító figyelmen kívül hagy, a
forráskódot olvasó emberek számára viszont hasznosak lehetnek.

Íme egy egyszerű komment:

```rust
// hello, world
```

Rustban az idiomatikus kommentstílus két perjellel kezdi a kommentet, és a
komment a sor végéig tart. Az egy sornál hosszabb kommenteknél minden sorba ki
kell tenned a `//` jelet, így:

```rust
// So we're doing something complicated here, long enough that we need
// multiple lines of comments to do it! Whew! Hopefully, this comment will
// explain what's going on.
```

A kommentek kódot tartalmazó sorok végére is kerülhetnek:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-24-comments-end-of-line/src/main.rs}}
```

Gyakrabban azonban ebben a formában találkozol velük: a komment külön sorban
áll az általa magyarázott kód fölött:

<span class="filename">Fájlnév: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-25-comments-above-line/src/main.rs}}
```

A Rustban van egy másfajta komment is, a dokumentációs komment, amelyről a 14.
fejezet [„Crate publikálása a Crates.io-ra”][publishing]<!-- ignore --> című
alfejezetében lesz szó.

[publishing]: ch14-02-publishing-to-crates-io.html
