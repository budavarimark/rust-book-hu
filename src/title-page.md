# A Rust programozási nyelv

_Írta Steve Klabnik, Carol Nichols és Chris Krycho, a Rust közösség
közreműködésével_

A szöveg jelen változata feltételezi, hogy a Rust 1.97.0 (megjelent 2026-07-09)
vagy újabb verzióját használod, és hogy minden projekted *Cargo.toml* fájljában
szerepel az `edition = "2024"` beállítás, amely a Rust 2024 Edition idiómáit
kapcsolja be. A Rust telepítéséről és frissítéséről az [1. fejezet „Telepítés”
szakaszában][install]<!-- ignore --> olvashatsz, az editionökről pedig az [E
függelékben][appendix-e]<!-- ignore --> találsz információt.

A HTML-formátum online elérhető a
[https://doc.rust-lang.org/stable/book/](https://doc.rust-lang.org/stable/book/)
címen, offline pedig a `rustup`-pal telepített Rust részeként; a megnyitásához
futtasd a `rustup doc --book` parancsot.

Több közösségi [fordítás][translations] is elérhető.

Ez a szöveg [nyomtatott és e-könyv formátumban a No Starch Press
gondozásában][nsprust] is kapható.

[install]: ch01-01-installation.html
[appendix-e]: appendix-05-editions.html
[nsprust]: https://nostarch.com/rust-programming-language-3rd-edition
[translations]: appendix-06-translation.html

> **🚨 Interaktívabb tanulási élményre vágysz? Próbáld ki a Rust könyv egy másik
> változatát, amelyben kvízek, kiemelések, vizualizációk és még sok más
> található**: <https://rust-book.cs.brown.edu>
