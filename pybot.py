import discord
import asyncio
import requests
import json

client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.content.startswith('!c'):
        msg = message.content.split()
        print(msg)
        if len(msg) < 3:
            symbol = msg[1].upper()
            print(symbol)
            r = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=" + symbol + "&tsyms=BTC,USD")

            data = r.json()
            price = "{0:.2f}".format(data['RAW'][symbol]['USD']['PRICE'])
            btcPrice = "{0:.8f}".format(data['RAW'][symbol]['BTC']['PRICE'])
            print(btcPrice)
            percent = "{0:.2f}".format(data['RAW'][symbol]['BTC']['CHANGEPCT24HOUR'])

            em = discord.Embed(title="**"+symbol+"**", description="*BTC Price*: \u20bf"+btcPrice+" | *USD Price*: $"+price, color=0x004080)
            # em.add_field(name="BTC Price:", value="\u20bf"+btcPrice, inline=True)
            # em.add_field(name="USD Price:", value="$"+price, inline=True)
            em.set_footer(text="24hr Change: "+str(percent)+"%")

            await client.send_message(message.channel, embed=em)
        else:
            symbol = msg[1].upper()
            print(symbol)
            r = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=" + symbol + "&tsyms=BTC,USD")

            data = r.json()
            price = "{0:.2f}".format(data['RAW'][symbol]['USD']['PRICE'])
            btcPrice = "{0:.8f}".format(data['RAW'][symbol]['BTC']['PRICE'])
            print(btcPrice)
            percent = "{0:.2f}".format(data['RAW'][symbol]['BTC']['CHANGEPCT24HOUR'])
            em = discord.Embed(title=symbol, color=0x004080)
            em.add_field(name="BTC Price:", value="\u20bf" + btcPrice, inline=True)
            em.add_field(name="USD Price:", value="$" + price, inline=True)
            em.set_footer(text="24hr Change: " + str(percent) + "%")

            await client.send_message(message.channel, embed=em)
    elif message.content.startswith('!info'):
        msg = message.content.split()
        print(msg)
        symbol = msg[1].upper()
        print(symbol)
        exchange = requests.get("https://min-api.cryptocompare.com/data/top/exchanges?fsym=" +symbol+ "&tsym=BTC")
        exchange = exchange.json()
        if not exchange['Data']:
            topexchange = "Unknown"
        else:
            topexchange = exchange['Data'][0]['exchange']
        id = requests.get("http://api.relativity.fund/api/12nBA81e1NAu81Z/U8Ha8102jfm7261NVZ0p129kL/json/coin/getID/" + symbol)
        id = json.loads(id.text)
        print(id['coin_id'])
        symbolid = str(id['coin_id'])
        r = requests.get("https://www.cryptocompare.com/api/data/coinsnapshotfullbyid/?id=" + symbolid)
        data = r.json()
        twitter = data['Data']['General']['Twitter']
        website = data['Data']['General']['AffiliateUrl']
        name = data['Data']['General']['Name']
        print(name)
        market = requests.get("https://api.coinmarketcap.com/v1/ticker/" + name.lower())
        market = json.loads(market.text)
        marketcap = int(float(market[0]['market_cap_usd']))

        em = discord.Embed(title=name, color=0x004080)
        em.add_field(name="Twitter:", value=twitter, inline=True)
        em.add_field(name="Website:", value=website, inline=True)
        em.add_field(name="Market Cap USD:", value="$"+"{:,}".format(marketcap), inline=True)
        em.add_field(name="Top Exchange:", value=topexchange, inline=True)
        await client.send_message(message.channel, embed=em)


client.run('')