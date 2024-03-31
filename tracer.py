import re
import subprocess
from json import loads
from urllib import request
import argparse

ip_regex = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')

RU_DICT = {
    'invalid input': 'Не удается разрешить системное имя узла',
    'tracing': 'Трассировка маршрута',
    'host unreachable': 'Заданный узел недоступен.',
    'trace complete': 'Трассировка завершена',
    'max hops': 'с максимальным числом прыжков'
}


class NetworkResponse:
    def __init__(self, data: dict):
        self._data = data
        self._analyze()

    def _analyze(self):
        self.ip = self._data.get('ip') or '--'
        self.city = self._data.get('city') or '--'
        self.country = self._data.get('country') or '--'
        self.hostname = self._data.get('hostname') or '--'
        if org := self._data.get('org'):
            self.AS, self.provider = org.split()[0], ' '.join(org.split()[1:])
        else:
            self.AS, self.provider = '--', '--'


class Output:
    _IP_LENGTH = 15
    _AS_LENGTH = 6
    _PROVIDER_LENGTH = 25

    def __init__(self):
        self._number = 1

    def print(self, ip, AS, country, city, provider):
        if self._number == 1:
            self._print_header()
        string = f'{self._number}' + ' ' * (3 - len(str(self._number)))
        string += ip + self._spaces(self._IP_LENGTH, len(ip))
        string += AS + self._spaces(self._AS_LENGTH, len(AS))
        string += provider + self._spaces(self._PROVIDER_LENGTH, len(provider))
        string += f'{country}/{city}'

        self._number += 1
        print(string)

    @staticmethod
    def _print_header():
        print('№  IP' + ' ' * 16 + 'AS' + ' ' * 7 +
              'Provider' + ' ' * 20 + 'Country/City')

    @staticmethod
    def _spaces(expected: int, actual: int) -> str:
        return ' ' * (3 + (expected - actual))


def get_route(address: str, os_lang: dict[str, str]):
    tracert = subprocess.Popen(['tracert', address], stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
    get_as = False
    output = Output()
    for line in iter(tracert.stdout.readline, ""):
        line = line.decode(encoding='cp866')
        if line.find(os_lang['invalid input']) != -1:
            print(line)
            break
        elif line.find(os_lang['tracing']) != -1:
            print(line, end='')
            end = ip_regex.findall(line)[0]
        elif line.find(os_lang['max hops']) != -1:
            get_as = True
        elif line.find(os_lang['host unreachable']) != -1:
            print(line.removeprefix(' '))
            break
        elif line.find(os_lang['trace complete']) != -1:
            print(line)
            break

        try:
            ip = ip_regex.findall(line)[0]
        except IndexError:
            continue

        if get_as:
            response = get_as_number_by_ip(ip)
            output.print(response.ip, response.AS,
                         response.country, response.city, response.provider)
            if ip == end:
                print('Трассировка завершена.')
                break


def get_as_number_by_ip(ip) -> NetworkResponse:
    inf = loads(request.urlopen('https://ipinfo.io/' + ip + '/json').read())
    return NetworkResponse(inf)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Autonomous Systems tracert')
    parser.add_argument('address', type=str,
                        help='Destination to which utility traces route.')
    return parser.parse_args()


if __name__ == '__main__':
    site = parse_args()
    get_route(site.address, RU_DICT)
