import os
import binascii
import pandas as pd
from flask import Flask
from cardano_explorer import blockfrost_api
from healthcheck import HealthCheck, EnvironmentDump


app = Flask(__name__)
health = HealthCheck(app, "/health")
envdump = EnvironmentDump(app, "/env")


@app.route('/')
def root():
    logo = "https://cnft.tools/static/assets/" + \
           "projectthumbs/ghostchain_bot/7086.jpeg"
    return f"<img src='{logo}'/><br/><br/>Access the app " + \
           "<a href='/health'>Healthcheck</a> " + \
           "and <a href='/env'>" + \
           "environnement</a> information"


@app.route("/<wallet>", methods=['GET'])
def main(wallet):

    api_key = os.environ['BF_API_KEY']
    gc_policy_id = "8021c0ab3285cc3cfff2b7e61e96ece565fb37279b67666741587b54"
    ha_policy_id = "f0ff48bbb7bbe9d59a40f1ce90e9e9d0ff5002ec48f232b49ca0fb9a"
    cardano_mainnet = blockfrost_api.Auth(api_key=api_key)
    assets_info = pd.read_csv('gh_scv.csv', sep='\t')

    try:
        wallet_info = cardano_mainnet.address_info(wallet)
    except Exception as err:
        wallet_info = ''

    if not wallet_info:
        try:
            hexify = str(binascii.hexlify(bytes(wallet, 'utf-8')), "utf-8")
            wallet = cardano_mainnet.asset_addresses(ha_policy_id +
                                                     hexify)['address'][0]
            wallet_info = cardano_mainnet.address_info(wallet)
        except Exception as err:
            return str(err)
    gh = [i["unit"] for i in wallet_info["amount"]
          if gc_policy_id in i["unit"]]
    if gh:
        return str(assets_info.loc[
                   assets_info['asset'].isin(gh)
                   ].dna_reward.sum())
    else:
        return str(0.0)


if __name__ == '__main__':
    port = 5100

    app.run(host="0.0.0.0", port=port)
