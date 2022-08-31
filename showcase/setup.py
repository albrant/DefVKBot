from django.core.management import utils


def main():
    """Функция создания файла .env с секретными данными"""
    with open('.env', 'w') as f:
        f.write(f'SECRET_KEY={utils.get_random_secret_key()}\n')
        f.write('VK_API_TOKEN=\n')
        f.write('ID_PUBLIC=\n')


if __name__ == '__main__':
    main()
