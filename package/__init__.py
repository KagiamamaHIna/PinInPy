from ._pinin4cpp_cffi import lib,ffi
from enum import IntEnum
import cffi

_pffi = ffi

ffi = cffi.FFI()

__version__ = "1.0.0"
__all__ = ["PinIn", "TreeSearcher", "Logic", "Keyboard", "PinInConfig", "DeserializeException", "PinInInitException", "TreeSearcherInitException"]

def _create_pinin(handle):
    if handle == ffi.NULL:
        return None
    return ffi.gc(handle,lib.PinInCpp_PinIn_Free)
    
def _create_tree_searcher(handle):
    if handle == ffi.NULL:
        return None
    return ffi.gc(handle,lib.PinInCpp_TreeSearcher_Free)

class Logic(IntEnum):
    BEGIN = lib.PinInCpp_BEGIN
    CONTAIN = lib.PinInCpp_CONTAIN
    EQUAL = lib.PinInCpp_EQUAL

class Keyboard(IntEnum):
    NULLKeyboard = lib.PinInCpp_NULLKeyboard
    QUANPIN = lib.PinInCpp_QUANPIN
    DAQIAN = lib.PinInCpp_DAQIAN
    XIAOHE = lib.PinInCpp_XIAOHE
    ZIRANMA = lib.PinInCpp_ZIRANMA
    SOUGOU = lib.PinInCpp_SOUGOU
    ZHINENG_ABC = lib.PinInCpp_ZHINENG_ABC
    GUOBIAO = lib.PinInCpp_GUOBIAO
    MICROSOFT = lib.PinInCpp_MICROSOFT
    PINYINPP = lib.PinInCpp_PINYINPP
    ZIGUANG = lib.PinInCpp_ZIGUANG

class PinInConfig:
    pinin:PinIn
    keyboard:Keyboard
    fZh2Z:bool
    fSh2S:bool
    fCh2C:bool
    fAng2An:bool
    fIng2In:bool
    fEng2En:bool
    fU2V:bool
    fFirstChar:bool
    def __init__(self, pinin:PinIn):
        self.pinin = pinin
        rawCfg = lib.PinInCpp_PinIn_GetConfig(pinin.cdata)
        self.keyboard = rawCfg.keyboard
        self.fZh2Z = rawCfg.fZh2Z != bytes([0])
        self.fSh2S = rawCfg.fSh2S != bytes([0])
        self.fCh2C = rawCfg.fCh2C != bytes([0])
        self.fAng2An = rawCfg.fAng2An != bytes([0])
        self.fIng2In = rawCfg.fIng2In != bytes([0])
        self.fEng2En = rawCfg.fEng2En != bytes([0])
        self.fU2V = rawCfg.fU2V != bytes([0])
        self.fFirstChar = rawCfg.fFirstChar != bytes([0])
    def set_keyboard(self, keyboard:Keyboard):
        self.keyboard = keyboard
        return self
    def set_fZh2Z(self, enable:bool):
        self.fZh2Z = enable
        return self
    def set_fSh2S(self, enable:bool):
        self.fSh2S = enable
        return self
    def set_fCh2C(self, enable:bool):
        self.fCh2C = enable
        return self
    def set_fAng2An(self, enable:bool):
        self.fAng2An = enable
        return self
    def set_fIng2In(self, enable:bool):
        self.fIng2In = enable
        return self
    def set_fEng2En(self, enable:bool):
        self.fEng2En = enable
        return self
    def set_fU2V(self, enable:bool):
        self.fU2V = enable
        return self
    def set_fFirstChar(self, enable:bool):
        self.fFirstChar = enable
        return self

    def commit(self):
        rawCfg = lib.PinInCpp_PinIn_GetConfig(self.pinin.cdata)
        rawCfg.keyboard = self.keyboard
        rawCfg.fZh2Z = bytes([self.fZh2Z and 1 or 0])
        rawCfg.fSh2S = bytes([self.fSh2S and 1 or 0])
        rawCfg.fCh2C = bytes([self.fCh2C and 1 or 0])
        rawCfg.fAng2An = bytes([self.fAng2An and 1 or 0])
        rawCfg.fIng2In = bytes([self.fIng2In and 1 or 0])
        rawCfg.fEng2En = bytes([self.fEng2En and 1 or 0])
        rawCfg.fU2V = bytes([self.fU2V and 1 or 0])
        rawCfg.fFirstChar = bytes([self.fFirstChar and 1 or 0])
        lib.PinInCpp_PinIn_ConfigCommit(self.pinin.cdata, rawCfg)
        pass

class DeserializeException(Exception):
    message = "Normal?"
    code = "PinInCpp_DeserNormal"
    def __init__(self, code):
        if code == lib.PinInCpp_FileNotOpen:
            self.code = "PinInCpp_FileNotOpen"
            self.message = "File not successfully opened"
        elif code == lib.PinInCpp_DeserBinaryVersionInvalidException:
            self.code = "PinInCpp_DeserBinaryVersionInvalidException"
            self.message = "Invalid binary file version"
        elif code == lib.PinInCpp_DeserOutOfRange:
            self.code = "PinInCpp_DeserOutOfRange"
            self.message = "out-of-range exceptions"
        elif code == lib.PinInCpp_DeserBadAlloc:
            self.code = "PinInCpp_DeserBadAlloc"
            self.message = "bad allocation"

    def __str__(self):
        return f"{self.code}: {self.message}"

class PinInInitException(Exception):
    filename = None
    def __init__(self, filename):
        self.filename = filename
        pass
    def __str__(self):
        return f"PinInInitException: Please check if the {self.filename} file is valid"

class TreeSearcherInitException(Exception):
    filename = None
    def __init__(self, filename):
        self.filename = filename
        pass
    def __str__(self):
        return f"TreeSearcherInitException: Please check if the {self.filename} file is valid. Or check the PinIn object."

class PinIn:
    cdata = None
    def __init__(self, path:str):
        self.cdata = _create_pinin(lib.PinInCpp_PinIn_New(path.encode("utf-8")))
        if self.cdata == None:
            raise PinInInitException(path)
    
    @staticmethod
    def deserialize(path:str, keyboard:Keyboard = Keyboard.NULLKeyboard)->PinIn:
        pinin_getter = _pffi.new("PinInCpp_PinIn[1]")
        deser_error = lib.PinInCpp_PinIn_Deserialize(path.encode("utf-8"),keyboard,pinin_getter)
        if deser_error != lib.PinInCpp_DeserNormal:
            raise DeserializeException(deser_error)
        result = PinIn.__new__(PinIn)
        result.cdata = _create_pinin(pinin_getter[0])
        return result

    def serialize(self, path:str)->bool:
        return lib.PinInCpp_PinIn_Serialize(self.cdata, path.encode("utf-8")) != 0

    def get_config(self)->PinInConfig:
        return PinInConfig(self)
    
    def is_empty(self)->bool:
        return lib.PinInCpp_PinIn_Empty(self.cdata) != 0
    
    def pre_cache_string(self, input_str:str):
        lib.PinInCpp_PinIn_PreCacheString(self.cdata, input_str.encode("utf-8"))

    def pre_null_pinyin_id_cache(self):
        lib.PinInCpp_PinIn_PreNullPinyinIdCache(self.cdata)

    def is_char_cache_enabled(self)->bool:
        return lib.PinInCpp_PinIn_IsCharCacheEnabled(self.cdata) != 0
    
    def set_char_cache(self, enable:bool):
        lib.PinInCpp_PinIn_SetCharCache(self.cdata, enable and 1 or 0)


class TreeSearcher:
    cdata = None
    def __init__(self, logic:Logic, PathOrPinIn:str|PinIn):
        temp_handle = None
        if type(PathOrPinIn) == str:
            temp_handle = lib.PinInCpp_TreeSearcher_NewPath(logic, PathOrPinIn.encode("utf-8"))
        else:
            temp_handle = lib.PinInCpp_TreeSearcher_NewPinIn(logic, PathOrPinIn.cdata)
        self.cdata = _create_tree_searcher(temp_handle)
        if self.cdata == None:
            raise TreeSearcherInitException(PathOrPinIn)
    
    @staticmethod
    def deserialize(path:str, pinin:PinIn)->TreeSearcher:
        tree_getter = _pffi.new("PinInCpp_TreeSearcher[1]")
        deser_error = lib.PinInCpp_TreeSearcher_Deserialize(path.encode("utf-8"),pinin.cdata,tree_getter)
        if deser_error != lib.PinInCpp_DeserNormal:
            raise DeserializeException(deser_error)
        result = TreeSearcher.__new__(TreeSearcher)
        result.cdata = _create_tree_searcher(tree_getter[0])
        return result
        

    def get_pinin(self):
        empty_pinin = PinIn.__new__(PinIn)
        empty_pinin.cdata = _create_pinin(lib.PinInCpp_TreeSearcher_GetPinIn(self.cdata))
        if empty_pinin.cdata == None:
            raise Exception("PinIn: nullptr error")
        return empty_pinin

    def serialize(self, path:str)->bool:
        return lib.PinInCpp_TreeSearcher_Serialize(self.cdata, path.encode("utf-8")) != 0

    def put_string(self, item:str) -> int:
        return lib.PinInCpp_TreeSearcher_PutString(self.cdata, item.encode("utf-8"))

    def execute_search(self, search_str:str)->list[str]:
        resultData = lib.PinInCpp_TreeSearcher_ExecuteSearch(self.cdata, search_str.encode("utf-8"))
        resultData = ffi.gc(resultData, lib.PinInCpp_SearchResult_Free)

        bufSize = -1
        buf = None

        result = []
        resultSize = resultData.size

        if resultSize == 0:
            return result
        id_list = ffi.unpack(resultData.ids, resultSize)

        for id in id_list:
            size = lib.PinInCpp_TreeSearcher_GetStrSizeById(self.cdata, id) + 1

            if size > bufSize:
                bufSize = size * 2
                buf = ffi.new("char[]", bufSize)
            lib.PinInCpp_TreeSearcher_PutToCharBuf(self.cdata, id, buf, bufSize)
            result.append(ffi.string(buf).decode("utf-8"))
            
        return result
    
    def execute_search_get_ids(self, search_str:str)->list[int]:
        resultData = lib.PinInCpp_TreeSearcher_ExecuteSearch(self.cdata, search_str.encode("utf-8"))
        resultData = ffi.gc(resultData, lib.PinInCpp_SearchResult_Free)

        result = []
        resultSize = resultData.size

        if resultSize == 0:
            return result
        
        result = ffi.unpack(resultData.ids, resultSize)
        return result
    
    def get_str_by_id(self, id:int)->str:
        cid = ffi.cast("size_t", id)
        size = lib.PinInCpp_TreeSearcher_GetStrSizeById(self.cdata, cid) + 1
        buf = ffi.new("char[]", size)
        lib.PinInCpp_TreeSearcher_PutToCharBuf(self.cdata, cid, buf, size)
        return ffi.string(buf).decode("utf-8")
    
    def get_str_list_by_ids(self, ids:list[int])->list[str]:
        result = []
        bufSize = -1
        buf = None
        for id in ids:
            cid = ffi.cast("size_t", id)
            size = lib.PinInCpp_TreeSearcher_GetStrSizeById(self.cdata, cid) + 1
            if size > bufSize:
                bufSize = size * 2
                buf = ffi.new("char[]", bufSize)
            lib.PinInCpp_TreeSearcher_PutToCharBuf(self.cdata, cid, buf, bufSize)
            result.append(ffi.string(buf).decode("utf-8"))
        return result
    
    def str_pool_reserve(self, newcapacity:int):
        lib.PinInCpp_TreeSearcher_StrPoolReserve(self.cdata, ffi.cast("size_t", newcapacity))

    def refresh(self):
        lib.PinInCpp_TreeSearcher_Refresh(self.cdata)

    def shrink_to_fit(self):
        lib.PinInCpp_TreeSearcher_ShrinkToFit(self.cdata)
