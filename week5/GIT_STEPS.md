# Как сделать Week 5 через терминал (папки остаются на ноутбуке)

```bash
# 1. Один раз: клонируем репозиторий (локальная копия со всеми неделями останется на ноутбуке)
cd ~/Documents                      # любая папка, куда хотите
git clone https://github.com/mikami-306/threat_intellegence_vidar.git
cd threat_intellegence_vidar

# 2. Копируем папку week5 (из распакованного архива) в репозиторий
cp -r ~/Downloads/week5 ./week5     # Windows PowerShell: Copy-Item -Recurse $HOME\Downloads\week5 .\week5

# 3. Проверяем и запускаем локально
cd week5
python3 -m pip install pandas matplotlib requests
python3 generate_logs.py && python3 build_ioc_queries.py && python3 run_hunt.py
cd ..

# 4. Коммит (создаёт сохранённую версию) и отправка на GitHub
git status
git add week5
git commit -m "docs: add week 5 threat hunting report, queries and scripts"
git pull --rebase origin main       # если ветка называется master - замените
git push origin main
```
Если репозиторий уже клонирован: пропустите шаг 1, зайдите в папку и сделайте `git pull`.

## ELK (для скриншотов)
```bash
cd week5
docker compose up -d                # подождать 1-2 минуты
python3 load_to_elk.py
# Kibana: http://localhost:5601 -> Stack Management -> Data Views -> создать `sysmon-sim*` (timestamp: @timestamp)
# Discover -> вставить запросы из hunt_queries/elk_kql.md -> сделать скриншоты в week5/screenshots/
docker compose down
```
Затем: `git add week5 && git commit -m "docs: add week 5 kibana screenshots" && git push`.

## План защиты (7-8 минут)
1. 1 мин: интел- vs гипотеза-ориентированный хантинг, наша гипотеза (ClickFix -> PowerShell -> Vidar).
2. 2 мин: таблица H1-H4 и связь с Kill Chain / ATT&CK (неделя 4).
3. 3 мин: демо в Kibana: H1, H3, pivot по WS-04, таймлайн.
4. 1 мин: тюнинг (509 -> 3 -> 2) и ложные срабатывания.
5. 1 мин: вывод и переход к детектам (Sigma/MISP).
