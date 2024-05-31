import vk_api
import datetime
import xlsxwriter

print("Работа парсера началась:")

def fetch_posts(vk, owner_id):
    all_posts = []
    offset = 0
    while True:
        # Получаем записи со стены
        posts = vk.wall.get(owner_id=owner_id, count=100, offset=offset)['items']
        if not posts:
            break

        for post in posts:
            # Преобразуем дату из timestamp в год
            post_date = datetime.datetime.fromtimestamp(post['date']).year
            if post_date < 2014:
                return all_posts  # Прекращаем загрузку, если дата записи раньше 2014 года
            elif  2014 <= post_date <= 2025:
                all_posts.append(post) # Сохраняем все записи с 2022 по 2023 годы включительно

        offset += 100

    return all_posts

def write_to_excel(posts, filename):
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    # Заголовки столбцов
    headers = ['Уникальный идентификатор записи', 'Дата и время публикации', 'Текст записи', 'Количество комментариев', 'Информация о лайках', 'Количество просмотров']
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)

    # Записываем данные постов в Excel
    for row, post in enumerate(posts, start=1):
        worksheet.write(row, 0, post.get('id', 'n/d'))
        worksheet.write(row, 1, datetime.datetime.fromtimestamp(post.get('date', 0)).strftime('%Y-%m-%d %H:%M:%S'))
        worksheet.write(row, 2, post.get('text', 'n/d'))
        worksheet.write(row, 3, post['comments'].get('count', 'n/d') if 'comments' in post else 'n/d')
        worksheet.write(row, 4, post['likes'].get('count', 'n/d') if 'likes' in post else 'n/d')
        worksheet.write(row, 5, post['views'].get('count', 'n/d') if 'views' in post else 'n/d')

    workbook.close()

def main():
    try:
        # Используем токен вместо логина и пароля
        vk_session = vk_api.VkApi(token='vk1.a._c9uuABdVXku9-eoLokWDtAy4yHI0cpJxxQE-NVCeDoumEMvMb6bC9OIjZGF1AT5X_PtBYIfqLL4UeBCDdhmZt-hheHaXE9ViIky1Pc9dCChkBM718wyVP-P-y5DlwuaMFdeFiGqMUDqDldO2PcOMGvNitI_yH-jhHvYHy210k11ZStaEJxiFEfVpliERTfbDXOK6mQ64GnhBjZ0IQeAqw')
        vk_session._auth_token(reauth=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()

    'id группы -- ее название'
    '-39399849 -- Crypto мир. Сообщество крипто-энтузиастов'
    '-29387592 -- Bitcoin, майнинг Биткоин'
    '-143763740 -- Investorlife | Криптовалюта, Инвестиции, Биткоин'
    '-143585694 -- КриптоМания | Биткоин Криптовалюта Финансы NFT'
    '-46149731 -- Криптовалюта | Биткоин | Трейдер'
    '-159867640 -- Crypton. Биткоин и криптовалюты'
    '-118446604 -- Криптовалюта Биткоин'

    '-140880848 -- Эфириум/Ethereum'

    '-106835626 -- InvestFuture'
    '-23342771 -- Бизнес-секреты'
    '-201880129 -- Рофлы с Волк Стрит'
    ''
    ''



    # ID группы с минусом (например, для группы https://vk.com/club1, owner_id будет -1)
    owners_id = [-143763740]  # Замените -1 на ID вашей группы
    for owner_id in owners_id:
        try:
            posts = fetch_posts(vk, owner_id)
            print(f"Найдено {len(posts)} записей, начиная с 2022 года.")

            write_to_excel(posts, str(owner_id)[1:]+'.xlsx')
        except:
            pass

if __name__ == '__main__':
    main()