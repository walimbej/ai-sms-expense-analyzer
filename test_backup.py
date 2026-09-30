





























from iphone_backup_decrypt import EncryptedBackup
import getpass
import os

backup_path = "/Users/jwalimbe/Library/Application Support/MobileSync/Backup/00008020-000A6CCE1A46002E"

output_path = "/Users/jwalimbe/ai-sms-expense-analyzer/data/sms.db"

passphrase = getpass.getpass("Enter backup password: ")

backup = EncryptedBackup(
    backup_directory=backup_path,
    passphrase=passphrase
)

os.makedirs(os.path.dirname(output_path), exist_ok=True)

backup.extract_file(
    relative_path="Library/SMS/sms.db",
    domain_like="HomeDomain",
    output_filename=output_path
)

print("Messages database extracted successfully")
print(output_path)