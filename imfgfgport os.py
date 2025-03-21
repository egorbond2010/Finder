import os
import time
from pathlib import Path
from colorama import init, Fore, Style
from concurrent.futures import ThreadPoolExecutor
import struct
import datetime
import psutil
import win32api
import win32process
import win32con

# Инициализация colorama
init()

# Список подозрительных файлов (точные имена)
suspicious_files = set([
    ".flauncher", "exloader.exe", "flauncher.exe", "mrlauncher.exe", "r-launcher.exe", "mclauncher.exe", "impact.jar",
    "cheatengine.exe", "matix.jar", "wwe.jar", "grey.jar", "jessica.jar", "skillclient.jar", "skyclient.jar", "wolfram.jar",
    "huzuni.jar", "squad.jar", "tools.jar", "mc100.dll", "kyprak.exe", "zamorozka.jar", "aristois.jar", "oymine.exe",
    "sigma.jar", "hcl.exe", "advanced.jar", "xray.jar", "x-ray.jar", "hvii.exe", "wurst.jar", "erbaevhacks.exe", "akrien.jar",
    "neverhook.exe", "wild.exe", "archware.exe", "vape.exe", "lite.exe", "inertia.jar", "cortex.exe", "nathox.exe", "reverse.exe",
    "never.exe", "wintware.exe", "pyro.exe", "rage.exe", "r9.exe", "bypass.exe", "matrix.jar", "trash.exe", "undetectable.exe",
    "editme.dll", "celestial.jar", "deadcode.exe", "freecam.jar", "infinity.exe", "forceware.exe", "nursultan.exe", "groza.exe",
    "baritone.jar", "cabaletta.jar", "jigsaw.jar", "liquidbounce.jar", "gishcode.exe", "rename_me_please.dll",
    "future.jar", "rusherhack.jar", "konas.jar", "wintware.exe", "norules.exe", "eternity.jar", "wexside.exe", "rich.exe",
    "richpremium.exe", "editme.dll", "r3d.jar", "destroy.exe", "nightmare.exe", "bebraware.exe", "bolshoy.exe",
    "salhack.jar", ".wex.exe", "minced.exe", "ares.jar", "meteor.jar", "skill.jar", "r3dcraft.jar", "bleach.jar", "jello.jar",
    "richclient.exe", "liqued.jar", "kami.jar", "flux.jar", "betterpvp.jar", "xaero.jar", "journey.jar", "voxel.jar",
    "scroller.exe", "sigma5.jar", "loader.exe", "replaymod.jar", "mojang.exe"
])

# Список строк для поиска в javaw.exe
suspicious_strings = [
    "Doomsday", "o#McqUmEXL!rmU/", "F0FV7PPL2N11Q", "ICZiLyghPIgFYmk", "UhudOjqLJHIQUwqR`Y",
    "hud^U]heHuXaxwR", "hudVE]Lt", "mKlONdHuyPb]YlVWJm\\BwbIKcVlOWX", "ksKmBIHSZTwXKT", "laimWkASQ",
    "WRWiDx", "BT[CeZPbhrvdHf", "u;<r,7NVce;Ga25", "eObOiPdFJR", "Wu&XNC]30?3=7",
    "M%dlK7]u$'Y^8+$BZ", "x4qGlIFLPCS", "gwU]cumFVtfvAKiyaq", "DniuE^qJNEV", "sMS`EqNZ_U",
    "SCHEDULED_EXECUTABLES", "lookAheadStep", "Troxill", "trahil", "troxill", "zdcoder",
    "IIv.class", "ADd.class", "PAZZAZZZY^Z^Y[_", "6L~gKlyLK(O*", "84AHc2&Mi%Z",
    "ZgYm[CUQRN", "VaJeoZvd@", "radioegor146"
]

# Исключаемые системные папки
exclude_dirs = {"C:\\Windows", "C:\\ProgramData", "C:\\System Volume Information"}

# Подсчёт всех файлов
def count_files(directory):
    total_files = 0
    try:
        for root, dirs, files in os.walk(directory):
            if root != "C:\\" and any(root.startswith(excl) for excl in exclude_dirs):
                dirs[:] = []
                continue
            total_files += len(files)
    except Exception as e:
        print(f"{Fore.YELLOW}Ошибка при подсчёте файлов в {directory}: {e}{Style.RESET_ALL}")
    return total_files

# Поиск файлов с точным совпадением
def search_files(directory, suspicious_set, total_files, processed_files):
    found_files = []
    print(f"{Fore.YELLOW}Сканируем директорию: {directory}{Style.RESET_ALL}")
    try:
        for root, dirs, files in os.walk(directory):
            if root != "C:\\" and any(root.startswith(excl) for excl in exclude_dirs):
                dirs[:] = []
                continue
            for file in files:
                processed_files[0] += 1
                if processed_files[0] % 5000 == 0 or processed_files[0] == total_files:
                    percent = (processed_files[0] / total_files) * 100 if total_files > 0 else 100
                    print(f"\r{Fore.CYAN}Сканирование {directory}: [{percent:.1f}%]{Style.RESET_ALL}", end="")
                file_lower = file.lower()
                if file_lower in suspicious_set:
                    found_files.append(f"{Fore.RED}Найден: {file} | Путь: {os.path.join(root, file)}{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.YELLOW}Ошибка при сканировании {directory}: {e}{Style.RESET_ALL}")
    return found_files

# Проверка natives
def check_natives_size():
    minecraft_dir = os.path.join(os.getenv("APPDATA"), ".minecraft")
    versions_dir = os.path.join(minecraft_dir, "versions")
    found_files = []

    try:
        for version in os.listdir(versions_dir):
            if "1.16.5" in version:
                natives_dir = os.path.join(versions_dir, version, "natives")
                if os.path.exists(natives_dir):
                    for root, _, files in os.walk(natives_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            size_kb = os.path.getsize(file_path) / 1024
                            if size_kb > 17136:
                                found_files.append(f"{Fore.RED}Подозрительный файл в natives: {file} | Размер: {size_kb:.2f} KB | Путь: {file_path}{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.YELLOW}Ошибка при проверке natives: {e}{Style.RESET_ALL}")
    return found_files

# Проверка корзины
def check_recycle_bin():
    recycle_bin_path = "C:\\$Recycle.Bin"
    deleted_files = []
    last_clear_time = None

    if not os.path.exists(recycle_bin_path):
        print(f"{Fore.YELLOW}Корзина не найдена или недоступна.{Style.RESET_ALL}")
        return

    try:
        for root, dirs, files in os.walk(recycle_bin_path):
            for file in files:
                if file.startswith("$I"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "rb") as f:
                        data = f.read()
                        if len(data) >= 24:
                            timestamp = struct.unpack("<Q", data[8:16])[0]
                            delete_time = datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=timestamp / 10)
                            file_size = struct.unpack("<Q", data[16:24])[0]
                            name_offset = 24
                            if len(data) > name_offset:
                                file_name = data[name_offset:].decode("utf-16le").rstrip("\x00")
                                deleted_files.append((file_name, delete_time, file_size))
                                if last_clear_time is None or delete_time > last_clear_time:
                                    last_clear_time = delete_time
    except Exception as e:
        print(f"{Fore.YELLOW}Ошибка при чтении корзины: {e}{Style.RESET_ALL}")

    if deleted_files:
        print(f"\n{Fore.YELLOW}--- Удалённые файлы в корзине ---{Style.RESET_ALL}")
        for file_name, delete_time, file_size in deleted_files:
            print(f"{Fore.YELLOW}Файл: {file_name} | Удалён: {delete_time} | Размер: {file_size / 1024:.2f} KB{Style.RESET_ALL}")
    if last_clear_time:
        print(f"{Fore.YELLOW}Последняя активность корзины (примерная очистка): {last_clear_time}{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}Корзина пуста или не использовалась.{Style.RESET_ALL}")

# Сканирование строк в javaw.exe
def scan_javaw_strings():
    print(f"{Fore.GREEN}Сканирование строк в javaw.exe началось...{Style.RESET_ALL}")
    found_strings = []

    # Поиск процесса javaw.exe
    javaw_pid = None
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'].lower() == "javaw.exe":
            javaw_pid = proc.info['pid']
            break

    if not javaw_pid:
        print(f"{Fore.YELLOW}Процесс javaw.exe не найден.{Style.RESET_ALL}")
        return

    try:
        # Открываем процесс с правами чтения памяти
        process_handle = win32api.OpenProcess(win32con.PROCESS_VM_READ | win32con.PROCESS_QUERY_INFORMATION, False, javaw_pid)
        if not process_handle:
            print(f"{Fore.YELLOW}Не удалось открыть процесс javaw.exe. Запустите с правами администратора.{Style.RESET_ALL}")
            return

        # Получаем информацию о памяти процесса
        memory_regions = win32process.EnumProcessModules(process_handle)
        for module in memory_regions:
            base_addr = module
            try:
                # Читаем память (например, первые 1MB для теста)
                buffer_size = 1024 * 1024  # 1MB
                memory_content = win32process.ReadProcessMemory(process_handle, base_addr, buffer_size)
                memory_str = memory_content.decode('utf-8', errors='ignore')

                # Ищем подозрительные строки
                for suspicious in suspicious_strings:
                    if suspicious in memory_str:
                        found_strings.append(f"{Fore.RED}Найдена строка: {suspicious}{Style.RESET_ALL}")
            except Exception as e:
                continue  # Пропускаем недоступные регионы памяти

        win32api.CloseHandle(process_handle)

        if found_strings:
            print(f"\n{Fore.RED}--- Подозрительные строки в javaw.exe ---{Style.RESET_ALL}")
            for s in found_strings:
                print(s)
        else:
            print(f"{Fore.GREEN}Подозрительных строк в javaw.exe не найдено.{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.YELLOW}Ошибка при сканировании javaw.exe: {e}{Style.RESET_ALL}")

# Основная функция проверки системы
def scan_system():
    results = []
    directories = [
        os.getenv("APPDATA"),
        os.path.join(os.getenv("APPDATA"), ".minecraft", "mods"),
        os.path.join(os.getenv("APPDATA"), ".minecraft"),
        os.path.join(os.getenv("APPDATA"), ".minecraft", "versions"),
        "C:\\",
        "C:\\Program Files",
        "C:\\Program Files (x86)"
    ]

    total_files = sum(count_files(d) for d in directories if os.path.exists(d))
    processed_files = [0]

    with ThreadPoolExecutor(max_workers=8) as executor:
        future_to_dir = {executor.submit(search_files, d, suspicious_files, total_files, processed_files): d 
                         for d in directories if os.path.exists(d)}
        for future in future_to_dir:
            results.extend(future.result())

    results.extend(check_natives_size())
    print(f"\r{Fore.CYAN}Сканирование завершено: [100.0%]{Style.RESET_ALL}")

    if results:
        print(f"\n{Fore.RED}--- Найденные подозрительные файлы ---{Style.RESET_ALL}")
        for result in results:
            print(result)
    else:
        print(f"\n{Fore.GREEN}Подозрительных файлов не найдено.{Style.RESET_ALL}")

# Меню
def main_menu():
    while True:
        print(f"\n{Fore.MAGENTA}╔════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}║     Program Cheat Scanner  ║{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}╠════════════════════════════╣{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║  1 - Проверить систему     ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║  2 - Проверить корзину     ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║  3 - Сканировать javaw.exe ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║  4 - Выход                 ║{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}╚════════════════════════════╝{Style.RESET_ALL}")
        choice = input(f"{Fore.YELLOW}Выберите действие: {Style.RESET_ALL}")

        if choice == "1":
            print(f"{Fore.GREEN}Сканирование системы началось...{Style.RESET_ALL}")
            scan_system()
        elif choice == "2":
            print(f"{Fore.GREEN}Проверка корзины началась...{Style.RESET_ALL}")
            check_recycle_bin()
        elif choice == "3":
            scan_javaw_strings()
        elif choice == "4":
            print(f"{Fore.GREEN}Выход из программы.{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Неверный выбор, попробуйте снова.{Style.RESET_ALL}")
        time.sleep(1)

if __name__ == "__main__":
    main_menu()