#  Viewing and Editing Files 



When working on research projects or data analysis in Linux, it's common to view or edit text files directly from the command line. Here's a quick guide to the basic tools you'll encounter.

## File Viewing Tools

These commands allow you to **view the contents** of a file without opening it in a full editor:

* `cat filename` – Outputs the entire file to the terminal. Best for small files.
* `less filename` – Opens the file in a scrollable view. Use arrow keys to navigate, `q` to quit. **Recommended** for long files.
* `head filename` – Displays the **first 10 lines** of a file. Add `-n` to specify a different number (e.g., `head -n 20 filename`).
* `tail filename` – Shows the **last 10 lines** of a file. Great for checking logs.

## Text Editors

Text editors are important for writing batch scripts in high-performance computing environments. Users can choose between Nano (a beginner-friendly text editor) or Vim (a more powerful editor, especially in programming or large-scale text processing, but harder to learn) as their text editor on Quest.

## Editing Files with Nano
:::{seealso}
[Introduction to the Text Editor: Nano](https://www.youtube.com/watch?v=l2wBwT8e0h8&list=PLDzPlBW3jmQDbinD2XAo-DU2pxFs38ni1&index=3&t=2s) (YouTube)
:::

For quick edits, `nano` is a simple and beginner-friendly text editor:

* Open a file: `nano filename`
* Edit text directly in the terminal.
* Use `Ctrl + O` to save, `Ctrl + X` to exit, and `Ctrl + K` to cut a line.

Nano is available by default on most Linux systems and is easy to use, especially for newcomers.

## Editing Files with Vim

:::{seealso}
[Introduction to the Text Editor: Vim](https://www.youtube.com/watch?v=87bVF0aw4Hs&list=PLDzPlBW3jmQDbinD2XAo-DU2pxFs38ni1&index=2&t=1s) (YouTube)
:::

Vim is a modal editor — it has separate modes for navigating and inserting text. It has a steeper learning curve than Nano but offers extensive keyboard shortcuts and scripting capabilities that make it a powerful choice for programming and large-scale text editing.

Basic Vim commands to get started:

* Open a file: `vim filename`
* Enter insert mode (to type): press `i`
* Return to normal mode: press `Esc`
* Save and quit: type `:wq` then `Enter`
* Quit without saving: type `:q!` then `Enter`

