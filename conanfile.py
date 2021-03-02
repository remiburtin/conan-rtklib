import os
import glob
from conans import ConanFile, CMake, tools

class RTKLIBConan(ConanFile):
    name = "RTKLIB"
    description = "An Open Source Program Package for GNSS Positioning"
    license = "BSD 2-clause"
    topics = ("conan", "gnss")
    homepage = "http://www.rtklib.com/"
    settings = "os", "arch", "compiler", "build_type"
    exports_sources = ["CMakeLists.txt", "patches/**"]
    generators = "cmake", "cmake_find_package"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_galileo": [True, False],
        "with_beidou": [True, False],
        "with_qzss": [True, False],
        "with_irnss": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "with_galileo": True,
        "with_beidou": True,
        "with_qzss": True,
        "with_irnss": True,
    }

    _cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

    def _patch_sources(self):
        for patch in self.conan_data.get("patches", {}).get(self.version, []):
            tools.patch(**patch)

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = glob.glob('RTKLIB-*/')[0]
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake

        self._cmake = CMake(self)
        self._cmake.definitions["WITH_GALILEO"] = self.options.with_galileo
        self._cmake.definitions["WITH_BEIDOU"] = self.options.with_beidou
        self._cmake.definitions["WITH_QZSS"] = self.options.with_qzss
        self._cmake.definitions["WITH_IRNSS"] = self.options.with_irnss

        self._cmake.configure(build_folder=self._build_subfolder)

        return self._cmake

    def build(self):
        self._patch_sources()
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("LICENSE.txt", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.defines= ["DENAGLO"]

        if self.settings.os == "Windows" and not self.options.shared:
            self.cpp_info.system_libs = ["Winmm", "Ws2_32"]