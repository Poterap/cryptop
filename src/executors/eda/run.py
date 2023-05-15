from src.ds.modules.eda_auto import autoeda

print("Skrypt EDA jest uruchamiany...")
auto_eda = autoeda()
auto_eda.make_raport_from_directory('./src/parsers/D2/data/stooq_data_2023-05-09')
print("Skrypt EDA zakończony.")