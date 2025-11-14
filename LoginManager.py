# LoginManager.py
import json
import shioaji as sj

def login_from_config(config_path="config.json"):
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    api = sj.Shioaji(simulation=config.get("simulation", False))
    api.login(api_key=config["api_key"], secret_key=config["secret_key"], contracts_timeout=10000)
    print(f"✅ 登入成功｜模式：{'模擬' if config['simulation'] else '真實'}")

    if not config["simulation"]:
        api.activate_ca(
            ca_path=config["ca_path"],
            ca_passwd=config["ca_passwd"],
            person_id=config["person_id"]
        )
        print("✅ 憑證啟用成功")

    return api, config
