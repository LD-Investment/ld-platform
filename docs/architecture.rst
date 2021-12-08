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



Funds & Subscription
~~~~~~~~~~~~~~~

To use L&D Bots, user should subscribe to funds that compose of several bots. The service flow should be like; users see the list of currently operated funds,
their track records, simulation result, subscription fee etc.
Once user selects the bot, it should show the number of subscription by others, detailed information about the models and strategies etc.
Email notification of subscribe/unsubscribe event should be enabled, payment/cancellation system should also be considered and implemented.

.. note::
    In the future, we are planning to run this investment platform on top of **De-Fi Blockchain**
    so that any investment information like subscription fee, distribution of yields of funds, status of orders placed
    will be trustlessly operated. Also payment system will be integrated into this blockchain smart-contract as well.

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

This is the one of example we should take into account.

- Run type
    - Simulation : Run simulation by given range of time.
    - Dry-run : Run in real-time but do not actually place order.
    - Live-run : Run in real-time with actual order.

Control/Management
~~~~~~~~~~~~~~~~~~~~~~

After successfully subscribed to the bot, user will be able to control bot. **Control of Bot** can vary depending on types of bots.
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
~~~~~~~~~~~~~~~~~~~~~~~~

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

    [user] {bgcolor: "#e0e0e0"}
      *id {label: "smallint, not null"}
      email {label: "varchar, not null"}
      password {label: "varchar, not null"}

    [exchange_setting] {bgcolor: "#e0e0e0"}
      *id {label: "smallint, not null"}
      +user_id {label: "smallint, not null"}
      name {label: "varchar, not null"}
      api_key {label: "varchar, not null"}
      api_secret {label: "varchar, not null"}

    [user_subscribed_bot] {bgcolor: "#d1fff9"}
      *id {label: "smallint, not null"}
      +user_id {label: "smallint, not null"}
      +bot_id {label: "smallint, not null"}
      status {label: "varchar, not null"}
      run_type {label: "varchar, not null"}
      user_bot_setting {label: "json, not null"}
      subscription_start_date {label: "utctime, not null"}
      subscription_end_date {label: "utctime, not null"}

    [bot] {bgcolor: "#ececfc"}
      *id {label: "smallint, not null"}
      name {label: "varchar, not null"}
      type {label: "varchar, not null"}
      version {label: "varchar, not null"}
      default_setting {label: "json, not null"}

    [trade] {bgcolor: "#fcecec"}
      *id {label: "int, not null"}
      +user_subscribed_bot_id {label: "smallint, not null"}
      exchange {label: "varchar, not null"}
      pair {label: "varchar, not null"}
      is_open {label: "boolean, not null"}
      stop_loss {label: "float, null"}
      take_profit {label: "float, null"}

    [order] {bgcolor: "#fcecec"}
      *id {label: "int, not null"}
      +trade_id {label: "int, not null"}
      status {label: "varchar, not null"}
      symbol {label: "varchar, not null"}
      side {label: "varchar, not null"}
      price {label: "float, not null"}
      average {label: "float, not null"}
      amount {label: "float, not null"}
      filled {label: "float, null"}
      remaining {label: "float, null"}
      cost {label: "float, null"}

    # Relations

    user        1--* exchange_setting
    user        1--* user_subscribed_bot
    bot         1--* user_subscribed_bot
    trade       *--? user_subscribed_bot
    trade       1--* order

Django app structure
-------------------------

Before designing REST API URLs, need to define how we will structure Django Applications.

.. note::
    Applications include some combination of models, views, templates, template tags, static files, URLs, middleware, etc.

Please read and understand this `official django documentation`_ before commencing. This `discussion threads`_ is also helpful.

.. _`official django documentation`: https://docs.djangoproject.com/en/4.0/ref/applications/
.. _discussion threads: https://forum.djangoproject.com/t/why-do-we-need-apps/827/3


Applications
~~~~~~~~~~~~~~~~~~~

We can divide into 4 django applications mainly. Since cookie-cutter already setup app for ``Users``, we may extend this
structure and create rest 3 applications and integrate to root router and django setting.

1. **[P0] Users**
  - Sign up, Login in/out
  - Registration/update/deletion of exchange api/secret
  - Editing of user specific information (password, nickname etc)

2. **[P1] Funds**
  - Payment/initiation of fund and its subscription
  - Resuming/cancelling of fund subscription
  - Checking status of fund subscription

3. **[P0] Bots**
  - Running/stopping bot (of which subscription is active)
  - Selecting run type of bot (Simulation/Dry-run/Live-run)
  - Checking user's exchange info (validity of api key, check wallet etc)
  - Basic control of bot (RUN/STOP)
  - Editing bot specific settings (dynamic application to the bot)
  - Bot monitoring (real-time status, yields, recent history of trades/orders)
  - Bot reporting (aggregated yields, fees, comparison with other models etc)

4. **[P3] Payment**
  - Should be able to use various payment vendors like VISA, MASTERCARD etc
  - De-fi based payment system should be enabled in the future

5. **[P4] DataWarehouse**
  - Selecting time range and downloading from collector DB
  - Processing data into specific format (OHLVC, 5 min OB etc)
  - Can be exposed to external so that it can earn money as well

6. **[P2] Notification**
  - Sending message from django apps via Email, Telegram, KakaoTalk etc
  - Handling queuing/sending/retrial of messages
