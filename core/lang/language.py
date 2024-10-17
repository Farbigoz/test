import zlib
import io
import codecs

class UTF8String:
    
    #ctor
    def __init__(self, length, string):
        self.length = length
        self.string = string
        
    #static class methods    
    @classmethod
    def FromBytesIO(cls, data):
        length = cls.__ReadUint16BE(data)
        string = data.read(length).decode('utf-8')
        return cls(length, string)
    
    @classmethod
    def FromString(cls, string):
        return cls(len(string), string)    
    
    #public
    def WriteBytesIO(self, data):
        data.write(self.length.to_bytes(2, byteorder="big"))
        data.write(self.string.encode('utf-8'))
        
    #private
    def __ReadUint16BE(data):
        byte = data.read(2)
        return int.from_bytes(byte, byteorder="big")  # whar?

class Entry:
    
    #ctor
    def __init__(self, key, value):
        self.key = key
        self.value = value
    
    #public
    def WriteBytesIO(self, data):
        self.key.WriteBytesIO(data)
        self.value.WriteBytesIO(data)
        
    def SetValue(self, value):
        self.value = UTF8String.FromString(value)
        
    #static class methods
    @classmethod
    def FromBytesIO(cls, data):
        return cls(UTF8String.FromBytesIO(data), UTF8String.FromBytesIO(data))
    
    @classmethod
    def FromKeyValuePair(cls, key, value):
        return cls(UTF8String.FromString(key), UTF8String.FromString(value))
    
class LangFile:

    #ctor
    def __init__(self, filename):
        fd = open(filename, "rb")

        self.entries = []

        self.inflated_size = fd.read(4)
        self.zlibdata = fd.read()

        self.__ParseFile()

    #public 
    def Save(self, filename):
        
        data = io.BytesIO()
        data.write(self.__WriteUint32BE(self.entry_count))
        for entry in self.entries:
            entry.WriteBytesIO(data)       
        
        with open(filename, "wb") as fd:
            self.inflated_size = data.getbuffer().nbytes
            fd.write(self.inflated_size.to_bytes(4, byteorder="little"))
            self.zlibdata = zlib.compress(data.getbuffer())
            fd.write(self.zlibdata)
        
    def Dump(self, filename):
        with codecs.open(filename, "w", "utf-8") as fd:
            for entry in self.entries:
                fd.write(f"{entry.key.string}={entry.value.string}\n")

    #private
    def __ParseFile(self):
        self.data = io.BytesIO(zlib.decompress(self.zlibdata))
        self.entry_count = self.__ReadUint32BE(self.data)

        while len(self.entries) < self.entry_count:
            self.entries.append(Entry.FromBytesIO(self.data))
        pass

    def __ReadUint32BE(self, data):
        byte = data.read(4)
        return int.from_bytes(byte, byteorder="big")  # whar?
    
    def __WriteUint32BE(self, number):
        return number.to_bytes(4, byteorder="big")
    
    #overrides
    def __setitem__(self, key, value):
        for entry in self.entries:
            if entry.key.string == key:
                entry.SetValue(value)
                return
        self.entries.append(Entry.FromKeyValuePair(key, value))
        self.entry_count += 1
        
    def __getitem__(self, key):
        for entry in self.entries:
            if entry.key.string == key:
                return entry.value.string
        return None