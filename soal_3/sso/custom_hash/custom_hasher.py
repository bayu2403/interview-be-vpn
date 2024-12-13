import hvac
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from dotenv import load_dotenv
import os

load_dotenv()

vault_client = hvac.Client(url=os.getenv("VAULT_ADDR"))
vault_client.token = os.getenv("VAULT_TOKEN")

class CustomPBKDF2PasswordHasher(PBKDF2PasswordHasher):
    def encode(self, password, salt, iterations=None):
        secret_key = self.get_secret_key_from_vault(self.project_name)
        
        if not secret_key:
            raise ValueError(f"Secret key for project '{self.project_name}' not found.")
        
        password_with_key = password + secret_key
        print(f"Encoding: password='{password_with_key}', salt='{salt}'")
        return super().encode(password_with_key, salt, iterations)

    def verify(self, password, encoded):
        print(f"Verifying: password='{password}', encoded='{encoded}'")
        return super().verify(password, encoded)

    def get_secret_key_from_vault(self, project_name):
        secret_path = f"secret/{project_name}_SECRET_KEY"
        try:
            secret_response = vault_client.secrets.kv.read_secret_version(path=secret_path)
            secret_key = secret_response['data']['data']['value']
            return secret_key
        except Exception as e:
            print(f"Error retrieving secret from Vault: {e}")
            return None