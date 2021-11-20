(WIP) Architecture
======================

.. index:: design, architecture


Service Definition
------------------------

User
~~~~~~~~~~~~~~

Users of L&D Platform are investors who seek to subscribe best performing bot or product of L&D Investment.
For now, we are only accepting private investor. Use should be able to register their Exchange API key/secret, change
settings of their bot, basic information etc.

Bots
~~~~~~~~~~~~~~~

**L&D Platform** provides various investment products called bots. Each bots can fall into 3 main categories.

1. **Automated Bot**
2. **Manual Bot**
3. **Indicator Bot**

*Automated bot*, as you can infer from its name, runs by itself with L&D developed strategies. Strategies can be
AI-driven, Scalping-driven or any combination of these two or more domains. Detailed information are highly confidential
and only designated personnel can access. These bots, once launched, with either static/dynamic bot settings, run by
itself until user stops.

*Manual bot* is a bot that user should interact with L&D Platform UI to trigger orders or trades. This is not something
related to strategy-driven bot but sort of a tool with few rules and pre-defined system in it.

..

    One of example is a *Ttadak bot*
    where user should play *Buy game* or *Sell game*. Each game places two orders at nearly same time but with very high leverage level,
    so that depending on user's level of fee and short-term price trends, user can earn money or not. User should be able to
    set a custom setting of this bot as well.

*Indicator bot*, last but not least, is rather a bot that helps user to decide better investment judgement. It can be either price
trends prediction model, long-term / short-term predicative models but this bot does not have anything to do with actual trade
or order. Most of models used in indicator bot are either inherited in Automated bot. The data that this bot produces are either
displayed in L&D Platform UI or can be pushed to various mediums like Telegram, Slack etc.

..

    One of good example is ``Future predicative model`` that pushes price estimation information to the user. This information will
    include something like



Subscription
~~~~~~~~~~~~~~~

To use L&D Bots, user should subscribe to it. The service flow should be like; users see the list of currently operated bots, their track records, simulation result, subscription fee etc.
Once user selects the bot, it should show the number of subscription by others, detailed information about the models and strategies etc.
Email notification of subscribe/unsubscribe event should be enabled, payment/cancellation system should also be considered and implemented.

.. note::
    In the future, we are planning to run this investment platform on top of ``De-Fi Blockchain``
    so that any investment information like subscription fee, distribution of yields of funds, status of orders placed
    will be trustlessly operated. Also payment system will be corporated into this blockchain system as well.

Settings
~~~~~~~~~~~~~~~

Settings can be categorized into two parts: User specific settings and Bot specific settings.

1. User-specific setting
2. Bot-specific setting

*User-specific setting* includes account setting (e.g password change, resign, payment method and info), trade setting
(e.g exchange API key/secret, global trade setting etc).

*Bot-specific setting* are settings for each subscribed bot. Since we have many different kinds of bots (automated, manual, indicator),
there are many settings that are bind to these bots. Settings may include the leverage level, target yield per game,
rebalancing period, minimum amount of order per trade, take profit price, stop loss price etc. These default settings per
bots should be persisted and user - who subscribed a bot and launched it - should be able to change settings for their own needs.

Control/Management
~~~~~~~~~~~~~~

After successful subscribed to the bot, user will be able to control bot. **Control of Bot** can vary depending on types of bots.
Basic control bot bots can be categorized as follows.

- Automated Bot
    - ``START``
    - ``STOP``
    - ``EDIT SETTING``

- Manual Bot
    - ``START``
    - ``STOP``
    - ``EDIT SETTING``
    - Bot specific control
        - E.g Ttadak bot has ``BUY GAME``, ``SELL GAME``

- Indicator
    - ``START``
    - ``STOP``
    - ``EDIT SETTING``

.. note::

    Especially the *Bot specific control* of *Manual Bot* requires additional software engineering stack like gRPC, which is
    a high performance Remote Procedure Call (RPC) technology topped with HTTP2.0 and Protobuf message protocol.
    Since **the time between user performs control and the actual order received by exchange API server should be very fast**
    in some bots (e.g Ttadak bot)


Monitoring/Report
~~~~~~~~~~~~~~~~~~~~~

User may wonder about the performance of bot - how much did the bot each earn and what is the accumulated yield of my
subscribed bots?


ERD
-------------------------

Please refer `BurntSushi ERD`_ to know how to draw ERD using kroki tool.

.. _BurntSushi ERD: https://github.com/BurntSushi/erd

.. kroki::
    :caption: L&D Platform ERD
    :type: erd

    # Entities

    [player] {bgcolor: "#d0e0d0"}
      *player_id {label: "varchar, not null"}
      full_name {label: "varchar, null"}
      team {label: "varchar, not null"}
      position {label: "player_pos, not null"}
      status {label: "player_status, not null"}

    [team] {bgcolor: "#d0e0d0"}
      *team_id {label: "varchar, not null"}
      city {label: "varchar, not null"}
      name {label: "varchar, not null"}

    [game] {bgcolor: "#ececfc"}
      *gsis_id {label: "gameid, not null"}
      start_time {label: "utctime, not null"}
      week {label: "usmallint, not null"}
      season_year {label: "usmallint, not null"}
      season_type {label: "season_phase, not null"}
      finished {label: "boolean, not null"}
      home_team {label: "varchar, not null"}
      home_score {label: "usmallint, not null"}
      away_team {label: "varchar, not null"}
      away_score {label: "usmallint, not null"}

    [drive] {bgcolor: "#ececfc"}
      *+gsis_id {label: "gameid, not null"}
      *drive_id {label: "usmallint, not null"}
      start_field {label: "field_pos, null"}
      start_time {label: "game_time, not null"}
      end_field {label: "field_pos, null"}
      end_time {label: "game_time, not null"}
      pos_team {label: "varchar, not null"}
      pos_time {label: "pos_period, null"}

    [play] {bgcolor: "#ececfc"}
      *+gsis_id {label: "gameid, not null"}
      *+drive_id {label: "usmallint, not null"}
      *play_id {label: "usmallint, not null"}
      time {label: "game_time, not null"}
      pos_team {label: "varchar, not null"}
      yardline {label: "field_pos, null"}
      down {label: "smallint, null"}
      yards_to_go {label: "smallint, null"}

    [play_player] {bgcolor: "#ececfc"}
      *+gsis_id {label: "gameid, not null"}
      *+drive_id {label: "usmallint, not null"}
      *+play_id {label: "usmallint, not null"}
      *+player_id {label: "varchar, not null"}
      team {label: "varchar, not null"}

    [meta] {bgcolor: "#fcecec"}
      version {label: "smallint, null"}
      season_type {label: "season_phase, null"}
      season_year {label: "usmallint, null"}
      week {label: "usmallint, null"}

    # Relationships

    player      *--1 team
    game        *--1 team {label: "home"}
    game        *--1 team {label: "away"}
    drive       *--1 team
    play        *--1 team
    play_player *--1 team

    game        1--* drive
    game        1--* play
    game        1--* play_player

    drive       1--* play
    drive       1--* play_player

    play        1--* play_player

    player      1--* play_player
