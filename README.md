<p align="center">
    <h1>RiMusic Database Generator</h1>
    <p>Generate watch history and playlists from your YouTube history</p>
</p>

# Prerequisites

Before getting into the conversion, there are some stuff that need to be done.

1. Internet connection (duh!)
2. Google account with history turned on
3. A computer capable of running [Python](https://www.python.org/)
4. YouTube watch history. [Follow these steps](https://github.com/knighthat/RiMusic-Database-Generator/wiki/retrieve-youtube-watch-history-from-youtube-takeout) to get one

# Setup

1. Clone this repository 

    ```sh
    $ git clone --depth 1 https://github.com/knighthat/RiMusic-Database-Generator && cd RiMusic-Database-Generator
    ```
2. Install virtual environment & dependencies

    > You might need to install venv module. Look it up on Google

    ```sh
    $ python -m venv .venv
    ```

    ```sh
    $ .venv/bin/pip install requirements.txt
    ```
3. Run script

    ```sh
    $ .venv/bin/python main [convert|get-playlist-map|write]
    ```

# Usage

## Commands

### convert

```sh
$ .venv/bin/python main convert
```

This command will let you convert YouTube and YouTube Music watch history into JSON files. All files will be saved at `./listened` folder.

You may notice that the some files are stored directly inside `./listened` and some stored inside another folder named after artist's of that song.\
This is because once the script detect you have listened to this artist for more than 1 song, it'll categorize songs into a directory.

### get-playlist-map

```sh
$ .venv/bin/python main get-playlist-map
```

Do you have hundreds or thousands of songs to put into playlists? Can you feel the pain of doing it?

Worry not, I'll give you some "_pain killer_".\
You can categorize artists into different playlists such as language, genre, collections, etc.

Once the command is executed, you'll get a file named `playlists.json` in your main directory.

> It is very crucial to use this command after [convert](#convert) command, because it'll get aritst's names from `./listened` folder

Assigning playlist name(s) to aritst and let the app lift the heavy part for you. Here's my example:

```json
{
  "Logic": [
    "Rap",
    "English"
  ],
  "CHUNG HA": [
    "Korean"
  ],
  "Bon Jovi": [
    "Rock",
    "English"
  ]
}
```

### write

```sh
$ .venv/bin/python main write
```

This will be your final command. Once executed, it'll read everything inside `./listened` directory and write the data to the database.

### generate

```sh
$ ./venv/bin/python main generate
```

This command will create an empty database for you to write your watch history


# Watch out

[convert](#convert) command quries YouTube Music for song details.
Sending multiple quries in a short amount of time results in denial of access, or block.

I ran some tests and the result shows that you can send about 200 queries every 10 minutes. But your mileage is vary.

It is better to do this on public network, i.e coffe shop. YTM goes easier on commercial internet but nothing guarantee this.

# Why am I not making the script to run everything in **1** go?

There are many reasons why the script isn't made to work with **ONE** single command but rather multiple steps

1. Points of failure

    * There are multiple unpredictable points of failure in the script.
    * For example, YouTube returns invalid response, block queries, etc.
    * If the script is designed to work in 1 go, each failure will reset the
    script to the beginning.

2. Ease of maintainance

    * I'm aiming to support this app as long as I can. Therefore, updating
    * code base is a chore. The more you put into the app, the harder it is
    to maintain it.
    * By spliting it up into multiple parts, each part can be updated individually
    without interfering with others.

3. Customization

    * Customization will always be my first priority, thus, letting users
    interact with the app along the way is ensured.
    * At step like deciding which artist or playlist to like/create. 
    User can be in total control before it is imported to database.

4. Compile once, run anytime

    * Each step will generate a "snapshot", this allows user to continue
    rather than start from the beginning over again.