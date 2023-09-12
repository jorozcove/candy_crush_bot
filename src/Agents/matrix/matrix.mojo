from random import rand
from memory import memset_zero
from python import Dictionary, Python
from utils.vector import DynamicVector


struct CandyMatrix:
    var data: DTypePointer[DType.float64]
    var x: Int
    var y: Int
    var candies: Dictionary
    var np: PythonObject
    
    fn __init__(inout self, x: Int, y: Int):
        self.data = DTypePointer[DType.float64].alloc(x * y)
        rand[DType.float64](self.data, x * y)
        self.x = x
        self.y = y
        self.candies = Python.dict()
        try:
            self.np = Python.import_module("numpy")
            self.initialize_candies()
        except:
            pass
    
    fn initialize_candies(self) raises -> None:
        let candies_name: PythonObject
        candies_name = self.np.array(["b", "b_p", "b_sh", "b_sv", "g", "g_p", "g_sh", "g_sv", "o", "o_p", "o_sh", "o_sv", "p", "p_p", "p_sh", "p_sv", "r", "r_p", "r_sh", "r_sv", "y", "y_p", "y_sh", "y_sv"])
        for i in range(candies_name.size):
            self.candies[candies_name[i].to_string()] = i

    fn is_empty(self) -> Bool:
        var count: Int = 0
        for i in range(self.x):
            for j in range(self.y):
                if self[i, j] == '-':
                    count += 1
        return count == self.x * self.y    
        
    fn zero(inout self):
        memset_zero(self.data, self.x * self.y)
    
    fn __copyinit__(inout self, existing: Self):
        self.x = existing.x
        self.y = existing.y
        self.candies = existing.candies
        self.data = DTypePointer[DType.float64].alloc(self.x * self.y)
        self.np = existing.np
        for i in range(self.x):
            for j  in range(self.y):
                self[i, j] = existing[i, j]
        
    fn __del__(owned self):
        self.data.free()
    
    fn value_to_text[nelts: Int](self, item: Int) -> String:
        try:
            let dictKeys = Python.import_module("dictKeys")
            return dictKeys.get_dict_key(self.candies.keys(), self.candies.values(), item).to_string()
        except:
            return '-'
    
    fn get_num(self, row: Int, col: Int) -> Int:
        return self.load_item[1](row, col).to_int()
    
    @always_inline
    fn __getitem__(self, row: Int, col: Int) -> String:
        let item: Int = self.load_item[1](row, col).to_int()
        return self.value_to_text[1](item)
    
    @always_inline
    fn load_item[nelts: Int](self, row: Int, col: Int) -> SIMD[DType.float64, nelts]:
        return self.data.simd_load[nelts](col * self.y + row)
    
    @always_inline
    fn __setitem__(self, row: Int, col: Int, val: String):
        try:
            self.store_item[1](row, col, self.candies.get(val).to_float64())
        except:
            self.store_item[1](row, col, 0)
    
    @always_inline
    fn store_item[nelts: Int](self, row: Int, col: Int, val: SIMD[DType.float64, nelts]):
        self.data.simd_store[nelts](col * self.y + row, val)
        
    @always_inline
    fn __str__(self: Self) -> String:
        return self.to_string()
    
    @always_inline
    fn to_string(self: Self) -> String:
        var string: String = ''
        string += '[\n'
        for i in range(self.x):
            string += "["
            for j in range(self.y):
                string += self[i, j]
                string += ", "
            string += "]\n"
        string += "]"
        return string