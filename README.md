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
* Iosevka font
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

## Movement
* Everything vim (to the furthest extent)

## Tools
### Communication
* weechat for irc
### Editor
* vim - check the vim directory for more
### Terminal Emulator
* kitty
### Shell
* Abbreviations: 
  * I have a file where I store generic abbreviations of the form abbrev "expansion", then I can generate specific abbreviations for the specific shell I'm using at the moment (check out abbreviations folder)
* fish
### Latex Writing
* vim + vimtex + ultisnips (feel free to check out my other repo for some snippets)
### Music
* Spotify
  * Musixmatch for lyrics

## Server System
* vim-gtk (for ultisnips)
* my-snips repo
* tmux
* fish, then `chsh -s /usr/bin/fish`
* ranger
