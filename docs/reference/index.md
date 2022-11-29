# API Reference

<style>
  .doc-function .doc-contents {
    display: none;
  }

  .doc-contents > *:not(.doc-children) {
    display: none !important;
  }

  .toc > ul > li > ul > li > ul > li > ul  {
    display: none !important;
  }
</style>

## Where to Start

You probably want to start with the [`Secret`][secret_type.Secret] class, which has many commonly-used methods to operate with secrets.

## Sections

### [Exceptions][secret_type.exceptions]

This module contains exceptions that are used by the rest of the library.

### [SecretMonad][secret_type.monad.SecretMonad]

This class mixes in monad-like [`wrap`][secret_type.monad.SecretMonad.wrap] and [`unwrap`][secret_type.monad.SecretMonad.unwrap] methods to [`Secret`][secret_type.Secret].

### [Types][secret_type.typing.types]

This module contains types that are used by the rest of the library.

### [Containers][secret_type.Secret]

This section contains specialized containers for holding secrets of various types.
