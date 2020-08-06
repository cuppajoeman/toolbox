# General System 
Most of these configurations are tailored around a minimal linux distribution where you choose what programs/features you want. 
In addition I have spent a minimal amount of time improving aesthetics of the system and most of the time on functionality

If you would like to try out my configurations for a certain program first make a backup of your file, then use stow eg)

You would like to try out my vim configuration
1. Backup
  `mv ~/.vimrc ~/.vimrc.bak`

2. Stow
  `cd basic-system`
  `stow vim`

3. Try out the configuration

4. Done with configuration (check out man stow for more options)
  `stow --delete vim`
  
5. Move your config back in 
  `mv ~/.vimrc.bak ~/.vimrc`

## Graphical
* X
* i3wm
* picom for transparency
* Font:
  * iosevka-fixed-slab
* For the following you can use lxappearance
  * Adwaita-dark gtk theme
  * high-contrast icon theme
  * thedot mouse cursor


## Input
* trackball 
  * see mouse-settings, Note: the config must be stowed to /etc
* keyboard

## Output
* Monitor
  * `mons` for configuring output
* Sound
  * Pulsemixer to change volume

## Movement
* Everything vim (to the furthest extent)

## Tools
### Man pages
### IRC
* weechat 
  * plugins
    * vimode.py
    * go.py
    * weechat-notify-send
  * bindings
    * alt-b toggles buflist
    * alt-n toggles nicklist
  * configurations
    * limit the nicklist size
    * hide join/leave messages (intelligently)
### Editor
* vim - check the vim directory for more
### Terminal Emulator
* st
### Shell
* fish
### Latex Writing
* vim + vimtex + ultisnips (feel free to check out my other repo for some snippets)
### Music
* Spotify
### Version Control
* Git
  * Set default diff viewer
  ```
  git config --global diff.tool vimdiff
  git config --global difftool.prompt false
  git config --global alias.d difftool
  ```
  * Set the default editor to vim
### Mathmatics
* Qalculate - for quick calculation
* geogebra-5 - for 2d/3d graphing
* lang. to check conjectures


## Server System
* vim-gtk (for ultisnips)
* my-snips repo
* tmux
* fish, then `chsh -s /usr/bin/fish`
* ranger
