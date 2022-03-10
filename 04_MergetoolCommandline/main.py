import cmd

from pynames import GENDER, LANGUAGE
from pynames.generators import iron_kingdoms
from pynames.generators import scandinavian
from pynames.generators import russian
from pynames.generators import mongolian
from pynames.generators import korean
from pynames.generators import goblin
from pynames.generators import orc
from pynames.generators import elven


class PyNamesShell(cmd.Cmd):
    _language = LANGUAGE.NATIVE

    generators = {
        'iron_kingdoms': {
            'gobber': iron_kingdoms.GobberFullnameGenerator(),
            'thurian': iron_kingdoms.ThurianFullnameGenerator(),
            'morridane': iron_kingdoms.MorridaneFullnameGenerator(),
            'tordoran': iron_kingdoms.TordoranFullnameGenerator(),
            'ryn': iron_kingdoms.RynFullnameGenerator(),
            'dwarf': iron_kingdoms.DwarfFullnameGenerator(),
            'iossan': iron_kingdoms.IossanNyssFullnameGenerator(),
            'nyss': iron_kingdoms.IossanNyssFullnameGenerator(),
            'caspian': iron_kingdoms.CaspianMidlunderSuleseFullnameGenerator(),
            'midlunder': iron_kingdoms.CaspianMidlunderSuleseFullnameGenerator(),
            'sulese': iron_kingdoms.CaspianMidlunderSuleseFullnameGenerator(),
            'khadoran': iron_kingdoms.KhadoranFullnameGenerator(),
            'ogrun': iron_kingdoms.OgrunFullnameGenerator(),
            'trollkin': iron_kingdoms.TrollkinFullnameGenerator(),
        },
        'scandinavian': {
            'traditional': scandinavian.ScandinavianNamesGenerator(),
        },
        'russian': {
            'pagan': russian.PaganNamesGenerator(),
        },
        'mongolian': {
            'traditional': mongolian.MongolianNamesGenerator(),
        },
        'korean': {
            'traditional': korean.KoreanNamesGenerator(),
        },
        'goblin': {
            'custom': goblin.GoblinGenerator(),
        },
        'orc': {
            'custom': orc.OrcNamesGenerator(),
        },
        'elven': {
            'dnd': elven.DnDNamesGenerator(),
            'warhammer': elven.WarhammerNamesGenerator(),
        },

    }

    genders = {'male': GENDER.MALE, 'female': GENDER.FEMALE}

    def _parse(self, args):
        list_args = args.split()
        gender = 'male'
        if len(list_args) == 1:
            class_ = list_args[0]
            subclass = self.generators[class_]
        elif len(list_args) == 2:
            class_ = list_args[0]
            if list_args[1] in self.genders:
                gender = list_args[1]
                subclass = list(self.generators[class_].keys())[0]
            else:
                subclass = list_args[1]
        else:
            class_ = list_args[0]
            subclass = list_args[1]
            gender = list_args[2]
        return class_.lower(), subclass.lower(), self.genders[gender.lower()]

    def _info_parse(self, args):
        list_args = args.split()
        type_ = None
        if len(list_args) == 1:
            class_ = list_args[0]
            subclass = list(self.generators[class_].keys())[0]
        elif len(list_args) == 2:
            class_ = list_args[0]
            if list_args[1] in self.genders:
                type_ = list_args[1]
                subclass = list(self.generators[class_].keys())[0]
            elif list_args[1] == 'language':
                type_ = list_args[1]
                subclass = list(self.generators[class_].keys())[0]
            else:
                subclass = list_args[1]
        else:
            class_ = list_args[0]
            subclass = list_args[1]
            type_ = list_args[2]
        return class_.lower(), subclass.lower(), type_

    def do_language(self, language: str = LANGUAGE.NATIVE):
        if language.lower() in LANGUAGE.ALL:
            self._language = language.lower()
        else:
            self._language = LANGUAGE.NATIVE

    def do_generate(self, args):
        try:
            class_, subclass, gender = self._parse(args)
        except Exception as ex:
            print('incorrect input parameters')
            return

        generator = self.generators[class_][subclass]
        if self._language not in generator.languages:
            target_language = LANGUAGE.NATIVE
        else:
            target_language = self._language

        ans = generator.get_name_simple(gender, target_language)
        print(ans)
        return

    def do_info(self, args):
        try:
            class_, subclass, type_ = self._info_parse(args)
        except Exception as ex:
            print('incorrect input parameters')
            return
        generator = self.generators[class_][subclass]
        print(class_, subclass, type_)
        if type_ in self.genders:
            print(generator.get_names_number(self.genders[type_]))
        elif type_ == 'language':
            print(*generator.languages)
        elif type_ is None:
            print(generator.get_names_number())
        else:
            print('incorrect input parameters')

        return

    def do_exit(self, args):
        return True


if __name__ == '__main__':
    PyNamesShell().cmdloop()
