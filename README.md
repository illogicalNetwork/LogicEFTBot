
<p align="center"><img src="https://illogical.network/strim/BrainOnly.png" alt="Logo" width=40% height=40%" /></p><h1 align="center">Logic's EFT Bot</h1>
<p align="center">
  <b>To have the bot join your channel, please click here and click 'Authorize.' </b><br />
  To make sure the bot can bypass any URL restrictions, please make sure you type <br />
  <code>/mod LogicEFTBot</code> <br />in your chat after authorizing. Once you 'authorize' the bot should join your channel!
</p>

### Usage

The bot has very basic and has only one moderation command which you can find below. Currently all commands with Type  of `cooldown` are all under the same cooldown. This means that if any command with Type `cooldown` is used successfully all other commands with Type of `cooldown` are under cooldown. Each channel has their own `cooldown` with a default of 10 seconds.


| Command| Type                                             | Usage |
|-----------------------|--------------------------------------------------|--------------------------------------------------|
| !astat   | `cooldown`| Retrieves in-game ammo `flesh` and `penetration` values. Ex: `!astat 9x19 RIP` |
| !medical | `cooldown`| Retrieves medical item use time. Ex: `!medical surv` |
| !price | `cooldown`| Retrieves flea market price. Ex: `!price Slick` |
| !slot  | `cooldown`| Retrieves price per slot of item based off the flea market. Ex: `!slot Slick`|
| !wiki  | `cooldown` | Retrieves EFT Wiki Link of item requested. Ex: `!wiki slick` |
| !help  | `information`| Display this help message. |
| !eftbot| `information`| Display this help message. |                
| !setCD** | `information`| Sets the cooldown for the bot in seconds. |
> Commands denoted with `**` are reserved to "Moderators" and the "Streamer" of the channel the bot is in.

Note - All `cooldown` commands do not require exact search entries. Some examples can be found below:

 - !astat 995 >> `The flesh damage of 5.56x45 M995 is: 40 and the armor penetration is: 53.`
 - !astat 545x39 BS >> `The flesh damage of 545x39 BS is: 40 and the armor penetration is: 51.`
 - !medical prop >> `The usage time of Surv12 is: 20 seconds.`
 - !price slick >> `The price of LBT 6094A Slick Plate Carrier (80/80) is: 390,000 roubles.`
 - !slot slick >> `The price per slot of LBT 6094A Slick Plate Carrier (80/80) is: 43333 rubles.`
 - !wiki >> `The link to the wiki is https://escapefromtarkov.gamepedia.com/LBT_6094A_Slick_Plate_Carrier`



