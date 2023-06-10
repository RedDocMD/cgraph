from clang.cindex import CursorKind, Index, CompilationDatabase
from pathlib import Path


def print_cursor(cursor, file):
    ext = cursor.extent
    start = ext.start
    end = ext.end
    if start.file.name != end.file.name:
        raise RuntimeError("start and end are in different files: {} & {}".format(start.file, end.file))
    if start.file.name != file:
        return
    # with open(start.file.name) as f:
    #     cont = f.read()
    # print("{} => {}:{} -> {}".format(kind, start.file, start.line, cont[start.offset:end.offset]))
    kind = cursor.kind
    print("{} - {}:{}:{} - {}".format(kind, start.file.name, start.line, start.column, cursor.displayname))


def visit_cursor(cursor, file):
    kind = cursor.kind
    print_cursor(cursor, file)
    # if kind == CursorKind.CALL_EXPR:
    #     print_cursor(cursor, file)
    # elif kind == CursorKind.FUNCTION_DECL and cursor.is_definition():
    #     print_cursor(cursor, file)
    for child in cursor.get_children():
        visit_cursor(child, file)


idx = Index.create()
cwd = Path.cwd()
comp_db = CompilationDatabase.fromDirectory(cwd)

c_files = []
for child in cwd.iterdir():
    if child.suffix == '.c' and child.is_file():
        c_files.append(child)

for file in c_files:
    if "2" in str(file):
        continue
    cc = list(comp_db.getCompileCommands(str(file)))
    args = list(cc[0].arguments)[1:]
    if "-o" in args:
        i = args.index("-o")
        args = args[:i]
    else:
        args = args[:-1]
    tu = idx.parse(file, args)
    print('File: ' + str(file))
    cur = tu.cursor
    if tu.diagnostics:
        for diag in tu.diagnostics:
            print(diag)
    visit_cursor(cur, str(file))

# print(CursorKind.get_all_kinds())