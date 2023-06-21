from os import getcwd, path

DIRNAME = "storage"

class ManagerFiles:

    def __init__(self, name, extension):
        filename = f"{name}.{extension}"
        self._filepath = path.join(getcwd(), DIRNAME, filename)

        if not path.exists(self._filepath):
            file = open(self._filepath, 'w')
            file.close()

    @property
    def list_sitenames(self):
        sitenames = []

        with open(self._filepath, 'r') as file:
            for line in file:
                line = line.replace('\n', '')
                data = line.split('|')
                sitenames.append(data[0])

        return sitenames

    def search_data_file(self, name : str):
        data = None

        with open(self._filepath, 'r') as file:
            for line in file:
                line = line.replace('\n', '')

                if name in line:
                    data = line.split('|')
                    data = {
                        'site': data[0],
                        'username': data[1],
                        'password': data[2],
                        'key': data[3]
                    }
                    break

        return data

    def exist_data_file(self, name : str) -> bool:
        return self.search_data_file(name) is not None

    def add_data_file(self, data : list):
        data_format = "{0}|{1}|{2}|{3}\n".format(data['site'], data['username'], data['password'], data['key'])

        with open(self._filepath, 'a') as file:
            file.write(data_format)

    def delete_data_file(self, name : str) -> bool:
        index = None

        with open(self._filepath, 'r') as file:
            lines = file.readlines()

            for i, line in enumerate(lines):
                if name in line:
                    index = i
                    break

        if index is not None:
            del lines[index]

            with open(self._filepath, 'w') as file:
                file.writelines(lines)

            return True

        return False
