import hvac
import os

VAULT_ADDR = "http://localhost:8200" 
VAULT_TOKEN = "myroot"

client = hvac.Client(url=VAULT_ADDR)
client.token = VAULT_TOKEN

if not client.is_authenticated():
    print("Vault authentication failed")
    exit(1)

secrets = {
    "PROJECT_1_SECRET_KEY": "supersecretkey1",
    "PROJECT_2_SECRET_KEY": "supersecretkey2"
}

for project, secret_value in secrets.items():
    secret_path = f"secret/{project}"
    try:
        client.secrets.kv.v2.create_or_update_secret(
            path=secret_path,
            secret={"value": secret_value}
        )
        print(f"Successfully stored secret for {project}")
    except Exception as e:
        print(f"Failed to store secret for {project}: {e}")
