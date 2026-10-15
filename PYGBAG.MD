# Pygbag options

Pygbag is a command-line tool used to package Python and Pygame-CE applications into WebAssembly for execution in modern web browsers. The primary command structure is `pygbag your.app.folder`, which builds the application and starts a local test server.

The tool supports numerous command-line options to customize the build process, server behavior, and application metadata.

## Standard Options

*   **--bind ADDRESS**: Specify the alternate bind address for the local server (default: `localhost`).
*   **--PYBUILD PYBUILD**: Specify the Python version to use for the build (default: `3.11`).
*   **--app_name APP_NAME**: Set the user-facing name of the application (default: `test`).
*   **--ume_block UME_BLOCK**: Specify whether to wait for user media engagement before running (default: `1`).
*   **--can_close CAN_CLOSE**: Specify if the window should ask for confirmation before closing (default: `0`).
*   **--cache CACHE**: Define the md5-based URL cache directory.
*   **--package PACKAGE**: Set a unique package name.
*   **--title TITLE**: Set a nice-looking name for the app.
*   **--version VERSION**: Override the prebuilt version path (default: `0.8.2`).
*   **--build**: Build only, without running the test server.
*   **--html**: Build as HTML with embedded assets (pygame-script).
*   **--no_opt**: Turn off asset optimization.
*   **--archive**: Create a `build/web.zip` archive suitable for itch.io.
*   **--icon ICON**: Specify an icon PNG file (minimum 32x32, should be `favicon.png`).
*   **--cdn CDN**: Set the web site to cache locally (default: `https://pygame-web.github.io/archives/0.8/`).
*   **--template TEMPLATE**: Specify an `index.html` template (default: `default.tmpl`).
*   **--ssl SSL**: Enable SSL using `server.pem` and `key.pem`.
*   **--port [PORT]**: Specify an alternate port for the local server (default: `8000`).
*   **--disable-sound-format-error**: Prevent exceptions for audio files with unsupported formats (not recommended).

## Developer Options

*   **--git**: Force the CDN to use the current Git GitHub CI build.
*   **--dev**: Change the port to `8666` and use a local build served on `8000`.

## Usage Notes

*   **Testing**: After running the command, navigate to `http://localhost:8000` in a modern browser (V8-based browsers like Chrome, Brave, or Chromium are preferred).
*   **Debugging**: Append `?-i` to the URL (e.g., `http://localhost:8000?-i`) to access a terminal with a REPL and a downsized canvas.
*   **Pygame-Script**: If built with the `--html` flag, access the game at `http://localhost:8000/test.html` (assuming a folder named "test").
*   **Compatibility**: Pygbag only supports **pygame-ce** (Pygame Community Edition). Mobile Safari and Chrome on iOS require version 15.x or later.
