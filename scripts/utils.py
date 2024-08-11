java_testvars = {
    "int": "0",
    "Integer": "1",
    "double": "3.14",
    "Double": "3.14",
    "float": "3.14",
    "Float": "3.14",
    "long": "1000000",
    "Long": "1000000",
    "String": "hello",
    "boolean": "True",
    "Boolean": "True",
    "char": 'a',
    "Character": 'a',
    "List<Integer>": "Arrays.asList(1, 2, 3)",
    "List<List<Integer>>": "Arrays.asList(Arrays.asList(1, 2, 3))",
    "List<Double>": "Arrays.asList(1.0, 2.0, 3.0)",
    "List<Float>": "Arrays.asList(1.0f, 2.0f, 3.0f)",
    "List<String>": "Arrays.asList(\"one\", \"two\", \"three\")",
    "List<Object>": "Arrays.asList()",
    "Set<Integer>": "new HashSet<>(Arrays.asList(1, 2, 3))",
    "Set<String>": "new HashSet<>(Arrays.asList(\"red\", \"green\", \"blue\"))",
    "Map<String,Integer>": "new HashMap<>() {{ put(\"one\", 1); put(\"two\", 2); put(\"three\", 3); }}",
    "Object": "new Object()",
    "Void": "null"
}

cpp_testvars = {
    "int": "0",
    "int32_t": "1",
    "double": "3.14",
    "float": "3.14",
    "long": "1000000",
    "int64_t": "1000000",
    "string": "\"hello\"",
    "bool": "true",
    "char": "'a'",
    "vector<int>": "{ 1, 2, 3 }",
    "vector<double>": "{ 1.0, 2.0, 3.0 }",
    "vector<float>": "{ 1.0f, 2.0f, 3.0f }",
    "vector<string>": "{ \"one\", \"two\", \"three\" }",
    "set<int>": "{ 1, 2, 3 }",
    "set<string>": "{ \"red\", \"green\", \"blue\" }",
    "map<string,int>": "{ {\"one\", 1}, {\"two\", 2}, {\"three\", 3} }",
    "void*": "nullptr"
}


def gen_a_cpp_valid_input(para):
    if para.startswith("(") and para.endswith(")"):
        para = para[1:-1]
    ps = para.split(",")
    vars = []
    for p in ps:
        idx = p.rindex(" ")
        typ = p[:idx].strip()
        pn = p[idx:].strip()
        if typ in cpp_testvars:
            vars.append(cpp_testvars[typ])
        else:
            return None
    return ", ".join(vars)

def gen_a_java_vaild_input(para):
    if para.startswith("(") and para.endswith(")"):
        para = para[1:-1]
    ps = para.split(",")
    vars = []
    for p in ps:
        idx = p.rindex(" ")
        typ = p[:idx].strip()
        pn = p[idx:].strip()
        if typ in java_testvars:
            vars.append(java_testvars[typ])
        else:
            return None
    return ", ".join(vars)
