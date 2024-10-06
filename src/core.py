from src.__init__ import *
from src.coinsweeper import Coinsweeper
def menu():
    print(f"         {Colors.MAGENTA}=> Main Menu\n")
    menu_item(1, "Start Script")
    menu_item(2, 'Edit Config')
    menu_item(3, 'About Devolopers')
    menu_item(99, 'Exit')
    options = {
        '1': start_script,
        '2': edit_config,
        '3': about_devoloper,
        '99': exit_code
    }
    print()
    while True:
        choice = input(f'{Colors.CYAN} Choice : ')
        if choice not in options:
            print(f'{Colors.YELLOW} Choose Valid Option')
            continue
        break

    options[choice]()
        
def start_script():
    while True:
        awak()
        tokens = load_tokens()
        log(Colors.CYAN + f' Number of Accounts {Colors.GREEN}{len(tokens)}')
        
        for index, token in enumerate(tokens):
            try:
                log_line()
                countdown_timer(random.randint(config('MIN_TIME_BETWEEN_ACCOUNTS', 10), config('MAX_TIME_BETWEEN_ACCOUNTS', 15)))
                account = Coinsweeper(token, random_proxy(), config('TIMEOUT', 6))
                log(f'{Colors.BLUE} Account Number : {Colors.GREEN}{index+1}')
                log(f'{Colors.BLUE} Account Username : {Colors.GREEN}{get_username(token)}')
                log(f'{Colors.YELLOW} Trying To Login ...')
                res = account.login()

                if res == 'success': log(f'{Colors.GREEN} Done Login Success !')
                else:
                    if res == 'fail':
                        log(f'{Colors.RED} Faild To Login Please Check Account Token !')
                    else:
                        log(f'{Colors.BLACK} {res}')
                        log(f'{Colors.RED} UnExpected Erro Please Contact With Devoloper To Fix !')
                    continue
                
                # res = account.daily_login()

                # if res == 'claimed':
                #     log(f'{Colors.BLUE} Daily login {Colors.GREEN}Claimed !')
                # elif res=='already_claimed':
                #     log(f'{Colors.BLUE} Daily login {Colors.GREEN}Aleady Claimed !')
                # else:
                #     log(f'{Colors.RED} {res}')

                for __ in range(random.randint(config('MIN_GAMES_PER_ACCOUNT', 4), config('MAX_GAMES_PER_ACCOUNT', 9))):
                    res = account.user_info()

                    if not res['success']:
                        log(f'{Colors.RED} Faild To Retrive Account info !')
                        break
                    time.sleep(3)
                    score = res['score']
                    log(f'{Colors.BLACK} ---------------------------------')
                    log(f"{Colors.BLUE} Account Balance : {Colors.GREEN}{score}")

                    countdown_timer(config('SMALL_DELAY', 3))

                    log(f' {Colors.BLUE}Starting game !')
                    res = account.start_game()
                    
                    if res == 'success': log(f' {Colors.GREEN}Done Game Has Started !')
                    else:
                        log(f' {Colors.BLACK} {res}')
                        log(f' {Colors.RED} UnExpected Erro Please Contact With Devoloper To Fix !')
                        continue
                    
                    gameTime = random.randint(config('MIN_GAME_TIME', 65), config('MAX_GAME_TIME', 185))
                    # gameTime = 60
                    # countdown_timer(gameTime)
                    countdown_timer(config('SMALL_DELAY', 3))

                    key = config('KEY', 'NOT SET')
                    if key == 'NOT SET':
                        log(f'{Colors.RED} Please Set Access Key First.')
                        exit_code()
                    
                    log(f' {Colors.BLUE}Getting game data ... ')
                    
                    retry = config('MAX_RETRY', 3)
                    for __ in range(retry):
                        res, status_code = account.game_data(key, gameTime)
                        if res == 'success':
                            log(f' {Colors.GREEN}Done Game Data Dumped !')
                            retry = 0
                            break
                        
                        if status_code==429:
                            log(f'{Colors.RED} Rate Limit For this key !')
                            retry = 1
                            break
                        
                        if status_code==403:
                            log(f'{Colors.RED} This key is Not Active !')
                            retry = 1
                            break

                        if status_code==401:
                            log(f'{Colors.RED} Invaild Key !')
                            retry = 1
                            break
                        
                        if status_code==400:
                            log(f'{Colors.RED} Key is Required !')
                            retry = 1
                            break
                    
                    if retry:
                        log(f' {Colors.RED}Faild To Dump Game Data !')
                        log(f' {Colors.RED}{res}')
                        continue

                    # countdown_timer(config('SMALL_DELAY', 3))
                    
                    countdown_timer(gameTime-lost_time(account.game_response['createdAt']))

                    is_win = choose_based_on_percentage(config('WINNING_PERCENTAGE', 80))
                    
                    if is_win:
                        log(f' {Colors.BLUE}Wining The Game ...')
                        res = account.win_game()
                    else:
                        log(f' {Colors.BLUE}Losing The Game ...')
                        res = account.lose_game()

                    if res == 'success':
                        log(f' {Colors.GREEN}Success + {int(account.game["score"]*is_win)} (^__*)')
                    else:
                        log(f' {Colors.RED}Faild To Finish The Game !')
                        log(f' {Colors.RED}If This message appear more than onece Please Tell The Devoloer [WARRING] !')
                        continue
                    
                    countdown_timer(random.randint(config('MIN_DELAY_AFTER_GAME', 5), config('MAX_DELAY_AFTER_GAME', 9)))

                countdown_timer(config('SMALL_DELAY', 3))
            except KeyboardInterrupt:
                exit_code()
            except Exception as E:
                log(f'{Colors.RED} {E}')
        countdown_timer(random.randint(config('MIN_DELAY_BEFORE_RESTART', 700), config('MAX_DELAY_BEFORE_RESTART', 1000)))
            

def edit_config():
    awak()
    config_values = read_config()
    i=1
    print(f"         {Colors.MAGENTA}=> Edit Config\n")
    conf = []
    for key, val in config_values.items():
        menu_item(i, key+Colors.YELLOW+' : '+Colors.GREEN+str(val))
        conf.append([key, val])
        i += 1
    menu_item(99, f'{Colors.YELLOW}Back\n')

    while True:
        choice = input(f'{Colors.CYAN} Choice : ')
        if choice == '99':
            awak()
            menu()
            return
        try:int(choice)
        except:
            print(f'{Colors.YELLOW} Choose Valid Intger')
            continue

        if int(choice)<1 or int(choice)>len(conf):
            print(f'{Colors.YELLOW} Choose Valid Option')
            continue
        break

    choice = int(choice)-1
    while True:
        value = input(f'{Colors.GREEN} {conf[choice][0]} = ')
        
        if not value.strip():
            print(f'{Colors.YELLOW} Enter Vaild Value !')
            continue
        break
    
    try: value = eval(value)
    except: pass
    edit_config_value(conf[choice][0], value)

    awak()
    menu()

    
def about_devoloper():
    awak()
    print(f"{Colors.BLUE} Devoloper : {Colors.GREEN}Abdo Sleem")
    print(f"{Colors.BLUE} Github : {Colors.GREEN}https://github.com/scriptvip")
    print(f"{Colors.BLUE} Telegram : {Colors.GREEN}https://t.me/glitch_no")
    log_line()
    input(f"\n   {Colors.YELLOW} Press Enter To Back !")
    awak()
    menu()

def exit_code():
    log_line()
    log(f'{Colors.RED} Exiting ...')
    exit()