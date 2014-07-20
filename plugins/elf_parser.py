from ODA.documentation.pluginprototype import PlugInTemplate
#pip install pyelftools worked
from elftools.elf.elffile import ELFFile
from io import BytesIO

class PlugIn(PlugInTemplate):
    def __init__(self, app):
        super().__init__(app)

    def run(self):
        self.app.core.plugin_manager.plugins['conditional_plugin_registry'].register('ELF', self.parse)

    def set_blob(self, blob):
        self.blob = BytesIO(blob)
        self.parser = ELFFile(self.blob)

    def __get_sections(self):
        arch = str(self.parser.elfclass)
        #Sections
        #Strings - do that elsewhere - maybe move elf-parser out to a plugin that is called from other plugins...
        section_count = self.parser['e_shnum']
        sections_data = []
        for i in range(section_count):
            section_offset = self.parser['e_shoff'] + i * self.parser['e_shentsize']
            self.blob.seek(section_offset)
            section_header = self.parser.structs.Elf_Shdr.parse_stream(self.blob)
            sections_data.append([section_header['sh_name'], section_header['sh_type'], section_offset])
        self.blob.seek(0)
        self.app.plugin_manager.plugins['fileid'].info['sections'] = sections_data
        self.app.plugin_manager.plugins['fileid'].build_ui()

    def __get_imports_exports(self):
        #Parse dynsym for imports and exports
        #Replicate readelf -Ws libzeitgeist-1.0.so.1
        pass

    def __get_reloc(self):
        #Parse for relocations so you can see things that move and rebase the hex blob as well...
        pass        

    def __get_strings(self):
        #Parse for declared strings before you search for strings with a regex...
        pass        

    def parse(self):
        self.__get_sections()
        self.__get_imports_exports()
        self.__get_reloc()
        self.__get_strings()
